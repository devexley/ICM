# Migrations

Implements the README requirement: *schema changes go through migration files, not by editing `schema.sql` directly.*

## Flow

```
docker compose up  →  seed.php
                         ├─ DELETE db.sqlite (fresh state)
                         ├─ EXEC schema.sql          (baseline only)
                         ├─ run_migrations()         (lib/migrate.php)
                         └─ INSERT seed data         (uses migrated columns)
```

`tests/test.php` calls `seed.php` first, so CI and local tests use the same path.

## Tracking

Applied files are recorded in `schema_migrations` (`version` = filename). Each `.sql` file runs at most once per database file. Because `seed.php` wipes the DB on every start, all migrations re-apply on each container boot — which matches the take-home’s “known state every run” behavior.

## Files

| File | Feature | Schema change |
|------|---------|---------------|
| `001_add_public_id.sql` | Task 2 — human-readable IDs | `ALTER TABLE documents ADD COLUMN public_id` + unique index |
| `002_add_published_at.sql` | Task 1 — scheduled publishing | `ALTER TABLE documents ADD COLUMN published_at` |

## What stays out of `schema.sql`

These columns are **only** added via migrations:

- `documents.public_id`
- `documents.published_at` (UTC `Y-m-d H:i:s`; staff UI uses US Central)

Verify with: `python3 ../../scripts/validate_icm.py` (folio migration checks) or `tests/test.php` (runtime column check).
