"""MCP server exposing the interview guides in resources/ as tools.

Run it with:  python mcp/server.py   (speaks MCP over stdio)
"""
from __future__ import annotations

import sys
from pathlib import Path

from fastmcp import FastMCP

# Running this file as a script puts mcp/ on sys.path, not the project root,
# so add the root to be able to import the app package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.data import list_guide_names, load_guide  # noqa: E402

mcp = FastMCP("interview-guides")


@mcp.tool
def list_guides() -> list[str]:
    """List the available interview guide names."""
    return list_guide_names()


@mcp.tool
def get_guide(name: str) -> str:
    """Return the full markdown of one guide, e.g. 'ml-case-guide'."""
    try:
        return load_guide(name)
    except FileNotFoundError:
        available = ", ".join(list_guide_names())
        raise ValueError(f"Unknown guide '{name}'. Available guides: {available}") from None


if __name__ == "__main__":
    mcp.run()
