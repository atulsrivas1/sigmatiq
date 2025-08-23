# Create a Model

Goal: set up a new strategy model using a known pack.

Steps
1) Pick a pack: `make packs` then `make pack-detail PACK_ID=zerosigma`.
2) Create: `make init-auto TICKER=SPY ASSET=opt HORIZON=0dte CADENCE=hourly PACK_ID=zerosigma`.
3) Confirm files were created under packs and models folders.

Assumptions & Open Questions
- Assumption: templates exist for your pack.

Related reading
- ../products/models.md
- ../MODELING_PIPELINE_GUIDE.md
