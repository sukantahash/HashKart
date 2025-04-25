from marshmallow import Schema, fields, validate

class PaymentSchema(Schema):
    id = fields.Int(dump_only=True),
    order_id = fields.Int(required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=1))
    status = fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    provider_payment_id = fields.Str(dump_only=True)

class ConfirmPaymentSchema(Schema):
    payment_id = fields.UUID(required=True) # provider_payment_id