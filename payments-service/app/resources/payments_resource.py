from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.schemas.payment_schema import PaymentSchema, ConfirmPaymentSchema
from app.gateway import payment_gateway
from app.models.payments import Payment
from app import db

payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)
confirm_payment_schema = ConfirmPaymentSchema()

class CreatePayment(Resource):
    @jwt_required()
    def post(self):
        try:
            user_id = int(get_jwt_identity())
            json_data = request.get_json()
            data = payment_schema.load(json_data)

            init_payment_result = payment_gateway.create_payment(
                data.get('amount'),
                data.get('order_id'),
                user_id
            )

            # add payment to db
            payment = Payment(
                user_id=user_id,
                order_id = data.get('order_id'),
                amount = data.get('amount'),
                status = "pending",
                payment_provider = "mock",
                provider_payment_id=init_payment_result.get('payment_id')
            )
            db.session.add(payment)
            db.session.commit()

            return {
                "payment_id": init_payment_result.get('payment_id'),
                "client_secret": init_payment_result.get('client_secret')
            }, 201
        
        except ValidationError as err:
            return {"errors": err.messages}, 400
        except Exception as e:
            print(str(e))
            return {"errors": str(e)}, 500


class ConfirmPayment(Resource):
    @jwt_required()
    def post(self):
        """
        Confirms the payment with the given payment_id
        """ 
        try:
            print("Payment confirm starting")
            user_id = int(get_jwt_identity())
            data = confirm_payment_schema.load(request.get_json())
            payment_id = data.get('payment_id')
            verify_payment_result = payment_gateway.verify_payment(payment_id)

            if verify_payment_result.get('status') != "success":
                return {"errors": "Payment verification failed"}, 400
            
            payment = Payment.query.filter_by(provider_payment_id=str(payment_id), user_id=user_id).first()

            if not payment:
                return {"errors": "Payment not found"}, 404
            
            payment.status = "success"
            db.session.commit()

            return {"message": "Payment confirmed"}, 200
        
        except Exception as e:
            print(str(e))
            return {"errors": str(e)}, 500
        

class PaymentsResource(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = int(get_jwt_identity())
            payments = Payment.query.filter_by(user_id=user_id)
            return payments_schema.dump(payments), 200
        except Exception as e:
            return {"error": str(e)}, 500