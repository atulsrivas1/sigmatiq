# Stock Bracketed Alerts — How-To

This guide explains the new stock alerts that include actionable entry and exit brackets.

## What’s Included
- side: implied by strategy (buy for breakout/momentum)
- entry_mode: next_session_open (daily) or next_bar_open (intraday)
- entry_ref_px: price used to compute brackets (close for preview; runtime can substitute next open)
- stop_px, target_px: ATR-based brackets (defaults: stop=1.2×ATR, target=2.0×ATR)
- time_stop_minutes: flatten if neither bracket hits (default: 120)
- rr: risk:reward ratio = (target−entry)/(entry−stop)
- context: close, atr_14, score_total (scanner) or confidence (ML)

## Policy
Add the following under your policy’s `execution` section (optional; defaults applied if omitted):
```
policy:
  execution:
    brackets:
      enabled: true
      entry_mode: next_session_open   # or next_bar_open
      mode: atr                       # atr|range (atr default)
      atr_period: 14
      atr_mult_stop: 1.2
      atr_mult_target: 2.0
      time_stop_minutes: 120
      min_rr: 1.5
```

## How it’s computed
- ATR floor: we floor ATR at 0.05% of price to avoid overly tight stops in low-vol regimes.
- Entry reference: preview uses last `close`; live runtimes can replace with the next open to match `entry_mode`.
- Filtering: if `min_rr` is set, alerts below this RR are suppressed.

## Outputs
- API `/scan`: writes `products/edge-lab/live_data/<model_id>/signals.csv` containing bracket fields.
- ML alerts: `make alerts MODEL_ID=<model_id>` appends bracket fields when `close` and `atr_14` exist in the matrix.

## Example
```
Ticker,Date,Side,EntryMode,EntryRefPx,StopPx,TargetPx,TimeStopMin,RR,Score
AAPL,2025-08-06,buy,next_session_open,199.30,196.90,203.30,120,2.00,0.81
```

## Next steps
- Options overlay: select contracts and compute premium-equivalent brackets (single leg first).
- Calibration: sweep `atr_mult_*` to target an RR/hit-rate; expose via an endpoint.
