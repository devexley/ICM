# Source

Cloned from: https://github.com/devexley/folio-takehome

Refresh app code (preserving ICM overlay):

```bash
# From repo root — backup ICM files if needed, or use git subtree/submodule later
git clone --depth 1 https://github.com/devexley/folio-takehome.git /tmp/folio-sync
rsync -a --exclude='stages' --exclude='CONTEXT.md' --exclude='_config' --exclude='CLAUDE.md' --exclude='SOURCE.md' /tmp/folio-sync/ products/folio-takehome/
```

Prefer **git submodule** for long-term sync; this monorepo copy is for local ICM hub convenience.
