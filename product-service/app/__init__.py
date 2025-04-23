from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    
    api = Api(app)
    
    # Add resource routes
    from app.resources.product import ProductList, ProductDetail
    api.add_resource(ProductList, '/products')
    api.add_resource(ProductDetail, '/products/<int:product_id>')

    with app.app_context():
        db.create_all()
    
    return app