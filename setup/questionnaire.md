# Portfolio Setup Questionnaire

Configure the **hub factory** (Layer 3), not a single product run.

## Portfolio

1. **Hub name / org:**
2. **Default verify ethos** (tests required, migration policy, etc.):

## Products

3. **Active products** (name, path under `products/`, stack):
4. **Planned integrations** (which products will share contracts later):

## Agent workflow

5. **Primary agent environment** (e.g. Claude Code, Cursor):
6. **Review gates** (which stage boundaries need human sign-off):

## After setup

- Copy answers into `_config/conventions.md`
- Register each product in hub `CONTEXT.md`
- Run `python3 scripts/validate_icm.py`

Per-product setup: use `products/<name>/_config/` and that product's stages.
