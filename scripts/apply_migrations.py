#!/usr/bin/env python
"""
Apply SQL migrations in order against a Postgres database.

Connection sources (in order of precedence):
- DATABASE_URL (e.g., postgres://user:pass@host:port/db)
- DB_* env vars: DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

Usage:
  python scripts/apply_migrations.py --dir products/sigma-lab/api/migrations
  python scripts/apply_migrations.py --dir products/sigma-lab/api/migrations --dry-run
"""
import argparse
import os
from pathlib import Path
import sys

# Load .env if available (repo root or product api dir)
try:
    from dotenv import load_dotenv  # type: ignore
    # Try repo root .env
    root_env = Path(__file__).resolve().parents[1] / '.env'
    if root_env.exists():
        load_dotenv(dotenv_path=root_env)
    # Try product api .env (products/sigma-lab/.env)
    prod_env = Path(__file__).resolve().parents[2] / 'products' / 'sigma-lab' / '.env'
    if prod_env.exists():
        load_dotenv(dotenv_path=prod_env, override=False)
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
    dbname = os.getenv('DB_NAME') or os.getenv('DB_DATABASE') or os.getenv('PGDATABASE') or 'postgres'
    return psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', required=True, help='Directory containing *.sql migrations')
    ap.add_argument('--dry-run', action='store_true', help='List files without applying')
    args = ap.parse_args()

    mig_dir = Path(args.dir)
    if not mig_dir.exists() or not mig_dir.is_dir():
        print(f"Migration dir not found: {mig_dir}", file=sys.stderr)
        sys.exit(1)
    files = sorted([p for p in mig_dir.glob('*.sql')])
    if not files:
        print(f"No .sql migrations found in {mig_dir}")
        return
    print(f"Found {len(files)} migrations in {mig_dir}")
    for f in files:
        print(f" - {f.name}")
    if args.dry_run:
        print("Dry-run mode: not applying migrations.")
        return

    try:
        conn = get_conn()
    except Exception as e:
        print(f"Failed to connect to DB: {e}", file=sys.stderr)
        sys.exit(2)
    try:
        with conn:
            with conn.cursor() as cur:
                for f in files:
                    sql = f.read_text(encoding='utf-8')
                    print(f"Applying {f.name}...")
                    cur.execute(sql)
        print("Migrations applied successfully.")
    finally:
        try:
            conn.close()
        except Exception:
            pass

if __name__ == '__main__':
    main()
