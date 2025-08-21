# Run a Backtest

Goal: replay rules on history and score performance.

Steps
1) Build data: `make build MODEL_ID=... START=... END=... TICKER=...`.
2) Backtest: `make backtest MODEL_ID=... THRESHOLDS=0.55,0.60,0.65 SPLITS=5`.
3) View scoreboard: `make leaderboard MODEL_ID=...`.

Tips
- Try gated backtest for momentum guard.

Related reading
- ../products/performance-leaderboards.md
- ../MODELING_REFERENCE.md
