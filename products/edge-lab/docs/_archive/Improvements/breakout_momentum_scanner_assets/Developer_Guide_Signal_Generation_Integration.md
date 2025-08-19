
# Developer Guide — Integrating the Breakout & Momentum Scanner into **Sigmatiq Edge**

*Generated: 2025-08-15 04:25 UTC*

This guide shows **how the Breakout & Momentum scanner fits into the current system** as a first‑class **signal‑generation** workflow. It maps the scanner’s artifacts (indicator set, script, config) to **Edge Core** services, **Edge Packs**, and the **Custom Model Builder** UI, and spells out minimal API calls, file paths, policies, and ops.

---

## 1) System Context — Where this lives

The scanner plugs into the same **Edge Core pipeline** used by all strategies:  
**`define → build dataset → train → backtest → policy → deploy → live alerts`**. The scanner uses the first, second, and last stages by default (rule‑based signals), and can use **train/backtest** if you choose the ML variant. fileciteturn0file0

Strategy assets are shipped as **Edge Packs**. The scanner’s indicator set lives under the **SwingEdge** pack alongside models/policies so it’s versioned, reproducible, and UI‑discoverable. fileciteturn0file1

The **Custom Model Builder** (wizard) already knows how to: (a) list indicators from the registry, (b) write `indicator_set.yaml` under a pack, (c) generate `model_config.yaml` + `policy.yaml`, and (d) run a **Preview** build for coverage checks before full runs. fileciteturn0file2

---

## 2) What we’re integrating

**Artifacts provided (already generated):**

- **Indicator set (pack‑level):** `packs/swingedge/indicator_sets/swing_eq_breakout_scanner.yaml`  
  Computes EMA(20/50), RSI(14), ADX(14), returns(5/20/63), LR_R2(126), ATR(14), STDDEV(20), Bollinger(20,2), OBV, CMF(20). (All are built‑ins in your registry.) fileciteturn0file5  
- **Scanner script (CLI skeleton):** `scripts/scanner_breakout_momentum.py`  
  Calls your builder/API, applies the gates, computes the **BreakoutMomentumScore**, ranks top‑N, and writes CSV.
- **Config:** `scanner_config.json` — thresholds & weights.
- **Guide:** `docs/scanner/SwingEdge_BreakoutMomentum_Scanner_Guide.md` — functional spec (signals, score, thresholds, run options).

> These are pack‑native, reproducible assets that align with your pipeline and naming rules. fileciteturn0file0 fileciteturn0file1

---

## 3) Integration patterns (choose one, or run both)

### A) **Rule‑based Signal Model** (fastest path)
Use the indicator set to build features nightly, **no ML training**. Compute score & gates → **signals**.

**Flow:**
1. **Define**: Keep the indicator set in the SwingEdge pack (or select it in the UI builder). fileciteturn0file1 fileciteturn0file2  
2. **Build dataset**: For the equity universe, call **`POST /build_matrix`** with `cadence=daily` and this indicator set. (Your adapters provide Polygon daily bars; already wired.) fileciteturn0file5  
3. **Signal transform**: From the latest row per ticker, compute **Donchian/BoS**, momentum filters, and the composite score. Keep **Top‑N** or those above a threshold. (Script provided.)  
4. **Policy & deploy**: Attach a minimal **policy** (cooldown, max trades/day; optional `size_by_conf` using `score_total`). Validate via `/validate_policy`. Push to **live alerts**. fileciteturn0file4 fileciteturn0file0

Optional: Create a logical **model_id** to track these signals in the UI (see §5).

---

### B) **Trainable SwingEdge Model** (ML path)
Use the same features + a label (e.g., `fwd_ret_10d`) and train/backtest, then emit daily predictions as signals.

**Flow:**
1. **Define**: same indicator set; **model config** includes labels (e.g., `fwd_ret_10d`) and any `features.custom` you want.  
2. **Train**: `POST /train` (walk‑forward with embargo); **Backtest** with thresholds/top% selection and policy. Results appear in **Leaderboard**. fileciteturn0file5  
3. **Deploy**: nightly `build_matrix` + predict → **signals** filtered by policy (momentum gate is supported in policy). fileciteturn0file4

---

## 4) API & file mapping

**Key endpoints (existing/planned):**  
- `POST /build_matrix` — compute features from the pack indicator set (daily). **Used by both patterns.** fileciteturn0file5  
- `POST /preview_matrix` — quick 1–2 day validation for coverage/NaN before a full run. **Used by UI Builder.** fileciteturn0file2  
- `POST /models`, `POST /indicator_sets` — create/update model & set (UI writes YAML under the pack). fileciteturn0file2  
- `POST /train`, `POST /backtest` — ML path only; persists to DB & leaderboard. fileciteturn0file5  
- `GET /validate_policy` — schema validation before any run that emits/executes signals. fileciteturn0file4  
- `GET /leaderboard` — inspect backtest results (ML path). fileciteturn0file5  
- `GET /healthz` — checks Polygon connectivity & entitlements (helpful before large builds). fileciteturn0file5

**Paths & naming:**  
- **Indicator set:** `packs/swingedge/indicator_sets/swing_eq_breakout_scanner.yaml`  
- **Optional model config (logical holder for signals):** `packs/swingedge/model_configs/universe_eq_swing_daily_scanner.yaml`  
- **Policy:** `packs/swingedge/policy_templates/universe_eq_swing_daily_scanner.yaml`  
- **Naming format:** `<ticker>_<asset>_<horizon>_<cadence>[_<algo>|_<variant>]` (e.g., `universe_eq_swing_daily_scanner`). fileciteturn0file3  
- **Matrices/Artifacts/Plots:** standard per‑model folders as in ADRs. fileciteturn0file3

---

## 5) Minimal configs

**Model (logical, for bookkeeping & policy):**
```yaml
model_id: universe_eq_swing_daily_scanner
ticker: universe
asset_type: eq
horizon: swing
cadence: daily
indicator_set: swing_eq_breakout_scanner
labels:
  kind: none           # rule-based signal model (no ML)
features: {}
```

**Policy (re‑use your schema; validated via API):**
```yaml
name: swingedge_default_v1
version: 1
policy:
  risk:
    max_drawdown: 0.10
    max_exposure: 100000
  execution:
    slippage_bps: 1.0
    size_by_conf: false          # set true to size by score_total
    conf_cap: 1.0
    momentum_gate: false
    momentum_min: 0.0
    momentum_column: score_total
  alerting:
    cooldown_minutes: 5
    max_trades_per_day: 10
```
This conforms to the **Policy Schema** and will pass `/validate_policy`. fileciteturn0file4

---

## 6) Orchestration (nightly job)

**Option A — API‑driven (recommended for prod):**
1. (Optional) `GET /healthz` — verify Polygon up + entitlements. fileciteturn0file5  
2. `POST /build_matrix` for the universe (daily).  
3. Run `scanner_breakout_momentum.py` to gate & rank; write `scans/breakout_momentum/YYYY‑MM‑DD.csv`.  
4. Post signals to the **Live Signal Runtime** with the policy attached (cooldown, max trades/day). fileciteturn0file0

**Option B — Local builder:** call your internal dataset builder directly from the script (same steps 3–4).

Schedule with cron/K8s; keep logs under the existing structured logging policy noted in **Status & Plans**. fileciteturn0file5

---

## 7) UI integration (Custom Model Builder)

- **Step 3** lists the scanner indicators (grouped); saving writes the set to `packs/swingedge/...`.  
- **Step 5** runs **Preview** (1–2 days) to ensure IV/bars are present and NaN% within thresholds.  
- **Step 6** persists the model & policy and orchestrates builds/backtests if you go the ML route. fileciteturn0file2

---

## 8) Data, caching, and universe hygiene

- **Data providers:** Polygon bars; IV not required for this scanner (equities only), but available for options overlays.  
- **Caching:** historical only; **never cache today** for live requests.  
- **Universe:** price ≥ \$5; ADV_20 ≥ 500k–1M; optional optionability filter.  
These are aligned with the adapters and plans in **Status & Plans**. fileciteturn0file5

---

## 9) Observability & Governance

- All artifacts (indicator sets, model/policy files) are versioned under the **SwingEdge** pack per ADR‑0003. fileciteturn0file1  
- Backtests (ML path) are persisted to DB with runs/folds and plots; leaderboard available via API/UI. fileciteturn0file5  
- **/validate_policy** gate prevents misconfigured runs (missing sections or invalid types). fileciteturn0file4

---

## 10) Extending to options (optional)

If you convert scan picks to **options trades**, re‑use your existing options features (IV rank, IV–RV, flow families) via the UI indicator catalog and the `features.flow.*` toggles in the model config (opt‑only). The builder and policy enforcement are already in place. fileciteturn0file2

---

## 11) Testing

- **Smoke tests:** API shape checks for `/build_matrix` (daily) on a small universe.  
- **Preview checks:** ensure NaN% < 30% and no missing required columns. fileciteturn0file2  
- **No‑mocks policy:** integration checks are run with live Polygon only when the env flag is set (see **Status & Plans**). fileciteturn0file5

---

## 12) Quick checklist

- [ ] Commit `packs/swingedge/indicator_sets/swing_eq_breakout_scanner.yaml`. fileciteturn0file1  
- [ ] (Optional) Create logical model + policy per §5; validate with `/validate_policy`. fileciteturn0file4  
- [ ] Add nightly job: `build_matrix` → run scanner script → publish signals. fileciteturn0file0  
- [ ] (Optional) ML path: add labels → train/backtest → deploy; monitor via leaderboard. fileciteturn0file5

---

## References
- **ADR‑0001: Architectural Overview** — pipeline, core services. fileciteturn0file0  
- **ADR‑0003: Edge Packs** — pack structure & conventions. fileciteturn0file1  
- **Custom Model Builder (UI Plan)** — UI steps, preview, and small API additions. fileciteturn0file2  
- **Model Naming** — auto‑generated IDs & file paths. fileciteturn0file3  
- **Policy Schema** — required fields & validation endpoint. fileciteturn0file4  
- **Status & Plans** — what’s implemented, adapters, endpoints, and tooling. fileciteturn0file5
