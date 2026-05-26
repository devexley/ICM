# Portability

This workspace is designed to be **cloned anywhere** and run with minimal setup. The ICM hub is plain files and Python scripts; products (e.g. Folio) ship their own runtime (Docker).

## Verified

On a fresh clone:

```bash
python3 scripts/validate_icm.py
cd products/folio-takehome
docker compose build
docker compose run --rm app php tests/test.php
```

Expected: hub validation **PASSED**, tests **5 passed, 0 failed**.

## Dependencies

### Required — Folio app (primary path)

| Dependency | Notes |
|------------|--------|
| **Docker** | Engine with **Compose** (`docker compose`) |
| **Network** (first run) | Pulls `php:8.3-cli` and builds the image (~30s) |

Included **inside the container** (no host install):

- PHP 8.3 CLI
- `pdo_sqlite` extension
- SQLite

### Required — ICM hub tooling

| Dependency | Notes |
|------------|--------|
| **Python 3** | `scripts/validate_icm.py`, `scripts/icm_run.py` (stdlib only) |
| **Git** | Clone and version control |

### Optional

| Dependency | Notes |
|------------|--------|
| AI agent (Claude Code, Cursor, etc.) | Reads `CLAUDE.md` / `CONTEXT.md`; not required to run the app |
| Free **port 8000** | Folio default; change `products/folio-takehome/docker-compose.yml` if in use |

### Not required

- `.env` files or API keys
- Node.js / npm
- Host PHP (when using Docker)
- Separate clone of [devexley/folio-takehome](https://github.com/devexley/folio-takehome) — app lives under `products/folio-takehome/`
- External database server (`db.sqlite` is local, gitignored, recreated by `seed.php`)

## Fresh-clone quick start

```bash
git clone <your-repo-url> ICM
cd ICM

# Hub structure + Folio migration policy
python3 scripts/validate_icm.py

# Folio app
cd products/folio-takehome
docker compose up
# → http://localhost:8000

# Tests (separate terminal)
docker compose exec app php tests/test.php
```

From hub root (with logging + validation):

```bash
python3 scripts/icm_run.py exec --product folio-takehome -- docker compose exec app php tests/test.php
```

## Repository layout

| Path | Role |
|------|------|
| Hub root | Routing, org conventions, validators |
| `products/folio-takehome/` | Self-contained product (app + ICM overlay) |
| `products/folio-takehome/migrations/` | Feature schema (not `schema.sql`) |
| `logs/hub.log` | Local activity log (gitignored) |

Folio is a **monorepo copy**, not a git submodule. See `products/folio-takehome/SOURCE.md` only if syncing from upstream.

## Caveats

1. **Clone URL** — Push this repo to your remote; there is no fixed upstream for the hub itself.
2. **`db.sqlite`** — Created at runtime; never required in git.
3. **Timezone** — `products/folio-takehome/lib/bootstrap.php` uses `America/Chicago`.
4. **Port 8000** — Default bind; adjust compose file if it conflicts.
5. **Host PHP** — Supported in theory (PHP 8.3+ with `pdo_sqlite`); README and Dockerfile assume Docker.

## Adding another product

1. Create `products/<name>/` with `CLAUDE.md`, `CONTEXT.md`, `_config/`, `stages/`.
2. Register in hub `CONTEXT.md`.
3. Document product-specific dependencies here or in that product's `CLAUDE.md`.
4. Run `python3 scripts/validate_icm.py`.
