# Stage 03 — Implement (Layer 2)

## Inputs

| Source | Location | Layer | Scope |
|--------|----------|-------|-------|
| Design | `../02_design/output/` | 4 | design.md, migrations.md, test-plan.md |
| Product conventions | `../../_config/conventions.md` | 3 | audit_log, migration rules |
| Codebase | `../../` (app root) | 4 | Implement per approved design |

## Process

1. Add migration file(s) per design — do not edit `schema.sql` for features.
2. Implement features in priority order from `01_discovery/output/scope.md`.
3. Add tests in `tests/test.php` (one per shipped feature minimum).
4. Log audit events for create, schedule, share actions.
5. Write implementation notes to `output/`.

## Outputs

| Artifact | Location |
|----------|----------|
| Code changes | App tree (`public/`, `lib/`, migrations, `tests/`) |
| Implementation log | `output/implementation.md` |

## Audits

- [ ] Matches approved design (or documents deviations in implementation.md)
- [ ] Tests exist for each shipped feature
