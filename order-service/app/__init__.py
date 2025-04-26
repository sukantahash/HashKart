from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from flask_restful import Api

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    api = Api(app)

    # add resources
    from app.resources.order_resource import OrderResource, OrderListCreateResource, OrderSuccess
    from app.resources.cart_resource import CartResource
    from app.resources.checkout_resource import CheckoutResource

    api.add_resource(OrderResource, '/orders/<int:order_id>')
    api.add_resource(OrderListCreateResource, '/orders')
    api.add_resource(CartResource, '/cart')
    api.add_resource(CheckoutResource, '/checkout')
    api.add_resource(OrderSuccess, '/orders/order-success')

    with app.app_context():
        db.create_all()

    return app