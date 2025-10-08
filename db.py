import os
import psycopg2

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    # sslmode goes in the connect() call, not in get()
    return psycopg2.connect(DATABASE_URL, sslmode="require")

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