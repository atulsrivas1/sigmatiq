from __future__ import annotations
import argparse
import os
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description="Apply SQL migrations in order")
    ap.add_argument('--dir', dest='dir', default='migrations', help='Migrations directory (default: migrations)')
    ap.add_argument('--dry-run', action='store_true', help='List migrations without applying or connecting to DB')
    args = ap.parse_args()
    # Load product-local .env if present for DB_* vars
    try:
        from dotenv import load_dotenv  # type: ignore
        here = Path(__file__).resolve()
        product_root = here.parents[2]  # products/sigma-lab
        env_path = product_root / '.env'
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
    except Exception:
        pass

    d = Path(args.dir)
    if not d.exists():
        raise SystemExit(f"Migrations directory not found: {d}")

    files = sorted([p for p in d.glob('*.sql')])
    if args.dry_run:
        for p in files:
            print(f"DRY-RUN: {p.name}")
        print(f"Total: {len(files)} migrations")
        return

    try:
        import psycopg2
    except Exception:
        raise SystemExit("psycopg2 is not installed; cannot apply migrations")

    user = os.getenv('DB_USER'); password = os.getenv('DB_PASSWORD'); host = os.getenv('DB_HOST'); port = os.getenv('DB_PORT'); database = os.getenv('DB_NAME')
    missing = [k for k,v in {'DB_USER':user,'DB_PASSWORD':password,'DB_HOST':host,'DB_PORT':port,'DB_NAME':database}.items() if not v]
    if missing:
        raise SystemExit(f"Database env vars missing: {', '.join(missing)}")

    conn = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    try:
        cur = conn.cursor()
        # Optional schema selection/creation
        schema = os.getenv('DB_SCHEMA')
        if schema:
            try:
                cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"; SET search_path TO "{schema}";')
                conn.commit()
                print(f"-- Using schema: {schema}")
            except Exception as e:
                print(f"-- Warning: could not ensure schema {schema}: {e}")
        for p in files:
            sql = p.read_text()
            print(f"-- Applying {p.name} ({len(sql)} bytes)")
            cur.execute(sql)
            conn.commit()
        print(f"Applied {len(files)} migrations")
    finally:
        conn.close()

if __name__ == '__main__':
    main()
