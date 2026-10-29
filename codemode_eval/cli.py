"""codemode-eval CLI: quantify code-orchestration token savings.

    python -m codemode_eval token-budget <tools.json>
"""

import argparse
import sys

from .token_budget import codemode_tokens, load_tools, reduction_ratio, schema_dump_tokens


def cmd_token_budget(args) -> int:
    tools = load_tools(args.tools)
    dump = schema_dump_tokens(tools)
    code = codemode_tokens()
    ratio = reduction_ratio(dump, code)
    print(f"tools={len(tools)} schema_dump_tokens={dump} codemode_tokens={code} reduction={ratio:.1%}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="codemode-eval", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("token-budget", help="compare schema-dump vs codemode token cost")
    b.add_argument("tools", help="JSON file of tool descriptors, or '-' for stdin")
    b.set_defaults(fn=cmd_token_budget)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
