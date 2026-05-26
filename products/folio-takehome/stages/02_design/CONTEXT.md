# Stage 02 — Design (Layer 2)

## Inputs

| Source | Location | Layer | Scope |
|--------|----------|-------|-------|
| Prior stage | `../01_discovery/output/` | 4 | Full discovery + scope |
| Product conventions | `../../_config/conventions.md` | 3 | Migrations, audit, tests |
| Features tracker | `../../_config/features.md` | 3 | Update with decisions |
| Hub conventions | `../../../_config/conventions.md` | 3 | Portfolio rules |

## Process

1. Resolve open items in `features.md` (ID format, search, scheduling).
2. Design migration approach and file layout.
3. Define URL/share-token strategy and rejected alternatives.
4. Outline test cases per feature.
5. **Human checkpoint:** confirm design before implement.

## Outputs

| Artifact | Location |
|----------|----------|
| Design doc | `output/design.md` |
| Migration plan | `output/migrations.md` |
| Test plan | `output/test-plan.md` |

## Audits

- [ ] `features.md` checkboxes reflect decisions
- [ ] No application code changed yet
