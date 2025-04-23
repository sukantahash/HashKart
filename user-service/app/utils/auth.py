import jwt
import datetime
from flask import current_app

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config.get('SECRET_KEY'), algorithm='HS256')


def decode_token(token):
    try:
        decodeed_token = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return decodeed_token.get('user_id')
    except:
        return None