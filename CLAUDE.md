# ICM Portfolio Hub — Layer 0 (Identity)

**Question this layer answers:** Where am I?

You are in an **Interpretable Context Methodology (ICM) portfolio hub**. One orchestrating agent routes to **discrete products** under `products/`, loads only scoped context per stage, and uses `integration/` when wiring multiple products.

## Hub map

| Path | Layer | Purpose |
|------|-------|---------|
| `CONTEXT.md` | 1 | Product index + cross-cutting routes |
| `_config/` | 3 | Org-wide factory (conventions, git, testing ethos) |
| `shared/contracts/` | 3 | Cross-product APIs/events (future integration) |
| `shared/`, `skills/` | 3 | Reusable reference and domain skills |
| `integration/` | 2 | Cross-product wiring (when needed) |
| `products/<name>/` | 1–4 | Discrete, buildable product workspaces |
| `setup/questionnaire.md` | — | Portfolio / org setup (once) |

## Products

| ID | Path | Description |
|----|------|-------------|
| folio | `products/folio-takehome/` | PHP/SQLite document-sharing take-home |

Add rows to hub `CONTEXT.md` when onboarding new products.

## Agent flow

1. Read hub `CONTEXT.md` → pick product (or `integration/`).
2. Read `products/<name>/CONTEXT.md` → pick stage.
3. Read stage `CONTEXT.md` → follow Inputs / Process / Outputs only.
4. Human reviews each stage `output/` before the next stage.

## References

- Paper: [Interpretable Context Methodology](https://arxiv.org/abs/2603.16021)
- Protocol: https://github.com/RinDig/Interpretable-Context-Methodology-ICM-
