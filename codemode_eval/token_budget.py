"""Token-budget analysis for code-orchestration vs schema-dump tool calling.

Quantifies the core Code Mode claim: describing tools as JSON schemas grows
linearly with tool count, while a single "write code" tool (plus on-demand
search/describe) is a near-constant baseline.
"""

from __future__ import annotations

import json
from typing import Any

CHARS_PER_TOKEN = 4
CODEMODE_FIXED_TOKENS = 1000  # search + execute constant baseline


def estimate_tokens(text: str) -> int:
    """Crude deterministic token estimate (~4 chars/token)."""
    return max(1, (len(text) + CHARS_PER_TOKEN - 1) // CHARS_PER_TOKEN)


def schema_dump_tokens(tools: list[dict[str, Any]]) -> int:
    """Token cost of dumping every tool's JSON schema into context."""
    return estimate_tokens(json.dumps(tools, sort_keys=True, separators=(",", ":")))


def codemode_tokens() -> int:
    """Token cost of the code-orchestration approach (fixed baseline)."""
    return CODEMODE_FIXED_TOKENS


def reduction_ratio(dump_tokens: int, code_tokens: int = CODEMODE_FIXED_TOKENS) -> float:
    """Fraction of tokens saved by code orchestration over schema dump."""
    if dump_tokens <= 0:
        return 0.0
    return (dump_tokens - code_tokens) / dump_tokens


def load_tools(path: str) -> list[dict[str, Any]]:
    """Load a list of tool descriptors from JSON (file or stdin '-')."""
    if path == "-":
        import sys
        return json.load(sys.stdin)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)
