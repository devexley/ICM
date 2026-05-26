# Folio Take-Home — Layer 1 (Product Routing)

**Hub:** `../../CONTEXT.md`  
**Identity:** `CLAUDE.md`

## Features in scope (README)

1. Scheduled publishing  
2. Human-readable document IDs  
3. Share by name (search)

## Stages

| Stage | Folder | Role |
|-------|--------|------|
| 1 | `stages/01_discovery/` | Read codebase + requirements; capture ambiguities |
| 2 | `stages/02_design/` | Migrations, ID format, search semantics, tradeoffs |
| 3 | `stages/03_implement/` | Code + tests in this product tree |
| 4 | `stages/04_verify/` | Docker, tests, fresh-clone checklist |

## Layer 3 (this product)

| File | Purpose |
|------|---------|
| `_config/conventions.md` | PHP/SQLite, migrations, audit_log |
| `_config/features.md` | Feature notes and open decisions |
| `stages/*/references/` | Stage-scoped reference |

## Hub Layer 3 (read when needed)

| File | Purpose |
|------|---------|
| `../../_config/conventions.md` | Portfolio-wide rules |
| `../../shared/contracts/` | Future cross-service contracts |

## Rules

- Implement only in this product directory (app root = `products/folio-takehome/`).
- Do not load other `products/*` unless hub routes to `integration/`.
