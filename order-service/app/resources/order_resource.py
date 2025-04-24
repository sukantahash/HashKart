from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.models.order import Order, OrderItem
from app.schemas.order_schema import OrderSchema, OrderItemSchema
from app import db

order_schema = OrderSchema()
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


class OrderResource(Resource):
    @jwt_required()
    def get(self, order_id):
        try:
            order = Order.query.get_or_404(order_id)
            return order_schema.dump(order), 200
        except Exception as e:
            return {"error": str(e)}, 400
