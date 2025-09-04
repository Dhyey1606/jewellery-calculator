import sqlite3

DB_FILE = "gold_rates.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_rates (
            id INTEGER PRIMARY KEY,
            rate REAL NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Ensure a single row with id=1 exists
    cur.execute("INSERT OR IGNORE INTO gold_rates (id, rate) VALUES (1, 0)")
    conn.commit()
    cur.close()
    conn.close()
