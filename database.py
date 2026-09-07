"""
Database module for managing SQLite storage of e-commerce products.
"""
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
            url TEXT UNIQUE
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
        INSERT OR REPLACE INTO products (title, price, rating, description, category, url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, price, rating, description, category, url))
    product_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return product_id

def insert_products(products_list):
    """Insert a list of product dictionaries into the database avoiding duplicates."""
    connection = get_connection()
    cursor = connection.cursor()
    for p in products_list:
        cursor.execute("""
            INSERT OR REPLACE INTO products (title, price, rating, description, category, url)
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
    cursor.execute("SELECT * FROM products ORDER BY id ASC")
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

def get_categories():
    """Fetch distinct categories available in the database."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT DISTINCT category 
        FROM products 
        WHERE category IS NOT NULL AND category != '' AND category != 'Uncategorized'
        ORDER BY category ASC
    """)
    rows = cursor.fetchall()
    connection.close()
    return [row["category"] for row in rows]

def get_filtered_products(query=None, category=None, min_price=None, max_price=None, min_rating=None, sort_by=None):
    """
    Search, filter, and sort products dynamically.
    """
    connection = get_connection()
    cursor = connection.cursor()

    sql = "SELECT * FROM products WHERE 1=1"
    params = []

    if query:
        search_pattern = f"%{query.strip()}%"
        sql += " AND (title LIKE ? OR description LIKE ? OR category LIKE ?)"
        params.extend([search_pattern, search_pattern, search_pattern])

    if category:
        sql += " AND category = ?"
        params.append(category)

    if min_price is not None and min_price != "":
        try:
            sql += " AND price >= ?"
            params.append(float(min_price))
        except ValueError:
            pass

    if max_price is not None and max_price != "":
        try:
            sql += " AND price <= ?"
            params.append(float(max_price))
        except ValueError:
            pass

    if min_rating is not None and min_rating != "":
        try:
            sql += " AND rating >= ?"
            params.append(float(min_rating))
        except ValueError:
            pass

    # Sorting
    if sort_by == "price_asc":
        sql += " ORDER BY price ASC"
    elif sort_by == "price_desc":
        sql += " ORDER BY price DESC"
    elif sort_by == "rating_desc":
        sql += " ORDER BY rating DESC"
    elif sort_by == "rating_asc":
        sql += " ORDER BY rating ASC"
    else:
        sql += " ORDER BY id ASC"

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    connection.close()
    return [dict(row) for row in rows]

def search_products(query):
    """Search products by title, category, or description."""
    return get_filtered_products(query=query)

def get_analytics_summary():
    """Calculate summary statistics directly from SQLite for dashboard metrics."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            COUNT(*) as total_products,
            AVG(price) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price,
            AVG(rating) as avg_rating,
            COUNT(DISTINCT category) as total_categories
        FROM products
    """)
    row = cursor.fetchone()
    connection.close()

    if not row or row["total_products"] == 0:
        return {
            "total_products": 0,
            "avg_price": 0.0,
            "min_price": 0.0,
            "max_price": 0.0,
            "avg_rating": 0.0,
            "total_categories": 0
        }

    return {
        "total_products": row["total_products"] or 0,
        "avg_price": round(row["avg_price"] or 0.0, 2),
        "min_price": round(row["min_price"] or 0.0, 2),
        "max_price": round(row["max_price"] or 0.0, 2),
        "avg_rating": round(row["avg_rating"] or 0.0, 1),
        "total_categories": row["total_categories"] or 0
    }

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

    # 5. Categories
    cats = get_categories()
    print(f"Categories: {cats}")

    # 6. Analytics
    analytics = get_analytics_summary()
    print(f"Analytics Summary: {analytics}")

    print("--- Database Operations Test Complete ---\n")

if __name__ == "__main__":
    test_database_operations()