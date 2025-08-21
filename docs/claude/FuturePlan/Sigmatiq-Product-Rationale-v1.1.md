# Sigmatiq — Product Rationale and Architecture (v1.1)

**Source:** January 2024 discussion transcript. Consolidated as rationale to accompany the Spec and Workflow. 【9†source】

---

## 1) Core principles
- **Evidence over opinion.** Validate at each stage.  
- **Progressive complexity.** Start simple, scale sophistication.  
- **Safety by default.** Conservative defaults and gates.  
- **User empowerment.** Control at every step. 【9†source】

## 2) Pack as personality
Packs express a trading vibe across time horizon, risk appetite, decision style, market preference, and execution character. Personality drives indicator families and data cadence. This ensures coherence. 【9†source】

## 3) Model as subset
Packs are supermarkets; models are shopping lists. Users pick subsets within guardrails. This maximizes flexibility while keeping coherence and validation intact. 【9†source】

## 4) Sweep as execution alpha
Sweeps optimize *how* to trade without changing *what* to trade. They search thresholds, timing, and sizing that extract edge from a fixed model. 【9†source】

## 5) Trust pipeline
Confidence builds in stages: backtest → SigmaSim (paper) → SigmaPilot (live). This gates risk with real‑world validation before automation. 【9†source】

## 6) Product ecosystem
- **Lab:** Build packs and models.  
- **Sim:** Validate via paper trading.  
- **Market:** Share and monetize proven strategies.  
- **Pilot:** AI‑powered execution. 【9†source】

## 7) Technical architecture
- **Data:** Timeseries store for OHLCV and indicators; object storage for artifacts; OLAP for queries.  
- **Compute:** Backtests and sweeps with progress, pruning, and cancellation.  
- **ML:** XGBoost baseline with time‑series cross‑validation and calibration.  
- **Lineage:** SHAs for configs and artifacts across the pipeline. 【9†source】

## 8) Flow diagram
```
Pack (Blueprint) 
  → Model (Configuration) 
  → Sweep (Optimization)
  → Training (ML Model)
  → Publishing (Activation)
  → Alerts (Signals)
  → Execution (Trading)
```
【9†source】

## 9) Design decisions and open items
- Two‑tier sweeps (simple vs custom) and plan‑based caps.  
- Trained‑model‑centric publishing to match artifact lineage.  
- Separate alert generation vs delivery latency monitoring.  
- Future: ensembles, conflict resolution improvements, real‑time adaptation, international expansion. 【9†source】

## 10) Change log vs v1.0
- Resolved naming: `position_size_pct` used for Swing simple sweeps. `top_pct` reserved for other families.  
- Custom sweep caps clarified (1,000 standard, 3,000 pro) with pruning semantics.  
- Publish endpoint centered on trained artifacts.  
- Latency SLO separated for generation and delivery. 【8†source】【10†source】
