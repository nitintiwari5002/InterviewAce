import sqlite3

DB_PATH = "users.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT UNIQUE,
            email TEXT,
            password TEXT
        )
        """
    )

    conn.commit()
    conn.close()

def register_user(username, email, password):
    if not username or not email or not password:
        return False

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def register_company(company_name, email, password):
    if not company_name or not email or not password:
        return False

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO companies (company_name, email, password) VALUES (?, ?, ?)",
            (company_name, email, password),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password),
    )
    user = cur.fetchone()
    conn.close()
    return user

def login_company(company_name, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM companies WHERE company_name=? AND password=?",
        (company_name, password),
    )
    company = cur.fetchone()
    conn.close()
    return company