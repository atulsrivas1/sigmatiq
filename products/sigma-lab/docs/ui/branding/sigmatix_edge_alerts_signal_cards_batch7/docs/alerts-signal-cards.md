# Sigmatiq Sigma — Batch 7: Alerts & Signal Cards

Accent-aware dashboard primitives for **live trading signals** and **system notifications**, designed for dark/light themes and all Sigma Pack identities.

## Files
- `components/alerts.css` — Info/Success/Warning/Danger + **Signal** (accent) variant
- `components/signal-cards.css` — Signal card with sparkline, confidence bar, tags, actions
- `components/dashboard.css` — Layout helpers (grid, panels, hero, KPIs)
- `tokens/colors.css`, `tokens/typography.css`, `tokens/sigma-pack-themes.css` — tokens for standalone preview
- `preview/index.html` — Live feed demo (`aria-live="polite"`) + variants
- `data/signal-feed.sample.json` — structure for streaming signals

## Signal schema (suggested)
```json
{
  "edge": "zero",
  "symbol": "SPY",
  "side": "Long",
  "model": "ZE-Alpha",
  "confidence": 0.78,
  "tags": ["0DTE", "microstructure"],
  "ts": "2025-08-15T12:30:00Z"
}
```
- Map `edge` → `data-edge="<key>"` to theme (Zero/Swing/Long/Overnight/Custom).
- Render confidence as a percentage width on `.confidence > span`.

## Accessibility
- Alerts use `role="status"` and concise copy. Prefer queueing high-priority alerts at the top.
- Live feed has `aria-live="polite"` to announce incoming signals without stealing focus.

## Integration tips
- Replace demo JS push loop with your WebSocket/stream handler.
- Mount signal cards into a virtualized list for long feeds.
- Swap canvas sparkline with your chart lib; keep `.spark` element as mount target.