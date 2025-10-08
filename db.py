import os
import psycopg2

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set!")
    
    if not DATABASE_URL.startswith("postgresql://"):
        raise ValueError(f"Invalid DATABASE_URL format: {DATABASE_URL[:20]}...")
    
    # Connection string already has sslmode=require, so don't add it again
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