# ICM Portfolio Hub — Layer 1 (Routing)

**Question this layer answers:** Where do I go?

## Products

| ID | Path | Stack | Verify command |
|----|------|-------|----------------|
| folio | `products/folio-takehome/` | PHP, SQLite, Docker | `docker compose exec app php tests/test.php` |

**Status:** `folio` = example / active take-home (source: [devexley/folio-takehome](https://github.com/devexley/folio-takehome)).

## Routing

| User intent | Load |
|-------------|------|
| Work on Folio | `products/folio-takehome/CONTEXT.md` |
| Cross-service integration | `integration/CONTEXT.md` |
| Org-wide rules | `_config/conventions.md` |
| Shared API contracts | `shared/contracts/` (when present) |
| Portfolio setup | `setup/questionnaire.md` |

## Rules

- Do **not** load all products at once. Pick one product, then one stage.
- Product code and product stages live under `products/<name>/` only.
- Hub `stages/` does not exist — stages are **per product**.
