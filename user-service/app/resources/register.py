from flask_restful import Resource
from flask import request
from app.models.users import User
from app import db
from app.schemas.user_schema import UserRegisterSchema
from marshmallow import ValidationError

class UserRegister(Resource):
    def post(self):
        json_data = request.get_json()
        schema = UserRegisterSchema()

        try:
            data = schema.load(json_data)
        except ValidationError as err:
            return {'errors': err.messages}, 400

        if User.query.filter_by(username=data.get('username')).first():
            return {"message": "User already exists"}, 400
        
        user = User(username=data.get('username'), email=data.get('email'))
        user.set_password(data.get('password'))

        db.session.add(user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201
    
    