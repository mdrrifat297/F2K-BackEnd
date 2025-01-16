import sqlite3

# SQLite ডাটাবেস কানেকশন তৈরি
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

# টেবিল তৈরি (যদি না থাকে)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")

conn.commit()
