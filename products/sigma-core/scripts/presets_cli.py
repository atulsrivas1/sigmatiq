#!/usr/bin/env python3
"""
Presets CLI: create/update universe presets so you can load CSV rosters.

Examples:
  python scripts/presets_cli.py create --id sp100 --title "S&P 100" --desc "Large-cap subset" --source "S&P" --version 2024-08
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path

# Load .env from sigma-core folder (self-contained)
try:
    from dotenv import load_dotenv  # type: ignore
    core_env = Path(__file__).resolve().parents[1] / '.env'
    if core_env.exists():
        load_dotenv(dotenv_path=core_env)
except Exception:
    pass


def get_conn():
    import psycopg2
    url = os.getenv('DATABASE_URL')
    if url:
        return psycopg2.connect(url)
    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', '5432'))
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', '')
    dbname = os.getenv('DB_NAME', 'postgres')
    return psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)


def cmd_create(args: argparse.Namespace) -> None:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sc.universe_presets (preset_id, title, description, source, version, symbol_count)
                VALUES (%s,%s,%s,%s,%s, COALESCE((SELECT COUNT(*) FROM sc.universe_preset_symbols WHERE preset_id=%s), 0))
                ON CONFLICT (preset_id) DO UPDATE SET title=EXCLUDED.title, description=EXCLUDED.description, source=EXCLUDED.source, version=EXCLUDED.version
                """,
                (args.id, args.title, args.desc, args.source, args.version, args.id),
            )
        conn.commit()
    print("ok")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Presets CLI")
    sp = ap.add_subparsers(dest="cmd", required=True)
    p1 = sp.add_parser("create", help="create or update a preset")
    p1.add_argument("--id", required=True, help="preset id (e.g., sp100)")
    p1.add_argument("--title", required=True, help="title")
    p1.add_argument("--desc", default="", help="description")
    p1.add_argument("--source", default="Internal", help="source")
    p1.add_argument("--version", default="", help="version string (e.g., 2024-08)")
    p1.set_defaults(func=cmd_create)
    return ap


def main() -> None:
    ap = build_parser()
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

