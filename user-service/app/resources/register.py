from flask_restful import Resource
from flask import request
from app.models.users import User
from app import db

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data.get('username').first()):
            return {"message": "User already exists"}, 400
        
        user = User(username=data.get('username'), email=data.get('email'))
        user.set_password(data.get('password'))

        db.session.add(user)
        db.session.commit()

        return {"message": "User registered successfully"}, 201
    
    