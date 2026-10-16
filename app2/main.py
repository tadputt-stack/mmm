from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1001, "name": "Coffee", "price": "10.99"},
    {"id": 1002, "name": "Soda", "price": "15.99"},
    {"id": 1003, "name": "Tea", "price": "12.99"},
]

@app.get("/")
def home():
    return {"message": "Welcome to My API"}


@app.get("/products")
def get_products():
    return products

@app.get("/product")
def get_product(id: int):
    for product in products:
        if product["id"] == id:
            return product
        return {"error": "Product not found" }