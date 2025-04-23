import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class Config:
    DEBUG = True
    SECRET_KEY = 'product_service_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(base_dir, 'products.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'common_jwt_secret'  # Secret key for JWT
