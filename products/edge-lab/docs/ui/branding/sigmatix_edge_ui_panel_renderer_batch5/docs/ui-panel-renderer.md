# Sigmatiq Edge – UI Panel Renderer (Batch 5)

Schema-driven renderer that turns `ui_panels.json` into **forms**, **tabs**, and **result views**.

## Schema (example)

```json
{
  "pack": "ZeroEdge",
  "version": "1.3.0",
  "panels": [
    {
      "id": "config",
      "title": "Configuration",
      "layout": "form+preview",
      "fields": [
        { "id": "symbol", "label": "Symbol", "type": "text", "required": true, "placeholder": "SPY" },
        { "id": "lookback", "label": "Lookback", "type": "number", "min": 10, "max": 500, "step": 10, "value": 120 },
        { "id": "entry_policy", "label": "Entry Policy", "type": "select", "options": [["breakout","Breakout"],["reversal","Reversal"]], "value": "breakout" },
        { "id": "risk_pct", "label": "Max Risk %", "type": "number", "value": 1.0, "adornment": "%" },
        { "id": "live_alerts", "label": "Live Alerts", "type": "switch", "value": true, "inline": true },
        { "id": "metrics", "label": "Backtest Metrics", "type": "checkbox-group", "options": [["cagr","CAGR"],["sharpe","Sharpe"],["mdd","Max Drawdown"]] },
        { "id": "horizon", "label": "Horizon", "type": "radio-group", "options": [["intraday","Intraday (0DTE)"],["swing","Swing"]], "value": "intraday" }
      ],
      "actions": [
        { "id": "run_backtest", "label": "Run Backtest", "kind": "primary" },
        { "id": "save_template", "label": "Save Template", "kind": "secondary" }
      ]
    },
    {
      "id": "results",
      "title": "Results",
      "layout": "tabs",
      "tabs": [
        { "id": "equity", "label": "Equity Curve", "type": "chart", "source": "backtest.equity" },
        { "id": "metrics", "label": "Metrics", "type": "table", "source": "backtest.metrics" },
        { "id": "trades", "label": "Trades", "type": "table", "source": "backtest.trades", "paginated": true }
      ]
    }
  ]
}
```

## Usage

```html
<link rel="stylesheet" href="/tokens/colors.css">
<link rel="stylesheet" href="/tokens/typography.css">
<link rel="stylesheet" href="/components/ui-panel-renderer.css">
<script src="/components/ui-panel-renderer.js"></script>

<div id="mount"></div>
<script>
  fetch('/packs/zero/ui_panels.json')
    .then(r => r.json())
    .then(schema => SigmatiqUIPanels.renderUIPanels(document.getElementById('mount'), schema));
</script>
```

## Notes
- Renderer supports field types: `text`, `number`, `search`, `textarea`, `select`, `switch`, `checkbox-group`, `radio-group`.
- Result tabs: `chart` (simple canvas line chart), `table` (metrics/trades). You can inject real data after backtest runs.
- Accent color is driven by `data-edge="zero|swing|long|overnight|custom"` on `<html>` or a container.
- Accessibility: forms use labels/titles; tabs use `role="tablist"`/`role="tab"` and `aria-selected`.

## Extensibility
- Add new field types by extending `fieldControl()` in `ui-panel-renderer.js`.
- Replace `generateDemoBacktest()` with real API callbacks in your app.
- For charts, you can swap the canvas routine with your preferred charting library;
  keep the container `#chart-<id>` to mount external charts.