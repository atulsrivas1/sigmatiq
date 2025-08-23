# Catalog Explainers — Design Package

Purpose
- Define how we document indicators, indicator sets, and trading strategies for non‑traders using rich, API‑delivered metadata. No implementation in this package — only design, templates, and seeding guidance.

Contents
- `content-models.md` — canonical fields for Indicators, Sets, Strategies, and shared assets (Media, Tags, References, Glossary).
- `api-readonly-spec.md` — read‑only catalog endpoints that return explainer payloads.
- `taxonomy.md` — categories, personas, difficulty, risk, and use‑case tags (controlled vocabulary).
- `editorial-workflow.md` — author/review/publish states, templates, style, and quality gates.
- `seeding-plan.md` — how to populate the catalog from existing docs and artifacts.
- `examples/` — sample explainer payloads (JSON) for quick reference.
- `ai-assistant-spec.md` — future assistant to simplify terms and explainers for non‑traders.

Scope & Non‑Goals
- Scope: metadata, content structure, and API responses for explainers.
- Non‑Goals: database schema, migrations, or service code.
