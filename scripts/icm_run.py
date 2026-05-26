#!/usr/bin/env python3
"""
Run a command from the ICM hub with pre/post validation and append-only logging.

Usage:
  icm_run.py validate
  icm_run.py exec [--product NAME] -- COMMAND [ARGS...]
  icm_run.py git [--product NAME] -- GIT_ARGS...

Logs: logs/hub.log (product, command, exit code, validate, git summary)
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
LOG_FILE = LOG_DIR / "hub.log"
VALIDATOR = ROOT / "scripts" / "validate_icm.py"


def log_line(text: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {text}\n")
    print(text)


def run_validate() -> int:
    if not VALIDATOR.is_file():
        log_line("VALIDATE skip (no validate_icm.py)")
        return 0
    proc = subprocess.run([sys.executable, str(VALIDATOR)], cwd=ROOT, capture_output=True, text=True)
    for line in proc.stdout.splitlines():
        log_line(f"VALIDATE | {line}")
    if proc.stderr:
        for line in proc.stderr.splitlines():
            log_line(f"VALIDATE stderr | {line}")
    status = "PASS" if proc.returncode == 0 else "FAIL"
    log_line(f"VALIDATE result={status} exit={proc.returncode}")
    return proc.returncode


def git_summary(cwd: Path) -> str:
    parts = []
    for args, label in (
        (["git", "status", "--short"], "status"),
        (["git", "diff", "--stat"], "diff-stat"),
        (["git", "log", "-1", "--oneline"], "last-commit"),
    ):
        proc = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
        if proc.returncode == 0 and proc.stdout.strip():
            parts.append(f"{label}:\n{proc.stdout.strip()}")
    return "\n".join(parts) if parts else "(no git changes)"


def run_command(cmd: list[str], product: str | None, label: str) -> int:
    product_s = product or "(hub)"
    log_line(f"--- {label} product={product_s} cmd={' '.join(cmd)} ---")

    pre = run_validate()
    if pre != 0:
        log_line(f"ABORT {label}: pre-validation failed")
        return pre

    run_cwd = ROOT
    if product and product not in ("hub", "(hub)"):
        run_cwd = ROOT / "products" / product
        if not run_cwd.is_dir():
            log_line(f"ABORT {label}: product path missing: {run_cwd}")
            return 1

    proc = subprocess.run(cmd, cwd=run_cwd)
    log_line(f"{label} exit={proc.returncode}")

    post = run_validate()
    if post != 0:
        log_line(f"WARN {label}: post-validation failed")

    summary = git_summary(ROOT)
    for line in summary.splitlines():
        log_line(f"GIT | {line}")

    return proc.returncode if proc.returncode != 0 else post


def main() -> int:
    parser = argparse.ArgumentParser(description="ICM hub command runner with logging")
    sub = parser.add_subparsers(dest="action", required=True)

    sub.add_parser("validate", help="Run validate_icm.py only")

    exec_p = sub.add_parser("exec", help="Run arbitrary command")
    exec_p.add_argument("--product", help="Product id under products/")
    exec_p.add_argument("command", nargs="+", help="Command and arguments")

    git_p = sub.add_parser("git", help="Run git in hub root")
    git_p.add_argument("--product", help="Product context for log")
    git_p.add_argument("command", nargs="+", help="git subcommand and arguments")

    args = parser.parse_args()

    if args.action == "validate":
        return run_validate()

    if not args.command:
        parser.error("command required")

    if args.action == "exec":
        return run_command(args.command, getattr(args, "product", None), "EXEC")

    if args.action == "git":
        return run_command(["git", *args.command], getattr(args, "product", None), "GIT")

    return 1


if __name__ == "__main__":
    sys.exit(main())
