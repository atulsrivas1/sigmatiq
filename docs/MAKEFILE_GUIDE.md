# Makefile Guide

This short guide covers the core developer workflows using the root `Makefile`.

## Prerequisites
- API server reachable at `BASE_URL` (default `http://localhost:8001`).
- Python environment for helper scripts in `scripts/`.

## Variables
- `PACK_ID` (default `zeroedge`), `MODEL_ID`, `TICKER`, `START`, `END`, `ALLOWED_HOURS`, `THRESHOLDS`, `SPLITS`, `DISTANCE_MAX`.

## Create a model
- Manual: `make init MODEL_ID=spy_opt_0dte_hourly TICKER=SPY PACK_ID=zeroedge`
- Auto: `make init-auto TICKER=SPY ASSET=opt HORIZON=0dte CADENCE=hourly PACK_ID=zeroedge`

Creates `models/<PACK_ID>/<MODEL_ID>/README.md` and `policy.yaml`.

## Build matrix
`make build MODEL_ID=spy_opt_0dte_hourly START=2024-01-01 END=2024-03-31 TICKER=SPY`

## Train
`make train MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=9:30-10:30`

## Backtest
- Standard: `make backtest MODEL_ID=spy_opt_0dte_hourly THRESHOLDS=0.55,0.60,0.65 SPLITS=5`
- Gated: `make backtest-gated MODEL_ID=spy_opt_0dte_hourly MOMENTUM_MIN=0.1`

## Pipelines
- `make pipeline MODEL_ID=... START=... END=... TICKER=...`
- `make pipeline-gated ...`

## Sweep config
`make sweep-config MODEL_ID=spy_opt_0dte_hourly START=2024-01-01 END=2024-03-31`
→ writes `sweeps/<MODEL_ID>_sweep.yaml` with grid lists for build/train/backtest.

Use `make help` for a full target list.

