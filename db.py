import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL", sslmode = 'require')

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS gold_rates (
            id SERIAL PRIMARY KEY,
            rate NUMERIC NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
