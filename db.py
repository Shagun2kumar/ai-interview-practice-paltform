import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # USERS TABLE
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT,
            name TEXT,
            course TEXT
        )
    """)

    # RESULTS TABLE
    c.execute("""
        CREATE TABLE IF NOT EXISTS results(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            score INTEGER
        )
    """)

    conn.commit()
    conn.close()


# REGISTER USER
def register_user(username, password, name, course):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # check duplicate
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        conn.close()
        return False

    c.execute(
        "INSERT INTO users(username, password, name, course) VALUES(?,?,?,?)",
        (username, password, name, course)
    )

    conn.commit()
    conn.close()

    print("User Registered:", username)
    return True


# LOGIN USER
def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = c.fetchone()
    conn.close()

    print("Login Check:", user)
    return user


# SAVE SCORE
def save_score(username, score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO results(username, score) VALUES(?,?)",
        (username, score)
    )

    conn.commit()
    conn.close()

    print("Score Saved:", score)


# GET SCORES
def get_scores():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT username, score FROM results")
    data = c.fetchall()

    conn.close()
    return data

