import os

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

from product_inventory_cli.exceptions import (
    InsufficientStockError,
    ProductNotFoundError,
)

load_dotenv()

db_url = os.environ["DATABASE_URL"]

pool = ConnectionPool(db_url)


def add_product(name, price, stock):
    if price < 0:
        raise ValueError("Price cannot be negative")
    if stock < 0:
        raise ValueError("Stock cannot be negative")

    with pool.connection() as con, con.cursor() as cur:
        cur.execute(
            "INSERT INTO products (product_name, price, stock) VALUES (%s, %s, %s) RETURNING *", (name, price, stock))
        product = cur.fetchone()
        return product


def get_product(product_id):
    with pool.connection() as con, con.cursor() as cur:
        cur.execute(
            "SELECT * FROM products WHERE id=%s", (product_id,))
        row = cur.fetchone()

        if row is None:
            raise ProductNotFoundError("Product not found.")

        return row


def list_products():
    with pool.connection() as con, con.cursor() as cur:
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()

        return rows


def update_product(product_id, price, stock):
    if price < 0:
        raise ValueError("Price cannot be negative")
    if stock < 0:
        raise ValueError("Stock cannot be negative")

    with pool.connection() as con, con.cursor() as cur:
        cur.execute(
            "UPDATE products SET price=%s, stock=%s WHERE id=%s RETURNING *", (price, stock, product_id))

        row = cur.fetchone()

        if row is None:
            raise ProductNotFoundError("Product not found.")

        return row


def delete_product(product_id):
    with pool.connection() as con, con.cursor() as cur:
        cur.execute(
            "DELETE FROM products WHERE id=%s RETURNING *", (product_id,))

        row = cur.fetchone()

        if row is None:
            raise ProductNotFoundError("Product not found.")

        return row


def buy_product(product_id, quantity):
    if quantity <= 0:
        raise ValueError("Quantity must be 1 or more.")
    with pool.connection() as con, con.cursor() as cur:
        cur.execute("UPDATE products SET stock = stock - %s WHERE id = %s AND stock >= %s RETURNING *",
                    (quantity, product_id, quantity))
        update_row = cur.fetchone()

        cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
        select_row = cur.fetchone()

        if update_row is None and select_row is not None:
            raise InsufficientStockError(
                "Not enough stock for this product.")
        if update_row is None and select_row is None:
            raise ProductNotFoundError("Product not found in database.")

        cur.execute(
            "INSERT INTO orders (product_id, quantity) VALUES (%s, %s) RETURNING *", (product_id, quantity))

        row = cur.fetchone()

        return row
