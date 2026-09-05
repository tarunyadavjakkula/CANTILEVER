import sqlite3
import os

DATABASE_PATH = "data/products.db"

def create_database():
    """Create the database using SQLite and create the products table."""

    os.makedirs("data", exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

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

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()