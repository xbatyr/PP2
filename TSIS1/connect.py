import psycopg2
from config import load_config


def get_connection():
    params = load_config()
    return psycopg2.connect(**params)