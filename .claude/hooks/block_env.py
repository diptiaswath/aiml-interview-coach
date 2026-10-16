"""PreToolUse hook: block Claude from reading .env files (they hold secrets).

Claude Code sends the tool call as JSON on stdin. Exit code 2 blocks the call and
shows stderr to Claude; exit code 0 lets it through.
"""
from __future__ import annotations

import json
import sys


def main() -> int:
    event = json.load(sys.stdin)
    path = event.get("tool_input", {}).get("file_path", "")
    if ".env" in path and ".env.example" not in path:
        print(
            f"Blocked: reading '{path}' is not allowed because .env files hold secrets. "
            "Use .env.example to see which variables exist.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
