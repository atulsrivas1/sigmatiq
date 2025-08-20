# Convenience Makefile for Sigma Lab repo

.PHONY: ui ui-fe ui-fe-install ui-fe-build ui-fe-preview db-migrate db-migrate-dry docs-index docs-preview build train backtest init init-auto alerts brand-sweep

# Forward to the root Makefile, preserving variables
FWD=$(MAKE) -C ../.. 

ui:
	$(FWD) ui

ui-fe:
	$(FWD) ui-fe

ui-fe-install:
	$(FWD) ui-fe-install

ui-fe-build:
	$(FWD) ui-fe-build

ui-fe-preview:
	$(FWD) ui-fe-preview

db-migrate:
	$(FWD) db-migrate

db-migrate-dry:
	$(FWD) db-migrate-dry

docs-index:
	$(FWD) docs-index

docs-preview:
	$(FWD) docs-preview

build train backtest init init-auto alerts:
	$(FWD) $@ PACK_ID=$(PACK_ID) MODEL_ID=$(MODEL_ID) START=$(START) END=$(END) TICKER=$(TICKER)

# Run branding sweep to ensure legacy names are not present in UI sources
brand-sweep:
	@echo "Running brand sweep (Sigmatiq / ZeroSigma) in sigma-lab UI…"
	@node ui/scripts/brand_sweep.cjs
	@echo "Brand sweep OK"
