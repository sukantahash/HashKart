import uuid


class MockPaymentGateway:
    def create_payment(self, amount, order_id, user_id):
        """
        Simulate payment init
        """
        return {
            "payment_id": str(uuid.uuid4()),
            "amount": amount,
            "order_id": order_id,
            "user_id": user_id,
            "client_secret": "mock_client_secret"
        }
    
    def verify_payment(self, payment_id):
        """Payment confirmation"""
        return {
            "status": "success",
            "payment_id": payment_id
        }