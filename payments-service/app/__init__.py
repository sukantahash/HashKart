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
    app.url_map.strict_slashes = False
    
    # Add resource routes
    from app.resources.payments_resource import CreatePayment, ConfirmPayment, PaymentsResource
    print("Adding resources")
    api.add_resource(PaymentsResource, '/payments/', '/payments')
    api.add_resource(CreatePayment, '/payments/create')
    api.add_resource(ConfirmPayment, '/payments/confirm')

    with app.app_context():
        db.create_all()
    
    return app