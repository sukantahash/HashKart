from flask import Flask
from flask_restful import Api
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    api = Api(app)

    # Import resources
    from app.resources.register import UserRegister
    from app.resources.login import UserLogin

    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')

    with app.app_context():
        db.create_all()

    return app