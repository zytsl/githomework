"""命令行入口 / Command line entry point.

用法 / Usage:
    python -m src.cli 3 km mi
    python -m src.cli 100 c f
    python -m src.cli --list
"""

from __future__ import annotations

import argparse
import sys

from .converter import ConversionError, convert, units_of


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="convert",
        description="极简单位换算工具 / A tiny unit converter",
    )
    parser.add_argument("value", nargs="?", help="要换算的数值 / value to convert")
    parser.add_argument("src", nargs="?", help="原单位 / source unit")
    parser.add_argument("dst", nargs="?", help="目标单位 / target unit")
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出支持的单位 / list supported units",
    )
    return parser


def format_result(value: float, src: str, dst: str) -> str:
    """把换算结果格式化成一行文本 / Format one conversion result."""
    return f"{value} {src} = {convert(value, src, dst)} {dst}"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list:
        for kind in ("length", "mass", "temp"):
            print(f"{kind:6s}: {', '.join(units_of(kind))}")
        return 0

    if args.value is None or args.src is None or args.dst is None:
        parser.print_help()
        return 2

    try:
        value = float(args.value)
    except ValueError:
        print(f"错误 / error: 数值不合法 / not a number: {args.value!r}", file=sys.stderr)
        return 2

    try:
        print(format_result(value, args.src, args.dst))
    except ConversionError as exc:
        print(f"错误 / error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
