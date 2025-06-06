import json
import pytest
from app import db
from app.models.products import Product

@pytest.fixture(autouse=True)
def cleanup():
    yield
    db.session.query(Product).delete()
    db.session.commit()

def test_create_product(test_client, auth_token):
    response = test_client.post('/products', json={
        'name': 'Test_Product_1',
        'category': 'Electronics',
        'price': 150,
        'quantity': 10
    }, headers={'Authorization': f'Bearer {auth_token}'})
    
    if response.status_code != 201:
        print(response.get_json())  # Print the error message for debugging
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Test_Product_1'
    assert data['rating'] == 0

def test_get_products(test_client, auth_token):
    # Add products directly within the test
    product1 = Product(name='Product_1', category='Electronics', price=100, rating=4.5, quantity=10)
    product2 = Product(name='Product_2', category='Books', price=50, rating=4.0, quantity=5)
    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()

    response = test_client.get('/products', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

def test_get_product_by_id(test_client, auth_token):
    # Add product directly within the test
    product = Product(name='Product_3', category='Clothing', price=30, rating=3.5, quantity=20)
    db.session.add(product)
    db.session.commit()
    
    product_id = db.session.get(Product, product.id)
    
    response = test_client.get(f'/products/{product_id.id}', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Product_3'

def test_filter_by_category(test_client, auth_token):
    # Add products directly within the test
    product1 = Product(name='Product_4', category='Electronics', price=100, rating=4.5, quantity=10)
    product2 = Product(name='Product_5', category='electronics', price=50, rating=4.0, quantity=5)
    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()

    response = test_client.get('/products?category=electronics', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

def test_sort_by_price(test_client, auth_token):
    # Add products directly within the test
    product1 = Product(name='Product_6', category='Books', price=20, rating=3.0, quantity=15)
    product2 = Product(name='Product_7', category='Books', price=40, rating=4.0, quantity=5)
    db.session.add(product1)
    db.session.add(product2)
    db.session.commit()

    response = test_client.get('/products?sort_by=price&order=asc', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert data[0]['price'] == 20
    assert data[1]['price'] == 40
