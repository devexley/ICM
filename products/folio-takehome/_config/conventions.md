# Folio Conventions (Layer 3 — Product)

Overrides hub defaults only where noted; hub rules still apply.

## Stack

- PHP, SQLite, Docker Compose
- Edit on host; container mounts project

## Schema

- **Do not** edit `schema.sql` for feature work (baseline tables only).
- Add **migration file(s)** under `migrations/`; applied by `lib/migrate.php` from `seed.php`.
- Canonical docs: `migrations/README.md` and README § “Schema migrations (implemented on this branch)”.
- `docker compose up` re-seeds DB from scratch (known state each run).

## Audit

- Log document creation, scheduling changes, and share actions to `audit_log` (see `lib/bootstrap.php`).

## Tests

- Extend `tests/test.php` pattern.
- At least one test per shipped feature.

## Deliverables (take-home)

- Branch with clear commit story
- ~5 min video (approach, tradeoffs, AI workflow)
