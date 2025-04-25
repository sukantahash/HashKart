from marshmallow import Schema, fields, validate

CATEGORIES = ["Electronics", "Clothing", "Toys", "Books", "Others"]

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    category = fields.Str(required=True, validate=validate.OneOf(CATEGORIES))
    price = fields.Float(required=True)
    rating = fields.Float(required=False, load_default=0.0, validate=validate.Range(min=0, max=5))
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    created_at = fields.DateTime(dump_only=True)

product_schema = ProductSchema()
product_update_schema =ProductSchema(partial=True)
products_schema = ProductSchema(many=True)

