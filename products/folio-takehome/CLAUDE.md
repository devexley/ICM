# Folio Take-Home — Product Layer 0

**Parent hub:** `../../CLAUDE.md`  
**Product routing:** `CONTEXT.md`

## What this is

Minimal PHP/SQLite document-sharing app (Docker). Extend with scheduled publishing, readable IDs, and title search per README.

## Run

```bash
cd products/folio-takehome
docker compose up
# tests:
docker compose exec app php tests/test.php
```

App URL: http://localhost:8000

## ICM stages (this product)

`01_discovery` → `02_design` → `03_implement` → `04_verify`

Review each stage `output/` before continuing.

## Key paths

| Path | Role |
|------|------|
| `schema.sql` | Baseline only — feature columns via `migrations/*.sql` (see README § Schema migrations) |
| `migrations/README.md` | Migration flow and policy |
| `lib/bootstrap.php` | Helpers, audit_log pattern |
| `tests/test.php` | Test pattern |
| `stages/` | ICM stage contracts |
| `_config/` | Folio-specific Layer 3 |
