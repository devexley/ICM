# Integration — Layer 2 (Cross-Product)

**Question this layer answers:** How do we wire multiple products together?

Use this stage set only when connecting two or more products under `products/`.

## Inputs

| Source | Location | Layer | Scope |
|--------|----------|-------|-------|
| Hub conventions | `../_config/conventions.md` | 3 | Org rules |
| Product A contract | `../shared/contracts/` | 3 | As listed per integration task |
| Product B contract | `../shared/contracts/` | 3 | As listed per integration task |
| Product contexts | `../products/*/CONTEXT.md` | 1 | Routing only — do not load full codebases |

## Process

1. Name the integration goal (event, API, shared ID, etc.).
2. Draft or update contract markdown under `shared/contracts/`.
3. Document changes needed per product in `output/integration-plan.md`.
4. Implement in each product separately (product `03_implement` stages).
5. Record verification steps in `output/smoke-test.md`.

## Outputs

| Artifact | Location |
|----------|----------|
| Integration plan | `output/integration-plan.md` |
| Smoke test checklist | `output/smoke-test.md` |
| Contract drafts | `../shared/contracts/*.md` |

## Outputs folder

Write run artifacts to `integration/output/` (create per run).
