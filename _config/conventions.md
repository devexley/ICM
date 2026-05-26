# Portfolio Conventions (Layer 3 — Hub / Org)

Applies to **all products** unless a product `_config/` overrides with a documented exception.

## Repository layout

- Each product: `products/<name>/` with own `CONTEXT.md`, `stages/`, `_config/`.
- Cross-product contracts: `shared/contracts/` (canonical).
- Integration work: `integration/` only when wiring two or more products.

## Engineering norms

- **Plain text handoffs** — specs and stage outputs in Markdown.
- **One stage, one job** — discovery ≠ design ≠ implement ≠ verify.
- **Migrations** — schema changes via migration files, not editing canonical `schema.sql` in place (product-specific detail in product `_config/`).
- **Tests** — at least one test per feature you ship; run verify stage before calling work done.
- **Audit** — log sensitive actions when the product provides `audit_log` (see product config).

## Git

- Commit agent setup (ICM files) with the product when required by the exercise or team policy.
- Do not commit `stages/*/output/*` run artifacts (see root `.gitignore`).
- Product app artifacts (e.g. `db.sqlite`) stay ignored unless explicitly required.

## References (one-way)

- Products may read `shared/contracts/` and hub `_config/`.
- Products must **not** reference sibling `products/*` directly; use `integration/` + contracts.
