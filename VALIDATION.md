# ICM Hub Validation

## Hub (required)

- [ ] `CLAUDE.md` — portfolio map, product list
- [ ] `CONTEXT.md` — product index + routing (no hub-level `stages/`)
- [ ] `_config/conventions.md` — org-wide rules
- [ ] `shared/contracts/` — cross-product contracts (may be empty)
- [ ] `integration/CONTEXT.md` — cross-product workflow
- [ ] No legacy `stages/` at hub root

## Each product (required)

- [ ] `products/<name>/CLAUDE.md` + `CONTEXT.md`
- [ ] `products/<name>/_config/conventions.md`
- [ ] `products/<name>/stages/NN_*/` with Inputs, Process, Outputs
- [ ] Each stage: `references/`, `output/.gitkeep`
- [ ] Stage 02+ references prior stage outputs in Inputs

## Folio product

- [ ] App source present (`public/`, `lib/`, `docker-compose.yml`)
- [ ] Engineering stages: `01_discovery` … `04_verify`
- [ ] `SOURCE.md` documents upstream repo
- [ ] **Migrations:** `schema.sql` has no `public_id` / `published_at`; columns only in `migrations/*.sql`
- [ ] `seed.php` runs `schema.sql` then `run_migrations()`
- [ ] README § “Schema migrations (implemented on this branch)” documents approach

## Automated

```bash
python3 scripts/validate_icm.py
```

## Optional runtime verify (Folio)

```bash
cd products/folio-takehome && docker compose exec app php tests/test.php
```

Requires Docker and a running `docker compose up` container.
