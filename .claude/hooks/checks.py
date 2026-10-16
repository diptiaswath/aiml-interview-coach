"""PostToolUse hook: run ruff and mypy after Claude edits a file.

Exit code 2 shows stderr to Claude so the problem gets fixed; exit 0 means all clean.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
VENV_BIN = ROOT / ".venv" / "bin"

CHECKS = [
    ["ruff", "check", "app", "tests"],
    ["mypy", "app"],
]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    # Prefer the project's venv so the right tool versions are used.
    tool = VENV_BIN / cmd[0]
    if tool.exists():
        cmd = [str(tool), *cmd[1:]]
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def main() -> int:
    failures = []
    for cmd in CHECKS:
        result = run(cmd)
        if result.returncode != 0:
            failures.append(f"$ {' '.join(cmd)}\n{result.stdout}{result.stderr}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
