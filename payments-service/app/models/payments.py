from app import db
from datetime import datetime, timezone

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    order_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, default="pending")
    payment_provider = db.Column(db.String, default="mock")
    provider_payment_id = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))