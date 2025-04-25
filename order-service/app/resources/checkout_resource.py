from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.schemas.order_schema import OrderSchema, OrderItemSchema
from app import db
from config import Config
import requests

order_schema = OrderSchema()
order_item_schema = OrderItemSchema()

class CheckoutResource(Resource):
    def get_product_details(self, product_id, jwt_token):
        response = requests.get(
            f"{Config.BASE_PRODUCTS_API}/{product_id}",
            headers={
                "Authorization": f"Bearer {jwt_token}",
                "Content-Type": 'application/json'
            },
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            raise Exception(f"Products Out of Stock")
        else:
            raise Exception(response.reason)
    
    def calculate_order_total(self, cart_items, jwt_token):
        total_amount = 0
        for item in cart_items:
            product_id = item.product_id
            product_detail = self.get_product_details(product_id, jwt_token)
            total_amount = product_detail.get('price') * item.quantity
        return total_amount

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            user_id = get_jwt_identity()
            # get current jwt_token
            jwt_token = None
            auth_header = request.headers.get('Authorization', None)
            if auth_header and auth_header.startswith('Bearer'):
                jwt_token = auth_header.split(' ')[1]
            cart_items = CartItem.query.filter_by(user_id=user_id).all()
            
            if not cart_items:
                return {"message": "Cart is empty"}, 400
            
            # calculate order total
            total_amount = self.calculate_order_total(cart_items, jwt_token)
            
            with db.session.begin_nested():
                new_order = Order(user_id=user_id, status='pending', order_total=total_amount)
                db.session.add(new_order)
                db.session.flush()  # Ensure new_order.id is available
                
                for item in cart_items:
                    new_order_item = OrderItem(
                        order_id=new_order.id,
                        product_id=item.product_id,
                        quantity=item.quantity
                    )
                    db.session.add(new_order_item)
                    db.session.delete(item)
            
            # create new payment for the order
            init_payment_response = requests.post(
                url=f"{Config.BASE_PAYMENTS_API}/create",
                headers={
                    "Authorization": f"Bearer {jwt_token}",
                    "Content-Type": 'application/json'
                },
                json={
                    "order_id": new_order.id,
                    "amount": total_amount
                }
            )
            if init_payment_response.status_code in  [200, 201]:
                payment_resp_json = init_payment_response.json()
                new_order.payment_id = payment_resp_json.get('payment_id')
            else:
                raise Exception(f"Payments API Error: {init_payment_response.reason}")

            return {
                "order_id": new_order.id,
                "amount": new_order.order_total,
                "payment_id": new_order.payment_id
            }, 200
        except ValidationError as err:
            db.session.rollback()
            return {"errors": err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
