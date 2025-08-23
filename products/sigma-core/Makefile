# Sigma Core — Makefile

.PHONY: help test build lint gen-indicator-seed gen-set-seed gen-strategy-seed gen-workflow-seed lint-catalog lint-strategies lint-workflows db-migrate db-migrate-dry lint-all

help:
	@echo "Sigma Core (shared library)"
	@echo "Targets:"
	@echo "  test                - run pytest (placeholder)"
	@echo "  build               - build wheel (placeholder)"
	@echo "  lint                - lint/type-check (placeholder)"
	@echo "  gen-indicator-seed  - generate SQL seed for sc.indicators from builtins"
	@echo "  gen-set-seed        - generate SQL seed for sc.indicator_sets from examples"
	@echo "  gen-strategy-seed   - generate SQL seed for sc.strategies from examples"
	@echo "  gen-workflow-seed   - generate SQL seed for sc.workflows from examples"
	@echo "  gen-recipes-seed    - generate SQL seed for sc.simple_recipes from examples"
	@echo "  lint-catalog        - check novice fields completeness in overrides JSON"
	@echo "  gen-recipes-seed    - generate SQL seed for sc.simple_recipes from examples"
	@echo "  lint-models         - validate model registry rows (novice, taxonomy, branding, scope)"
	@echo "  lint-model-packs    - validate model pack registry and consensus"
	@echo "  lint-training-cfg   - validate model training_cfg selection for novice safety"
	@echo "  lint-all            - run all linters (catalog, strategies, workflows, recipes, presets, models, packs)"
	@echo "  db-migrate          - apply SQL migrations in this package (uses products/sigma-core/.env)"
	@echo "  db-migrate-dry      - list SQL migrations without applying"
	@echo "  api-run             - run catalog API locally (FastAPI)"
	@echo "  preset-load         - load preset symbols from CSV (PRESET=, FILE=)"
	@echo "  preset-create       - create/update a preset (ID=, TITLE=, DESC=, SOURCE=, VERSION=)"
	@echo "  run-indicator       - run single indicator on CSV (NAME=, PARAMS=, IN=, OUT=)"
	@echo "  run-set-features    - build features from set on CSV (SET_JSON= or SET_ID=/VERSION=, IN=, OUT=)"
	@echo "  run-screen          - screen symbols in CSV by indicator rule (NAME=, PARAMS=, RULE=, IN=, SYM=, OUT=)"
	@echo "  run-backtest        - run CV backtest on a CSV (IN=, [SET_JSON=], [LABEL=], [LABEL_PARAMS=], [THRESHOLDS=], [TOP_PCT=])"
	@echo "  quick-sweep         - migrate DB then run a sample sweep (MODEL=, PRESET=, CAP=, BASE=http://localhost:8050)"
	@echo "  watchlist-create    - create watchlist (USER=, NAME=, SYMBOLS=, DEFAULT=0/1)"
	@echo "  watchlist-list      - list watchlists for a user (USER=)"

test:
	@echo "[placeholder] run: pytest -q"

build:
	@echo "[placeholder] run: python -m build"

lint:
	@echo "[placeholder] run: ruff check . && black --check . && mypy ."

gen-indicator-seed:
	python3 scripts/gen_sc_indicator_seed.py > migrations/0002_sc_seed_indicators.sql

gen-set-seed:
	python3 scripts/gen_sc_indicator_sets_seed.py > migrations/0003_sc_seed_indicator_sets.sql

gen-strategy-seed:
	python3 scripts/gen_sc_strategies_seed.py > migrations/0004_sc_seed_strategies.sql

gen-workflow-seed:
	python3 scripts/gen_sc_workflows_seed.py > migrations/0005_sc_seed_workflows.sql

gen-recipes-seed:
	python3 scripts/gen_sc_simple_recipes_seed.py > migrations/0008_sc_seed_simple_recipes.sql


lint-catalog:
	python3 scripts/lint_catalog_novice.py

lint-strategies:
	python3 scripts/lint_strategies_novice.py


lint-workflows:
	python3 scripts/lint_workflows_novice.py


lint-recipes:
	python3 scripts/lint_recipes.py


lint-presets:
	python3 scripts/lint_presets.py

lint-models:
	python3 scripts/lint_models.py

lint-model-packs:
	python3 scripts/lint_model_packs.py

lint-training-cfg:
	python3 scripts/lint_training_cfg.py

lint-all:
	$(MAKE) lint-catalog
	$(MAKE) lint-strategies
	$(MAKE) lint-workflows
	$(MAKE) lint-recipes
	$(MAKE) lint-presets
	$(MAKE) lint-models
	$(MAKE) lint-model-packs
	$(MAKE) lint-training-cfg

# --- DB Migrations (Sigma Core) ---
MIGRATIONS_DIR ?= migrations

db-migrate:
	@echo "Applying migrations in $(MIGRATIONS_DIR) using products/sigma-core/.env"
	python scripts/apply_migrations.py --dir $(MIGRATIONS_DIR)

db-migrate-dry:
	python scripts/apply_migrations.py --dir $(MIGRATIONS_DIR) --dry-run

api-run:
	uvicorn api.app:app --host 0.0.0.0 --port 8050 --reload

preset-load:
	@if [ -z "$(PRESET)" ] || [ -z "$(FILE)" ]; then \
		echo "Usage: make preset-load PRESET=sp500 FILE=./sp500.csv"; \
		exit 1; \
	fi
	python3 scripts/load_preset_symbols.py --preset $(PRESET) --file $(FILE) --truncate

preset-create:
	@if [ -z "$(ID)" ] || [ -z "$(TITLE)" ]; then \
		echo "Usage: make preset-create ID=sp100 TITLE='S&P 100' DESC='Large-cap subset' SOURCE='S&P' VERSION=2024-08"; \
		exit 1; \
	fi
	python3 scripts/presets_cli.py create --id $(ID) --title "$(TITLE)" --desc "$(DESC)" --source "$(SOURCE)" --version "$(VERSION)"

# --- Runner shortcuts ---
run-indicator:
	@if [ -z "$(NAME)" ] || [ -z "$(IN)" ] || [ -z "$(OUT)" ]; then \
		echo "Usage: make run-indicator NAME=rsi PARAMS='{}' IN=./data.csv OUT=./out.csv"; \
		exit 1; \
	fi
	python3 scripts/runner.py indicator-compute --name $(NAME) --params '$(PARAMS)' --input $(IN) --output $(OUT)

run-set-features:
	@if [ -z "$(IN)" ] || [ -z "$(OUT)" ]; then \
		echo "Usage: make run-set-features SET_JSON=./set.json IN=./data.csv OUT=./features.csv"; \
		echo "   or: make run-set-features SET_ID=macd_trend_pullback_v1 VERSION=1 IN=./data.csv OUT=./features.csv"; \
		exit 1; \
	fi
	@if [ -n "$(SET_JSON)" ]; then \
		python3 scripts/runner.py set-build-features --set-json $(SET_JSON) --input $(IN) --output $(OUT); \
	else \
		python3 scripts/runner.py set-build-features --set-id $(SET_ID) --version $(VERSION) --input $(IN) --output $(OUT); \
	fi

run-screen:
	@if [ -z "$(NAME)" ] || [ -z "$(RULE)" ] || [ -z "$(IN)" ]; then \
		echo "Usage: make run-screen NAME=rsi PARAMS='{}' RULE='rsi_14 > 70' IN=./multi.csv SYM=symbol OUT=./matches.txt"; \
		exit 1; \
	fi
	python3 scripts/runner.py screen --name $(NAME) --params '$(PARAMS)' --rule '$(RULE)' --input $(IN) --symbol-col $(SYM) --output $(OUT)

run-backtest:
	@if [ -z "$(IN)" ]; then \
		echo "Usage: make run-backtest IN=./data.csv SET_JSON=./set.json LABEL=hourly_direction LABEL_PARAMS='{}' THRESHOLDS='[0.55,0.6,0.65]' TOP_PCT=0.1 OUT=./bt.json"; \
		exit 1; \
	fi
	python3 scripts/runner.py backtest --input $(IN) $(if $(SET_JSON),--set-json $(SET_JSON),) --label $(if $(LABEL),$(LABEL),hourly_direction) --label-params '$(if $(LABEL_PARAMS),$(LABEL_PARAMS),{})' --thresholds '$(if $(THRESHOLDS),$(THRESHOLDS),[0.55,0.6,0.65])' $(if $(TOP_PCT),--top-pct $(TOP_PCT),) $(if $(ALLOWED_HOURS),--allowed-hours $(ALLOWED_HOURS),) $(if $(OUT),--output $(OUT),)

quick-sweep:
	@if [ -z "$(MODEL)" ]; then \
		echo "Usage: make quick-sweep MODEL=sq_macd_trend_pullback_5m PRESET=liquid_etfs CAP=20 BASE=http://localhost:8050"; \
		exit 1; \
	fi
	$(MAKE) db-migrate
	@echo "Running sweep for $(MODEL) on $(PRESET) (cap=$(CAP)) via $(if $(BASE),$(BASE),http://localhost:8050)"
	curl -sS -X POST "$(if $(BASE),$(BASE),http://localhost:8050)/models/$(MODEL)/backtest/sweep" -H "Content-Type: application/json" -d '{
	  "universe": {"preset_id": "$(if $(PRESET),$(PRESET),liquid_etfs)", "cap": $(if $(CAP),$(CAP),20)},
	  "grid": {"thresholds_list": [[0.55,0.6,0.65,0.7]], "allowed_hours_list": [[9,10,11,12,13,14,15]], "max_combos": 20, "min_trades": 50},
	  "persist": true,
	  "tag": "quick-sweep"
	}' | sed -e 's/{/\n{/g' -e 's/,/\n  ,/g'

watchlist-create:
	@if [ -z "$(USER)" ] || [ -z "$(NAME)" ]; then \
		echo "Usage: make watchlist-create USER=u123 NAME=mylist SYMBOLS='AAPL,MSFT,SPY' DEFAULT=1"; \
		exit 1; \
	fi
	python3 scripts/watchlists_cli.py create --user $(USER) --name $(NAME) --visibility private $(if $(DEFAULT),--default,) $(if $(SYMBOLS),--symbols $(SYMBOLS),)

watchlist-list:
	@if [ -z "$(USER)" ]; then \
		echo "Usage: make watchlist-list USER=u123"; \
		exit 1; \
	fi
	python3 scripts/watchlists_cli.py list --user $(USER)
