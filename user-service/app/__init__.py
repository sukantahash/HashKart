from flask import Flask
from flask_restful import Api
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    api = Api(app)

    # Import resources
    from app.resources.register import UserRegister
    from app.resources.login import UserLogin

    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')

    with app.app_context():
        db.create_all()

    return app