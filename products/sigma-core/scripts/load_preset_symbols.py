#!/usr/bin/env python3
"""
Load symbols into sc.universe_preset_symbols from a CSV/plain-text file.

Usage:
  python scripts/load_preset_symbols.py --preset sp500 --file ./sp500.csv [--truncate]

Reads products/sigma-core/.env for DB connection (DATABASE_URL or DB_* vars).
"""
import argparse
import csv
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


def read_symbols(path: Path) -> list[str]:
    text = path.read_text(encoding='utf-8')
    # Support simple newline-delimited or CSV with a 'symbol' column
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    # Heuristic: if first line contains comma or 'symbol', parse as CSV
    if ("," in lines[0]) or (lines[0].lower().startswith("symbol")):
        symbols: list[str] = []
        with path.open(newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            # If there is no header, fallback to first column
            if reader.fieldnames and 'symbol' in [fn.lower() for fn in reader.fieldnames]:
                # Map case-insensitively to 'symbol'
                sym_key = next(fn for fn in reader.fieldnames if fn.lower() == 'symbol')
                for row in reader:
                    sym = (row.get(sym_key) or '').strip().upper()
                    if sym:
                        symbols.append(sym)
            else:
                fh.seek(0)
                raw = csv.reader(fh)
                for row in raw:
                    if not row:
                        continue
                    sym = str(row[0]).strip().upper()
                    if sym and sym.lower() != 'symbol':
                        symbols.append(sym)
        return symbols
    # Plain list
    return [ln.split(',')[0].strip().upper() for ln in lines if ln]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--preset', required=True, help='Preset id (e.g., sp500)')
    ap.add_argument('--file', required=True, help='Path to CSV or plain list of symbols')
    ap.add_argument('--truncate', action='store_true', help='Clear existing symbols first')
    args = ap.parse_args()

    fpath = Path(args.file)
    if not fpath.exists():
        raise SystemExit(f"File not found: {fpath}")

    symbols = read_symbols(fpath)
    if not symbols:
        raise SystemExit("No symbols parsed from file")

    import psycopg2
    with get_conn() as conn:
        with conn.cursor() as cur:
            # Ensure preset exists
            cur.execute("SELECT 1 FROM sc.universe_presets WHERE preset_id = %s", (args.preset,))
            if not cur.fetchone():
                raise SystemExit(f"Preset not found: {args.preset}")
            if args.truncate:
                cur.execute("DELETE FROM sc.universe_preset_symbols WHERE preset_id = %s", (args.preset,))
            # Insert symbols
            for sym in symbols:
                cur.execute(
                    "INSERT INTO sc.universe_preset_symbols (preset_id, symbol) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (args.preset, sym),
                )
            # Update count on preset
            cur.execute(
                "UPDATE sc.universe_presets SET symbol_count = (SELECT COUNT(*) FROM sc.universe_preset_symbols WHERE preset_id = %s) WHERE preset_id = %s",
                (args.preset, args.preset),
            )
        conn.commit()
    print(f"Loaded {len(symbols)} symbols into preset '{args.preset}'.")


if __name__ == '__main__':
    main()

