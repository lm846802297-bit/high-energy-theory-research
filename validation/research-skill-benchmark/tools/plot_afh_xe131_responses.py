#!/usr/bin/env python3
"""Create deterministic SVG views of the pinned native Xe-131 AFH response CSV.

This is a presentation-only transformation of already-computed nuclear response
data. It does not evaluate the AFH package or calculate a new nuclear response.
Only the Python standard library is required.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

EXPECTED_ROWS = 2401
EXPECTED_A = 131
EXPECTED_Q_MIN = 0.0
EXPECTED_Q_MAX = 0.6
IMAGINARY_TOLERANCE = 2.0e-12
DIAGONAL = [
    ("W_M00_AFH", "M"),
    ("W_SigmaDoublePrime00_AFH", "Sigma double-prime"),
    ("W_SigmaPrime00_AFH", "Sigma prime"),
    ("W_PhiPP00_AFH", "Phi double-prime"),
    ("W_PhiTildePrime00_AFH", "Phi tilde-prime"),
    ("W_Delta00_AFH", "Delta"),
]
INTERFERENCE = [
    ("W_MPhiPP00_AFH", "M-Phi double-prime"),
    ("W_SigmaPrimeDelta00_AFH", "Sigma-prime-Delta"),
]
COLORS = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf"]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_rows(path: Path, expected_rows: int = EXPECTED_ROWS) -> list[dict[str, float]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"A", "q_GeV", *(name for name, _ in DIAGONAL + INTERFERENCE)}
        required.update(
            "Im_" + name.removeprefix("W_")
            for name, _ in DIAGONAL + INTERFERENCE
        )
        missing = sorted(required.difference(reader.fieldnames or []))
        if missing:
            raise ValueError(f"CSV is missing required columns: {missing}")
        rows: list[dict[str, float]] = []
        for line_number, record in enumerate(reader, start=2):
            try:
                row = {key: float(value) for key, value in record.items() if key is not None}
            except (TypeError, ValueError) as exc:
                raise ValueError(f"non-numeric CSV value at line {line_number}") from exc
            if not all(math.isfinite(value) for value in row.values()):
                raise ValueError(f"non-finite CSV value at line {line_number}")
            if row["A"] != EXPECTED_A:
                raise ValueError(f"unexpected isotope A={row['A']} at line {line_number}")
            rows.append(row)
    if len(rows) != expected_rows:
        raise ValueError(f"expected {expected_rows} rows, found {len(rows)}")
    q_values = [row["q_GeV"] for row in rows]
    if abs(q_values[0] - EXPECTED_Q_MIN) > 1e-14:
        raise ValueError(f"unexpected minimum q: {q_values[0]}")
    if abs(q_values[-1] - EXPECTED_Q_MAX) > 1e-12:
        raise ValueError(f"unexpected maximum q: {q_values[-1]}")
    if any(right <= left for left, right in zip(q_values, q_values[1:])):
        raise ValueError("q_GeV must be strictly increasing")
    imaginary_columns = [
        "Im_" + name.removeprefix("W_")
        for name, _ in DIAGONAL + INTERFERENCE
    ]
    maximum_imaginary = max(abs(row[column]) for row in rows for column in imaginary_columns)
    if maximum_imaginary > IMAGINARY_TOLERANCE:
        raise ValueError(
            f"imaginary response residual {maximum_imaginary:.6g} exceeds "
            f"{IMAGINARY_TOLERANCE:.6g}"
        )
    for column, _ in DIAGONAL:
        if any(row[column] <= 0.0 for row in rows):
            raise ValueError(f"{column} must be positive for the logarithmic plot")
    return rows


def _text(x: float, y: float, value: str, *, size: int = 15, anchor: str = "middle", weight: str = "normal") -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">'
        f"{escape(value)}</text>"
    )


def _polyline(points: list[tuple[float, float]], color: str, width: float = 2.1) -> str:
    coords = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline fill="none" stroke="{color}" stroke-width="{width}" points="{coords}"/>'


def _base_svg(title: str, description: str, width: int = 1120, height: int = 720) -> list[str]:
    return [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f"<title>{escape(title)}</title>",
        f"<desc>{escape(description)}</desc>",
        '<rect width="100%" height="100%" fill="white"/>',
        _text(width / 2, 42, title, size=23, weight="bold"),
    ]


def _x_map(q: float, left: float, right: float) -> float:
    return left + (q - EXPECTED_Q_MIN) / (EXPECTED_Q_MAX - EXPECTED_Q_MIN) * (right - left)


def _x_axis(parts: list[str], left: float, right: float, y: float) -> None:
    for tick in range(7):
        q = tick / 10.0
        x = _x_map(q, left, right)
        parts.append(f'<line x1="{x:.2f}" y1="{y:.2f}" x2="{x:.2f}" y2="{y+6:.2f}" stroke="#222"/>')
        parts.append(_text(x, y + 27, f"{q:.1f}", size=13))
    parts.append(f'<line x1="{left:.2f}" y1="{y:.2f}" x2="{right:.2f}" y2="{y:.2f}" stroke="#222" stroke-width="1.3"/>')
    parts.append(_text((left + right) / 2, y + 62, "Momentum transfer q_A (GeV)", size=16))


def make_diagonal_svg(rows: list[dict[str, float]], csv_sha256: str) -> str:
    width, height = 1120, 720
    left, right, top, bottom = 105.0, 790.0, 105.0, 590.0
    all_values = [row[column] for row in rows for column, _ in DIAGONAL]
    low_exp = math.floor(math.log10(min(all_values)))
    high_exp = math.ceil(math.log10(max(all_values)))
    if low_exp == high_exp:
        high_exp += 1
    def y_map(value: float) -> float:
        return bottom - (math.log10(value) - low_exp) / (high_exp - low_exp) * (bottom - top)
    parts = _base_svg(
        "Native AFH v6.0 Xe-131 diagonal responses",
        "Six positive native AFH response functions versus spatial momentum transfer. The vertical axis is logarithmic.",
        width,
        height,
    )
    for exponent in range(low_exp, high_exp + 1):
        y = y_map(10.0 ** exponent)
        parts.append(f'<line x1="{left:.2f}" y1="{y:.2f}" x2="{right:.2f}" y2="{y:.2f}" stroke="#dddddd" stroke-width="1"/>')
        parts.append(_text(left - 12, y + 5, f"10^{exponent}", size=12, anchor="end"))
    parts.append(f'<line x1="{left:.2f}" y1="{top:.2f}" x2="{left:.2f}" y2="{bottom:.2f}" stroke="#222" stroke-width="1.3"/>')
    _x_axis(parts, left, right, bottom)
    parts.append(_text(34, (top + bottom) / 2, "Response W (raw AFH convention)", size=15))
    for index, (column, label) in enumerate(DIAGONAL):
        points = [(_x_map(row["q_GeV"], left, right), y_map(row[column])) for row in rows]
        parts.append(_polyline(points, COLORS[index]))
        y = 145 + index * 34
        parts.append(f'<line x1="830" y1="{y-5}" x2="870" y2="{y-5}" stroke="{COLORS[index]}" stroke-width="3"/>')
        parts.append(_text(882, y, label, size=14, anchor="start"))
    parts.append(_text(830, 390, "Normalization", size=15, anchor="start", weight="bold"))
    parts.append(_text(830, 416, "Raw Native AFH v6.0", size=13, anchor="start"))
    parts.append(_text(830, 438, "isoscalar columns", size=13, anchor="start"))
    parts.append(_text(830, 478, "No factor-four equal-p=n", size=13, anchor="start"))
    parts.append(_text(830, 500, "conversion is applied.", size=13, anchor="start"))
    parts.append(f'<metadata>source=lm846802297-bit/radiative-dark-matter-nuclear-currents; commit=9ed185aefe29cebbaaf575c5b2ae4b3fc16b0078; csv_sha256={csv_sha256}</metadata>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def _symlog(value: float, threshold: float) -> float:
    return math.copysign(math.log10(1.0 + abs(value) / threshold), value)


def _format_tick(value: float) -> str:
    if value == 0.0:
        return "0"
    return f"{value:.2g}"


def _interference_panel(
    rows: list[dict[str, float]],
    column: str,
    label: str,
    color: str,
    panel_top: float,
    panel_bottom: float,
) -> list[str]:
    left, right = 105.0, 790.0
    values = [row[column] for row in rows]
    maximum = max(abs(value) for value in values)
    threshold = maximum * 1.0e-3
    transformed = [_symlog(value, threshold) for value in values]
    low = min(transformed)
    high = max(transformed)
    padding = 0.08 * max(high - low, 1.0)
    low -= padding
    high += padding
    def y_map(value: float) -> float:
        return panel_bottom - (_symlog(value, threshold) - low) / (high - low) * (panel_bottom - panel_top)
    parts: list[str] = [_text(105, panel_top - 18, f"{label} (signed symlog; linear threshold={threshold:.3g})", size=15, anchor="start", weight="bold")]
    tick_values = [-maximum, -threshold, 0.0, threshold, maximum]
    for tick in tick_values:
        y = y_map(tick)
        parts.append(f'<line x1="{left:.2f}" y1="{y:.2f}" x2="{right:.2f}" y2="{y:.2f}" stroke="{("#999999" if tick == 0 else "#e3e3e3")}" stroke-width="{(1.4 if tick == 0 else 1)}"/>')
        parts.append(_text(left - 12, y + 4, _format_tick(tick), size=11, anchor="end"))
    points = [(_x_map(row["q_GeV"], left, right), y_map(row[column])) for row in rows]
    parts.append(_polyline(points, color, 2.0))
    parts.append(f'<line x1="{left:.2f}" y1="{panel_top:.2f}" x2="{left:.2f}" y2="{panel_bottom:.2f}" stroke="#222"/>')
    parts.append(f'<line x1="{left:.2f}" y1="{panel_bottom:.2f}" x2="{right:.2f}" y2="{panel_bottom:.2f}" stroke="#222"/>')
    return parts


def make_interference_svg(rows: list[dict[str, float]], csv_sha256: str) -> str:
    parts = _base_svg(
        "Native AFH v6.0 Xe-131 signed interference responses",
        "Two signed interference responses plotted separately with symmetric-log vertical axes to retain their signs and dynamic ranges.",
    )
    parts.extend(_interference_panel(rows, "W_MPhiPP00_AFH", "M-Phi double-prime interference", "#1f77b4", 115.0, 315.0))
    parts.extend(_interference_panel(rows, "W_SigmaPrimeDelta00_AFH", "Sigma-prime-Delta interference", "#d62728", 405.0, 605.0))
    _x_axis(parts, 105.0, 790.0, 605.0)
    parts.append(_text(830, 165, "Signed interference terms", size=15, anchor="start", weight="bold"))
    parts.append(_text(830, 194, "are retained without", size=13, anchor="start"))
    parts.append(_text(830, 216, "taking absolute values.", size=13, anchor="start"))
    parts.append(_text(830, 265, "Each panel uses its own", size=13, anchor="start"))
    parts.append(_text(830, 287, "symlog threshold.", size=13, anchor="start"))
    parts.append(f'<metadata>source=lm846802297-bit/radiative-dark-matter-nuclear-currents; commit=9ed185aefe29cebbaaf575c5b2ae4b3fc16b0078; csv_sha256={csv_sha256}</metadata>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def generate(csv_path: Path, output_dir: Path) -> dict[str, Any]:
    rows = load_rows(csv_path)
    csv_digest = sha256_file(csv_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "xe131_diagonal_responses.svg": make_diagonal_svg(rows, csv_digest),
        "xe131_signed_interferences.svg": make_interference_svg(rows, csv_digest),
    }
    output_records = []
    for name, svg in outputs.items():
        path = output_dir / name
        path.write_text(svg, encoding="utf-8", newline="\n")
        data = path.read_bytes()
        output_records.append({
            "path": name,
            "size_bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        })
    return {
        "status": "PASS",
        "isotope_A": EXPECTED_A,
        "row_count": len(rows),
        "q_min_GeV": rows[0]["q_GeV"],
        "q_max_GeV": rows[-1]["q_GeV"],
        "maximum_imaginary_residual": max(
            abs(row["Im_" + name.removeprefix("W_")])
            for row in rows
            for name, _ in DIAGONAL + INTERFERENCE
        ),
        "csv_sha256": csv_digest,
        "outputs": output_records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = generate(args.csv, args.out_dir)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
