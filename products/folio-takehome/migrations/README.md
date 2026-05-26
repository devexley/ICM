# Migrations

SQL files run in lexical order after `schema.sql` on each `seed.php` / container start.

Tracked in `schema_migrations`. Do not edit `schema.sql` for feature work — add a new file here.

| File | Feature |
|------|---------|
| `001_add_public_id.sql` | Task 2 — human-readable document IDs |
| `002_add_published_at.sql` | Task 1 — scheduled publishing |
