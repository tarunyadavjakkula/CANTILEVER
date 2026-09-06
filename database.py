import sqlite3
import os

DATABASE_PATH = "data/products.db"

def get_connection():
    """Establish database connection with Row row_factory for dict-like access."""
    os.makedirs("data", exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def create_database():
    """Create the database using SQLite and create the products table."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL,
            rating REAL,
            description TEXT,
            category TEXT,
            url TEXT
        )
    """)

    connection.commit()
    connection.close()
    print("Database and table initialized successfully!")

def insert_product(title, price, rating, description, category, url):
    """Insert a single product into the products table."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO products (title, price, rating, description, category, url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, price, rating, description, category, url))
    product_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return product_id

def insert_products(products_list):
    """Insert a list of product dictionaries into the database."""
    connection = get_connection()
    cursor = connection.cursor()
    for p in products_list:
        cursor.execute("""
            INSERT INTO products (title, price, rating, description, category, url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            p.get('title'),
            p.get('price'),
            p.get('rating'),
            p.get('description'),
            p.get('category'),
            p.get('url')
        ))
    connection.commit()
    connection.close()

def get_all_products():
    """Fetch all products from the database."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

def get_product_by_id(product_id):
    """Fetch a single product by its primary key ID."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    connection.close()
    return dict(row) if row else None

def search_products(query):
    """Search products by title, category, or description."""
    connection = get_connection()
    cursor = connection.cursor()
    search_pattern = f"%{query}%"
    cursor.execute("""
        SELECT * FROM products 
        WHERE title LIKE ? OR category LIKE ? OR description LIKE ?
    """, (search_pattern, search_pattern, search_pattern))
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

def delete_product(product_id):
    """Delete a product by ID."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    deleted_count = cursor.rowcount
    connection.commit()
    connection.close()
    return deleted_count > 0

def clear_products():
    """Clear all records from the products table."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products")
    connection.commit()
    connection.close()

def test_database_operations():
    """Test CRUD operations using temporary sample products."""
    print("--- Running Database Operations Tests ---")
    create_database()
    clear_products()

    # 1. Insert Products
    sample_items = [
        {
            "title": "Wireless Bluetooth Headphones",
            "price": 49.99,
            "rating": 4.5,
            "description": "High quality wireless over-ear headphones.",
            "category": "Electronics",
            "url": "https://example.com/headphones"
        },
        {
            "title": "Ergonomic Gaming Mouse",
            "price": 29.95,
            "rating": 4.2,
            "description": "RGB gaming mouse with high DPI precision.",
            "category": "Electronics",
            "url": "https://example.com/mouse"
        },
        {
            "title": "Python Programming Guide",
            "price": 19.99,
            "rating": 4.8,
            "description": "Comprehensive guide to mastering Python.",
            "category": "Books",
            "url": "https://example.com/python-book"
        }
    ]

    insert_products(sample_items)
    print(f"Inserted {len(sample_items)} sample products.")

    # 2. Get All Products
    all_products = get_all_products()
    print(f"Total products in DB: {len(all_products)}")

    # 3. Get Product by ID
    first_id = all_products[0]["id"]
    product = get_product_by_id(first_id)
    print(f"Fetched product ID {first_id}: {product['title']}")

    # 4. Search Products
    search_results = search_products("Headphones")
    print(f"Search results for 'Headphones': {len(search_results)} item(s) found.")

    # 5. Delete Product
    delete_product(first_id)
    print(f"Deleted product ID {first_id}. Remaining count: {len(get_all_products())}")

    print("--- Database Operations Test Complete ---\n")

if __name__ == "__main__":
    test_database_operations()