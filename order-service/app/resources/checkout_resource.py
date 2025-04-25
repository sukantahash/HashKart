from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.schemas.order_schema import OrderSchema, OrderItemSchema
from app import db

order_schema = OrderSchema()
order_item_schema = OrderItemSchema()

class CheckoutResource(Resource):
    @jwt_required()
    def post(self):
        try:
            db.session.close_all()
            data = request.get_json()
            user_id = get_jwt_identity()
            cart_items = CartItem.query.filter_by(user_id=user_id).all()
            
            if not cart_items:
                return {"message": "Cart is empty"}, 400
            
            with db.session.begin_nested():
                new_order = Order(user_id=user_id, status='pending')
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
            
            # Here you would redirect to the payment service
            # For now, we simulate the redirection with a placeholder response
            payment_service_url = f"http://payment-service/checkout?order_id={new_order.id}"
            return {"message": "Redirect to payment service", "payment_url": payment_service_url}, 200
        except ValidationError as err:
            db.session.rollback()
            return {"errors": err.messages}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        finally:
            db.session.close_all()
