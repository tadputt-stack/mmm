from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from contextlib import closing
from typing import List, Optional
import sqlite3
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# สร้างโฟลเดอร์ static/assets สำหรับเก็บรูปภาพ
os.makedirs("static/assets", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


class Product(BaseModel):
    id: Optional[int] = None
    name: str
    image_path: str
    description: str
    price: float
    rating: float


def get_db_connection():
    # เชื่อมต่อกับไฟล์ beverage.db
    conn = sqlite3.connect("beverage.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/products", response_model=List[Product])
def read_products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return [dict(product) for product in products]


@app.get("/product")
def read_product(product_id: int):
    try:
        conn = get_db_connection()
        product = conn.execute(
            "SELECT * FROM products WHERE id = ?", (product_id,)
        ).fetchone()

        if not product:
            raise HTTPException(
                status_code=404, detail="Product not found"
            )

        return Product(**dict(product))
    finally:
        conn.close()


@app.post("/product", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    with closing(get_db_connection()) as conn:
        # ปรับเรียงลำดับคอลัมน์ให้ตรงกับโครงสร้างตาราง SQLite (id, name, description, price, rating, image_path)
        cur = conn.execute(
            """
            INSERT INTO products (name, description, price, rating, image_path)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                product.name,
                product.description,
                product.price,
                product.rating,
                product.image_path,
            ),
        )
        conn.commit()
        # นำ id ล่าสุดที่เพิ่มเข้าฐานข้อมูลใส่กลับไปที่ Object
        product.id = cur.lastrowid
    return product