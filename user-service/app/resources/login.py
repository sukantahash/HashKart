from flask_restful import Resource
from flask import request
from app.models.users import User
from app.utils.auth import generate_token

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        if not user or not user.check_password(data.get('password')):
            return {"message": "Invalid credentials"}, 401
        
        token = generate_token(user.id)
        return {"token": token}, 200