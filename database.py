import os
import psycopg2
from psycopg2.extras import DictCursor

DATABASE_URL = os.getenv("DATABASE_URL")


class CompatibleCursor:

    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, query, params=None):
        # Convert SQLite-style ? placeholders to PostgreSQL %s
        query = query.replace("?", "%s")
        return self.cursor.execute(query, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def __getattr__(self, name):
        return getattr(self.cursor, name)


class CompatibleConnection:

    def __init__(self, conn):
        self.conn = conn

    def cursor(self):
        return CompatibleCursor(
            self.conn.cursor(cursor_factory=DictCursor)
        )

    def commit(self):
        return self.conn.commit()

    def rollback(self):
        return self.conn.rollback()

    def close(self):
        return self.conn.close()

    def __getattr__(self, name):
        return getattr(self.conn, name)


def get_connection():

    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set."
        )

    conn = psycopg2.connect(DATABASE_URL)

    return CompatibleConnection(conn)