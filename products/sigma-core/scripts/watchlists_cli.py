#!/usr/bin/env python3
"""
Watchlists CLI

Create and manage user watchlists directly via DB (no API server required).

Examples:
  python scripts/watchlists_cli.py create --user u123 --name demo --symbols AAPL,MSFT,SPY --default
  python scripts/watchlists_cli.py add-symbols --user u123 --watchlist-id <uuid> --symbols TSLA,NVDA
  python scripts/watchlists_cli.py list --user u123
"""
from __future__ import annotations

import argparse
from typing import List

from sigma_core.storage.relational import get_db


def cmd_create(args: argparse.Namespace) -> None:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sc.watchlists (user_id, name, description, visibility, is_default)
                VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT (user_id, name) DO UPDATE SET description=EXCLUDED.description, visibility=EXCLUDED.visibility, is_default=EXCLUDED.is_default
                RETURNING watchlist_id
                """,
                (args.user, args.name, args.description or None, args.visibility or "private", bool(args.default)),
            )
            wid = cur.fetchone()[0]
            if args.symbols:
                symbols: List[str] = [s.strip() for s in args.symbols.split(',') if s.strip()]
                for sym in symbols:
                    cur.execute(
                        "INSERT INTO sc.watchlist_symbols (watchlist_id, symbol) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                        (wid, sym),
                    )
            conn.commit()
            print(str(wid))


def cmd_add_symbols(args: argparse.Namespace) -> None:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM sc.watchlists WHERE watchlist_id=%s AND user_id=%s", (args.watchlist_id, args.user))
            if not cur.fetchone():
                raise SystemExit("watchlist not found or not owned by user")
            symbols: List[str] = [s.strip() for s in args.symbols.split(',') if s.strip()]
            for sym in symbols:
                cur.execute(
                    "INSERT INTO sc.watchlist_symbols (watchlist_id, symbol) VALUES (%s,%s) ON CONFLICT DO NOTHING",
                    (args.watchlist_id, sym),
                )
            conn.commit()
            print("ok")


def cmd_list(args: argparse.Namespace) -> None:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT watchlist_id, name, description, visibility, is_default, created_at, updated_at
                FROM sc.watchlists WHERE user_id=%s ORDER BY is_default DESC, name
                """,
                (args.user,),
            )
            rows = cur.fetchall()
            for r in rows:
                print(f"{r[0]}\t{r[1]}\t{r[3]}\tdefault={r[4]}")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Watchlists CLI")
    sp = ap.add_subparsers(dest="cmd", required=True)

    p1 = sp.add_parser("create", help="create or update a watchlist; prints ID")
    p1.add_argument("--user", required=True, help="user id")
    p1.add_argument("--name", required=True, help="watchlist name")
    p1.add_argument("--description", help="description")
    p1.add_argument("--visibility", default="private", choices=["private","shared","public"], help="visibility")
    p1.add_argument("--default", action="store_true", help="mark as default")
    p1.add_argument("--symbols", help="comma-separated symbols to add")
    p1.set_defaults(func=cmd_create)

    p2 = sp.add_parser("add-symbols", help="add symbols to a watchlist")
    p2.add_argument("--user", required=True, help="user id")
    p2.add_argument("--watchlist-id", required=True, help="watchlist UUID")
    p2.add_argument("--symbols", required=True, help="comma-separated symbols to add")
    p2.set_defaults(func=cmd_add_symbols)

    p3 = sp.add_parser("list", help="list user watchlists")
    p3.add_argument("--user", required=True, help="user id")
    p3.set_defaults(func=cmd_list)

    return ap


def main() -> None:
    ap = build_parser()
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

