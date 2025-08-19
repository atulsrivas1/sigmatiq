Database Migrations (ADR 0002)

These SQL migrations initialize the artifact/versioning schema described in docs/adrs/0002-versioning-system.md.

Apply via Make:
  make db-migrate DB_NAME=edge_lab

Dry-run without applying:
  make db-migrate-dry DB_NAME=edge_lab

