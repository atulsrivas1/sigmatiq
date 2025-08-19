# AI Assistant — Spec v1

## Status
Draft — documentation-only; integrates with BTB v1 workflow and docs

## Goals
- Help users build, backtest, and train models through natural-language guidance.
- Answer “what/why/how” questions using live project context: API/DB, reports (CSV/Excel), run lineage, and docs.
- Reduce friction and errors by suggesting next actions and validating inputs before execution.

## UX Overview
- Chat panel: docked drawer (right) with compact mode; expandable to full height.
- Context-aware: the assistant receives the current route, selected model_id, risk_profile, and visible selections.
- Quick actions: inline chips to run common tasks (Preview, Build Matrix, Run Sweep, Open Leaderboard, Train Selected).
- Message types: text, code (commands), links to artifacts, small tables (rendered with monospace table or grid).
- Safety: confirmation prompts before any action that would start compute jobs.

## Capabilities (Tools)
The assistant operates in read-mostly mode with controlled tool calls:
- Docs search: search and quote from `products/sigma-lab/docs/**`.
- Reports & files:
  - List and read CSV/JSON under `products/sigma-lab/reports/**` and `static/backtest_plots/**` (metadata only).
  - Read Excel (`.xlsx`) via a server utility that converts to table JSON (preview-limited rows, e.g., 200 rows).
- DB summaries (read-only):
  - Leaderboard queries: top runs by metric, filters by model_id/risk_profile/tag/date.
  - Run detail by id; folds summary; recent runs per model.
  - Strict allowlist of SQL templates; parameters validated and bound.
- Pipeline helpers (suggest-only by default):
  - Generate Make commands and REST payloads for Build/Sweeps/Train.
  - Explain gate failures and suggest budget adjustments.
  - Compare configurations (summaries with links to plots/CSVs) and highlight trade-offs.

Optional (controlled execution, off by default):
- Execute API calls for sweeps or training after explicit user confirmation in-chat.

## Data Sources
- Database (read-only): `backtest_runs`, `backtest_folds`, optional `train_jobs`.
- Files: `reports/**`, `static/backtest_plots/**`, `matrices/**/<id>/*.csv` (metadata; content on request), `artifacts/**` (metadata only).
- Docs: ADRs, specs, runbooks for authoritative answers.

## Context & Lineage Injection
- Per message, the shell provides: route, selected model_id (if any), risk_profile, matrix_sha (if on Runs > Build), selection cart contents.
- The assistant includes lineage snippets (matrix_sha/config_sha/policy_sha/risk_sha) in suggestions where relevant.

## Privacy & Guardrails
- Default mode is read-only; any action that triggers compute (sweeps/train) requires explicit user confirmation.
- SQL is never free-form; only allowlisted parameterized templates are permitted.
- File reads are scoped to `products/sigma-lab/{reports,static,matrices,artifacts}`; large files are previewed with row/size limits.
- The assistant cites sources (file path/endpoint or run id) for factual answers.

## Error Handling & Hallucination Safeguards
- If a source isn’t available, the assistant states that and suggests how to generate it (e.g., run a sweep).
- If filters produce no rows, assistant offers nearby alternatives (e.g., relax date or tag).
- All tool outputs are echoed concisely and linked; ambiguous requests trigger clarifying questions.

## API Surfaces (high-level)
- POST `/assistant/query { message, context }` → streams assistant response; tool calls are mediated by the server.
- Tools exposed server-side:
  - `docs.search(query)` → snippets+paths
  - `reports.search({glob})` → file list
  - `reports.read_csv(path, {limit, columns})` → rows
  - `reports.read_xlsx(path, {sheet, limit})` → rows
  - `db.leaderboard(params)` → rows
  - `db.run_detail(id)` → summary
  - `pipeline.suggest(command|payload)` → dry-run commands
  - (opt-in) `pipeline.execute({kind, payload})` → job ids (confirmation required)

## Security & Limits
- Rate-limit per user; max concurrent tool calls.
- Stream responses; cap table previews (e.g., 200 rows) and truncate overly large text with “show more” affordance.

## Acceptance Criteria
- The assistant can:
  - Explain any field in Sweeps/Leaderboard/Train and “why” a row passed/failed Gate, citing budgets.
  - Summarize top N leaderboard rows for a model and risk profile.
  - Read a CSV/Excel report and answer a user’s question with a short table or stat, citing the file path.
  - Propose a sweep payload or Make command from natural language and ask for confirmation before executing.
  - Guide through the Create Model wizard steps (fields, naming, indicator sets, policy validation) and link to docs.
  - Honor guardrails (no compute without confirmation; read-only SQL via templates; scoped file access).

