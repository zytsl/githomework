"""单位换算核心逻辑 / Core conversion logic.

支持三类换算 / Three kinds of conversion:
  length (长度), mass (质量), temp (温度)

设计说明 / Design notes:
  长度与质量是线性换算，用「基准单位乘数」描述：
      value_in_base = value * factor
  温度是非线性换算，单独用函数描述。
"""

from __future__ import annotations

# 每个单位 -> 相对基准单位的乘数
#   length 基准: m ; mass 基准: g
FACTORS: dict[str, dict[str, float]] = {
    "length": {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "in": 0.0254,
        "ft": 0.3048,
        "mi": 1609.344,
    },
    "mass": {
        "mg": 0.001,
        "g": 1.0,
        "kg": 1000.0,
        "t": 1_000_000.0,
        "lb": 453.59237,
        "oz": 28.349523125,
    },
}


class ConversionError(ValueError):
    """换算参数不合法时抛出 / Raised for invalid conversion requests."""


def units_of(kind: str) -> list[str]:
    """返回某一类换算支持的全部单位 / List units supported by a kind."""
    if kind == "temp":
        return ["c", "f", "k"]
    if kind not in FACTORS:
        raise ConversionError(f"未知的换算类别 / unknown kind: {kind!r}")
    return list(FACTORS[kind])


def _convert_temp(value: float, src: str, dst: str) -> float:
    # 先统一转成摄氏度，再转成目标单位
    if src == "c":
        celsius = value
    elif src == "f":
        celsius = (value - 32.0) * 5.0 / 9.0
    elif src == "k":
        celsius = value - 273.15
    else:
        raise ConversionError(f"温度不支持的单位 / unknown temperature unit: {src!r}")

    if dst == "c":
        return celsius
    if dst == "f":
        return celsius * 9.0 / 5.0 + 32.0
    if dst == "k":
        return celsius + 273.15
    raise ConversionError(f"温度不支持的单位 / unknown temperature unit: {dst!r}")


def convert(value: float, src: str, dst: str) -> float:
    """把 value 从 src 单位换算成 dst 单位 / Convert value from src to dst.

    >>> convert(1, "km", "m")
    1000.0
    >>> round(convert(100, "c", "f"), 4)
    212.0
    """
    src = src.strip().lower()
    dst = dst.strip().lower()

    if src == dst:
        return float(value)

    if src in ("c", "f", "k") or dst in ("c", "f", "k"):
        if src in ("c", "f", "k") and dst in ("c", "f", "k"):
            return _convert_temp(float(value), src, dst)
        raise ConversionError(
            f"不能跨类别换算 / cannot convert across kinds: {src!r} -> {dst!r}"
        )

    for kind, table in FACTORS.items():
        if src in table and dst in table:
            return float(value) * table[src] / table[dst]

    raise ConversionError(
        f"无法换算 / cannot convert {src!r} -> {dst!r}；"
        f"支持的单位见 / supported units: {units_of('length') + units_of('mass') + units_of('temp')}"
    )
