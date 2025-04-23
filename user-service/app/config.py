import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(base_dir)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'user_service_secret_key')
    #SQLALCHEMY_DATABASE_URI = 'sqlite:////users.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(base_dir, 'users.db')
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    