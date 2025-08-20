Sigma Mock API

Purpose
- Lightweight FastAPI server that mocks the Sigma Lab API responses for UI development.
- Shapes mirror the real endpoints, but data is static and safe.

Run
- Python 3.10+
- Install: pip install -r requirements.txt
- Start: uvicorn mock_api.app:app --reload --port 8010

Endpoints (subset)
- GET /                      → service info and advertised endpoints
- GET /health                → status ok + versions
- GET /models                → list of models (with configs)
- GET /model_detail          → config + policy shape summary
- GET /indicator_sets        → indicator catalog snapshot
- GET /leaderboard           → paginated leaderboard rows
- GET /signals               → example model signals
- GET /option_signals        → example option signals
- GET /policy/explain        → policy shape validation result
- POST /calibrate_thresholds → threshold recommendation shape
- POST /scan                 → scanner result shape with rows
- POST /build_matrix         → returns a mocked path and row count
- POST /preview_matrix       → returns matrix stats (shapes only)
- POST /train                → returns a mocked artifact path and rows
- POST /backtest             → returns summary metrics + artifacts

