# Folio Conventions (Layer 3 — Product)

Overrides hub defaults only where noted; hub rules still apply.

## Stack

- PHP, SQLite, Docker Compose
- Edit on host; container mounts project

## Schema

- **Do not** edit `schema.sql` for feature work.
- Add **migration file(s)** you create; document approach in `02_design/output/`.
- `docker compose up` re-seeds DB from scratch (known state each run).

## Audit

- Log document creation, scheduling changes, and share actions to `audit_log` (see `lib/bootstrap.php`).

## Tests

- Extend `tests/test.php` pattern.
- At least one test per shipped feature.

## Deliverables (take-home)

- Branch with clear commit story
- ~5 min video (approach, tradeoffs, AI workflow)
