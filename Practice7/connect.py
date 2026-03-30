import psycopg2
from config import load_config


def get_connection():
    cfg = load_config()
    conn = psycopg2.connect(**cfg)
    return conn


conn = get_connection()
print("Connected successfully!")
conn.close()