import sys
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import pytest
from  app import create_app, db
from flask_jwt_extended import create_access_token
from  app.models.products import Product


@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'product_test_jwt_secret'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()

@pytest.fixture(scope='module')
def auth_token(test_app):
    with test_app.app_context():
        token = create_access_token(identity=str(1))
        return token

@pytest.fixture(scope='module')
def add_product():
    def _add_product(name, category, price, quantity, rating=0):
        product = Product(name=name, category=category, price=price, quantity=quantity, rating=rating)
        db.session.add(product)
        db.session.commit()
        return product
    return _add_product
