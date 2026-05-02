import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash


def get_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'spendly.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def create_user(name, email, password):
    conn = get_db()
    password_hash = generate_password_hash(password)
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def get_user_by_email(email):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user


def verify_user(email, password):
    user = get_user_by_email(email)
    if user is None:
        return None
    if check_password_hash(user["password_hash"], password):
        return user
    return None


def seed_db():
    conn = get_db()
    row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
    if row[0] > 0:
        conn.close()
        return

    password_hash = generate_password_hash("demo123")
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash)
    )
    conn.commit()

    user_id = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
    ).fetchone()["id"]

    expenses = [
        (user_id, 12.50,  "Food",          "2026-05-01", "Breakfast at cafe"),
        (user_id, 45.00,  "Transport",     "2026-05-03", "Monthly bus pass top-up"),
        (user_id, 120.00, "Bills",         "2026-05-05", "Electricity bill"),
        (user_id, 30.00,  "Health",        "2026-05-08", "Pharmacy – vitamins"),
        (user_id, 18.00,  "Entertainment", "2026-05-10", "Cinema ticket"),
        (user_id, 65.00,  "Shopping",      "2026-05-14", "New running shoes"),
        (user_id, 9.99,   "Other",         "2026-05-18", "Notebook and pens"),
        (user_id, 22.75,  "Food",          "2026-05-22", "Grocery run"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses
    )
    conn.commit()
    conn.close()
