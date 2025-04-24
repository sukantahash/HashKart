from marshmallow import Schema, fields, post_load, validate
from app.models.cart import CartItem

class CartSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))

    # @post_load
    # def make_cart(self, data, **kwargs):
    #     return Cart(**data)
