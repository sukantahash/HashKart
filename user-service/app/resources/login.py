from flask_restful import Resource
from flask import request
from app.models.users import User
from app.utils.auth import generate_token
from app.schemas.user_schema import UserLoginSchema, ValidationError

class UserLogin(Resource):
    def post(self):
        json_data = request.get_json()
        schema = UserLoginSchema()

        try:
            data = schema.load(json_data)
        except ValidationError as err:
            return {"erros": err.messages}, 400

        user = User.query.filter_by(username=data.get('username')).first()
        if not user or not user.check_password(data.get('password')):
            return {"message": "Invalid credentials"}, 401
        
        token = generate_token(user.id)
        return {"token": token}, 200