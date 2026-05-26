# ICM Portfolio Hub

[Interpretable Context Methodology](https://arxiv.org/abs/2603.16021) **portfolio hub**: one workspace to route across **discrete, buildable products** with shared conventions and future cross-service contracts.

## Layout

```text
ICM/
├── CLAUDE.md                 # Layer 0 — hub identity
├── CONTEXT.md                # Layer 1 — product index
├── _config/                    # Layer 3 — org-wide factory
├── shared/contracts/         # Layer 3 — cross-product APIs (future)
├── integration/              # Cross-product wiring
├── products/
│   └── folio-takehome/       # Example product + app source
│       ├── CLAUDE.md
│       ├── CONTEXT.md
│       ├── stages/             # discovery → design → implement → verify
│       └── …                   # PHP app (from GitHub)
└── scripts/validate_icm.py
```

## Validate

```bash
python3 scripts/validate_icm.py
```

## Hub activity log (local)

Run commands with pre/post ICM validation and append to `logs/hub.log`:

```bash
python3 scripts/icm_run.py validate
python3 scripts/icm_run.py exec --product folio-takehome -- docker compose exec app php tests/test.php
python3 scripts/icm_run.py git --product folio-takehome -- add -A
python3 scripts/icm_run.py git --product folio-takehome -- commit -m "message"
```

## Work on Folio

1. Open hub → read `CONTEXT.md` → `products/folio-takehome/`.
2. Run stages in order; review each `stages/*/output/` before continuing.
3. Build: `cd products/folio-takehome && docker compose up`.

## Add another product

1. Create `products/<name>/` with `CLAUDE.md`, `CONTEXT.md`, `_config/`, `stages/`.
2. Register in hub `CONTEXT.md`.
3. Re-run validator.

## References

- Paper: https://arxiv.org/abs/2603.16021
- Folio source: https://github.com/devexley/folio-takehome
