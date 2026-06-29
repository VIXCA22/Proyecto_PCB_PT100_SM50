from __future__ import annotations

import csv
import html
import shutil
import subprocess
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

    xs = [x for item in series for x, _ in item[1]]
    ys = [y for item in series for _, y in item[1]]
    x_min = min(xs) if x_min is None else x_min
    x_max = max(xs) if x_max is None else x_max
    auto_y_min = y_min is None
    auto_y_max = y_max is None
    y_min = min(ys) if auto_y_min else y_min
    y_max = max(ys) if auto_y_max else y_max
    if y_min == y_max:
        y_min -= 1
        y_max += 1
    y_pad = (y_max - y_min) * 0.08
    if auto_y_min:
        y_min -= y_pad
    if auto_y_max:
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

    for item in series:
        label, pts, color = item[:3]
        dash = item[3] if len(item) > 3 else ""
        points = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in pts)
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        lines.append(f'<polyline fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"{dash_attr} points="{points}"/>')
        for x, y in pts:
            lines.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="4.5" fill="{color}" stroke="#ffffff" stroke-width="2"/>')

    legend_x = width - right + 35
    legend_y = top + 12
    for idx, item in enumerate(series):
        label, _, color = item[:3]
        dash = item[3] if len(item) > 3 else ""
        y = legend_y + idx * 34
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        lines.append(f'<line x1="{legend_x}" y1="{y}" x2="{legend_x + 34}" y2="{y}" stroke="{color}" stroke-width="4" stroke-linecap="round"{dash_attr}/>')
        lines.append(f'<text x="{legend_x + 46}" y="{y + 6}" font-family="Arial, sans-serif" font-size="17" fill="#243b53">{html.escape(label)}</text>')

    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def add_svg_text(
    lines: list[str],
    text_lines: list[str],
    x: float,
    y: float,
    *,
    font_size: int,
    fill: str,
    weight: str = "400",
    anchor: str = "middle",
    line_height: int | None = None,
) -> None:
    if not text_lines:
        return
    line_height = line_height or int(font_size * 1.25)
    start_y = y - ((len(text_lines) - 1) * line_height) / 2
    weight_attr = f' font-weight="{weight}"' if weight != "400" else ""
    for idx, text in enumerate(text_lines):
        lines.append(
            f'<text x="{x:.1f}" y="{start_y + idx * line_height:.1f}" '
            f'text-anchor="{anchor}" font-family="Arial, sans-serif" '
            f'font-size="{font_size}"{weight_attr} fill="{fill}">{html.escape(text)}</text>'
        )


def add_block_box(
    lines: list[str],
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    stroke: str,
    fill: str,
    text_lines: list[str],
) -> None:
    lines.append(
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    )
    add_svg_text(lines, text_lines, x + w / 2, y + h / 2 + 5, font_size=14, fill="#111827", weight="700")


def add_arrow(lines: list[str], x1: float, y: float, x2: float, color: str) -> None:
    lines.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2 - 9:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="3"/>')
    lines.append(
        f'<polygon points="{x2 - 9:.1f},{y - 7:.1f} {x2:.1f},{y:.1f} {x2 - 9:.1f},{y + 7:.1f}" fill="{color}"/>'
    )


def build_block_diagram() -> list[Path]:
    out_path = FIG_DIR / "diagrama_bloques_valores_actuales.svg"
    width, height = 1280, 720
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
    ]

    add_svg_text(
        lines,
        ["Diagrama final - PCB de acondicionamiento de senal"],
        640,
        48,
        font_size=32,
        fill="#102a43",
        weight="700",
    )
    add_svg_text(
        lines,
        ["Valores actuales: PT100 Iexc = 0.5 mA, Rg = 1 kOhm; SM-50 Vexc = 10 V, Rg = 340 Ohm (160 + 180); FTP Cat5 / 8P8C"],
        640,
        78,
        font_size=17,
        fill="#334155",
    )

    rows = [
        {
            "title": "Canales de temperatura: 3x PT100, 3 hilos",
            "color": "#2563eb",
            "fill": "#eff6ff",
            "y": 118,
            "boxes": [
                ["PT100", "3 hilos"],
                ["Proteccion", "EMI/ESD"],
                ["Fuente", "Iexc=0.5 mA"],
                ["Offset desde", "B-Box / ref", "50 mV"],
                ["INA826/828", "Rg=1 kOhm", "G~50.4"],
                ["Filtro LP", "fc=159 Hz"],
                ["Ajuste nivel", "/salida"],
            ],
            "note": "Salida util PT100: 0 a 0.97 V despues de compensar offset; resolucion estimada 0.031 degC/LSB.",
        },
        {
            "title": "Canal de fuerza / torque: SM-50",
            "color": "#f97316",
            "fill": "#fff7ed",
            "y": 288,
            "boxes": [
                ["SM-50", "puente 350 Ohm"],
                ["Excitacion", "puente 10 V"],
                ["Proteccion", "entrada + filtro"],
                ["INA826/828", "Rg=340 Ohm", "G~146.3"],
                ["Filtro LP", "fc=482 Hz"],
                ["Ajuste nivel", "/salida"],
                ["Salida", "0-5 V aprox."],
            ],
            "note": "SM-50: 3 mV/V x 10 V = 30 mV FS; salida INA826 FS = 4.39 V con Rg=340 Ohm (160+180).",
        },
        {
            "title": "Alimentacion, enlace fisico y adquisicion",
            "color": "#16a34a",
            "fill": "#f0fdf4",
            "y": 460,
            "boxes": [
                ["BoomBox / B-Box", "+/-15 V", "100 mA max"],
                ["FTP Cat5", "8P8C blindado"],
                ["TVS + PPTC", "desacoplo"],
                ["Regulacion", "y referencias"],
                ["Distribucion a", "canales"],
                ["Entrada B-Box", "3 kOhm diff", "ADC 16 bits"],
            ],
            "note": "",
        },
    ]

    start_x = 70
    box_w = 118
    box_h = 62
    gap = 23
    for row in rows:
        y = float(row["y"])
        color = str(row["color"])
        add_svg_text(lines, [str(row["title"])], start_x, y - 18, font_size=18, fill=color, weight="700", anchor="start")
        for idx, text_lines in enumerate(row["boxes"]):
            x = start_x + idx * (box_w + gap)
            add_block_box(lines, x, y, box_w, box_h, stroke=color, fill=str(row["fill"]), text_lines=list(text_lines))
            if idx < len(row["boxes"]) - 1:
                add_arrow(lines, x + box_w, y + box_h / 2, x + box_w + gap - 4, color)
        if row["note"]:
            add_svg_text(lines, [str(row["note"])], start_x, y + box_h + 28, font_size=12, fill="#475569", anchor="start")

    footer_y = 622
    lines.append(
        f'<rect x="70" y="{footer_y}" width="1140" height="78" rx="8" fill="#f8fafc" stroke="#64748b" stroke-width="1.5"/>'
    )
    add_svg_text(
        lines,
        ["Pinout 8P8C por canal analogico: 1-2 = +15 V | 3 y 6 = 0 V/GND | 4 = OUT+/ADC+ | 5 = OUT-/ADC- | 7-8 = -15 V"],
        84,
        footer_y + 26,
        font_size=13,
        fill="#334155",
        weight="700",
        anchor="start",
    )
    add_svg_text(
        lines,
        ["Nota: valores finales SM-50 con Rg=340 Ohm (160+180), salida 0-5 V aprox.; memorias viejas quedan como trazabilidad."],
        84,
        footer_y + 54,
        font_size=13,
        fill="#334155",
        anchor="start",
    )

    lines.append("</svg>")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return [out_path]


def build_response_charts() -> list[Path]:
    pt100 = read_csv(SIM_DIR / "pt100_sweep_ng_20260625.csv")
    sm50 = read_csv(SIM_DIR / "sm50_sweep_positive_ng_20260625.csv")
    generated: list[Path] = []

    pt100_res_path = FIG_DIR / "pt100_resistencia.svg"
    pt100_res_series = [
        (
            "Valor nominal",
            [(float(row["TempC"]), float(row["R_PT100_NOM_OHM"])) for row in pt100],
            "#2563eb",
        ),
        (
            "Temperatura baja",
            [(float(row["TempC"]), float(row["R_PT100_LOW_OHM"])) for row in pt100],
            "#dc2626",
            "9 8",
        ),
        (
            "Temperatura alta",
            [(float(row["TempC"]), float(row["R_PT100_HIGH_OHM"])) for row in pt100],
            "#92400e",
            "9 8",
        ),
    ]
    svg_line_chart(
        pt100_res_path,
        "Variacion de resistencia del sensor PT100",
        "Temperatura nominal, T (C)",
        "Resistencia del PT100 (ohm)",
        pt100_res_series,
        x_min=0,
        x_max=100,
        y_min=95,
        y_max=142,
    )
    generated.append(pt100_res_path)

    pt100_out_path = FIG_DIR / "respuesta_pt100.svg"
    pt100_out_series = [
        (
            "Salida PT100 a B-Box",
            [(float(row["TempC"]), float(row["VOUT_PT100_BBOX_V"])) for row in pt100],
            "#2563eb",
        ),
        (
            "Salida filtrada",
            [(float(row["TempC"]), float(row["VOUT_PT100_FILT_V"])) for row in pt100],
            "#dc2626",
            "9 8",
        ),
    ]
    svg_line_chart(
        pt100_out_path,
        "Tension acondicionada del canal PT100",
        "Temperatura nominal, T (C)",
        "Tension electrica de salida (V)",
        pt100_out_series,
        x_min=0,
        x_max=100,
        y_min=2.2,
        y_max=3.4,
    )
    generated.append(pt100_out_path)

    sm50_bridge_path = FIG_DIR / "sm50_puente.svg"
    sm50_bridge_series = [
        (
            "VSEN+ - VSEN-",
            [(float(row["Load_lb"]), float(row["VBRIDGE_SM50_mV"])) for row in sm50],
            "#2563eb",
        )
    ]
    svg_line_chart(
        sm50_bridge_path,
        "Senal diferencial del puente SM-50",
        "Carga aplicada (lb)",
        "Tension diferencial del puente (mV)",
        sm50_bridge_series,
        x_min=0,
        x_max=50,
        y_min=0,
        y_max=32,
    )
    generated.append(sm50_bridge_path)

    sm50_out_path = FIG_DIR / "respuesta_sm50.svg"
    sm50_series = [
        (
            "Salida real hacia B-Box",
            [(float(row["Load_lb"]), float(row["VOUT_SM50_BBOX_V"])) for row in sm50],
            "#2563eb",
        ),
        (
            "Salida ideal",
            [(float(row["Load_lb"]), float(row["VOUT_SM50_IDEAL_V"])) for row in sm50],
            "#dc2626",
            "9 8",
        ),
        (
            "Referencia de 5 V",
            [(float(row["Load_lb"]), float(row["V_LIMIT_V"])) for row in sm50],
            "#92400e",
            "3 7",
        ),
    ]
    svg_line_chart(
        sm50_out_path,
        "Respuesta acondicionada del canal SM-50",
        "Carga aplicada (lb)",
        "Tension electrica de salida (V)",
        sm50_series,
        x_min=0,
        x_max=50,
        y_min=0,
        y_max=5,
    )
    generated.append(sm50_out_path)
    return generated


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


def render_asc_svg(src: Path, out: Path, title: str) -> bool:
    wires, flags, symbols = parse_asc(src)
    xs = [x for wire in wires for x in (wire[0], wire[2])] + [x for x, _, _ in flags] + [int(s["x"]) for s in symbols]
    ys = [y for wire in wires for y in (wire[1], wire[3])] + [y for _, y, _ in flags] + [int(s["y"]) for s in symbols]
    if not xs or not ys:
        print(f"Saltando {src}: no contiene elementos renderizables.")
        return False
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
    return True


def build_ltspice_previews() -> list[Path]:
    generated: list[Path] = []
    pt100_out = FIG_DIR / "ltspice_pt100_esquematico.svg"
    if render_asc_svg(
        ROOT / "ProyectoPCB_LTspice_PT100_SM50" / "01_SENSOR_PT100" / "Sensor_PT100.asc",
        pt100_out,
        "LTspice - canal PT100",
    ):
        generated.append(pt100_out)
    sm50_out = FIG_DIR / "ltspice_sm50_esquematico.svg"
    if render_asc_svg(
        ROOT / "ProyectoPCB_LTspice_PT100_SM50" / "02_SENSOR_SM50" / "sensor_SM50.asc",
        sm50_out,
        "LTspice - canal SM-50",
    ):
        generated.append(sm50_out)
    return generated


def export_pngs(svg_paths: list[Path]) -> None:
    inkscape = shutil.which("inkscape") or shutil.which("inkscape.com")
    if inkscape is None:
        print("Inkscape no esta disponible; se conservaron solo los SVG.")
        return

    for svg_path in svg_paths:
        png_path = svg_path.with_suffix(".png")
        subprocess.run(
            [
                inkscape,
                str(svg_path),
                "--export-type=png",
                f"--export-filename={png_path}",
            ],
            check=True,
        )


def copy_ltspice_pdf_previews() -> None:
    pdftoppm = shutil.which("pdftoppm")
    previews = [
        (
            ROOT / "ProyectoPCB_LTspice_PT100_SM50" / "01_SENSOR_PT100" / "escPT100.pdf",
            FIG_DIR / "ltspice_pt100_esquematico.pdf",
        ),
        (
            ROOT / "ProyectoPCB_LTspice_PT100_SM50" / "02_SENSOR_SM50" / "escSM50.pdf",
            FIG_DIR / "ltspice_sm50_esquematico.pdf",
        ),
    ]
    for src, dst in previews:
        if not src.exists():
            continue
        shutil.copy2(src, dst)
        if pdftoppm is None:
            print(f"pdftoppm no esta disponible; no se genero PNG desde {dst.name}.")
            continue
        subprocess.run(
            [
                pdftoppm,
                "-f",
                "1",
                "-l",
                "1",
                "-singlefile",
                "-png",
                "-r",
                "160",
                str(dst),
                str(dst.with_suffix("")),
            ],
            check=True,
        )


def main() -> None:
    ensure_dirs()
    generated = []
    generated.extend(build_block_diagram())
    generated.extend(build_response_charts())
    generated.extend(build_ltspice_previews())
    export_pngs(generated)
    copy_ltspice_pdf_previews()


if __name__ == "__main__":
    main()
