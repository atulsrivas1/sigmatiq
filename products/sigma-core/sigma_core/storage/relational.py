import os
from contextlib import contextmanager

try:
    import psycopg2
    from psycopg2 import pool as _pool
except Exception as e:  # pragma: no cover
    psycopg2 = None
    _pool = None


class Database:
    def __init__(self):
        self.pool = None

    def _ensure_pool(self):
        if self.pool is not None:
            return
        if psycopg2 is None or _pool is None:
            raise RuntimeError("psycopg2 is not installed; DB-backed registry is unavailable")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        database = os.getenv("DB_NAME")
        missing = [k for k, v in {
            'DB_USER': user, 'DB_PASSWORD': password, 'DB_HOST': host, 'DB_PORT': port, 'DB_NAME': database
        }.items() if not v]
        if missing:
            raise RuntimeError(f"Database env vars missing: {', '.join(missing)}")
        self.pool = _pool.SimpleConnectionPool(1, 20, user=user, password=password, host=host, port=port, database=database)

    @contextmanager
    def get_connection(self):
        self._ensure_pool()
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)


db = Database()


@contextmanager
def get_db():
    """Context-managed DB connection.

    Usage: with get_db() as conn: ...
    Raises RuntimeError with clear message if psycopg2 or env vars are missing.
    """
    with db.get_connection() as conn:
        yield conn
