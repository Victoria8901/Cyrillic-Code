import os
import psycopg2


def load_db():
    conn = psycopg2.connect(
        database='PROJECT',
        user='Project',
        password='0000',
        host='127.0.0.1',
        port=5432,
    )
    if conn:
        return conn
