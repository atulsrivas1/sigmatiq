from typing import List, Optional
from psycopg2.extras import RealDictCursor
from sigma_core.storage.relational import get_db


class WatchlistRegistry:
    def create_watchlist(self, *, user_id: str, name: str, description: Optional[str] = None, visibility: str = 'private', is_default: bool = False) -> dict:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    INSERT INTO sc.watchlists (user_id, name, description, visibility, is_default)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_id, name) DO UPDATE SET description = EXCLUDED.description, visibility = EXCLUDED.visibility, is_default = EXCLUDED.is_default
                    RETURNING watchlist_id, user_id, name, description, visibility, is_default, created_at, updated_at
                    """,
                    (user_id, name, description, visibility, is_default),
                )
                row = cur.fetchone(); conn.commit(); return dict(row)

    def list_watchlists(self, *, user_id: str) -> List[dict]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT watchlist_id, user_id, name, description, visibility, is_default, created_at, updated_at FROM sc.watchlists WHERE user_id = %s ORDER BY is_default DESC, name", (user_id,))
                return [dict(r) for r in cur.fetchall()]

    def get(self, *, watchlist_id: str) -> Optional[dict]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT watchlist_id, user_id, name, description, visibility, is_default, created_at, updated_at FROM sc.watchlists WHERE watchlist_id = %s", (watchlist_id,))
                row = cur.fetchone(); return dict(row) if row else None

    def delete(self, *, watchlist_id: str) -> None:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM sc.watchlists WHERE watchlist_id = %s", (watchlist_id,)); conn.commit()

    def add_symbols(self, *, watchlist_id: str, symbols: List[str]) -> int:
        if not symbols: return 0
        with get_db() as conn:
            with conn.cursor() as cur:
                for sym in symbols:
                    cur.execute(
                        "INSERT INTO sc.watchlist_symbols (watchlist_id, symbol) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        (watchlist_id, sym),
                    )
                conn.commit()
                return len(symbols)

    def remove_symbol(self, *, watchlist_id: str, symbol: str) -> None:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM sc.watchlist_symbols WHERE watchlist_id = %s AND symbol = %s", (watchlist_id, symbol)); conn.commit()

    def get_symbols(self, *, watchlist_id: str) -> List[str]:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT symbol FROM sc.watchlist_symbols WHERE watchlist_id = %s ORDER BY sort NULLS LAST, symbol", (watchlist_id,))
                return [r[0] for r in cur.fetchall()]
