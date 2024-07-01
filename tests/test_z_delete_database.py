import psycopg2
from config import config


def test_delete_database():
    conn = psycopg2.connect(dbname='postgres', **config())
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE test_db with (FORCE)')
    cur.close()
    conn.close()
