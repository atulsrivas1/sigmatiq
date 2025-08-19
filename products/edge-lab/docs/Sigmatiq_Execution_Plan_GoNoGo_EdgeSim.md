# Sigmatiq – Execution Plan, Go/No-Go, and Edge Sim PRD v1

## 0) Blunt Assessment
- Vision is strong. Winning requires simulator fidelity, trust tooling, and governance. Without these, it becomes another signals app.
- Moat = **verifiable evaluation** + **slippage/capacity scoring** + **policy‑first automation**.
- Ship narrow. Prove sim→live parity before any broad launch.

---

**What’s right**
- Full lifecycle is coherent: build → test → subscribe → automate.
- Edge‑first naming is consistent.
- Risk controls and disclosures are prioritized.


## 1) Go/No‑Go Checklist (Gate for Public Launch)
**Simulation parity**
- Sim→Live P&L error within **±10% at 95% CI** over ≥60 market days for at least 3 strategies.
- Fill model validated on: market orders, limit orders near touch, partial fills, and halts.

**Safety**
- Zero breaches of user risk limits in beta (max daily loss, per‑trade stops, exposure caps).
- Kill‑switch tested and recoverable within 30 seconds.

**Marketplace quality**
- ≥10 verified strategies with out‑of‑sample proof and capacity limits.
- Drift detection and auto‑downgrade live in production.

**Observability**
- Per‑trade attribution (signal vs execution), latency histograms, slippage distributions.

**Compliance**
- Model cards and disclosures on every listing. Audit logs immutable. Marketing content compliant.

Go only when all green. Otherwise continue private beta.

---

## 2) Differentiation & Moat
- **Verifiable evaluation**: signed artifacts, reproducible backtests, walk‑forward only.
- **Capacity & slippage scoring**: publish CI bands and capacity thresholds per strategy.
- **Policy‑first automation**: EdgePilot with conservative presets and progressive unlocks.
- **Creator reputation**: versioning, change logs, and transparent strike rates by regime.

---

## 3) Biggest Risks & Mitigations
- **Simulator mismatch** → Queue/route heuristics, L2 where affordable, live variance alerts, continuous calibration.
- **Cold start** → Curate initial creators, minimum standards, rev‑share incentives, waitlist for users.
- **Regulatory drift** → Standardized disclosures, audit trails, and gated publishing workflow.
- **Data cost/latency** → Start equities L1; use delayed L2 sampling for calibration; cache aggressively.
- **Model drift** → Automatic re‑eval, stability score, delist on persistent underperformance.

---

## 4) Success Metrics (falsifiable)
- Sim→Live P&L delta: **≤10%** median over 60 days.
- Conversion: **≥30%** of EdgeSim users subscribe to at least one EdgeMarket feed.
- Safety: **0** uncontrolled limit breaches in rolling 90 days.
- Creator quality: **≥70%** of listed strategies maintain positive out‑of‑sample after 90 days.

---

## 5) Go‑to‑Market Wedge
- Ship **US equities live** first. Keep **SPY options** in sim until fill gap <10% P&L.
- Private beta for EdgeMarket. No open listings until trust tooling is proven.
- Lead with trust: model cards, slippage‑aware stats, capacity caps.

---


## 5a) Onboarding UX Guardrails
- **Risk‑tier presets**: Conservative, Moderate, Aggressive with default caps for sizing, daily loss, leverage, and concentration.
- **Progressive unlocks**: raise limits only after N trades and zero breaches over rolling windows.
- **First‑run checklist** before enabling EdgePilot: broker link, kill‑switch test, policy review.
- **Clear labels**: backtest vs. forward vs. live on every chart and metric.
- **Sanity alerts**: unusual turnover, concentration spikes, or drawdown acceleration trigger reviews.


## 6) Build Order & Milestones
**M0–M2**
- Point‑in‑time data store; evaluation service; model registry; model cards v1.
- EdgeSim v1: L1 fills + queue heuristic; cost model; experiment tracking.

**M2–M4**
- Edge Lab packs (via edge_core): 2 equity baselines + 1 SPY options pack.
- Edge Pilot v1: one broker, equities only; policy presets; kill‑switch; audit logs.

**M4–M6**
- Creator SDK + verification pipeline. EdgeMarket (private) with curated listings.
- Observability: per‑trade attribution; slippage/latency dashboards.

**M6–M9**
- Capacity scoring; drift detection; delisting policy. Add second broker.

---


## 6a) Broker & Execution Policy Roadmap
- **Routing & venues**: document default routing, venue preferences, odd‑lot handling, and auction participation; expose per‑strategy policy.
- **Order types & TIF**: v1 Market/Limit with DAY/IOC; roadmap for GTC, stop‑limit, bracket/OCO.
- **Throughput & throttles**: per‑account QPS caps, retry/backoff on rejects, duplicate‑order suppression.
- **Reject handling**: standardized codes, auto‑downgrade to sim on persistent rejects.
- **Latency SLOs**: decision→route→fill histograms with p50/p95 budgets; alert on drift.
- **Broker rollout**: start with a single equities broker; add second broker after SLOs met and parity verified.


## 7) EdgeSim – PRD v1
**Objective**
- Provide broker‑accurate paper trading to de‑risk strategies and calibrate sim→live parity.

**In‑Scope**
- Equities L1 data; limit/market orders; partial fills; fees; borrow estimates where relevant.
- Policy engine: position sizing, per‑trade stop, take‑profit, daily loss cap, time‑based exits.
- Experiment tracking with versioned configs and seeded randomness.

**Out‑of‑Scope (v1)**
- Options live fills; complex order types (OCO, MOC), multi‑leg; portfolio margin.

**Personas**
- Retail trader validating a model. Creator preparing a listing.

**Core Features**
- **Fill model**: touch‑aware limit logic, queue position heuristic, irregular trading halts handling.
- **Latency model**: configurable decision→route→exchange latency; jitter distribution.
- **Cost model**: commissions, fees, SEC/TAF, estimated slippage; net‑of‑fees P&L.
- **Policies**: JSON policy schema with server‑side enforcement.
- **Benchmarks**: SPY/QQQ buy‑and‑hold, equal‑risk baseline.
- **Reports**: P&L, hit rate, PF, Sharpe/Sortino, MDD, exposure, turnover; sim→live variance when paired with EdgePilot results.

**APIs (sketch)**
- `POST /sim/runs` {strategy_ref, policy_ref, seed, data_window}
- `GET /sim/runs/{id}` status + metrics
- `POST /policies` {caps, stops, tps, cooldowns}
- `GET /reports/{run_id}` metrics, trades, attribution

**Data**
- Point‑in‑time bars and quotes. Corporate actions applied at decision time.

**NFRs**
- Deterministic replay given seed and inputs. 99p run time < 2 min for 1y equities per strategy.
- Audit trail for all inputs/outputs. PII minimal and encrypted.

**Telemetry**
- Metrics: sim runtime, fill error vs. live, policy breach attempts blocked.

**Acceptance Criteria**
- Backtest → EdgeSim parity within defined tolerances on reference strategies.
- Reproducibility: identical results on re‑run with same seed and data snapshot.

**Rollout**
- Internal alpha with 3 reference strategies. External beta with 50 users.

---

## 8) Creator SDK & Verification Pipeline
- **Packaging**: strategy as container or wheel with entrypoints; pinned deps.
- **Signing**: content‑addressed artifact; signature verified on publish.
- **Repro Eval**: runner replays train/val/test; walk‑forward enforced; data leakage checks.
- **Outputs**: model card JSON; capacity estimate; confidence intervals; change log.
- **Gating**: must pass integrity checks and EdgeSim burn‑in before listing on EdgeMarket.

---

## 9) EdgeMarket – Trust & Scoring
- **Integrity**: o/s proof, versioned history, slippage‑aware returns, latency impact.
- **Scoring**: risk‑adjusted returns by regime; stability; capacity; drawdown profile; CI bands.
- **Ranking**: surface strategies within user‑declared risk envelope.
- **Controls**: user caps per feed; delist on drift or integrity failure.

---


## 9a) Abuse & Manipulation Detection
- **Pumpy feed detection**: spikes in volume/volatility and correlated social signals flag listings for review.
- **Regime‑flip monitoring**: sudden parameter or behavior shifts trigger quarantine and re‑validation.
- **Survivorship/signal spamming**: detect excessive strategy forking, duplicate signals, and selective publishing.
- **Performance inflation checks**: slippage anomalies, look‑ahead leakage tests, and outlier clustering.
- **Responses**: ranking penalty, temporary suspension, forced re‑eval, or delisting with audit log entries.


## 10) Compliance & Governance
- Model cards and disclosures mandatory. Net‑of‑fees only. Clear backtest vs. forward labels.
- Immutable audit logs; admin approvals for listing; KYC/AML for creators where applicable.
- Marketing content pattern‑checked for performance claims.

---

## 11) Unit Economics Skeleton
- **Costs**: market data, infra, storage, support, rev‑share.
- **Revenue**: subscriptions per feed, bundles, enterprise seats.
- **Targets**: gross margin ≥70% per mature feed; LTV/CAC ≥3.

---

## 12) Action Items (Next 2 Weeks)
- Lock success metrics and CI thresholds.
- Define reference strategies and data sources for calibration.
- Draft policy JSON schema. Implement EdgeSim API stubs.
- Prepare creator SDK MVP spec and publishing flow.
This document has been superseded by the dated version under the same folder:

- products/edge-lab/docs/Sigmatiq_Execution_Plan_GoNoGo_EdgeSim_PRD_v1_UPDATED_2025-08-16.md

Please refer to that file for the current plan. This stub remains to avoid broken references.
