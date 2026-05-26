#!/usr/bin/env python3
"""
Validate ICM portfolio hub + product workspaces.
Based on: Van Clief & McDermott, Interpretable Context Methodology (2026).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGE_DIR_RE = re.compile(r"^\d{2}_[a-z][a-z0-9_]*$")
REQUIRED_SECTIONS = ("## Inputs", "## Process", "## Outputs")

errors: list[str] = []


def ok(msg: str) -> None:
    print(f"  OK  {msg}")


def fail(msg: str) -> None:
    print(f"  FAIL  {msg}")
    errors.append(msg)


def check_exists(path: Path, label: str) -> None:
    if path.exists():
        ok(label)
    else:
        fail(f"Missing: {path.relative_to(ROOT)}")


def check_stage_contract(stage_path: Path, prefix: str = "") -> None:
    ctx = stage_path / "CONTEXT.md"
    name = f"{prefix}{stage_path.name}" if prefix else stage_path.name
    if not ctx.exists():
        fail(f"{name}: no CONTEXT.md")
        return
    text = ctx.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        if section not in text:
            fail(f"{name}: CONTEXT.md missing '{section}'")
        else:
            ok(f"{name}: has {section.strip()}")
    if len(text.splitlines()) > 80:
        fail(f"{name}: CONTEXT.md exceeds 80 lines ({len(text.splitlines())})")
    else:
        ok(f"{name}: CONTEXT.md line count OK")


def validate_stages(stages_root: Path, label_prefix: str = "") -> None:
    if not stages_root.is_dir():
        fail(f"Missing: {stages_root.relative_to(ROOT)}")
        return
    stages = sorted(p for p in stages_root.iterdir() if p.is_dir())
    if not stages:
        fail(f"No stages under {stages_root.relative_to(ROOT)}")
        return
    ok(f"{stages_root.relative_to(ROOT)}: {len(stages)} stage(s)")
    prev_num: int | None = None
    for stage in stages:
        if not STAGE_DIR_RE.match(stage.name):
            fail(f"Bad stage folder name: {stage.name}")
            continue
        num = int(stage.name[:2])
        if prev_num is not None and num <= prev_num:
            fail(f"Stage order not increasing: {stage.name}")
        prev_num = num
        check_exists(stage / "references", f"{stage.name}/references/")
        check_exists(stage / "output", f"{stage.name}/output/")
        check_stage_contract(stage, label_prefix)
    for stage in stages:
        if stage.name.startswith("01_"):
            continue
        ctx = (stage / "CONTEXT.md").read_text(encoding="utf-8")
        if "output/" not in ctx and "../" not in ctx:
            rel = stages_root.relative_to(ROOT)
            fail(f"{rel}/{stage.name}: Inputs should reference prior stage paths")


def validate_folio_migrations(product_path: Path) -> None:
    """README requirement: feature schema via migrations/, not schema.sql."""
    prefix = "folio migrations"
    schema_path = product_path / "schema.sql"
    if not schema_path.is_file():
        fail(f"{prefix}: missing schema.sql")
        return
    schema_text = schema_path.read_text(encoding="utf-8").lower()
    for col in ("public_id", "published_at"):
        if col in schema_text:
            fail(f"{prefix}: schema.sql must not define {col} (use migrations/)")
        else:
            ok(f"{prefix}: schema.sql omits {col}")

    migrate_py = product_path / "lib" / "migrate.php"
    check_exists(migrate_py, f"{prefix}: lib/migrate.php")
    seed = product_path / "seed.php"
    if seed.is_file():
        seed_text = seed.read_text(encoding="utf-8")
        if "run_migrations" not in seed_text:
            fail(f"{prefix}: seed.php must call run_migrations()")
        else:
            ok(f"{prefix}: seed.php calls run_migrations()")
        if "schema.sql" not in seed_text:
            fail(f"{prefix}: seed.php must load schema.sql before migrations")
        else:
            ok(f"{prefix}: seed.php loads schema.sql")

    mig_dir = product_path / "migrations"
    sql_files = sorted(mig_dir.glob("*.sql")) if mig_dir.is_dir() else []
    if len(sql_files) < 2:
        fail(f"{prefix}: expected at least 2 migrations/*.sql files")
    else:
        ok(f"{prefix}: {len(sql_files)} migration file(s)")
    for required, needle in (
        ("001_add_public_id.sql", "public_id"),
        ("002_add_published_at.sql", "published_at"),
    ):
        path = mig_dir / required
        if not path.is_file():
            fail(f"{prefix}: missing {required}")
            continue
        body = path.read_text(encoding="utf-8").lower()
        if "alter table" not in body or needle not in body:
            fail(f"{prefix}: {required} should ALTER TABLE documents ADD {needle}")
        else:
            ok(f"{prefix}: {required} alters documents.{needle}")

    readme = product_path / "README.md"
    if readme.is_file():
        readme_text = readme.read_text(encoding="utf-8")
        if "Schema migrations (implemented" not in readme_text:
            fail(f"{prefix}: README should document migration implementation")
        else:
            ok(f"{prefix}: README documents migration approach")


def validate_product(product_path: Path) -> None:
    name = product_path.name
    print(f"\n--- Product: {name} ---")
    check_exists(product_path / "CONTEXT.md", f"{name}: CONTEXT.md")
    check_exists(product_path / "CLAUDE.md", f"{name}: CLAUDE.md")
    check_exists(product_path / "_config" / "conventions.md", f"{name}: _config/conventions.md")
    validate_stages(product_path / "stages", f"{name}/")
    if name == "folio-takehome":
        validate_folio_migrations(product_path)


def validate_hub() -> None:
    print(f"ICM hub validation: {ROOT}\n")
    print("--- Hub ---")
    check_exists(ROOT / "CLAUDE.md", "Layer 0: CLAUDE.md")
    check_exists(ROOT / "CONTEXT.md", "Layer 1: CONTEXT.md")
    check_exists(ROOT / "_config" / "conventions.md", "Layer 3: _config/conventions.md")
    check_exists(ROOT / "shared" / "contracts", "Layer 3: shared/contracts/")
    check_exists(ROOT / "skills", "Layer 3: skills/")
    check_exists(ROOT / "integration" / "CONTEXT.md", "integration/CONTEXT.md")
    check_exists(ROOT / "setup" / "questionnaire.md", "setup/questionnaire.md")

    hub_context = (ROOT / "CONTEXT.md").read_text(encoding="utf-8")
    if "products/" not in hub_context:
        fail("Hub CONTEXT.md should reference products/")
    else:
        ok("Hub CONTEXT.md routes to products/")

    products_root = ROOT / "products"
    if not products_root.is_dir():
        fail("Missing: products/")
        return
    products = sorted(p for p in products_root.iterdir() if p.is_dir())
    if not products:
        fail("No products under products/")
        return
    ok(f"Found {len(products)} product(s)")
    for product in products:
        validate_product(product)

    if (ROOT / "stages").exists():
        fail("Legacy hub stages/ should be removed (stages live under products/*/stages/)")


def print_summary() -> None:
    print()
    if errors:
        print(f"FAILED — {len(errors)} issue(s)")
        for e in errors:
            print(f"  - {e}")
    else:
        print("PASSED — ICM portfolio hub structure is valid")


def main() -> int:
    validate_hub()
    print_summary()
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
