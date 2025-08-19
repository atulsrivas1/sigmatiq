
# ZeroSigma v2 Indicators — Implementation Instructions
*Generated: 2025-08-15 03:48 UTC*

This document explains how to implement six **v2 indicators** in the Sigma Core indicator registry and how to wire them into the **Custom Model Builder** and **Sigma Packs** so they flow through `build → train → backtest` exactly as your architecture expects.

- Platform pipeline: **Sigma Core** `define → build dataset → train → backtest → policy → deploy → live alerts`. (ADR‑0001)  
- Strategy packaging: **Sigma Packs** carry indicator sets, model configs, and policies. (ADR‑0003)  
- UI contract: the **Custom Model Builder** wizard writes `indicator_set.yaml` and `model_config.yaml`, then runs a short **Preview** build to validate data coverage.  

---

## 0) Scope

Add the following indicators to the **indicator & feature registry**:
1. `open_gap_z` — gap at the open, normalized (ATR or intraday σ).
2. `first15m_range_z` — first N‑minutes range, normalized.
3. `atm_iv_open_delta` — ATM IV at open minus prior close.
4. `gamma_density_peak_strike` — strike with max ∑(|Γ|×OI).
5. `dist_to_gamma_peak` — spot − peak strike (signed).
6. `gamma_skew_left_right` — density right vs left of spot.

Once registered, update indicator sets (e.g., **Head‑Fake Reversal v2**, **Pin Drift v2**) so the UI can select and persist them per model.

---

## 1) Data dependencies (Polygon‑first)

- **Equity bars:** daily (for ATR), 5‑minute (for open and intraday stats).  
- **Options:** chain **snapshots** (IV, Δ/Γ/Θ/Vega) + **OI snapshot**.  
- **Rules:** *never cache today*; cache historical only. Use prior‑day OI if intraday OI isn't refreshed; same‑day expiry for 0DTE.  

---

## 2) Indicator specifications

### 2.1 `open_gap_z`
**Purpose:** size the opening gap vs typical volatility.

**Params (defaults):**
```yaml
atr_period: 14
open_time: "09:30"
norm: "atr"        # "atr" | "stddev5m"
tz: "America/New_York"
```

**Computation:**
- `gap = Open_today_09:30 − PrevClose`
- Denominator: `ATR_daily(atr_period)` if `norm="atr"`, else `std(5m returns, window=20)` measured up to the open.
- `open_gap_z = gap / max(denom, 1e-9)`

**Output column:** `open_gap_z`

---

### 2.2 `first15m_range_z`
**Purpose:** measure initial range expansion.

**Params (defaults):**
```yaml
window_mins: 15    # allow 15 or 30
norm: "atr"        # "atr" | "stddev5m"
tz: "America/New_York"
```

**Computation:**
- `range = High(09:30→09:45) − Low(09:30→09:45)` (shift end based on `window_mins`).
- Normalize by ATR_daily(14) **or** 5m returns std (window=20).  
- `first15m_range_z_{window_mins} = range / denom`

**Output column:** `first15m_range_z_15` (or `_30`).

---

### 2.3 `atm_iv_open_delta`
**Purpose:** confirm whether IV **softens or rises** from prior close to today’s open (useful for head‑fake context).

**Params (defaults):**
```yaml
open_sampling: "09:30-09:35"        # median within window
close_sampling_prev: "15:55-16:00"  # prior day EOD
atm_method: "nearest"               # "nearest" | "delta"
delta_target: 0.50                  # only if atm_method="delta"
expiry: "same_day"
tz: "America/New_York"
```

**Steps:**
1) **Prev close ATM IV**: sample previous session `close_sampling_prev`, pick ATM (nearest strike or by 0.50Δ), compute median IV.  
2) **Open ATM IV**: sample open window `open_sampling`, same ATM rule.  
3) `atm_iv_open_delta = IV_open − IV_prev_close`

**Output column:** `atm_iv_open_delta`

**Sigma cases:** if same‑day expiry absent, allow `expiry="front"` (nearest tenor) or return NaN.

---

### 2.4–2.6 Gamma density features
**Purpose:** quantify “pinning” pressure from **|Γ|×OI** density along strikes.

**Params (defaults):**
```yaml
expiry: "same_day"
delta_min: 0.05
delta_max: 0.75
tz: "America/New_York"
```

**Steps (at an evaluation time):**
1) Pull chain snapshot for `expiry="same_day"`.  
2) Join OI (prior‑day OI is acceptable intraday).  
3) Filter to options with `abs(delta) ∈ [delta_min, delta_max]`.  
4) Per strike: `density(K) = Σ_i |Gamma_i| × OI_i` (calls + puts).  
5) **Peak strike**: `K* = argmax_K density(K)` → `gamma_density_peak_strike = K*`.  
6) **Distance**: `dist_to_gamma_peak = spot − K*` (signed).  
7) **Skew**:  
   `left = Σ_{K<spot} density(K)`, `right = Σ_{K>spot} density(K)`  
   `gamma_skew_left_right = (right − left) / (right + left + 1e-9)`

**Output columns:** `gamma_density_peak_strike`, `dist_to_gamma_peak`, `gamma_skew_left_right`

---

## 3) Registry integration (Sigma Core)

Create (or extend) the following modules under `sigma_core/indicators/`:

- `intraday_open.py` → `open_gap_z`, `first15m_range_z`
- `options_iv.py` → `atm_iv_open_delta`
- `options_gamma.py` → `gamma_density_peak_strike`, `dist_to_gamma_peak`, `gamma_skew_left_right`

Each function:
- Declares **params** with defaults.
- Reads data via existing adapters (bars, options snapshots/OI).
- Returns either a scalar (per timestamp) or a dict mapping column names to values.
- Registers with the indicator registry so it appears in `GET /indicators` for the UI.

---

## 4) Column names (canonical)

- `open_gap_z`  
- `first15m_range_z_15` (or `_30`)  
- `atm_iv_open_delta`  
- `gamma_density_peak_strike`  
- `dist_to_gamma_peak`  
- `gamma_skew_left_right`

Keep names stable so `select_features(df)` is deterministic.

---

## 5) UI & Preview behavior

- **Model Builder Step 3:** indicators appear with descriptions and default params; the wizard writes them into `indicator_set.yaml`.  
- **Preview (`POST /preview_matrix`)**:  
  - Error if `atm_iv_open_delta` lacks both open and prior‑close snapshots.  
  - Error if gamma density has **no same‑day chain**; warn if density empty after delta filter.  
  - Global NaN guards: **fail >30%**, **warn 10–30%**.

---

## 6) Pack updates (examples)

### Head‑Fake Reversal (v2)
`products/sigma-lab/packs/zeroedge/indicator_sets/zeroedge_headfake_reversal_v2.yaml`
```yaml
name: zeroedge_headfake_reversal_v2
version: 1
indicators:
  - {{name: open_gap_z, atr_period: 14}}
  - {{name: first15m_range_z, window_mins: 15, norm: "atr"}}
  - {{name: atm_iv_open_delta, expiry: "same_day"}}
  # keep v1 features
  - {{name: rsi, period: 7}}
  - {{name: ema, window: 8}}
  - {{name: ema, window: 21}}
  - {{name: macd, fast: 8, slow: 21, signal: 5}}
  - {{name: atr, period: 14}}
  - {{name: stddev, window: 20}}
  - {{name: bollinger, window: 20, num_std: 2.0}}
  - {{name: iv_realized_spread, window: 20}}
  - {{name: pcr_volume}}
  - {{name: pcr_oi}}
  - {{name: oi_change_1d}}
  - {{name: vix_level}}
  - {{name: hour_of_day}}
  - {{name: day_of_week}}
```

### Pin Drift (v2)
(You already have `zeroedge_pin_drift_v2.yaml`; once features exist, switch models to use it.)

---

## 7) Tests (lean but effective)

- **Unit**  
  - Synthetic gaps/ranges produce expected z‑scores.  
  - Mock IV snapshots so `atm_iv_open_delta` sign matches the input.  
  - Gamma density detects a constructed `K*`; skew flips when you mirror densities.

- **Integration (Preview)**  
  - 2–3 recent sessions with valid chains and OI; check NaN% and warnings.  
  - One half‑day to confirm open/close handling.

---

## 8) Operational notes

- **Half‑days:** adjust open/close; for `atm_iv_open_delta`, prior‑close remains the regular close of the previous full or half session.  
- **Same‑day expiry missing:** allow a param to fall back to front‑month or return NaN; Preview will surface this clearly.  
- **Caching:** historical only; today is always live for snapshots.

---

## 9) Quick API snippets

- **Upsert indicator set:**
```json
{{
  "pack_id": "zeroedge",
  "scope": "pack",
  "name": "zeroedge_headfake_reversal_v2",
  "indicators": [
    {{ "name": "open_gap_z", "atr_period": 14 }},
    {{ "name": "first15m_range_z", "window_mins": 15, "norm": "atr" }},
    {{ "name": "atm_iv_open_delta", "expiry": "same_day" }}
  ]
}}
```

- **Preview (1–2 days):**
```json
{{
  "pack_id": "zeroedge",
  "model_id": "spy_opt_0dte_5m_rev1030",
  "start": "2025-08-04",
  "end": "2025-08-06"
}}
```

---

## References
- Sigma Core pipeline & capabilities (ADR‑0001).  
- Sigma Packs structure and conventions (ADR‑0003).  
- Custom Model Builder steps & small API additions (UI Plan).  
- Model naming contract (docs).  
- Policy schema & validation rules (docs).  
- Status & Plans — what’s implemented and adapters available.
