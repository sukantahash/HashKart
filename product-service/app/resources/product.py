from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app.models.products import Product
from app.schemas.products_schema import product_schema, products_schema, product_update_schema
from app import db
from werkzeug.exceptions import NotFound

class ProductList(Resource):
    @jwt_required()
    def get(self):
        try:
            category = request.args.get('category')
            sort_by = request.args.get('sort_by')
            order = request.args.get('order', 'asc')
            
            query = Product.query
            
            if category:
                query = query.filter(db.func.lower(Product.category) == category.lower())
            
            if sort_by:
                if order == 'desc':
                    query = query.order_by(db.desc(getattr(Product, sort_by)))
                else:
                    query = query.order_by(getattr(Product, sort_by))
            
            products = query.all()
            
            return products_schema.dump(products), 200
        except Exception as e:
            return {"message": str(e)}, 500

    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            validated_data = product_schema.load(data)
            new_product = Product(**validated_data)
            db.session.add(new_product)
            db.session.commit()
            return product_schema.dump(new_product), 201
        except ValidationError as err:
            return {"message": err.messages}, 400
        except Exception as e:
            return {"message": str(e)}, 500

class ProductDetail(Resource):
    @jwt_required()
    def get(self, product_id):
        try:
            product = Product.query.filter_by(id=product_id).first()
            if not product:
                return {"errors": f"Product Not Found for product_id: {product_id}"}, 404
            return product_schema.dump(product), 200
        except Exception as e:
            return {"errors": str(e)}, 500

    @jwt_required()
    def put(self, product_id):
        try:
            product = Product.query.filter_by(id=product_id).first()
            if not product:
                return {"errors": f"Product Not Found for product_id: {product_id}"}, 404
            update_data = product_update_schema.load(request.get_json(), partial=True)
            for key, value in update_data.items():
                setattr(product, key, value)
            db.session.commit()
            return product_schema.dump(product), 200
        except Exception as e:
            return {"errors": str(e)}, 500