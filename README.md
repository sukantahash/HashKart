# HashKart
HashKart application is one stop destination for all kinds of shopping needs for the customers. The application enables the users to view all the products items in the cart, to add the required items to the cart, to make the payments successfully and to apply the discount coupons 

# SetUp
- Install Docker and Docker Compose
- Run below steps

```bash
docker-compose build
docker-compose up -d
```

# API GateWay

API Gateway: NGIX 
Base URL: http://localhost:8080

Below Service APIs are also accessable through the api gateway url

# User Service API

User Service API for user registration and login

## Endpoints

### Register User

**URL:** `/users/register`  
**Method:** `POST`  
**Description:** Register new user

**Request Body:**
```json
{
  "username": "newhasher",
  "email": "newhasher@testmail.com",
  "password": "1234"
}

```

**Curl**

```bash
curl -X POST http://localhost:5001/users/register -H "Content-Type: application/json" -d '{"username":"newhasher", "email":"newhasher@testmail.com", "password":"1234"}'

```


### Login User

**URL:** `/users/login`  
**Method:** `POST`  
**Description:** User login

**Request Body:**
```json
{
  "username": "newhasher",
  "password": "1234"
}

```

**Curl**

```bash
curl -X POST http://localhost:5000/users/login -H "Content-Type: application/json" -d '{"username":"newhasher", "password":"1234"}'

```

**Response Example**

```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NTU5ODIyNCwianRpIjoiYzA3NDc0N2UtOTJjZi00YTUyLWE3YjQtMTY5MzZlYjkzYWNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDU1OTgyMjQsImNzcmYiOiI5NTA1ZGU3NC1jZjI3LTQ5MTctODQ3ZS02YWRjZTQ4ZTZkOWYiLCJleHAiOjE3NDU1OTkxMjR9.mSvdu6G22XzZjTQht4ZmZUAj6JTWUJhRqk5PKd6cXEc"
}
```

# Product Service API

The Product Service API allows you to manage products in a catalog. You can create, retrieve products, as well as filter and sort them based on various criteria.

## Endpoints

### Create Product

**URL:** `/products`  
**Method:** `POST`  
**Description:** Create a new product.

**Request Body:**
```json
{
    "name": "string",
    "category": "string",
    "price": "float",
    "quantity": "integer",
    "rating": "float"
}
```
### Response

- **201 Created:** Product created successfully.
- **400 Bad Request:** Invalid input.

### Example
```bash
curl -X POST http://localhost:5002/products \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer JWT_TOKEN" \
     -d '{
           "name": "Test_Product_1",
           "category": "Electronics",
           "price": 100,
           "quantity": 10,
           "rating": 4.5
         }'

```
### Get All Products

**URL:** `/products`  
**Method:** `GET`  
**Description:** Retrieve all products.

**Response:**
- **200 OK:** List of products.

**Example `curl` Command:**
```bash
curl -X GET http://localhost:5002/products \
     -H "Authorization: Bearer JWT_TOKEN"
```
### Get Product by ID

**URL:** `/products/{id}`  
**Method:** `GET`  
**Description:** Retrieve a product by its ID.

**Response:**
- **200 OK:** Product details.
- **404 Not Found:** Product not found.

**Example `curl` Command:**
```bash
curl -X GET http://localhost:5000/products/{id} \
     -H "Authorization: Bearer JWT_TOKEN"
```
### Filter Products by Category

**URL:** `/products?category={category}`  
**Method:** `GET`  
**Description:** Retrieve products filtered by category.

**Response:**
- **200 OK:** List of products in the specified category.

**Example `curl` Command:**
```bash
curl -X GET "http://localhost:5000/products?category={category}" \
     -H "Authorization: Bearer JWT_TOKEN"
```

### Sort Products by Price

**URL:** `/products?sort_by=price&order={asc|desc}`  
**Method:** `GET`  
**Description:** Retrieve products sorted by price.

**Response:**
- **200 OK:** List of products sorted by price.

**Example `curl` Command:**
```bash
curl -X GET "http://localhost:5000/products?sort_by=price&order={asc|desc}" \
     -H "Authorization: Bearer JWT_TOKEN"

```


# Order Service API

## Endpoints

###  Get All Orders

- **Endpoint:** `/orders`
- **Method:** `GET`
- **Request Headers:**
  - `Authorization: Bearer <token>`
- **CURL:**

  ```bash
  curl -X GET http://127.0.0.1:5003/orders -H "Authorization: Bearer <token>"

  ```


###  Get Order By ID

- **Endpoint:** `/orders/<order_id>`
- **Method:** `GET`
- **Request Headers:**
  - `Authorization: Bearer <token>`
- **CURL:**

```bash
 curl -X GET http://127.0.0.1:5003/orders/2 -H "Authorization: Bearer <token>"
```


###  Add to cart

- **Endpoint:** `/orders/cart`
- **Method:** `POST`
- **Request Headers:**
  - `Authorization: Bearer <token>`
- **Request Payload:**

```json
{
  "product_id": 1,
  "quantity": 1
}

```

- **CURL:**
```bash
curl -X GET http://127.0.0.1:5003/orders/cart -d '{payload}' -H "Authorization: Bearer <token>"
```

###  GET User Cart Items

- **Endpoint:** `/orders/cart`
- **Method:** `GET`
- **Request Headers:**
  - `Authorization: Bearer <token>`

- **CURL:**
```bash
curl -X GET http://127.0.0.1:5003/orders/cart-H "Authorization: Bearer <token>"
```

###  Checkout

- **Endpoint:** `/orders/checkout`
- **Method:** `POST`
- **Request Headers:**
  - `Authorization: Bearer <token>`
- **Request Payload:** {}
- **CURL:**
```bash
curl -X POST http://127.0.0.1:5003/checkout -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{}'
```


###  Order Success

- **Endpoint:** `/orders/order-success`
- **Method:** `POST`
- **Request Headers:**
  - `Authorization: Bearer <token>`
- **Request Payload:** 
```json
{
  "order_id": 3
}

```
- **CURL:**
```bash
curl -X POST http://127.0.0.1:5003/orders/order-success -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"order_id":3}'
```

# Payments Service API

## Endpoints

### Create Payment

- **Endpoint:** `/payments/create`
- **Method:** `POST`
- **Request Headers:**
  - `Authorization: Bearer <token>`
- **Request Payload:**

 ```json
  {
    "order_id": 1,
    "amount": 100
  }
```
- **CURL:**
```bash
curl -X POST http://127.0.0.1:5004/api/payments/create -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"order_id":1,"amount":100}'

```

### Confirm Payment

- **Endpoint:** `/payments/confirm`
- **Method:** `POST`
- **Request Headers:**
  - `Authorization: Bearer <token>`
- **Request Payload:**

 ```json
{
  "payment_id": "c4c08750-284f-4b8e-b08a-9cbd9f8089a3"
}

```
- **CURL:**
```bash
curl -X POST http://127.0.0.1:5004/api/payments/confirm -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{"payment_id":"c4c08750-284f-4b8e-b08a-9cbd9f8089a3"}'

```