# Sigmatix Edge – Developer Makefile

# Configurable vars (can be overridden on the command line)
PACK_ID ?= zeroedge
MODEL_ID ?=
TICKER ?= SPY
START ?=
END ?=
EXPIRY ?=$(END)
ALLOWED_HOURS ?=
THRESHOLDS ?=0.55,0.60,0.65
SPLITS ?=5
DISTANCE_MAX ?=7
BASE_URL ?= http://localhost:8001
OUT ?= reports/test_indicators
MOMENTUM_MIN ?= 0.0
MOMENTUM_COLUMN ?= momentum_score_total

.PHONY: help ui health models init init-auto build train backtest backtest-gated pipeline pipeline-gated sweep-config check-backend test-indicators validate-policy import-catalog leaderboard db-migrate db-migrate-dry db-seed docs-index docs-preview ui-fe ui-fe-install ui-fe-build ui-fe-preview wiki-clean wiki-clean-all

help:
	@echo "Targets:"
	@echo "  ui                  Run FastAPI locally (port 8001)"
	@echo "  health              Call /healthz against API (requires ui)"
	@echo "  models              List models for PACK_ID ($(PACK_ID))"
	@echo "  init                Scaffold directories for MODEL_ID"
	@echo "  init-auto           Auto-generate model_id from parts and scaffold"
	@echo "  build               Build matrix via API (needs START/END/MODEL_ID)"
	@echo "  train               Train model via API (needs MODEL_ID)"
	@echo "  backtest            Backtest via API (needs MODEL_ID)"
	@echo "  backtest-gated      Backtest with momentum gate overrides"
	@echo "  pipeline            build -> train -> backtest"
	@echo "  pipeline-gated      build -> train -> backtest-gated (uses momentum gate)"
	@echo "  sweep-config        Generate sweep YAML for MODEL_ID (grid params)"
	@echo "  check-backend       Smoke test real API (health, build, train, backtest, leaderboard)"
	@echo "  test-indicators     Run live Polygon indicator test script"
	@echo "  test-indicators-csv Generate CSV with all indicators + summary"
	@echo "  validate-policy     Validate policy YAML for MODEL_ID/PACK_ID"
	@echo "  leaderboard         Query DB leaderboard (PACK_ID optional, MODEL_ID optional)"
	@echo "  import-catalog      Parse Excel indicator catalog into docs/indicators/*.json"
	@echo "  indicators          List registered indicators (flat)"
	@echo "  indicators-groups   List registered indicators grouped by category"
	@echo "  docs-help           Show help index"
	@echo "  preview             Build a short matrix and report NaNs (v2 thresholds)"
	@echo "  alerts              Score latest rows and write live signals.csv"
	@echo "  preview-stock       Preview a stocks-only model (hourly matrix)"
	@echo "  scan                Run Breakout & Momentum scanner on a universe"
	@echo "  scan-breakout       Run breakout scanner"
	@echo "  scan-meanrevert     Run mean reversion scanner"
	@echo "  scan-trend          Run trend-follow scanner"
	@echo "  scan-squeeze        Run volatility contraction scanner"
	@echo "  scan-rs             Run relative strength scanner"
	@echo "  scan-highmomo       Run high momentum scanner"
	@echo "  calibrate-scanner   Recommend score threshold for Top-N"
	@echo "  scan-nasdaq100      Run breakout scanner on nasdaq100 preset"
	@echo "  scan-nasdaq200      Run breakout scanner on nasdaq200 preset"
	@echo "  scan-sp100          Run breakout scanner on sp100 preset"
	@echo "  scan-sp500          Run breakout scanner on sp500 preset"
	@echo "  scan-russell1000    Run breakout scanner on russell1000 preset
	@echo "  expirations         List upcoming option expirations via API""
	@echo "  db-migrate          Apply SQL migrations in ./migrations to DB (DB_* envs)"
	@echo "  db-migrate-dry      List SQL migrations without applying"
	@echo "  db-seed             Seed DB with minimal sample rows (signals, option_signals, backtest_runs)"
	@echo "  docs-index          Generate docs/INDEX.md listing docs files"
	@echo "  docs-preview        Serve docs/ directory on localhost (port 8008 by default)"
	@echo "  ui-fe-install       Install UI deps (edge-ui)"
	@echo "  ui-fe               Start UI dev server on 5173 (proxy /api → 8001)"
	@echo "  ui-fe-build         Build UI for production"
	@echo "  ui-fe-preview       Preview built UI (default port 4173)"
	@echo "  wiki-clean          Remove local wiki build dirs (.wiki_*)"
	@echo "  wiki-clean-all      Remove wiki build dirs and local wiki clone"
	@echo "Vars: PACK_ID, MODEL_ID, TICKER, START, END, EXPIRY, ALLOWED_HOURS, THRESHOLDS, SPLITS, DISTANCE_MAX, BASE_URL, DB_*"

ui:
	uvicorn edge_api.app:app --host 0.0.0.0 --port 8001 --reload

health:
	@[ -n "$(TICKER)" ] || (echo "TICKER is required"; exit 1)
	curl -sS "$(BASE_URL)/healthz?ticker=$(TICKER)" | jq .

models:
	curl -sS "$(BASE_URL)/models?pack_id=$(PACK_ID)" | jq .

init:
	@[ -n "$(MODEL_ID)" ] || (echo "MODEL_ID is required"; exit 1)
	python scripts/create_model.py --pack_id $(PACK_ID) --model_id $(MODEL_ID) --ticker $(TICKER)

init-auto:
	@[ -n "$(TICKER)" ] || (echo "TICKER is required"; exit 1)
	@[ -n "$(ASSET)" ] || (echo "ASSET=opt|eq is required"; exit 1)
	@[ -n "$(HORIZON)" ] || (echo "HORIZON=0dte|intraday|swing|long is required"; exit 1)
	@[ -n "$(CADENCE)" ] || (echo "CADENCE=5m|15m|hourly|daily is required"; exit 1)
	python scripts/create_model.py --pack_id $(PACK_ID) --ticker $(TICKER) --asset $(ASSET) --horizon $(HORIZON) --cadence $(CADENCE) --algo $(ALGO) --variant $(VARIANT)

build:
	@[ -n "$(MODEL_ID)" ] || (echo "MODEL_ID is required"; exit 1)
	@[ -n "$(START)" ] || (echo "START=YYYY-MM-DD is required"; exit 1)
	@[ -n "$(END)" ] || (echo "END=YYYY-MM-DD is required"; exit 1)
	curl -sS -X POST "$(BASE_URL)/build_matrix" \
	 -H "Content-Type: application/json" \
	 -d "{\"model_id\":\"$(MODEL_ID)\",\"pack_id\":\"$(PACK_ID)\",\"start\":\"$(START)\",\"end\":\"$(END)\",\"ticker\":\"$(TICKER)\",\"distance_max\":$(DISTANCE_MAX)}" | jq .

train:
	@[ -n "$(MODEL_ID)" ] || (echo "MODEL_ID is required"; exit 1)
	curl -sS -X POST "$(BASE_URL)/train" \
	 -H "Content-Type: application/json" \
	 -d "{\"model_id\":\"$(MODEL_ID)\",\"pack_id\":\"$(PACK_ID)\",\"allowed_hours\":\"$(ALLOWED_HOURS)\",\"calibration\":\"sigmoid\"}" | jq .

backtest:
	@[ -n "$(MODEL_ID)" ] || (echo "MODEL_ID is required"; exit 1)
	curl -sS -X POST "$(BASE_URL)/backtest" \
	 -H "Content-Type: application/json" \
	 -d "{\"model_id\":\"$(MODEL_ID)\",\"pack_id\":\"$(PACK_ID)\",\"thresholds\":\"$(THRESHOLDS)\",\"splits\":$(SPLITS),\"allowed_hours\":\"$(ALLOWED_HOURS)\"}" | jq .

backtest-gated:
	@[ -n "$(MODEL_ID)" ] || (echo "MODEL_ID is required"; exit 1)
	curl -sS -X POST "$(BASE_URL)/backtest" \
	 -H "Content-Type: application/json" \
	 -d "{\"model_id\":\"$(MODEL_ID)\",\"pack_id\":\"$(PACK_ID)\",\"thresholds\":\"$(THRESHOLDS)\",\"splits\":$(SPLITS),\"allowed_hours\":\"$(ALLOWED_HOURS)\",\"momentum_gate\":true,\"momentum_min\":$(MOMENTUM_MIN),\"momentum_column\":\"$(MOMENTUM_COLUMN)\"}" | jq .

pipeline: build train backtest

pipeline-gated: build train backtest-gated

# Generate a sweep configuration YAML for the given model
sweep-config:
	@[ -n "$(MODEL_ID)" ] || (echo "MODEL_ID is required"; exit 1)
	@mkdir -p sweeps
	@echo "writing sweeps/$(MODEL_ID)_sweep.yaml"
	@cat > sweeps/$(MODEL_ID)_sweep.yaml <<EOF
model_id: $(MODEL_ID)
pack_id: $(PACK_ID)
ticker: $(TICKER)

build:
  start: "$(START)"         # e.g., 2024-01-01
  end: "$(END)"             # e.g., 2024-06-30
  distance_max: [5, 7, 9]

train:
  calibration: [sigmoid, isotonic]
  allowed_hours: ["$(ALLOWED_HOURS)"]

backtest:
  thresholds: [[0.55,0.60,0.65], [0.60,0.65,0.70]]
  splits: [3, 5]
  allowed_hours: ["$(ALLOWED_HOURS)"]

notes: |
  Edit this file to adjust the parameter grid. Each list defines sweep values.
  A runner (not included) can iterate over the cartesian product.
EOF

# Wiki clean utilities
wiki-clean:
	rm -rf .wiki_build .wiki_flat

wiki-clean-all:
	rm -rf .wiki_build .wiki_flat .wiki_repo

# --- Backend smoke test (real API) ---
check-backend:
	@[ -n "$(TICKER)" ] || (echo "TICKER is required"; exit 1)
	@[ -n "$(MODEL_ID)" ] || (echo "MODEL_ID is required"; exit 1)
	@[ -n "$(START)" ] || (echo "START=YYYY-MM-DD is required"; exit 1)
	@[ -n "$(END)" ] || (echo "END=YYYY-MM-DD is required"; exit 1)
	@echo "[1/5] Health → $(BASE_URL)/healthz"; \
	curl -fsS "$(BASE_URL)/healthz?ticker=$(TICKER)" | jq . >/dev/null && echo "OK" || (echo "Health check failed"; exit 1)
	@echo "[2/5] Build → $(BASE_URL)/build_matrix"; \
	curl -fsS -X POST "$(BASE_URL)/build_matrix" -H "Content-Type: application/json" \
	  -d "{\"model_id\":\"$(MODEL_ID)\",\"pack_id\":\"$(PACK_ID)\",\"start\":\"$(START)\",\"end\":\"$(END)\",\"ticker\":\"$(TICKER)\",\"distance_max\":$(DISTANCE_MAX)}" \
	  | jq .ok >/dev/null && echo "OK" || (echo "Build failed"; exit 1)
	@echo "[3/5] Train → $(BASE_URL)/train"; \
	curl -fsS -X POST "$(BASE_URL)/train" -H "Content-Type: application/json" \
	  -d "{\"model_id\":\"$(MODEL_ID)\",\"pack_id\":\"$(PACK_ID)\",\"allowed_hours\":\"$(ALLOWED_HOURS)\",\"calibration\":\"sigmoid\"}" \
	  | jq .ok >/dev/null && echo "OK" || (echo "Train failed"; exit 1)
	@echo "[4/5] Backtest → $(BASE_URL)/backtest"; \
	curl -fsS -X POST "$(BASE_URL)/backtest" -H "Content-Type: application/json" \
	  -d "{\"model_id\":\"$(MODEL_ID)\",\"pack_id\":\"$(PACK_ID)\",\"thresholds\":\"$(THRESHOLDS)\",\"splits\":$(SPLITS),\"allowed_hours\":\"$(ALLOWED_HOURS)\"}" \
	  | jq .ok >/dev/null && echo "OK" || (echo "Backtest failed"; exit 1)
	@echo "[5/5] Leaderboard → $(BASE_URL)/leaderboard"; \
	curl -fsS "$(BASE_URL)/leaderboard?pack_id=$(PACK_ID)&model_id=$(MODEL_ID)&limit=$(SPLITS)" | jq .rows >/dev/null && echo "OK" || (echo "Leaderboard failed"; exit 1)
	@echo "All checks passed against $(BASE_URL)."

test-indicators:
	@[ -n "$(START)" ] || (echo "START=YYYY-MM-DD is required"; exit 1)
	@[ -n "$(END)" ] || (echo "END=YYYY-MM-DD is required"; exit 1)
	python scripts/test_indicators_polygon.py --ticker $(TICKER) --start $(START) --end $(END) --expiry $(EXPIRY) --out $(OUT) --write_csvs
	@echo "Summary written to $(OUT)/summary.json"

test-indicators-csv:
	@[ -n "$(START)" ] || (echo "START=YYYY-MM-DD is required"; exit 1)
	@[ -n "$(END)" ] || (echo "END=YYYY-MM-DD is required"; exit 1)
	python scripts/test_indicators_full_polygon.py --ticker $(TICKER) --start $(START) --end $(END) --expiry $(EXPIRY) --out_csv reports/indicators_full.csv --out_summary reports/indicators_full_summary.json
	@echo "CSV written to reports/indicators_full.csv; summary at reports/indicators_full_summary.json"

validate-policy:
	@[ -n "$(MODEL_ID)" ] || (echo "MODEL_ID is required"; exit 1)
	curl -sS "$(BASE_URL)/validate_policy?model_id=$(MODEL_ID)&pack_id=$(PACK_ID)" | jq .

leaderboard:
	curl -sS "$(BASE_URL)/leaderboard?pack_id=$(PACK_ID)&model_id=$(MODEL_ID)&limit=$(SPLITS)" | jq .

import-catalog:
	@if [ -f "AlgoTraderAI_Indicators_Polygon_First.md" ]; then \
		python scripts/import_indicator_catalog_md.py --md AlgoTraderAI_Indicators_Polygon_First.md; \
	elif [ -f "AlgoTraderAI_Indicators_Polygon_First.xlsx" ]; then \
		python scripts/import_indicator_catalog.py --xlsx AlgoTraderAI_Indicators_Polygon_First.xlsx; \
	else \
		echo "No catalog file found (expected MD or XLSX in repo root)"; exit 1; \
	fi

indicators:
	curl -sS "$(BASE_URL)/indicators" | jq .

indicators-groups:
	curl -sS "$(BASE_URL)/indicators?group=true" | jq .

docs-help:
	@echo "Open docs/help/README.md"

alerts:
	@[ -n "$(MODEL_ID)" ] || (echo "MODEL_ID is required"; exit 1)
	@python scripts/generate_live_alerts.py --model_id $(MODEL_ID) --csv matrices/$(MODEL_ID)/training_matrix_built.csv --threshold 0.60 --allowed_hours $(ALLOWED_HOURS)

db-migrate:
	@echo "Applying migrations in ./migrations"
	python scripts/apply_migrations.py --dir migrations

db-migrate-dry:
	@python scripts/apply_migrations.py --dir migrations --dry-run

db-seed:
	python scripts/seed_sample_data.py

DOCS_PORT ?= 8008
docs-index:
	python scripts/generate_docs_index.py --root docs --out docs/INDEX.md

docs-preview:
	@echo "Serving docs on http://localhost:$(DOCS_PORT) (Ctrl+C to stop)"
	python -m http.server $(DOCS_PORT) --directory docs

# --- Wiki ---
.PHONY: wiki-sync
wiki-sync:
	./scripts/wiki-sync.sh

# --- UI (Frontend) ---
FRONTEND_DIR ?= edge_ui
UI_PORT ?= 5173

ui-fe-install:
	cd $(FRONTEND_DIR) && npm install

ui-fe:
	cd $(FRONTEND_DIR) && npm run dev

ui-fe-build:
	cd $(FRONTEND_DIR) && npm run build

ui-fe-preview:
	cd $(FRONTEND_DIR) && npm run preview

# (Mock/API UI targets removed: using real backend as requested)


preview:
	@[ -n "$(MODEL_ID)" ] || (echo "MODEL_ID is required"; exit 1)
	@[ -n "$(START)" ] || (echo "START=YYYY-MM-DD is required"; exit 1)
	@[ -n "$(END)" ] || (echo "END=YYYY-MM-DD is required"; exit 1)
	@echo "Previewing $(MODEL_ID) ($(PACK_ID)) from $(START) to $(END)"
	@python scripts/preview_model.py --model_id $(MODEL_ID) --pack_id $(PACK_ID) --start $(START) --end $(END) --out reports/preview_$(MODEL_ID).json

preview-stock:
	@[ -n "$(MODEL_ID)" ] || (echo "MODEL_ID is required"; exit 1)
	@[ -n "$(START)" ] || (echo "START=YYYY-MM-DD is required"; exit 1)
	@[ -n "$(END)" ] || (echo "END=YYYY-MM-DD is required"; exit 1)
	@echo "Previewing stocks model $(MODEL_ID) ($(PACK_ID)) from $(START) to $(END)"
	@python scripts/preview_stock_model.py --model_id $(MODEL_ID) --pack_id $(PACK_ID) --start $(START) --end $(END) --out reports/preview_stock_$(MODEL_ID).json

scan:
	@[ -n "$(UNIVERSE)" -o -n "$(UNIVERSE_CSV)" ] || (echo "Provide UNIVERSE=AAPL,MSFT,SPY or UNIVERSE_CSV=path/to.csv"; exit 1)
	@[ -n "$(START)" ] || (echo "START=YYYY-MM-DD is required"; exit 1)
	@[ -n "$(END)" ] || (echo "END=YYYY-MM-DD is required"; exit 1)
	@MODEL_ID_EFFECTIVE=$${MODEL_ID:-universe_eq_swing_daily_scanner}; \
	PACK_ID_EFFECTIVE=$${PACK_ID:-swingedge}; \
	CMD="python scripts/scanner_breakout_momentum.py --pack_id $$PACK_ID_EFFECTIVE --model_id $$MODEL_ID_EFFECTIVE --start $(START) --end $(END) --top_n $${TOP_N:-50}"; \
	if [ -n "$(UNIVERSE_CSV)" ]; then CMD="$$CMD --universe_csv $(UNIVERSE_CSV)"; else CMD="$$CMD --tickers $(UNIVERSE)"; fi; \
	sh -c "$$CMD"

scan-breakout:
	@$(MAKE) scan PACK_ID=swingedge MODEL_ID=universe_eq_swing_daily_breakout_scanner UNIVERSE="$(UNIVERSE)" UNIVERSE_CSV="$(UNIVERSE_CSV)" START=$(START) END=$(END) TOP_N=$(TOP_N)

scan-meanrevert:
	@$(MAKE) scan PACK_ID=swingedge MODEL_ID=universe_eq_swing_daily_meanrevert_scanner UNIVERSE="$(UNIVERSE)" UNIVERSE_CSV="$(UNIVERSE_CSV)" START=$(START) END=$(END) TOP_N=$(TOP_N)

scan-trend:
	@$(MAKE) scan PACK_ID=swingedge MODEL_ID=universe_eq_swing_daily_trend_follow_scanner UNIVERSE="$(UNIVERSE)" UNIVERSE_CSV="$(UNIVERSE_CSV)" START=$(START) END=$(END) TOP_N=$(TOP_N)

scan-squeeze:
	@$(MAKE) scan PACK_ID=swingedge MODEL_ID=universe_eq_swing_daily_vol_contraction_scanner UNIVERSE="$(UNIVERSE)" UNIVERSE_CSV="$(UNIVERSE_CSV)" START=$(START) END=$(END) TOP_N=$(TOP_N)

scan-rs:
	@$(MAKE) scan PACK_ID=swingedge MODEL_ID=universe_eq_swing_daily_rel_strength_scanner UNIVERSE="$(UNIVERSE)" UNIVERSE_CSV="$(UNIVERSE_CSV)" START=$(START) END=$(END) TOP_N=$(TOP_N)

scan-highmomo:
	@$(MAKE) scan PACK_ID=swingedge MODEL_ID=universe_eq_swing_daily_high_momentum_scanner UNIVERSE="$(UNIVERSE)" UNIVERSE_CSV="$(UNIVERSE_CSV)" START=$(START) END=$(END) TOP_N=$(TOP_N)

scan-api:
	@[ -n "$(UNIVERSE)" -o -n "$(UNIVERSE_CSV)" ] || (echo "Provide UNIVERSE=AAPL,MSFT,SPY or UNIVERSE_CSV=path/to.csv"; exit 1)
	@[ -n "$(START)" ] || (echo "START=YYYY-MM-DD is required"; exit 1)
	@[ -n "$(END)" ] || (echo "END=YYYY-MM-DD is required"; exit 1)
	@MODEL_ID_EFFECTIVE=$${MODEL_ID:-universe_eq_swing_daily_scanner}; \
	PACK_ID_EFFECTIVE=$${PACK_ID:-swingedge}; \
	PAYLOAD='{ "pack_id": "'"$$PACK_ID_EFFECTIVE"'", "model_id": "'"$$MODEL_ID_EFFECTIVE"'", "start": "$(START)", "end": "$(END)", "top_n": '$${TOP_N:-50} }'; \
	if [ -n "$(UNIVERSE_CSV)" ]; then PAYLOAD=$$(echo $$PAYLOAD | jq --arg p "$(UNIVERSE_CSV)" '. + {universe_csv: $p}'); else PAYLOAD=$$(echo $$PAYLOAD | jq --arg t "$(UNIVERSE)" '. + {tickers: $t}'); fi; \
	curl -sS -X POST "$(BASE_URL)/scan" -H "Content-Type: application/json" -d "$$PAYLOAD" | jq .

calibrate-scanner:
	@[ -n "$(MODEL_ID)" ] || (echo "MODEL_ID is required"; exit 1)
	@GRID=$${GRID:-0.50,0.55,0.60,0.65,0.70}; TOP=$${TOP_N:-50}; \
	curl -sS -X POST "$(BASE_URL)/calibrate_thresholds" \
	 -H "Content-Type: application/json" \
	 -d "{\"model_id\":\"$(MODEL_ID)\",\"pack_id\":\"$(PACK_ID)\",\"grid\":\"$$GRID\",\"top_n\":$$TOP}" | jq .

scan-nasdaq100:
	@$(MAKE) scan-breakout UNIVERSE_CSV=data/universe/nasdaq100.csv START=$(START) END=$(END) TOP_N=$(TOP_N)

scan-nasdaq200:
	@$(MAKE) scan-breakout UNIVERSE_CSV=data/universe/nasdaq200.csv START=$(START) END=$(END) TOP_N=$(TOP_N)

scan-sp100:
	@$(MAKE) scan-breakout UNIVERSE_CSV=data/universe/sp100.csv START=$(START) END=$(END) TOP_N=$(TOP_N)

scan-sp500:
	@$(MAKE) scan-breakout UNIVERSE_CSV=data/universe/sp500.csv START=$(START) END=$(END) TOP_N=$(TOP_N)

scan-russell1000:
	@$(MAKE) scan-breakout UNIVERSE_CSV=data/universe/russell1000.csv START=$(START) END=$(END) TOP_N=$(TOP_N)


expirations:
	@[ -n "$(TICKER)" ] || (echo "TICKER is required"; exit 1)
	@python scripts/list_expirations.py --ticker $(TICKER) --weeks $${WEEKS:-12} --base_url $(BASE_URL)
