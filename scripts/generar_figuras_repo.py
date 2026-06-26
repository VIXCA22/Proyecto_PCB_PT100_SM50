from __future__ import annotations

import csv
import html
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "docs" / "figuras"
SIM_DIR = ROOT / "docs" / "simulacion"


def ensure_dirs() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    SIM_DIR.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def nice_num(value: float) -> str:
    if abs(value) >= 10:
        return f"{value:.0f}"
    if abs(value) >= 1:
        return f"{value:.1f}"
    return f"{value:.2f}"


def svg_line_chart(
    path: Path,
    title: str,
    x_label: str,
    y_label: str,
    series: list[tuple[str, list[tuple[float, float]], str]],
    x_min: float | None = None,
    x_max: float | None = None,
    y_min: float | None = None,
    y_max: float | None = None,
) -> None:
    width, height = 1280, 720
    left, right, top, bottom = 110, 360, 80, 95
    plot_w = width - left - right
    plot_h = height - top - bottom

    xs = [x for _, pts, _ in series for x, _ in pts]
    ys = [y for _, pts, _ in series for _, y in pts]
    x_min = min(xs) if x_min is None else x_min
    x_max = max(xs) if x_max is None else x_max
    y_min = min(ys) if y_min is None else y_min
    y_max = max(ys) if y_max is None else y_max
    if y_min == y_max:
        y_min -= 1
        y_max += 1
    y_pad = (y_max - y_min) * 0.08
    y_min -= y_pad
    y_max += y_pad

    def sx(x: float) -> float:
        return left + (x - x_min) / (x_max - x_min) * plot_w

    def sy(y: float) -> float:
        return top + (y_max - y) / (y_max - y_min) * plot_h

    lines: list[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">',
        '<rect width="1280" height="720" fill="#ffffff"/>',
        f'<text x="110" y="45" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="#1f2933">{html.escape(title)}</text>',
        f'<text x="{left + plot_w / 2:.1f}" y="685" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" fill="#243b53">{html.escape(x_label)}</text>',
        f'<text x="32" y="{top + plot_h / 2:.1f}" transform="rotate(-90 32 {top + plot_h / 2:.1f})" text-anchor="middle" font-family="Arial, sans-serif" font-size="20" fill="#243b53">{html.escape(y_label)}</text>',
        f'<rect x="{left}" y="{top}" width="{plot_w}" height="{plot_h}" fill="#f7fafc" stroke="#bcccdc" stroke-width="1"/>',
    ]

    for i in range(6):
        x = x_min + (x_max - x_min) * i / 5
        px = sx(x)
        lines.append(f'<line x1="{px:.1f}" y1="{top}" x2="{px:.1f}" y2="{top + plot_h}" stroke="#d9e2ec" stroke-width="1"/>')
        lines.append(f'<text x="{px:.1f}" y="{top + plot_h + 28}" text-anchor="middle" font-family="Arial, sans-serif" font-size="16" fill="#52606d">{nice_num(x)}</text>')
    for i in range(6):
        y = y_min + (y_max - y_min) * i / 5
        py = sy(y)
        lines.append(f'<line x1="{left}" y1="{py:.1f}" x2="{left + plot_w}" y2="{py:.1f}" stroke="#d9e2ec" stroke-width="1"/>')
        lines.append(f'<text x="{left - 14}" y="{py + 5:.1f}" text-anchor="end" font-family="Arial, sans-serif" font-size="16" fill="#52606d">{nice_num(y)}</text>')

    for label, pts, color in series:
        points = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in pts)
        lines.append(f'<polyline fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round" points="{points}"/>')
        for x, y in pts:
            lines.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="4.5" fill="{color}" stroke="#ffffff" stroke-width="2"/>')

    legend_x = width - right + 35
    legend_y = top + 12
    for idx, (label, _, color) in enumerate(series):
        y = legend_y + idx * 34
        lines.append(f'<line x1="{legend_x}" y1="{y}" x2="{legend_x + 34}" y2="{y}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>')
        lines.append(f'<text x="{legend_x + 46}" y="{y + 6}" font-family="Arial, sans-serif" font-size="17" fill="#243b53">{html.escape(label)}</text>')

    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def build_response_charts() -> None:
    pt100 = read_csv(SIM_DIR / "pt100_sweep_ng_20260625.csv")
    sm50 = read_csv(SIM_DIR / "sm50_sweep_positive_ng_20260625.csv")

    pt100_series = [
        (
            "Salida PT100 a B-Box",
            [(float(row["TempC"]), float(row["VOUT_PT100_BBOX_V"])) for row in pt100],
            "#2563eb",
        ),
        (
            "Entrada diferencial INA",
            [(float(row["TempC"]), float(row["VDIFF_INA_V"])) for row in pt100],
            "#16a34a",
        ),
    ]
    svg_line_chart(
        FIG_DIR / "respuesta_pt100.svg",
        "Respuesta simulada del canal PT100",
        "Temperatura del PT100 (C)",
        "Voltaje (V)",
        pt100_series,
    )

    grouped: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for row in sm50:
        rg = row["RG_ohm"]
        grouped[f"RG {rg} ohm"].append((float(row["LoadFrac"]) * 100.0, float(row["VOUT_SM50_BBOX_V"])))

    colors = ["#dc2626", "#7c3aed", "#0891b2", "#ea580c", "#15803d"]
    sm50_series = [(label, sorted(points), colors[i % len(colors)]) for i, (label, points) in enumerate(sorted(grouped.items()))]
    svg_line_chart(
        FIG_DIR / "respuesta_sm50.svg",
        "Respuesta simulada del canal SM-50",
        "Carga / torque relativo (%)",
        "Salida a B-Box (V)",
        sm50_series,
        x_min=0,
        x_max=100,
        y_min=0,
    )


def parse_asc(path: Path) -> tuple[list[tuple[int, int, int, int]], list[tuple[int, int, str]], list[dict[str, str]]]:
    wires: list[tuple[int, int, int, int]] = []
    flags: list[tuple[int, int, str]] = []
    symbols: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = raw.split()
        if not parts:
            continue
        if parts[0] == "WIRE" and len(parts) >= 5:
            wires.append(tuple(map(int, parts[1:5])))
        elif parts[0] == "FLAG" and len(parts) >= 4:
            flags.append((int(parts[1]), int(parts[2]), " ".join(parts[3:])))
        elif parts[0] == "SYMBOL" and len(parts) >= 5:
            current = {"kind": parts[1], "x": parts[2], "y": parts[3], "rot": parts[4], "inst": "", "value": ""}
            symbols.append(current)
        elif parts[0] == "SYMATTR" and current is not None and len(parts) >= 3:
            key = parts[1]
            value = " ".join(parts[2:])
            if key == "InstName":
                current["inst"] = value
            elif key == "Value":
                current["value"] = value
    return wires, flags, symbols


def render_asc_svg(src: Path, out: Path, title: str) -> None:
    wires, flags, symbols = parse_asc(src)
    xs = [x for wire in wires for x in (wire[0], wire[2])] + [x for x, _, _ in flags] + [int(s["x"]) for s in symbols]
    ys = [y for wire in wires for y in (wire[1], wire[3])] + [y for _, y, _ in flags] + [int(s["y"]) for s in symbols]
    min_x, max_x = min(xs) - 180, max(xs) + 260
    min_y, max_y = min(ys) - 220, max(ys) + 180
    width, height = max_x - min_x, max_y - min_y

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="900" viewBox="{min_x} {min_y} {width} {height}">',
        f'<rect x="{min_x}" y="{min_y}" width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{min_x + 24}" y="{min_y + 70}" font-family="Arial, sans-serif" font-size="64" font-weight="700" fill="#1f2933">{html.escape(title)}</text>',
        f'<text x="{min_x + 24}" y="{min_y + 120}" font-family="Arial, sans-serif" font-size="34" fill="#52606d">{html.escape(str(src.relative_to(ROOT)))}</text>',
    ]

    for x1, y1, x2, y2 in wires:
        lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#2f4f4f" stroke-width="10" stroke-linecap="round"/>')

    for sym in symbols:
        x, y = int(sym["x"]), int(sym["y"])
        kind = Path(sym["kind"]).name.lower()
        inst = sym.get("inst", "")
        value = sym.get("value", "")
        label = inst if not value else f"{inst}  {value}"
        if "res" in kind:
            body = [(x, y + 30), (x + 20, y + 5), (x + 45, y + 55), (x + 70, y + 5), (x + 95, y + 55), (x + 115, y + 30)]
            points = " ".join(f"{px},{py}" for px, py in body)
            lines.append(f'<polyline fill="none" stroke="#111827" stroke-width="8" points="{points}"/>')
        elif "cap" in kind:
            lines.append(f'<line x1="{x}" y1="{y}" x2="{x + 95}" y2="{y}" stroke="#111827" stroke-width="8"/>')
            lines.append(f'<line x1="{x + 35}" y1="{y - 45}" x2="{x + 35}" y2="{y + 45}" stroke="#111827" stroke-width="8"/>')
            lines.append(f'<line x1="{x + 60}" y1="{y - 45}" x2="{x + 60}" y2="{y + 45}" stroke="#111827" stroke-width="8"/>')
        elif "voltage" in kind:
            lines.append(f'<circle cx="{x + 35}" cy="{y + 35}" r="42" fill="#fef3c7" stroke="#111827" stroke-width="7"/>')
            lines.append(f'<text x="{x + 35}" y="{y + 47}" text-anchor="middle" font-family="Arial, sans-serif" font-size="42" fill="#111827">V</text>')
        else:
            lines.append(f'<rect x="{x - 8}" y="{y - 8}" width="150" height="82" rx="0" fill="#e0f2fe" stroke="#0f172a" stroke-width="6"/>')
            lines.append(f'<text x="{x + 67}" y="{y + 27}" text-anchor="middle" font-family="Arial, sans-serif" font-size="28" font-weight="700" fill="#0f172a">{html.escape(inst)}</text>')
            lines.append(f'<text x="{x + 67}" y="{y + 58}" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" fill="#334155">{html.escape(Path(sym["kind"]).name[:16])}</text>')
        if label:
            lines.append(f'<text x="{x}" y="{y - 22}" font-family="Arial, sans-serif" font-size="30" fill="#1f2933">{html.escape(label)}</text>')

    for x, y, label in flags:
        color = "#166534" if label not in {"0"} else "#475569"
        lines.append(f'<circle cx="{x}" cy="{y}" r="14" fill="{color}"/>')
        lines.append(f'<text x="{x + 24}" y="{y + 10}" font-family="Arial, sans-serif" font-size="30" fill="{color}">{html.escape(label)}</text>')

    lines.append("</svg>")
    out.write_text("\n".join(lines), encoding="utf-8")


def build_ltspice_previews() -> None:
    render_asc_svg(
        ROOT / "ProyectoPCB_LTspice_PT100_SM50" / "01_SENSOR_PT100" / "Sensor_PT100.asc",
        FIG_DIR / "ltspice_pt100_esquematico.svg",
        "LTspice - canal PT100",
    )
    render_asc_svg(
        ROOT / "ProyectoPCB_LTspice_PT100_SM50" / "02_SENSOR_SM50" / "sensor_SM50.asc",
        FIG_DIR / "ltspice_sm50_esquematico.svg",
        "LTspice - canal SM-50",
    )


def main() -> None:
    ensure_dirs()
    build_response_charts()
    build_ltspice_previews()


if __name__ == "__main__":
    main()
