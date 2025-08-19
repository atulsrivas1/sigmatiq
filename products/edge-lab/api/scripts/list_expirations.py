#!/usr/bin/env python3
from __future__ import annotations
import argparse, sys, json
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import requests


def main():
    ap = argparse.ArgumentParser(description='List upcoming option expirations via API helper')
    ap.add_argument('--ticker', required=True)
    ap.add_argument('--start', default=None, help='YYYY-MM-DD (default: today)')
    ap.add_argument('--weeks', type=int, default=12)
    ap.add_argument('--base_url', default='http://localhost:8001')
    args = ap.parse_args()

    url = f"{args.base_url}/options/expirations"
    try:
        r = requests.get(url, params={'ticker': args.ticker, 'start': args.start, 'weeks': args.weeks}, timeout=30)
        r.raise_for_status()
        print(json.dumps(r.json(), indent=2))
    except Exception as e:
        print(f"Error calling {url}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
