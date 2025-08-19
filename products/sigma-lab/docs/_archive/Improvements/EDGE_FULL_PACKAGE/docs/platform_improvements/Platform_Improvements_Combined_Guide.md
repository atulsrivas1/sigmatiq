
# Sigmatiq Sigma — Signal Generation & Scanner Platform
## Roadmap + Developer Guide (Combined)
*Generated: 2025-08-15 20:56 UTC*

This document is a single reference for improving and operating the Sigma platform for rule‑based scanners and ML models that emit trading **signals**.

---

## Part I — Platform Improvement Roadmap

### Quick Wins (1–2 sprints)
1) **First‑class “Signal Jobs”.** Treat scanners as a model subtype that uses the same lifecycle as ML models (define→build→policy→deploy→live), but skips train/backtest by default.
2) **Complete UI/API trio.** Add `POST /indicator_sets`, `POST /models`, `POST /preview_matrix` so users can go idea → preview → run without leaving the UI.
3) **Preview hardening.** Required‑column checks + NaN thresholds (fail >30%, warn 10–30%) by indicator set.
4) **Pack manifest + linter.** `pack.yaml` + lint task to enforce directory layout, naming, and policy presence.
5) **Scanner policies.** Ship 2 templates: **Top‑N equal‑weight** and **score‑weighted**; validate with the existing policy validator.
6) **Universe service.** Central rules (price/ADV filters, point‑in‑time list) so scanners and models are reproducible.
7) **Run fingerprinting.** Stamp outputs with `{{pack_sha, indicator_set_sha, model_config_sha, policy_sha}}`.
8) **Health hints.** `/healthz` exposes bars continuity, IV/chain presence (if needed), DB connectivity, entitlements.
9) **Stocks‑only quick‑start.** Preinstall one SwingSigma scanner + policy so `/models` isn’t empty.
10) **Calibration endpoint.** `/calibrate_thresholds` sweeps gates (BoS/ADX/RSI) and writes the winning params.

### Medium Horizon (4–8 weeks)
11) **Feature governance v1.** Docstrings/defaults/tests/provider tags; surface via `GET /indicators?group=true`.
12) **Parameter recipes.** Persist grid‑sweep results as JSON “recipes” under packs.
13) **Signals DB.** Daily signals with ranks/gates/lineage → powers dashboards and audits.
14) **Backtest adapter for scanners.** Convert Top‑N lists into positions with costs/gates so scanners join the leaderboard.
15) **UI diff‑before‑run.** Show what changed (indicators/params/policy) + preview summary.
16) **Pack integration tests.** `make test-pack PACK_ID=...` runs preview and a minimal backtest in CI.

### Foundational (quarter+)
17) **Formal Signal Model contract in Core.** `transform(features) → signals` so rules and ML share the same lifecycle.
18) **Data QA invariants.** Fast‑fail on monotonic time, non‑negative volume, holiday/session alignment, IV sanity.
19) **Experiment tracking across packs.** Tags on runs and `/leaderboard?tag=...`.
20) **Realtime scanners.** Same policy/alerts runtime with cooldown enforcement at 5m cadence.

### Metrics
- Time‑to‑first‑signal ≤ 10 min from the UI.
- Preview failure rate (missing/NaN) < 5% after health hints.
- 100% runs have fingerprints; Signals DB can answer “what changed since yesterday?”.

---

## Part II — Developer Guide (Fit & Implementation)

**Pipeline:** define → build dataset → train → backtest → policy → deploy → live alerts.  
**Packs:** versioned bundles (indicator sets, model configs, policies).  
**Custom Model Builder:** writes sets/models/policies; runs **Preview** for coverage/NaNs before runs.

### Integration patterns
**A) Rule‑based Signal Job (scanner)** — build features nightly, compute gates + composite score, keep Top‑N → policy → live alerts.  
**B) Trainable model (SwingSigma)** — same features + label (e.g., `fwd_ret_10d`), train/backtest, publish nightly predictions → policy thresholds → signals.

### API & files mapping
- `POST /indicator_sets` → writes `packs/<pack>/indicator_sets/*.yaml`  
- `POST /models` → writes configs/policies with auto‑naming  
- `POST /preview_matrix` → 1–2 day build; columns + NaN stats + warnings  
- Existing `/build_matrix`, `/train`, `/backtest`, `/validate_policy`  
- **Naming:** `<ticker>_<asset>_<horizon>_<cadence>[_<algo>|_<variant>]`

### Minimal policy (works for scanners & models)
```yaml
name: pack_default_v1
version: 1
policy:
  risk: { max_drawdown: 0.10, max_exposure: 100000 }
  execution:
    slippage_bps: 1.0
    size_by_conf: false
    conf_cap: 1.0
    momentum_gate: false
    momentum_min: 0.0
    momentum_column: score_total
  alerting: { cooldown_minutes: 5, max_trades_per_day: 10 }
```

### Nightly orchestration
1) `GET /healthz` → 2) `POST /build_matrix` → 3) transform/predict → 4) policy → alerts → 5) persist signals + fingerprints.

---

*End of Combined Guide*
