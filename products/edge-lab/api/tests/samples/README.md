Samples for testing Signals endpoints (CSV fallback)

1) Start the API (another terminal)

   python products/edge-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload

2) Seed sample signals CSV

   The script copies a sample CSV into live_data/spy_opt_0dte_hourly/signals.csv

3) Run test script

   bash products/edge-lab/api/tests/samples/test_signals_endpoints.sh

Endpoints exercised
- GET /signals/leaderboard?start=&end=
- GET /signals/summary?model_id=&start=&end=
- GET /models/{model_id}/performance?start=&end=

