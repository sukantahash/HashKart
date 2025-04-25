import pytest
from flask import json
from app import create_app, db
from app.models.users import User
from app.utils.auth import create_access_token

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    # Add a test user
    user = User(username='testuser1', email='test@gmail.com')
    user.set_password('1234')
    db.session.add(user)
    db.session.commit()

def test_user_login_success(client, init_database):
    response = client.post('/login', json={
        'username': 'testuser1',
        'password': '1234'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data

def test_user_login_invalid_credentials(client, init_database):
    response = client.post('/login', json={
        'username': 'testuser2',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['message'] == 'Invalid credentials'

def test_user_register_success(client):
    response = client.post('/register', json={
        'username': 'newuser',
        'email': 'newuser@gmail.com',
        'password': 'newpass1234'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'User registered successfully'

def test_user_register_existing_user(client, init_database):
    response = client.post('/register', json={
        'username': 'testuser1',
        'email': 'test@gmail.com',
        'password': '1234'
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'User already exists'


