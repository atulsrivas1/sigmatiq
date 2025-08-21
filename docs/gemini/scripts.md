# Standalone Scripts

This document describes the standalone Python scripts used in the Sigmatiq project.

## apply_migrations.py

*   **Description**: This script applies SQL migrations in order against a PostgreSQL database. It can connect to the database using `DATABASE_URL` environment variable or individual `DB_*` environment variables.
*   **Usage**:

```bash
python scripts/apply_migrations.py --dir products/sigma-lab/api/migrations
python scripts/apply_migrations.py --dir products/sigma-lab/api/migrations --dry-run
```

*   **Arguments**:

| Name | Description |
| --- | --- |
| `--dir` | **Required**. Directory containing `*.sql` migrations. |
| `--dry-run` | If present, lists files without applying migrations. |

*   **Environment Variables**:

| Name | Description |
| --- | --- |
| `DATABASE_URL` | Full database connection URL (e.g., `postgres://user:pass@host:port/db`). |
| `DB_USER` | Database user. |
| `DB_PASSWORD` | Database password. |
| `DB_HOST` | Database host. |
| `DB_PORT` | Database port. |
| `DB_NAME` | Database name. |

## create_model.py

*   **Description**: This script scaffolds a new model directory and policy template. It can derive the `model_id` automatically based on provided arguments.
*   **Usage**:

```bash
python scripts/create_model.py --pack_id zerosigma --ticker SPY --asset opt --horizon 0dte --cadence hourly
```

*   **Arguments**:

| Name | Description |
| --- | --- |
| `--pack_id` | **Required**. The ID of the pack. |
| `--model_id` | The ID of the model. If not provided, it will be derived from other arguments. |
| `--ticker` | The ticker symbol. |
| `--asset` | The asset type (`opt` or `eq`). |
| `--horizon` | The trading horizon (`0dte`, `intraday`, `swing`, or `long`). |
| `--cadence` | The trading cadence (`5m`, `15m`, `hourly`, or `daily`). |
| `--algo` | The algorithm to use. |
| `--variant` | An optional variant name. |

## generate_indicators_reference.py

*   **Description**: This script generates a Markdown catalog of available indicators. It tries to import `sigma_core.indicators.registry` and introspect indicator classes. If imports fail, it falls back to listing files under `products/sigma-core/sigma_core/indicators/builtins`.
*   **Usage**:

```bash
python scripts/generate_indicators_reference.py --out docs/INDICATORS_REFERENCE.md
```

*   **Arguments**:

| Name | Description |
| --- | --- |
| `--out` | The output path for the Markdown catalog. Defaults to `docs/INDICATORS_REFERENCE.md`. |

## wiki-sync.sh

*   **Description**: This shell script syncs the `docs/` directory into the GitHub Wiki repo for the project. It copies `docs/` content to a temporary build folder, drops the leading `docs/` (so content sits at wiki root), excludes `_archive/`, ensures `Home.md` exists (from `INDEX.md`), clones or updates the `<repo>.wiki.git` repo, and pushes changes.
*   **Usage**:

```bash
./scripts/wiki-sync.sh
```
