# Assistant Hooks and Integrations (UI Implementation Guide)

Purpose
- Make the AI Assistant truly in-flow by adding inline hooks at key UI moments, while keeping actions safe and explicit.
- This guide specifies per-page trigger points, DOM selectors, example prompts, and the endpoint calls that follow.
- Pairs with API doc: `products/sigma-lab/docs/api/Assistant_API_Spec_v1.md`.

Global Concepts
- Toggle: global Assistant button `#assistantToggle` opens the drawer.
- Inline hooks: buttons or chips near errors, gates, empty states, and advanced forms. Use `data-ai-hook` and `data-ai-context` attributes.
- Safety: all mutating suggestions return a preview diff for user approval, then map to explicit endpoints (e.g., `PATCH /models/{id}` or `POST /backtest`).
- Context packet: consistent shape sent to `/assistant/query` (see Appendix).

Hook Patterns
- Ask AI to explain: shows a textual explanation and suggested next steps. No mutation.
- Ask AI to fix: returns a proposed config/policy/param patch; user sees a diff and applies.
- Ask AI to recommend: returns a suggested parameter set (e.g., sweeps grid) to prefill a form.

Per-Page Hooks

1) Designer — `#/models/:id/designer`
- Invalid policy keys or schema errors
  - Selector: `.policy-editor [data-error], .validation-drawer .error-item`
  - Hook: "Ask AI to fix"
  - Prompt: "Given these policy errors, propose a valid YAML patch that preserves intent. Explain changes."
  - Endpoint: `POST /assistant/query`
    - Action on accept: `PATCH /models/{id}` with `{ pack_id, config|policy_patch }`, then re-run `GET /validate_policy`.
- Indicator set generation
  - Selector: `.indicators-toolbar .generate-btn`
  - Hook: "Ask AI to generate indicator set for {ticker,horizon,cadence}"
  - Endpoint: `POST /assistant/query` → returns `{ indicators: [...] }`
    - Action on accept: `POST /indicator_sets` with `{ pack_id, scope, model_id?, name, indicators }`.
- Explain Execution Effective
  - Selector: `.execution-effective .help-icon`
  - Hook: "Explain how slippage_bps/size_by_conf/conf_cap affect PnL and gates"
  - Endpoint: `POST /assistant/query` (no mutation)

2) Composer — Build — `#/models/:id/composer/build`
- QA failure explanations
  - Selector: `.matrix-qa .badge-error, .matrix-qa .badge-warn`
  - Hook: "Explain why {metric} failed and propose Build params"
  - Endpoint: `POST /assistant/query` → `{ suggestions: { start,end,k_sigma,distance_max,... } }`
    - Action on accept: prefill form; user clicks `POST /build_matrix`.

3) Composer — Sweeps — `#/models/:id/composer/sweeps`
- Recommend sweeps grid
  - Selector: `.sweeps-form .ai-recommend`
  - Hook: "Recommend thresholds and hours variants based on last N runs and policy guardrails"
  - Endpoint: `POST /assistant/query` → `{ thresholds_variants, allowed_hours_variants, top_pct_variants }`
- Gate badge rationale
  - Selector: `.runs-table .gate-badge`
  - Hook: "Why did this fail Trades Gate?"
  - Endpoint: `POST /assistant/query` (explain; no mutation)

4) Composer — Leaderboard — `#/models/:id/composer/leaderboard`
- Compare and summarize
  - Selector: `.leaderboard-toolbar .compare-btn`
  - Hook: "Summarize differences for selected runs; suggest configs within min_trades"
  - Endpoint: `POST /assistant/query` (explain + recommend params)

5) Composer — Backtest — `#/models/:id/composer/backtest`
- Threshold suggestions
  - Selector: `.backtest-form .ai-suggest`
  - Hook: "Suggest thresholds balancing Sharpe and Trades; reflect parity"
  - Endpoint: `POST /assistant/query` → `{ thresholds, allowed_hours, calibration? }` 
    - Action on accept: set form; user runs `POST /backtest`.

6) Composer — Train — `#/models/:id/composer/train`
- Curate selection per Risk Profile
  - Selector: `.selection-cart .ai-curate`
  - Hook: "Select runs that pass {risk_profile} gates; explain exclusions"
  - Endpoint: `POST /assistant/query` → `{ curated_run_ids: [...] }`

7) Signals — `#/signals`
- Anomaly insights
  - Selector: `.signals-leaderboard .ai-insight`
  - Hook: "Why did fill_rate dip {date}? Provide hypotheses and checks"
  - Endpoint: `POST /assistant/query` (explain; no mutation)

8) Overlay — `#/overlay`
- Strike/spread recommendations
  - Selector: `.overlay-form .ai-recommend`
  - Hook: "Propose vertical width and target delta given IV and OI constraints"
  - Endpoint: `POST /assistant/query` → `{ target_delta, spread_width, min_oi }` 

9) Admin — `#/admin/*`
- Explain flags/quotas impacts; propose changes with preview
  - Selector: `.admin-table .ai-explain`
  - Endpoint: `POST /assistant/query` → `{ patch: {...} }`
  - Action on accept: show diff; when available, call `/admin/*` PATCH.

DOM Integration
- Add `data-ai-hook` to clickable elements that open the Assistant with a prepared prompt and context.
  - Example: `<button class="chip ai-fix" data-ai-hook data-ai-context="policy" data-error-ids="e1,e2">Ask AI to fix</button>`
- The global drawer listens for `click` on `[data-ai-hook]`, builds the context packet, and posts to `/assistant/query`.

Context Packet (summary)
- See full spec: Assistant_API_Spec_v1.md. Minimal:
```
{
  "route": "#/models/spy_opt_0dte_hourly/designer",
  "model_id": "spy_opt_0dte_hourly",
  "pack_id": "zerosigma",
  "risk_profile": "balanced",
  "view": "designer|build|sweeps|leaderboard|backtest|train|signals|overlay|admin",
  "form_values": { ...visible form fields... },
  "selection": [ ...run ids... ],
  "recent_api": {
    "/model_detail": { ... },
    "/validate_policy": { ... },
    "/leaderboard?model_id=...": { ... }
  },
  "user_prompt": "...if provided..."
}
```

Security & UX
- Never auto-apply changes. Always show a diff preview and route to the explicit endpoint (PATCH/POST) on user confirmation.
- Telemetry (optional): record which suggestions are accepted; privacy-safe and opt-in.

Appendix: Minimal Client Binding
- Global drawer element: `#assistantToggle` opens/closes `.assistant-drawer`.
- Bind `document.addEventListener('click', e => if (e.target.matches('[data-ai-hook]')) handleAIHook(e.target))`.
- `handleAIHook(el)` gathers context from DOM/store, opens drawer in loading state, calls `/assistant/query`, streams response; if `action.patch` present, render a diff with Apply/Cancel.

