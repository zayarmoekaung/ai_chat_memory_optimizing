import sqlite3

def db_connect(db_path):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn

def db_init(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        turn INTEGER,
        character TEXT,
        narration TEXT,
        data TEXT,
        timestamp TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS facts (
        id INTEGER PRIMARY KEY,
        character TEXT,
        fact TEXT,
        importance REAL,
        embedding BLOB,
        turn INTEGER
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS reflections (
        character TEXT PRIMARY KEY,
        reflection TEXT,
        last_updated_turn INTEGER
    )''')
    conn.commit()
    return c