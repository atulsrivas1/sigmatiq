# BTB Runbook — Operator Guide

## Scope
How to execute the Build → Sweeps → Leaderboard → Train pipeline safely with risk profiles and gates.

## Steps
1) Build Matrix
   - Choose model and date window; apply allowed‑hours (intraday packs).
   - Capture `matrix_sha`; review Matrix Profile (label balance, NaN%, leakage flags, coverage).

2) Run Sweeps
   - Select Risk Profile (C/B/A) or override budgets.
   - Define threshold/top%/hours variants; set splits and tag.
   - Start sweep; monitor progress; export CSV if needed.

3) Review Results / Leaderboard
   - Filter by model, pack, risk profile; enable "Pass Gate only".
   - Inspect Gate Badges (tooltips explain failures); open Compare modal as needed.
   - Add promising rows to Selection Cart.

4) Train
   - Open Runs > Train; review selections grouped by profile.
   - Pick algorithms, seeds, concurrency; confirm lineage preview.
   - Start training (only gate‑passing rows are enqueued unless overridden).

5) Monitor & Record
   - Track job statuses; capture final metrics; ensure artifacts stamped with shas.

## Tips
- Reuse matrices across profiles to save compute; avoid redundant sweeps (caching key provided).
- Treat failing gates as signals to tighten budgets or adjust dimensions before training.
- Pin top rows on the leaderboard and tag runs for future retrieval.

## Troubleshooting
- Gate failures: open tooltip; check budget usage bars; consider profile change or overrides.
- Leakage warnings: re‑examine feature set or hours filter; rebuild matrix.
- Capacity issues (0DTE): tighten spread limit, require higher OI/volume, or restrict hours.

