# HashKart
HashKart application is one stop destination for all kinds of shopping needs for the customers. The application enables the users to view all the products items in the cart, to add the required items to the cart, to make the payments successfully and to apply the discount coupons 


# Product Service API

The Product Service API allows you to manage products in a catalog. You can create, retrieve, update, and delete products, as well as filter and sort them based on various criteria.

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
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -d '{
           "name": "Test Product",
           "category": "Electronics",
           "price": 99.99,
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
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
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
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
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
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
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
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

