"""converter.py 的单元测试 / Unit tests.

两种运行方式都可以 / Runnable both ways:
    python tests/test_converter.py
    python -m pytest -q
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from src.converter import ConversionError, convert  # noqa: E402

TOL = 1e-9


def approx(actual: float, expected: float, tol: float = TOL) -> None:
    assert abs(actual - expected) <= tol, f"expected {expected}, got {actual}"


def test_length() -> None:
    approx(convert(1, "km", "m"), 1000.0)
    approx(convert(2500, "m", "km"), 2.5)
    approx(convert(1, "in", "cm"), 2.54)
    approx(convert(1, "mi", "km"), 1.609344)
    approx(convert(1, "yd", "m"), 0.9144)
    approx(convert(1760, "yd", "mi"), 1.0)
    approx(convert(1, "nmi", "m"), 1852.0)
    approx(convert(1_000_000, "um", "m"), 1.0)


def test_mass() -> None:
    approx(convert(1, "kg", "g"), 1000.0)
    approx(convert(1, "lb", "g"), 453.59237)
    approx(convert(16, "oz", "lb"), 1.0, tol=1e-9)
    approx(convert(1, "st", "lb"), 14.0)


def test_volume() -> None:
    approx(convert(1, "l", "ml"), 1000.0)
    approx(convert(1, "m3", "l"), 1000.0)
    approx(convert(1, "gal", "l"), 3.785411784)


def test_temperature() -> None:
    approx(convert(100, "c", "f"), 212.0, tol=1e-9)
    approx(convert(32, "f", "c"), 0.0, tol=1e-9)
    approx(convert(0, "c", "k"), 273.15, tol=1e-9)


def test_identity() -> None:
    approx(convert(42, "km", "km"), 42.0)


def test_invalid_input() -> None:
    for args in (("km", "c"), ("km", "nope")):
        try:
            convert(1, *args)
        except ConversionError:
            pass
        else:
            raise AssertionError(f"should have raised for {args}")


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for test in tests:
        test()
        print(f"ok  {test.__name__}")
    print(f"\n{len(tests)} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
