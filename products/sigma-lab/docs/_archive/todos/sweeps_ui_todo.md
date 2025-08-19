Backtest Sweeps — TODOs (Sigma Lab)

Scope
- Provide a first-class UI for sweeping backtests across parameter grids (thresholds, allowed_hours, top_pct) with guardrails and persistence.
- Complement with a backend endpoint and Make target; verify functionality on one model end-to-end.

Backend (complete first)
- [x] Endpoint POST /backtest_sweep with:
  - [x] thresholds_variants, allowed_hours_variants, top_pct_variants
  - [x] guardrails: min_trades, min_sharpe (filter outgoing results)
  - [x] parity metrics per combo when brackets enabled (hit_rate, avg_rr, avg_return_pct)
  - [x] persist combo runs to DB (backtest_runs + folds) with TAG
  - [x] write sweep summary JSON to products/sigma-lab/reports/ and return report_path
- [ ] Leaderboard: add tag filter to /leaderboard (optional but useful)
- [ ] Add unit/integration test for /backtest_sweep minimal path (mock data / small DF)

CLI/Make
- [x] make sweep target (param grids, tags, summary + leaderboard)
- [x] smoke pipeline guardrails and summary
- [ ] Optional: add make sweep-report to pretty-print latest report JSON

UI (Sweeps Panel)
- [x] Add Backtest Sweep route/panel with fields:
  - model_id, pack_id, date range, thresholds variants (semicolon), allowed_hours variants (semicolon), top_pct variants (semicolon), splits, embargo, tag
- [x] Buttons: Run Sweep, Run Preset
- [x] Results table: kind, thresholds/top_pct, hours, best_sharpe, best_cum
- [ ] Show link to report_path (download JSON) and timestamp badge
- [ ] Guard toggles: min_trades, min_sharpe (pass to API)
- [ ] Save/Load Preset (localStorage): store grids, dates, tag; add Presets dropdown
- [ ] Leaderboard: add filter by TAG and quick link from panel to /leaderboard?tag=TAG
- [ ] Progress UI (running N of M combos), cancel button (best-effort)
- [ ] Results table: add columns total_trades, parity hit_rate/avg_rr/avg_ret%
- [ ] Row action: "Train with this combo" (POST /train with allowed_hours and store model card)
- [ ] Row action: "Promote thresholds" (writes recommended thresholds to policy template)
- [ ] Export: download CSV of top-N combos
- [ ] Empty state and errors UX (retry advice)
- [ ] Docs link from panel to sweeps runbook

Optional Next
- [ ] Add link/button to download sweep report (report_path) from panel results
- [ ] Add guard toggles (min_trades, min_sharpe) and presets (localStorage)
- [ ] Add Leaderboard view with TAG filter and quick link from panel

Validation Plan (one-model end-to-end)
- Model: spy_opt_0dte_hourly, Pack: zerosigma
- Window: 2024-06-01 to 2024-06-30
- Grids:
  - thresholds_variants: ["0.50,0.52,0.54", "0.55,0.60,0.65"]
  - allowed_hours_variants: ["13,14,15", "13,14"]
  - top_pct_variants: [0.10, 0.15]
- Tag: sweep_jun2024
- Steps:
  1) Run via UI (Run Preset) and via make sweep (same grids)
  2) Confirm report_path and download JSON
  3) Check /leaderboard rows for TAG, verify top Sharpe/cum
  4) Spot check parity metrics when brackets enabled in policy
- 5) From the panel, filter leaderboard by TAG and confirm top rows align

Nice-to-haves
- Button to promote a selected combo to a named policy threshold set
- Export top-N rows to CSV with params/metrics
- Show delta vs previous sweep by TAG
