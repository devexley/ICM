# Stage 01 — Discovery (Layer 2)

## Inputs

| Source | Location | Layer | Scope |
|--------|----------|-------|-------|
| Hub conventions | `../../../_config/conventions.md` | 3 | Org rules |
| Product conventions | `../../_config/conventions.md` | 3 | Stack, migrations, audit |
| Features tracker | `../../_config/features.md` | 3 | Open decisions |
| App README | `../../README.md` | 3 | Task + requirements |
| Codebase | `../../public/`, `../../lib/`, `schema.sql` | 4 | Read selectively — map flows first |

## Process

1. Map admin, share, and recipient flows.
2. List ambiguities (IDs vs tokens, migration strategy, search meaning).
3. Note risks in existing code worth flagging in video.
4. Propose feature order and scope for ~3h budget.
5. Write discovery brief to `output/` — **no implementation**.

## Outputs

| Artifact | Location |
|----------|----------|
| Discovery brief | `output/discovery.md` |
| Feature order + scope | `output/scope.md` |

## Audits

- [ ] No code changes outside `output/`
- [ ] All three README features addressed in scope
