# ADR 0002: Versioning System

## Status

Accepted

## Context

We need a system for versioning all the artifacts in the system, including indicators, models, and policies. This is essential for reproducibility and governance.

## Decision

We will implement a versioning system based on the following principles:

- **Semantic Versioning:** All artifacts will be versioned using semantic versioning (e.g., `1.0.0`).
- **Immutability:** Once an artifact is versioned, it should be immutable. Any changes to the artifact should result in a new version.
- **Centralized Registry:** All versioned artifacts will be stored in PostgreSQL via `sigma_platform` migrations/schemas (per product DB with optional schema separation).

### Database Schema (illustrative)

The database schema for the registry will be as follows:

**`indicator_sets` table:**

| Column        | Type           | Constraints      |
| ------------- | -------------- | ---------------- |
| `id`          | `SERIAL`       | `PRIMARY KEY`    |
| `name`        | `VARCHAR(255)` | `NOT NULL`       |
| `version`     | `VARCHAR(255)` | `NOT NULL`       |
| `description` | `TEXT`         |                  |
| `created_at`  | `TIMESTAMP`    | `DEFAULT NOW()`  |
| `updated_at`  | `TIMESTAMP`    | `DEFAULT NOW()`  |

**`indicators` table:**

| Column             | Type           | Constraints                 |
| ------------------ | -------------- | --------------------------- |
| `id`               | `SERIAL`       | `PRIMARY KEY`               |
| `indicator_set_id` | `INTEGER`      | `REFERENCES indicator_sets` |
| `name`             | `VARCHAR(255)` | `NOT NULL`                  |
| `version`          | `VARCHAR(255)` | `NOT NULL`                  |
| `params`           | `JSONB`        |                             |
| `created_at`       | `TIMESTAMP`    | `DEFAULT NOW()`             |
| `updated_at`       | `TIMESTAMP`    | `DEFAULT NOW()`             |

**`model_versions` table:**

| Column             | Type           | Constraints      |
| ------------------ | -------------- | ---------------- |
| `id`               | `SERIAL`       | `PRIMARY KEY`    |
| `name`             | `VARCHAR(255)` | `NOT NULL`       |
| `version`          | `VARCHAR(255)` | `NOT NULL`       |
| `description`      | `TEXT`         |                  |
| `artifact_uri`     | `VARCHAR(255)` | `NOT NULL`       |
| `data_hash`        | `VARCHAR(255)` | `NOT NULL`       |
| `git_sha`          | `VARCHAR(255)` | `NOT NULL`       |
| `metrics`          | `JSONB`        |                  |
| `created_at`       | `TIMESTAMP`    | `DEFAULT NOW()`  |
| `updated_at`       | `TIMESTAMP`    | `DEFAULT NOW()`  |

**`policy_versions` table:**

| Column        | Type           | Constraints      |
| ------------- | -------------- | ---------------- |
| `id`          | `SERIAL`       | `PRIMARY KEY`    |
| `name`        | `VARCHAR(255)` | `NOT NULL`       |
| `version`     | `VARCHAR(255)` | `NOT NULL`       |
| `description` | `TEXT`         |                  |
| `spec`        | `JSONB`        |                  |
| `created_at`  | `TIMESTAMP`    | `DEFAULT NOW()`  |
| `updated_at`  | `TIMESTAMP`    | `DEFAULT NOW()`  |

## Consequences

### Positive

- **Reproducibility & Governance:** Immutable versions with lineage fields enable reliable comparisons/audits.
- **Library/pack decoupling:** Packs can evolve independently while products pin versions.
- **Powerful Queries:** A database allows for rich queries and analytics on artifacts.
- **Powerful Queries:** A database allows for rich queries and analytics on the artifacts.

### Negative

- **Initial complexity:** More complex than file-only; requires DB and migrations.
- **Discipline required:** Enforcing immutability and release processes across repos.
