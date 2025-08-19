
# Paper Trader & Alerts — Low‑Level Design (LLD)
*Generated: 2025-08-15 20:56 UTC*

## 1) APIs

### 1.1 Paper Accounts
- `POST /paper/accounts` → create paper account  
  Body: `{ name, cash, margin_mode, commission_bps, slippage_bps, vp_limit, default_fill_model }`  
  Resp: `{ account_id, ok }`
- `GET /paper/accounts/:id` → balances, positions snapshot

### 1.2 Orders & Fills
- `POST /paper/orders`  
  Body:
  ```json
  {
    "account_id": "pa_123",
    "model_id": "universe_eq_swing_daily_scanner",
    "signal_id": "sig_2025-08-15_AAPL",
    "symbol": "AAPL",
    "side": "buy",
    "qty": 100,
    "tif": "MKT",
    "limit_px": null,
    "fill_model": "next_bar_open",
    "bracket": {
      "enabled": true,
      "mode": "atr",
      "atr_mult_stop": 1.2,
      "atr_mult_target": 2.0,
      "time_stop_minutes": 120
    }
  }
  ```
- `POST /paper/cancel` `{ order_id }`  
- `POST /paper/replace` `{ order_id, qty?, limit_px? }`  
- `GET /paper/orders|fills|positions|portfolio?account_id=...`

### 1.3 Alerts
- `GET /paper/alerts/stream?account_id=...` (SSE)  
- `GET /paper/alerts?since=...` (paged pull)

**Event types:** Signal, OrderAccepted, Rejected, PartiallyFilled, Filled, StopHit, TargetHit, TimeStop, Flat, Error.

## 2) Event Schema
```json
{
  "event_id": "ev_001",
  "account_id": "pa_123",
  "model_id": "spy_eq_swing_daily",
  "symbol": "AAPL",
  "etype": "Filled",
  "ts": "2025-08-15T14:31:00Z",
  "payload": {"order_id":"po_789", "fill_px":196.02, "qty":100},
  "fingerprint": {"pack_sha":"...", "model_config_sha":"...", "policy_sha":"..."}
}
```

## 3) Fill Engine
- Models: **next_bar_open** (default), **moc**, **limit_cross**  
- Slippage/costs: commission + bps; **VP cap** on bar volume  
- Calendar: exchange‑aware; **no look‑ahead** (fills on next bar/tick only)

## 4) DB Schemas (DDL)
```sql
CREATE TABLE paper_accounts (
  account_id text PRIMARY KEY,
  name text, cash double precision, buying_power double precision,
  margin_mode text, commission_bps double precision, slippage_bps double precision,
  vp_limit double precision, cfg_sha text, created_at timestamptz default now()
);

CREATE TABLE paper_orders (
  order_id text PRIMARY KEY,
  account_id text, model_id text, signal_id text, symbol text, side text,
  qty integer, tif text, limit_px double precision, status text,
  ts timestamptz, pack_sha text, model_config_sha text, policy_sha text
);

CREATE TABLE paper_fills (
  id bigserial PRIMARY KEY,
  order_id text, fill_ts timestamptz, fill_px double precision, qty integer, fee_bps double precision
);

CREATE TABLE paper_positions (
  account_id text, symbol text, qty integer, avg_px double precision,
  mtm_px double precision, pnl_unreal double precision, pnl_real double precision,
  PRIMARY KEY (account_id, symbol)
);

CREATE TABLE paper_equity_snapshots (
  account_id text, date date, equity double precision,
  cash double precision, margin double precision, exposure double precision,
  PRIMARY KEY (account_id, date)
);

CREATE TABLE paper_alerts (
  id bigserial PRIMARY KEY,
  account_id text, model_id text, symbol text,
  severity text, etype text, ts timestamptz, text text, dedup_key text
);
```

## 5) Brackets (Stops/Targets)
- **ATR mode:** stop = entry − k_s×ATR(14); target = entry + k_t×ATR(14); optional time stop.  
- **Range mode:** swing low/high or Donchian band; measured‑move targets.  
- Enforced as **OCO** by the Paper Broker.

## 6) Allocation & Netting
- Capital policies: equal‑weight, score‑weighted, or per‑model risk caps.  
- Net same‑symbol intents across models; maintain attribution for P&L.

## 7) Parity & Safeguards
- Parity mode: same costs/slippage as backtests → paper matches historical logic.  
- Safeguards: halt on missing bars/coverage; show `/healthz` hints; rate‑limit handling.
