# Sigmatiq — Tone of Voice & Microcopy Guide v1

## Purpose
Make the product clear, candid, and safe. Write like a disciplined operator, not a promoter.

## Voice
Analytical. Transparent. Disciplined. Teacher‑mindset. Pragmatic.

## Core Rules
- Prefer numbers to adjectives.  
- Put risk and assumptions upfront.  
- Avoid promises of returns.  
- Be brief. One idea per sentence.  
- Use active voice.  
- Use consistent terms (see Lexicon).

## Style
- Capitalization: Sentence case for UI labels and headings.  
- Numerics: 1–9999 with separators (e.g., 12,500). Two decimals max unless precision matters.  
- Time: ISO or unambiguous dates (e.g., 2025‑08‑16).  
- Buttons: Verb + object (e.g., “Run Backtest”).  
- Tooltips: One sentence. State purpose or caveat.  
- Errors: Say what failed, why, and how to fix. Avoid blame.

## Compliance statements (use when performance appears)
- “Past performance does not guarantee future results.”  
- “Simulated results may differ from live execution due to fills, slippage, and routing.”  
- “Positions and automation are governed by your policies and limits.”

## Empty/Loading/Error Patterns
**Loading**: “Loading…”. Use skeletons for tables and cards.  
**Empty**: State what’s missing + next step.  
**Error**: “We couldn’t <action>. <Short reason>. Try again.”

Examples:  
- Empty table: “No models yet. Create your first model.”  
- Error fetch: “We couldn’t load models. Check network and retry.”  
- Validation: “Ticker is required.”

## Microcopy by Route

### `/` Dashboard
- Card titles: “Recent Models”, “Last Runs”, “Quick Actions”, “Health”  
- CTA: “Create Model”, “Run Backtest”, “Open Sweeps”  
- Empty: “No recent models.” CTA “Create Model”  
- Health statuses: “API: ok · DB: warn · Data: ok”

### `/models` List
- Search placeholder: “Search model_id…”  
- Filters: “Pack”, “Sort by updated”  
- Row actions: “Open”, “Sweeps”, “Backtest”  
- Empty: “No models match your filters.” CTA “Clear filters”  
- Error: “We couldn’t load models. Retry.”

### `/models/new` Create Wizard
**Step 1 — Basics**  
- Labels: “Ticker”, “Asset”, “Horizon”, “Cadence”  
- Helper: “We auto‑preview model_id from your choices.”  
- Validation: “Ticker is required.”

**Step 2 — Indicator Set**  
- Toggle: “Use pack default”  
- Tooltip: “Start with the pack defaults. Customize later.”

**Step 3 — Policy**  
- Button: “Validate Policy”  
- Success: “Policy looks valid.”  
- Error: “Policy failed checks. Review highlighted fields.”

**Step 4 — Preview**  
- Button: “Run Preview”  
- Coverage note: “NaN coverage above threshold blocks save.”

**Step 5 — Save**  
- Button: “Create Model”  
- Success toast: “Model created.” Redirect to detail.

### `/models/:modelId` Detail
- Section headers: “Summary”, “Latest”, “Quick Run”, “Shortcuts”  
- Buttons: “Build”, “Train”, “Backtest”  
- Links: “Open Sweeps”, “Open Leaderboard”, “Open Signals”, “Options Overlay”  
- Empty Latest: “No runs yet. Use Quick Run to start.”

### `/runs` Build/Train/Backtest
- Build: “Run Build” → result: “Matrix ready.”  
- Train: “Run Train” → “Artifact saved.”  
- Backtest: “Run Backtest” → show “Plots” and “Metrics”.  
- Error: “Backtest failed. Review parameters and retry.”

### `/sweeps`
- Controls: “Thresholds variants”, “Allowed hours variants”, “Top % variants”, “Guards”  
- Buttons: “Run Sweep”, “Export All CSV”, “Train with this combo”  
- Empty: “No results. Adjust variants or relax guards.”

### `/leaderboard`
- Filters: “Model”, “Pack”, “Tag”, “Sort”  
- Columns: “started_at”, “model_id”, “best_sharpe”, “best_cum_ret”, “tag”  
- Empty: “No runs found for your filters.”

### `/signals`
- Filters: “Date”, “Ticker”  
- Download: “Export CSV”  
- Disclaimer: include compliance statements.

### `/overlay` Options Overlay
- Inputs: “Expiry / DTE target”, “Target delta”, “Min OI”  
- Summary: “Overlay count”, “Parity summary”  
- Error: “Quotes unavailable for the selected date/expiry.”

### `/health`
- Headline: “System health”  
- Status: “ok | warn | error”  
- CTA: “View docs for common issues.”

### `/docs`
- Buttons: “AGENTS.md”, “BACKLOG.md”, “Runbooks”, “Indicators REF”, “Policy Schema”

## Lexicon
Prefer: **strategy**, **signal**, **policy**, **capacity**, **slippage**, **parity**, **drawdown**, **out‑of‑sample**.  
Avoid: **tip**, **guarantee**, **win rate** without context, **risk‑free** (except “risk‑free simulation”).

## Template Snippets
- Banner warning: “Live automation paused by your daily loss cap.”  
- Toast success: “Backtest complete. View leaderboard.”  
- Tooltip parity: “Compares live fills vs. simulated fills.”  
- Inline hint: “Seat limits protect subscribers from crowding.”

## Internationalization
- Keep strings short for translation.  
- Do not embed units inside numbers; keep as separate tokens.  
- Use UTC‑safe timestamps or display user timezone.

## Accessibility
- Use descriptive aria‑labels on icon‑only buttons.  
- Every form field has a label and an error message container.  
- Focus ring visible on all interactive elements.
