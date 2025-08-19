#!/usr/bin/env bash
set -euo pipefail

API_BASE=${API_BASE:-http://localhost:8001}
ROOT_DIR=$(cd "$(dirname "$0")/../../../.." && pwd)

MODEL_ID="spy_opt_0dte_hourly"
LIVE_DIR="$ROOT_DIR/live_data/$MODEL_ID"
mkdir -p "$LIVE_DIR"
cp "$(dirname "$0")/signals_sample.csv" "$LIVE_DIR/signals.csv"

echo "Seeded $LIVE_DIR/signals.csv"

echo "\n== /signals/leaderboard =="
curl -sS "$API_BASE/signals/leaderboard?start=2025-08-15&end=2025-08-16" | jq . | sed -e 's/\\n/ /g'

echo "\n== /signals/summary =="
curl -sS "$API_BASE/signals/summary?model_id=$MODEL_ID&start=2025-08-15&end=2025-08-16" | jq .

echo "\n== /models/{id}/performance =="
curl -sS "$API_BASE/models/$MODEL_ID/performance?start=2025-08-15&end=2025-08-16" | jq .

echo "\nDone."

