import sqlite3

def initiate_db():
    connection = sqlite3.connect("test_telegram.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    """)

    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect("test_telegram.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()

    connection.commit()
    connection.close()

    return products

# initiate_db()
# connection = sqlite3.connect("test_telegram.db")
# cursor = connection.cursor()
#
# for number in range(1, 5):
#     cursor.execute("INSERT INTO Products(title, description, price) VALUES (?, ?, ?)", (f"Продукт {number}", f"Описание {number}", number * 100))
#
# connection.commit()
# connection.close()

