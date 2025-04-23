import jwt
import datetime
from flask import current_app
from flask_jwt_extended import create_access_token

def generate_token(user_id):
    access_token = create_access_token(identity=str(user_id))
    return access_token


def decode_token(token):
    try:
        decodeed_token = jwt.decode(token, current_app.config.get('JWT_SECRET_KEY'), algorithms=['HS256'])
        return decodeed_token.get('user_id')
    except:
        return None