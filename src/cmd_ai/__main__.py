from __future__ import annotations

import argparse
import sys

from cmd_ai.knowledge_base import OSName, ShellName, suggest_command


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cmd-ai",
        description="Convert a natural-language task into an OS/shell-specific command.",
    )

    parser.add_argument(
        "query",
        nargs="*",
        help="Natural-language request (e.g., 'list files in this folder').",
    )
    parser.add_argument(
        "--os",
        dest="os_name",
        choices=["Windows", "Linux"],
        default="Windows",
        help="Target OS.",
    )
    parser.add_argument(
        "--shell",
        choices=["PowerShell", "CMD", "Bash"],
        default="PowerShell",
        help="Target shell.",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.15,
        help="Minimum match score required to return a command.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    query = " ".join(args.query).strip()
    if not query:
        parser.print_help(sys.stderr)
        return 2

    os_name: OSName = args.os_name
    shell: ShellName = args.shell

    cmd = suggest_command(query, os_name=os_name, shell=shell, min_score=args.min_score)
    if cmd is None:
        print("No matching command found.", file=sys.stderr)
        return 1

    print(cmd)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
