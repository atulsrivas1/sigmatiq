
# Alerts Integration Guide (Models → Paper Trader)
*Generated: 2025-08-15 20:56 UTC*

**Alert sources**
- Model **Signal** decisions
- Paper **Execution** lifecycle (OrderAccepted/Rejected/PartiallyFilled/Filled/StopHit/TargetHit/TimeStop/Flat)
- **Account** state (BP low, exposure caps, policy gates)

**Normalized envelope**
```json
{
  "ts": "2025-08-15T14:31:00Z",
  "model_id": "spy_eq_swing_daily",
  "account_id": "pa_123",
  "symbol": "AAPL",
  "severity": "info|warn|error",
  "etype": "Filled",
  "text": "Filled 100 AAPL @ 196.02; stop 193.60, target 200.02",
  "dedup_key": "po_789#filled#2025-08-15"
}
```

**Delivery & UI**
- SSE stream for live; paged pull for history.  
- Filters by model/account/severity/event; deep‑link to order/position detail.

**Policy‑aware messages**
- Momentum/cooldown gates emit **warn** with thresholds.  
- Bracket alerts carry reason (ATR stop, ML stop, time stop).

**Ops**
- Attach run fingerprints to every alert for reproducibility.  
- Surface `/healthz` state and DB connectivity.
