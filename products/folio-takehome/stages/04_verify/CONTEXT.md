# Stage 04 — Verify (Layer 2)

## Inputs

| Source | Location | Layer | Scope |
|--------|----------|-------|-------|
| Implementation | `../03_implement/output/implementation.md` | 4 | What was built / skipped |
| Design test plan | `../02_design/output/test-plan.md` | 4 | Expected coverage |
| App tree | `../../` | 4 | Run against live container |

## Process

1. `docker compose up` — confirm app serves on :8000.
2. `docker compose exec app php tests/test.php` — all pass.
3. Manual smoke: admin, share link, scheduling edge, search (if built).
4. Fresh-clone mental check: README setup still valid.
5. Record results and video talking points in `output/`.

## Outputs

| Artifact | Location |
|----------|----------|
| Verify report | `output/verify.md` |
| Video outline | `output/video-outline.md` |

## Audits

- [ ] Test command documented with pass/fail
- [ ] Skipped features explained with rationale
