from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.models.cart import CartItem
from app.schemas.cart_schema import CartSchema
from app import db

cart_schema = CartSchema()
cart_item_schema = CartSchema(many=True)

class CartResource(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            user_id = int(get_jwt_identity())
            data.update({"user_id": user_id})
            cart_data = cart_schema.load(data)
            
          
            new_cart_item = CartItem(**cart_data)
            db.session.add(new_cart_item)
            db.session.commit()
            return cart_schema.dump(new_cart_item), 201
        except ValidationError as err:
            # db.session.rollback()
            return {"errors": err.messages}, 400
        except Exception as e:
            # db.session.rollback()
            return {"error": str(e)}, 500
    

class CartGetResource(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            cart_items = CartItem.query.filter_by(user_id=user_id).all()
            return cart_item_schema.dump(cart_items), 200
        except Exception as e:
            return {"error": str(e)}, 500
