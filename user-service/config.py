import os
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'user_service_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(base_dir, 'users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'common_jwt_secret'  # Secret key for JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    