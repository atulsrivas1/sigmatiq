Parity Quickstart (Underlying vs Premium)

This guide shows how to generate option overlays from stock signals, compute underlying-based and premium-based parity, and list overlays later.

Prereqs
- Run the API locally: `python products/edge-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload`
- Build + generate signals for your model (e.g., stock scan or pipeline).

POST /options_overlay
- Base body:
  {
    "model_id": "spy_0dte_hourly",
    "pack_id": "zeroedge",
    "date": "2024-08-15",
    "option_mode": "single"  // or "vertical"
  }

Flags
- include_underlying_parity (bool, default true):
  Computes if next session’s underlying highs/lows hit the stock target/stop.
- include_premium_parity (bool, default true):
  Fetches option quotes for next session and checks if premium targets/stops are hit.
- write_parity_csv (bool, default false):
  When premium parity runs, writes a per-overlay outcomes CSV to `reports/<model_id>/options_parity_<date>_<expiry>.csv`.

Examples
1) Underlying-only parity:
  curl -sS -X POST "http://localhost:8001/options_overlay" \
    -H "Content-Type: application/json" \
    -d '{"model_id":"spy_0dte_hourly","pack_id":"zeroedge","date":"2024-08-15","include_underlying_parity":true,"include_premium_parity":false}'

2) Premium-only parity (vertical 5-wide) + CSV:
  curl -sS -X POST "http://localhost:8001/options_overlay" \
    -H "Content-Type: application/json" \
    -d '{"model_id":"spy_0dte_hourly","pack_id":"zeroedge","date":"2024-08-15","option_mode":"vertical","spread_width":5,"include_underlying_parity":false,"include_premium_parity":true,"write_parity_csv":true}'

3) List overlays:
  curl -sS "http://localhost:8001/option_signals?model_id=spy_0dte_hourly&limit=20&offset=0"

Notes
- When DB is not configured, options overlay still computes/returns parity summaries and will write CSV locally if enabled. Listing via `/option_signals` requires DB.
- Premium parity depends on quote availability for the next session; if missing, `parity_premium` may be null and CSV may not be written.
- Parity CSVs are written under `products/edge-lab/reports/<model_id>/` when enabled.
