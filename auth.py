import sqlite3
import hashlib

def connect_db():
    return sqlite3.connect("data/users.db")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_users_table():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_user(username, password, role="user"):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?)",
                (username, hash_password(password), role))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    result = cur.fetchone()
    conn.close()

    return result[0] if result else None