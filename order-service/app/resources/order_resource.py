from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.models.order import Order, OrderItem
from app.schemas.order_schema import OrderSchema, OrderItemSchema
from app import db
from config import Config
import requests

order_schema = OrderSchema()
order_update_schema = OrderSchema(partial=True)
orders_schema = OrderSchema(many=True)
order_item_schema = OrderItemSchema()

class OrderListCreateResource(Resource):
    @jwt_required()
    def get(self):
        try:
            orders = Order.query.all()
            orders_data = order_schema.dump(orders, many=True)
            for order in orders_data:
                order_items = OrderItem.query.filter_by(order_id=order['id']).all()
                order['order_items'] = order_item_schema.dump(order_items, many=True)
            return orders_data, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            user_id = get_jwt_identity()  # Extract user_id from JWT
            data.update({"user_id": user_id})
            order_data = order_schema.load(data)
            
            with db.session.begin():
                new_order = Order(
                    user_id=user_id,
                    status='pending'
                )
                db.session.add(new_order)
                db.session.flush()
                for item in order_data.get('order_items', []):
                    order_item_data = order_item_schema.load(item)
                    new_order_item = OrderItem(
                        order_id=new_order.id,
                        product_id=order_item_data.get('product_id'),
                        quantity=order_item_data.get('quantity')
                    )
                    db.session.add(new_order_item)
            
            return order_schema.dump(new_order), 201
        except ValidationError as err:
            db.session.rollback()
            return {"errors": err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

class OrderSuccess(Resource):
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
    jwt_required()
    def post(self):
        try:
            data = request.get_json()
            order_id = data.get('order_id')
            order = Order.query.filter_by(id=order_id).first()
            if not order:
                return {"error": "Order Not Found"}, 404
            # get current jwt_token
            jwt_token = None
            auth_header = request.headers.get('Authorization', None)
            if auth_header and auth_header.startswith('Bearer'):
                jwt_token = auth_header.split(' ')[1]
            # update the quantity of products
            for item in order.order_items:
                product_detail = self.get_product_details(item.product_id, jwt_token)
                current_quantity = product_detail.get('quantity')
                order_quantity = item.quantity
                if current_quantity-order_quantity < 0:
                    raise Exception(f"Insufficient Stock to complete the order")
                
                response = requests.put(
                    url=f"{Config.BASE_PRODUCTS_API}/{item.product_id}",
                    headers={
                        "Authorization": f"Bearer {jwt_token}",
                        "Content-Type": 'application/json'
                    },
                    json={"quantity": current_quantity - order_quantity}
                )
                if response.status_code != 200:
                    raise Exception(f"Error Updating Products: {response.reason}")
            order.status = "success"
            db.session.commit()
            return order_schema.dump(order), 200
        except Exception as e:
            return {"errors": str(e)}, 500

class OrderResource(Resource):
    @jwt_required()
    def get(self, order_id):
        try:
            order = Order.query.filter_by(id=order_id).first()
            if not order:
                return {"error": "Order Not Found"}, 404
            return order_schema.dump(order), 200
        except Exception as e:
            return {"error": str(e)}, 400

    @jwt_required()
    def put(self, order_id):
        try:
            order = Order.query.filter_by(id=order_id).first()
            if not order:
                return {"errors": f"Order Not Found for order_id: {order_id}"}, 404
            update_data = order_update_schema.load(request.get_json(), partial=True)
            for key, value in update_data.items():
                setattr(Order, key, value)
            db.session.commit()
            return order_update_schema.dump(order), 200
        except Exception as e:
            return {"errors": str(e)}, 500