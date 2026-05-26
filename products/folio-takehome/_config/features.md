# Folio Features — Open Decisions

Track decisions here during `02_design`; link from stage outputs.

## 1. Scheduled publishing

- [ ] Visibility rule before `published_at`
- [ ] User-facing copy for "not yet available"
- [ ] Audit events to log

## 2. Human-readable document IDs

- [x] Format: `{slug}-{4char}` (e.g. `welcome-packet-a3f2`)
- [x] Collision handling: retry random suffix
- [x] Complements share tokens (recipients still use opaque `view.php?token=`)

## 3. Share by name

- [ ] Search semantics (exact / prefix / fuzzy)
- [ ] Justification in design output

## Integration (future)

- Contracts live in hub `shared/contracts/` — not in this repo until needed.
