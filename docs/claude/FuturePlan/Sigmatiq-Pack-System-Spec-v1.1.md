# Sigmatiq Pack System — Specification (v1.1)

**Status:** Draft for review  
**Audience:** Engineering, Product, QA  
**Scope:** Packs, Models, Sweeps, Training, Publishing, Alerts, APIs, Non‑functional, Testing

## 0) Executive overview
Packs define trading personalities and tools. Models are user instances derived from packs. Sweeps optimize execution parameters. Training turns configurations into ML artifacts. Publishing moves artifacts into production with a trust pipeline: backtest → paper trade → live. Alerts are generated in real time and routed to execution or notifications. 【9†source】【10†source】

---

## 1) Pack requirements

### 1.1 Definition
A Pack is a cohesive blueprint with a trading personality and a catalog of components: indicators, features, strategies, gates, and policies. It declares supported instruments and defaults. 【10†source】

### 1.2 Personality dimensions
`time_horizon`, `risk_appetite`, `decision_style`, `market_preference`, `execution_character`. These govern indicator choices and data cadence. Coherence is mandatory. 【9†source】【10†source】

### 1.3 Types
- **Official packs:** Maintained by Sigmatiq, validated, updated.  
- **Premium user packs:** Private by default, reviewable, monetizable if approved. 【10†source】

### 1.4 Core components (required)
Namespace, supported instruments, default instrument, indicators, features, strategies, gates, policies, tags. 【10†source】

### 1.5 Validation rules
- **Coherence:** Reject mismatched timeframes, enforce risk consistency, validate instrument compatibility.  
- **Minimums:** ≥3 indicators, ≤15 indicators, ≥1 default strategy, all gates defined.  
- **Performance sanity:** Backtest ≥1 year, ≥10 trades, Sharpe ≥ −0.5 (default). 【10†source】

**Implementation note:** Provide a linter with machine‑readable error codes and remediation text. 【10†source】

---

## 2) Model requirements

### 2.1 Definition
A Model is a user‑configured subset of its parent pack. It selects instruments, indicators, strategy, and risk profile within pack bounds. 【9†source】【10†source】

### 2.2 Creation
Inputs: pack selection, model name (unique per user), instrument choice, selected indicators (subset), strategy, risk profile, instrument‑specific settings. 【10†source】

### 2.3 Constraints
Only components from parent pack. Enforce coherence. Name uniqueness per user. Minimum one indicator. Server‑side validation mirrors client. 【10†source】

### 2.4 Instrument specifics
- **Stocks:** `ticker`, `position_type`, share size or percentage.  
- **Options:** `underlying`, `option_type`, default DTE, default strike, contract size.  
- **Futures:** `contract`, `contract_month`, contract size, roll strategy. 【10†source】

---

## 3) Sweep requirements (v1.1)

### 3.1 Definition
Sweeps vary execution parameters only. They do not change instruments, indicators, features, or strategy. 【9†source】

### 3.2 Modes
- **Simple sweep:** Preset, fast, default.  
- **Custom sweep:** Expanded grid, premium. 【10†source】

### 3.3 Parameter registry
Pack‑aware registry declares sweepable fields and ranges.

- **Common:** `thresholds` (float[]), `allowed_hours` (array of hour lists or `"all_day"`).  
- **Swing packs:** `position_size_pct` (int% of capital). Replaces `top_pct` in Swing context.  
- **Reserved:** `top_pct` kept for rank‑based selection in other pack families.  
- **Optional:** risk and pack‑specific fields (e.g., `stop_loss`, `take_profit`, `max_positions`, `hold_days`). 【10†source】【8†source】

### 3.4 Simple sweep
Required: `thresholds`, `allowed_hours`, and for Swing packs `position_size_pct`. Combination cap ≤45 by default profile. Packs may define an alternative simple profile if still ≤45. 【10†source】【8†source】

### 3.5 Custom sweep
Standard tier cap ≤1,000 combos. Pro tier cap ≤3,000 with queueing and pruning. Pruning uses dominance and early‑stop on stable top‑N; retained configs are fully backtested. 【10†source】【8†source】

### 3.6 Execution and SLAs
Simple <5 minutes. Custom <30 minutes for ≤1,000 combos; pro tier may exceed due to queueing. Progress updates ≥ every 10 seconds. Cancellation supported with persisted partial results. 【10†source】

### 3.7 Quality gates
Defaults: `min_trades`=20, `min_sharpe`=0.0, `max_drawdown`=50%. Optional `min_win_rate`. Status: PASS, MARGINAL, FAIL. Only PASS/MARGINAL eligible for training. 【10†source】

### 3.8 Results
Leaderboard ranks by Sharpe; show total return, trades, max drawdown, gate status. Persist all results with tags, CSV export, and `config_hash` for lineage. 【10†source】【8†source】

### 3.9 API
`POST /sweeps`, `GET /sweeps/{id}`, `GET /sweeps/{id}/results`, `DELETE /sweeps/{id}`. Behavior unchanged; parameter names clarified. 【10†source】

### 3.10 Telemetry and errors
Emit combo‑level timings, gates, and data snapshot IDs. Error codes: SWS‑1001..4001 with machine/human messages. 【10†source】

---

## 4) Training requirements

### 4.1 Selection
Users choose one or more PASS/MARGINAL configs. Warn if >5 selections. Highlight near‑duplicates. 【10†source】

### 4.2 ML training
Default: XGBoost. Hyperparameters swept over small grids. Validation: time‑series split, 5 folds, 1‑day embargo. Outputs: model pickle, metadata, validation metrics. SLA ≤15 minutes per config, progress updates, checkpoints, optional parallelism. Add deterministic seeds and leakage checks. 【10†source】【8†source】

### 4.3 Post‑training
Present training and validation metrics, feature importance, sample predictions. Users publish or discard. Discard frees resources and logs an audit event. 【10†source】

---

## 5) Publish and lifecycle

### 5.1 Object of record
Publishing is **trained‑model centric**. Primary endpoint:  
`POST /trained-models/{trained_model_id}/publish`  
A compatibility route may resolve a base model to its latest trained artifact. 【8†source】【10†source】

### 5.2 Stages
- **Paper trading (SigmaSim):** Mandatory trust bridge with performance tracking.  
- **Go‑live (SigmaPilot):** Broker integration, caps, and automation toggles. 【9†source】【8†source】

### 5.3 Settings
Name, description, alert frequency, max alerts/day, paper‑trade first with duration, live date, broker settings. 【8†source】

---

## 6) Alert generation requirements

### 6.1 Real‑time processing
Ingest OHLCV and required market data per pack cadence. Calculate all indicators and features in real time. Handle missing data gracefully, maintain history, cache intermediates. 【10†source】

### 6.2 Latency SLOs
Define T0 = data ingress. T1 = alert persisted. **Generation latency** SLO: T1−T0 ≤100 ms p99. Track **delivery latency** to each channel separately with its own targets. Show both on dashboards. 【10†source】【8†source】

### 6.3 Alert schema
**Stock alert** fields: `alert_id`, `timestamp`, `model_id`, `action`, `instrument`, `ticker`, `quantity`, `confidence`, `entry_price`, `stop_loss`, `take_profit`, `urgency`, `valid_until`.  
**Options alert** adds option fields: `underlying`, `option_type`, `strike`, `expiration`, `contracts`.  
Extensions: metadata, backtest stats, and routing are optional blocks. Schema stability is enforced for core fields. 【10†source】【8†source】

### 6.4 Distribution
Routes: SigmaPilot, SigmaSim, Email/SMS/Push, Webhook. Conflict handling via user‑defined wrappers: first‑wins, highest‑confidence, ensemble. All routed decisions are audited. 【10†source】

---

## 7) Non‑functional requirements

- **Performance:** Pack load <1s; model creation <5s; simple sweep <5m; custom sweep <30m; training <15m/config; alert generation <100 ms. 【10†source】  
- **Scalability:** 100k concurrent users, 1M models, 10M alerts/day, 5 years history. 【10†source】  
- **Reliability:** 99.9% alert generation uptime; 99.5% training/sweeps; graceful degradation and automatic recovery. 【10†source】  
- **Security:** Encryption at rest and in transit, auth, rate limits, audit trails. 【10†source】  
- **Compliance:** SEC hooks, GDPR, SOC 2, financial audit trails. 【10†source】

---

## 8) UI requirements

- **Pack selection:** Cards, tags, search, performance previews.  
- **Model builder:** Drag‑and‑drop, real‑time validation, presets, optional YAML editor.  
- **Sweeps:** Simple/Advanced toggle, parameter ranges, runtime estimates, progress visualization, cancellation.  
- **Leaderboard:** Sortable, selection checkboxes, comparison tools, export.  
- **Alerts dashboard:** Real‑time stream, metrics, filter/search, historical view, latency badges. Ensure client/server validation parity. 【10†source】

---

## 9) API surface (selected)

- **Packs:** `GET /packs`, `GET /packs/{id}`, `POST /packs` (premium), `PUT /packs/{id}`, `DELETE /packs/{id}`.  
- **Models:** `GET /models`, `GET /models/{id}`, `POST /models`, `PUT /models/{id}`, `DELETE /models/{id}`.  
- **Publishing:** `POST /trained-models/{trained_model_id}/publish`, `POST /trained-models/{trained_model_id}/unpublish`.  
- **Sweeps:** `POST /sweeps`, `GET /sweeps/{id}`, `GET /sweeps/{id}/results`, `DELETE /sweeps/{id}`.  
- **Training:** `POST /training`, `GET /training/{job_id}`, `GET /training/{job_id}/results`, `DELETE /training/{job_id}`.  
- **Alerts:** `GET /alerts`, `GET /alerts/{alert_id}`, `POST /alerts/acknowledge`, `GET /alerts/performance`. 【10†source】

---

## 10) Testing and acceptance

- **Unit:** ≥90% coverage.  
- **Integration:** End‑to‑end flows, API validation, DB integrity.  
- **Performance:** Load 10k concurrent users, stress breaking points, alert latency tests.  
- **UAT:** 100 beta users, feedback incorporation, success metrics.  
- **Golden datasets:** Deterministic backtests to detect drift.  
- **Chaos tests:** Alert pipeline fault‑injection.  
- **Acceptance criteria:** Boxes per subsystem with latency SLOs, lineage proofs, and reproducibility checks. 【10†source】

---

## 11) Documentation
User guides, pack creation tutorial, API reference, troubleshooting. Technical docs on architecture, schema, APIs, deployment. 【10†source】

---

## 12) Migration and compatibility
Semantic versioning for packs. Backward compatibility for two major versions. Migration scripts with rollback and post‑checks. Data lineage preserved. 【10†source】

---

## 13) Acceptance checklist (v1.1 delta)
- [ ] Pack validator emits machine‑readable errors and blocks incoherent configs. 【10†source】  
- [ ] Models enforce server‑side rules identical to client. 【10†source】  
- [ ] Simple sweeps use `position_size_pct` for Swing packs; legacy `top_pct` mapped via shim. 【8†source】【10†source】  
- [ ] Custom sweeps obey plan caps and pruning; progress every 10s; cancel safe. 【10†source】  
- [ ] Training uses deterministic seeds and leakage checks; completes ≤15m/config. 【10†source】  
- [ ] Publish is trained‑model centric; compatibility route documented. 【8†source】【10†source】  
- [ ] Alerts meet generation SLO and show delivery latency separately; schema stable with optional extensions. 【10†source】【8†source】  
- [ ] Lineage recorded: `config_hash`, data snapshot IDs, artifact hash on every alert. 【9†source】【8†source】
