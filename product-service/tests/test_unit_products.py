import pytest
from app import db
from app.models.products import Product

@pytest.fixture(scope='module')
def init_db(test_app):
    with test_app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_product_creation(init_db):
    product = Product(name='Test Product', category='Electronics', price=99.99, rating=4.5, quantity=10)
    db.session.add(product)
    db.session.commit()
    assert product.id is not None
