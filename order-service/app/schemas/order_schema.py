from marshmallow import Schema, fields, post_load, validate
from app.models.order import Order, OrderItem

class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    status = fields.Str(required=False, load_default='pending')
    order_date = fields.DateTime(dump_only=True)
    payment_id = fields.Str(dump_only=True)
    order_items = fields.List(fields.Nested('OrderItemSchema'), required=True, validate=validate.Length(min=1))

    # @post_load
    # def make_order(self, data, **kwargs):
    #     return Order(**data)

class OrderItemSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(dump_only=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))

    # @post_load
    # def make_order_item(self, data, **kwargs):
    #     return OrderItem(**data)
