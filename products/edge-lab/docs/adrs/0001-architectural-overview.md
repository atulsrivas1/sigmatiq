# ADR 0001: Architectural Overview

## Status

Accepted

## Context

We need a system for developing, backtesting, and deploying trading models for different time horizons (0DTE, short-term, long-term). The system should be easy to use, maintainable, and scalable.

## Decision

We will ship a product-first architecture composed of:

- Shared libraries: **edge_core** (data, features, models, backtests) and **edge_platform** (DB/migrations, API helpers, policy, IO).
- Product apps: initially **Edge Lab** (authoring/backtests), with future products **Edge Sim**, **Edge Market**, and **Edge Pilot**.

The shared libraries will provide a consistent pipeline for all products:
`define -> build dataset -> train -> backtest -> policy -> deploy -> live alerts`

Shared libraries will have the following capabilities:
- Indicator & Feature Registry
- Data Adapters
- Dataset Builder
- Training & Model Registry
- Backtesting Engine
- Policy Engine
- Live Signal Runtime
- Observability & Governance
- Orchestration & API

**Horizon Profiles** will be a first-class concept, allowing different configurations per time horizon.

Strategies will be shipped as **Edge Packs**, versioned content that plugs into the shared libraries. Each pack will contain:
- `indicator_set.yaml`
- `feature_defs.py`
- `label_functions.py`
- `model_configs/`
- `policy_templates/`
- `backtest_templates/`
- `ui_panels.json`

UIs will be per-product (e.g., Edge Lab UI) targeting their matching product API. A gateway is optional for unified ingress.

## Consequences

### Positive

- **Clean separation of concerns:** Shared libraries separated from product apps and strategy packs.
- **Reusability:** The core components can be reused across all applications.
- **Consistency:** The consistent pipeline ensures that all strategies are developed and deployed in the same way.
- **Scalability:** The event-driven architecture and the separation of concerns make the system scalable.
- **Governance:** The centralized registries and the versioning system provide good governance and reproducibility.

### Negative

- **Initial complexity:** More moving parts than a monolith (libs + product apps + packs).
- **Coordinated versioning:** Requires dependency/version management between products and shared libraries.
