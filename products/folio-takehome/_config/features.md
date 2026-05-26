# Folio Features — Open Decisions

Track decisions here during `02_design`; link from stage outputs.

## 1. Scheduled publishing

- [x] Recipients blocked until `published_at` (view shows "Not yet available")
- [x] Optional `publish_at` on admin create; blank = immediate
- [x] `audit_log` action `schedule` when publish time is in the future

## 2. Human-readable document IDs

- [x] Format: `{slug}-{4char}` (e.g. `welcome-packet-a3f2`)
- [x] Collision handling: retry random suffix
- [x] Complements share tokens (recipients still use opaque `view.php?token=`)

## 3. Share by name

- [x] Search semantics: case-sensitive SQL `LIKE 'term%'` title prefix (fast, predictable for staff UI)
- [x] Admin search form + audit_log on search

## Integration (future)

- Contracts live in hub `shared/contracts/` — not in this repo until needed.
