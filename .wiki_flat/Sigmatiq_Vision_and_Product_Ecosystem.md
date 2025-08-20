# Sigmatiq – Vision and Product Ecosystem (for Retail Investors and Traders)

## Executive Summary

Sigmatiq builds an institutional‑grade, retail‑first platform that turns market data and AI models into usable signals, safe practice, and automated execution. The Sigma product family delivers the full lifecycle: **discover → validate → simulate → subscribe → automate → review**.

**Products**

- **Sigma Lab** – authoring and evaluation: preview, build/train/backtest, sweeps/leaderboard, model cards and lineage.
- **Sigma Sim** – broker‑aware paper trading to validate signals and risk settings before capital is at risk.
- **Sigma Market** – curated feeds from AI models and vetted human traders with transparency and scoring.
- **Sigma Pilot** – policy‑driven automation and position management across supported brokers.

**Why it matters**

- Gives retail traders structured, transparent decision tools.
- Lowers error rates and latency between signal and execution.
- Enforces risk discipline through consistent guardrails and post‑trade analytics.

---

## Vision & Mission

**Vision:** Level the playing field by packaging quant methods and AI into trustworthy tools anyone can use.

**Mission:** Deliver measurable edge across the retail trading journey with transparent models, realistic testing, and controlled automation.

**Core Principles**

1. **Evidence over opinion** – all signals carry provenance, assumptions, and expected ranges.
2. **Transparency** – model cards, data sheets, and post‑trade attribution are standard.
3. **Risk first** – controls are enabled by default; users must opt into higher risk.
4. **Human control** – automation is reversible and bounded by user policies.
5. **Continuous learning** – every trade feeds evaluation loops and improves models.

---

## Market Context (implications for Sigmatiq)

- Retail activity remains a durable slice of equity volume and options demand.
- Algorithmic tooling is now mainstream; the gap is **governed execution** and **trustworthy evaluation**.
- Social/copy trading creates discovery but needs **suitability, disclosure, and guardrails**.

**Implications**

- Compete on **quality of evaluation** and **risk controls**, not just on signal count.
- Make paper‑to‑live transition safe and auditable.
- Treat provider credibility as a first‑class artifact (ratings, slippage‑aware returns, drawdown history, out‑of‑sample proof).

---

## Personas & Jobs‑to‑Be‑Done

1. **Novice Retail Trader** – “Show me strategies that fit my risk and teach me as I go.”
   - Jobs: discover vetted signals; practice risk‑free; start small with guardrails.
2. **Intermediate Self‑Directed** – “I want customization and automation with clear metrics.”
   - Jobs: tweak features/indicators; validate with realistic costs; automate with limits.
3. **Strategy Producer (Human or AI)** – “I have an edge and want distribution.”
   - Jobs: publish with disclosures; monetize; build reputation via verified performance.
4. **Compliance‑minded Investor** – “Don’t let me blow up.”
   - Jobs: enforce max loss, exposure, leverage; get audit trails and alerts.

---

## Product Pillars

### 1) Sigma Lab

**What**: Model authoring and evaluation for packs (ZeroSigma 0DTE, SwingSigma, LongSigma, OvernightSigma, MomentumSigma, Scanners) with a builder.

**Experience**

- Feature/indicator selector with recipes.
- Walk‑forward and cross‑validation defaults.
- Transaction‑cost and slippage modeling; regime segmentation.
- Model cards with assumptions, data windows, performance ranges, and failure modes.

**Outputs**

- Training matrices, model artifacts, backtests + plots, model cards/lineage, and deployable signal feeds.

---

### 2) SigmaSim

**What**: Broker‑accurate paper trading that mirrors live routing rules and pacing.

**Experience**

- Simulated fills using L1/L2, queue position heuristics, and exchange/broker routing analogs.
- Policy engine for sizing, max daily loss, per‑trade stop, take‑profit, and time‑based exits.
- Experiment tracking: link settings to results; compare against benchmarks.

**Outputs**

- Forward‑test report: PnL, hit rate, PF, Sharpe/Sortino, MDD, exposure; alerts on drift vs. backtest.

---

### 3) Sigma Market

**What**: Curated catalog of AI and human strategies with monetized model feeds.

**Trust & Monetization**

- **Integrity checks**: out‑of‑sample proof, slippage‑aware returns, latency impact, data‑leak detection.
- **Scoring**: risk‑adjusted metrics across regimes; stability and capacity grades; confidence intervals.
- **Disclosures**: model cards, data sheets, trade logs, versioning, and change history.

**Trust & Monetization**

- **Monetization model (v0)**: subscription tiers (retail/pro); later bundles and enterprise seats.
- **Integrity checks**: out‑of‑sample proof, net‑of‑fees returns, parity (sim→live) reporting, data‑leak detection.
- **Capacity controls**: seat limits and slippage monitoring to protect subscribers.
- **Scoring**: risk‑adjusted metrics across regimes; stability and capacity grades; confidence intervals.
- **Disclosures**: versioned model cards, lineage, trade logs, and change history with risk statements.

---

### 4) SigmaPilot

**What**: Execution automation bound by user policies.

**Controls**

- Per‑feed caps; per‑day loss limits; per‑symbol exposure; cooldowns after losses.
- Broker integration; dry‑run toggles; staging from SigmaSim to live via graduated limits.

**Observability**

- Real‑time dashboard of fills, slippage, latency, and exceptions.
- Post‑trade attribution: signal quality vs. execution quality.

---

## Trust, Safety, and Governance

- **Model Risk Management**: documented lifecycle, approvals, and periodic re‑validation.
- **AI Transparency**: model cards and data sheets for every public feed.
- **Backtesting Discipline**: no survivor bias; point‑in‑time data; no look‑ahead; enforce walk‑forward.
- **Forward Testing**: mandatory SigmaSim burn‑in before SigmaMarket eligibility.
- **Provider Vetting**: KYC/AML as applicable; code signing for AI strategies; change‑control audits.
- **User Protection**: defaults to conservative sizing; kill‑switch; anomaly detectors on behavior and PnL.
- **Disclosure**: standardized risk statements; net‑of‑fees reporting; benchmark comparisons.

---

## Architecture (High‑Level)

1. **Data Plane**: market data adapters, feature pipelines, point‑in‑time stores.
2. **Model Plane**: training, validation, model registry, model cards.
3. **Simulation & Execution Plane**: SigmaSim engine, policy engine, broker adapters, order router.
4. **Marketplace Plane**: catalog, entitlement, billing, ratings, compliance checks.
5. **Observability & Governance**: metrics lake, lineage, audit logs, alerting, approvals.
6. **Privacy & Security**: tenant isolation, secret management, signed artifacts, least‑privilege.

---

## KPIs & Guardrails

**Acquisition/Engagement**: activation to first simulation; conversion from SigmaSim to first live trade; subscription attach rate.

**Quality/Trust**: share of strategies with positive out‑of‑sample; slippage delta vs. sim; strategy churn; dispute rate.

**Risk**: percent of sessions hitting risk limits; drawdown distribution; incident count.

**Financial**: ARPU, gross margin per feed, creator payout ratio, LTV/CAC, churn.

**Guardrails**

- Hard stops on daily loss and leverage.
- Auto‑downgrade of feeds on drift or integrity failures.
- Mandatory disclosures in all public performance views.
- Marketplace seat limits enforced by capacity; entitlement gating for signals; audit logs for publish/update/unpublish.

---

## Go‑to‑Market (Phased)

**Phase 0 – Alpha (private)**: recruit creators; enforce publishing standards; gather slippage baselines.

**Phase 1 – Beta (waitlist)**: Sigma Lab + Sigma Sim to retail; limited Sigma Market with curated paid listings; transparent leaderboards and trust scores.

**Phase 2 – General Availability**: broaden asset classes; Sigma Pilot with tiered risk policies.

**Distribution**: content education, verified creator program, broker partnerships, TradingView/Discord communities, referral incentives.

---

## Roadmap (0–12 Months)

**0–3 mo**: core data/feature pipelines; backtest engine with walk‑forward; first model packs; SigmaSim MVP; model cards.

**3–6 mo**: Sigma Market v1 (catalog, billing, vetting, paid listings); Sigma Pilot pilot with caps; observability v1.

**6–12 mo**: capacity/risk scoring; creator SDK; multi‑asset support; governance dashboards; internationalization.

---

## Risks & Mitigations

- **Overfitting/backtest inflation** → strict validation rules; out‑of‑sample gates; independent review.
- **Execution mismatch vs. sim** → exchange‑aware fill modeling; live‑to‑sim variance monitoring; broker diversity.
- **Regulatory drift** → configurable disclosures; marketing rule compliance patterns; audit logs.
- **Provider quality variance** → tiering, probation, delisting criteria; user feedback with evidence.
- **User over‑risking** → default conservative policies; progressive unlocks; education.

---

## What Success Looks Like

- Retail users move from ad‑hoc signals to disciplined, policy‑bound strategies.
- Strategy creators monetize transparently and build reputations on verified out‑of‑sample results.
- SigmaPilot flows run with low error rates and explainable performance deltas.

---

## Appendix – Glossary (select)

- **Model Card**: standardized document describing a model’s data, evaluation, and limits.
- **Point‑in‑Time Data**: data as it existed at the decision timestamp, without future revisions.
- **Walk‑Forward**: sequential train/test splits that preserve time ordering.
- **Capacity**: estimated strategy capital limit before slippage materially degrades returns.
- **Risk Envelope**: recommended constraints for a strategy (sizing, stops, exposure, leverage).
This document has been superseded by the dated version under the same folder:

- products/sigma-lab/docs/Sigmatiq_Vision_and_Product_Ecosystem_v3_2025-08-16.md

Please refer to that file for the current vision. This stub remains to avoid broken references.
