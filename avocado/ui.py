"""
Terminal UI Utilities (ANSI Colors & Theme-Adaptive Transparent Graphics Engine v1.8.0)
Features:
- Dynamic Theme Matching (Graphics tint to Avocado, Matrix, Dracula, Ocean, Amber themes)
- Resilient Height & Width Scaling (Fits small terminal windows without hiding text)
- Transparent background rendering
"""
import os
import sys
import re
from avocado.calendar_clock import get_calendar_lines, get_clock_info
from avocado.graphics import get_theme_colored_avocado

# ANSI Color Codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"

THEME_COLORS = {
    "avocado": {
        "primary": "\033[38;2;86;180;89m",     # Avocado Green (#56b459)
        "accent": "\033[38;2;163;209;107m",    # Light Lime (#a3d16b)
        "header": "\033[38;2;244;208;63m",     # Warm Yellow (#f4d03f)
        "text": "\033[38;2;230;237;243m",      # Off-white
        "muted": "\033[38;2;110;118;129m",     # Gray
        "border": "\033[38;2;50;80;50m"        # Dark Green Border
    },
    "matrix": {
        "primary": "\033[38;2;0;255;102m",
        "accent": "\033[38;2;51;255;153m",
        "header": "\033[38;2;153;255;187m",
        "text": "\033[38;2;204;255;221m",
        "muted": "\033[38;2;0;102;41m",
        "border": "\033[38;2;0;153;51m"
    },
    "dracula": {
        "primary": "\033[38;2;203;166;247m",
        "accent": "\033[38;2;245;194;231m",
        "header": "\033[38;2;137;180;250m",
        "text": "\033[38;2;205;214;244m",
        "muted": "\033[38;2;108;112;134m",
        "border": "\033[38;2;116;199;236m"
    },
    "ocean": {
        "primary": "\033[38;2;56;189;248m",
        "accent": "\033[38;2;125;211;252m",
        "header": "\033[38;2;129;140;248m",
        "text": "\033[38;2;224;242;254m",
        "muted": "\033[38;2;71;85;105m",
        "border": "\033[38;2;14;165;233m"
    },
    "amber": {
        "primary": "\033[38;2;255;176;0m",
        "accent": "\033[38;2;255;204;0m",
        "header": "\033[38;2;255;221;102m",
        "text": "\033[38;2;255;238;170m",
        "muted": "\033[38;2;153;106;0m",
        "border": "\033[38;2;204;140;0m"
    }
}

def get_theme(theme_name="avocado"):
    return THEME_COLORS.get(theme_name.lower(), THEME_COLORS["avocado"])

def clear_screen():
    print("\033[H\033[2J\033[3J", end="")

def make_progress_bar(pct, length=10, fill_char="█", empty_char="░"):
    filled = int(round(length * (pct / 100.0)))
    return fill_char * filled + empty_char * (length - filled)

def truncate_and_pad(text, width):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    plain = ansi_escape.sub('', text)

    if len(plain) > width:
        return plain[:max(1, width - 1)] + "…"
    else:
        pad_len = max(0, width - len(plain))
        return text + (' ' * pad_len)

def render_neofetch(colors, status=None):
    p = colors["primary"]
    a = colors["accent"]
    t = colors["text"]
    m = colors["muted"]
    r = RESET

    if not status:
        from avocado.status import get_macos_status
        status = get_macos_status()

    # Get theme-adaptive transparent graphics
    graphic_lines = get_theme_colored_avocado(colors, mode="normal")

    cpu_bar = make_progress_bar(status['cpu_usage'], 10)
    ram_bar = make_progress_bar(status['ram_pct'], 10)

    sys_info = [
        f"{BOLD}{p}user@macbook-pro{r}",
        f"{m}----------------{r}",
        f"{t}OS:{r}                {status['os']}",
        f"{t}Host:{r}              {status['model']}",
        f"{t}Kernel:{r}            {status['kernel']}",
        f"{t}GPU:{r}               {status['gpu']}",
        f"{t}CPU:{r}               {status['cpu_brand']}",
        f"{t}CPU Graph:{r}         [{a}{cpu_bar}{r}] {status['cpu_usage']}%",
        f"{t}RAM Graph:{r}         [{a}{ram_bar}{r}] {status['used_ram_gb']}/{status['total_ram_gb']}GB",
        f"{t}Battery:{r}           🔋 {status['batt_pct']}% ({status['power_source']})",
        f"{t}Network:{r}           {status['local_ip']} ({status['net_if']})",
        f"{t}Uptime:{r}            {status['uptime']}"
    ]

    out_lines = [f"\n{BOLD}{a}AVOCADO THEME-MATCHED ASCII HARDWARE SUMMARY{r}\n"]

    max_rows = max(len(graphic_lines), len(sys_info))
    for i in range(max_rows):
        art_l = graphic_lines[i] if i < len(graphic_lines) else " " * 36
        info_l = sys_info[i] if i < len(sys_info) else ""
        out_lines.append(f"  {art_l}   {info_l}")

    return "\n".join(out_lines) + "\n"

def render_dashboard(status, weather, config):
    colors = get_theme(config.get("theme", "avocado"))
    p = colors["primary"]
    a = colors["accent"]
    h = colors["header"]
    t = colors["text"]
    m = colors["muted"]
    b = colors["border"]
    r = RESET

    try:
        cols, rows = os.get_terminal_size()
    except Exception:
        cols, rows = 100, 28

    w = max(76, cols - 2)
    lines = []

    # Dynamic Height Cap so small windows never hide content off bottom
    max_visible_rows = max(6, min(rows - 9, 14))

    # Single-Panel Stacked Layout for small/narrow windows (cols < 95)
    if cols < 95:
        lines.append(f"{b}┌{'─' * (w - 2)}┐{r}")
        title_str = " [AVOCADO] MAC OS TERMINAL DASHBOARD "
        lines.append(f"{b}│{r} {a}.---.{r} {BOLD}{p}{title_str}{r}{' ' * max(0, w - 8 - len(title_str))}{b}│{r}")
        lines.append(f"{b}├{'─' * (w - 2)}┤{r}")

        lines.append(f"{b}│{r} {BOLD}{h}💻 HARDWARE TELEMETRY{r}{' ' * max(0, w - 23)}{b}│{r}")
        lines.append(f"{b}│{r}  " + truncate_and_pad(f"Model: {status['model']} | OS: {status['os']} | CPU: {status['cpu_brand']}", w - 5) + f" {b}│{r}")
        lines.append(f"{b}│{r}  " + truncate_and_pad(f"CPU: {status['cpu_usage']}% | RAM: {status['used_ram_gb']}/{status['total_ram_gb']}GB | Disk: {status['disk_avail']} Free", w - 5) + f" {b}│{r}")
        lines.append(f"{b}├{'─' * (w - 2)}┤{r}")

        lines.append(f"{b}│{r} {BOLD}{h}🌦 WEATHER ({weather.get('city', 'Location')}){r}{' ' * max(0, w - 15 - len(weather.get('city', 'Location')))}{b}│{r}")
        lines.append(f"{b}│{r}  " + truncate_and_pad(f"Temp: {weather.get('temp')} ({weather.get('desc')}) | Wind: {weather.get('wind')}", w - 5) + f" {b}│{r}")
        lines.append(f"{b}├{'─' * (w - 2)}┤{r}")

        clock_info = get_clock_info()
        lines.append(f"{b}│{r} {BOLD}{h}📅 CALENDAR ({clock_info['time']}){r}{' ' * max(0, w - 19 - len(clock_info['time']))}{b}│{r}")
        for cl in get_calendar_lines()[:min(5, max_visible_rows)]:
            lines.append(f"{b}│{r}  " + truncate_and_pad(cl, w - 5) + f" {b}│{r}")
        lines.append(f"{b}└{'─' * (w - 2)}┘{r}")
        return "\n".join(lines)

    # 3-Column Equal Split Layout for Wide Terminals (cols >= 95)
    col_w = max(28, (w - 6) // 3)
    total_inner_w = col_w * 3 + 4

    lines.append(f"{b}┌{'─' * (total_inner_w)}┐{r}")
    title_str = " [AVOCADO] MAC OS TERMINAL DASHBOARD & CONTROL CENTER "
    lines.append(f"{b}│{r} {a}.---.{r}  {BOLD}{p}{title_str}{r}{' ' * max(0, total_inner_w - 9 - len(title_str))}{b}│{r}")
    lines.append(f"{b}│{r} {p}( (O) ){r} {m}Theme-Matched Transparent Graphics | Responsive Height/Width Grid{r}{' ' * max(0, total_inner_w - 71)}{b}│{r}")
    lines.append(f"{b}├{'─' * col_w}┬{'─' * (col_w + 2)}┬{'─' * col_w}┤{r}")

    c1_h = truncate_and_pad(f"{BOLD}{h}💻 HARDWARE TELEMETRY{r}", col_w)
    c2_h = truncate_and_pad(f"{BOLD}{h}🌦 ASCII WEATHER{r}", col_w + 2)
    c3_h = truncate_and_pad(f"{BOLD}{h}📅 CALENDAR & 12H TIME{r}", col_w)

    lines.append(f"{b}│{r} {c1_h} {b}│{r} {c2_h} {b}│{r} {c3_h} {b}│{r}")
    lines.append(f"{b}├{'─' * col_w}┼{'─' * (col_w + 2)}┼{'─' * col_w}┤{r}")

    cpu_bar = make_progress_bar(status['cpu_usage'], 8)
    ram_bar = make_progress_bar(status['ram_pct'], 8)
    disk_bar = make_progress_bar(status['disk_pct'], 8)

    col1 = [
        f"{t}Model:{r} {status['model']}",
        f"{t}OS:{r} {status['os']}",
        f"{t}Kernel:{r} {status['kernel']}",
        f"{t}GPU:{r} {status['gpu']}",
        f"{t}CPU:{r} {status['cpu_brand']}",
        f"{t}CPU Load:{r} [{a}{cpu_bar}{r}] {status['cpu_usage']}%",
        f"{t}Load Avg:{r} {status['load_avg']}",
        f"{t}RAM:{r} [{a}{ram_bar}{r}] {status['used_ram_gb']}/{status['total_ram_gb']}G",
        f"{m}Free:{r} {status['free_ram_gb']}G | {m}Swap:{r} {status['swap_used']}",
        f"{t}Disk:{r} [{a}{disk_bar}{r}] {status['disk_avail']} Free",
        f"{t}Battery:{r} 🔋 {status['batt_pct']}% ({status['power_source'][:8]})",
        f"{t}IP:{r} {status['local_ip']}",
        f"{t}Uptime:{r} {status['uptime']}"
    ]

    art_lines = weather.get("art", [""])
    col2 = [
        f"{BOLD}{a}{weather.get('city', 'Location')}{r}",
        f"Temp: {BOLD}{weather.get('temp', '22°C')}{r} ({weather.get('desc', 'Clear')})",
        f"Wind: {weather.get('wind', '12 km/h')}",
        ""
    ]
    for art_l in art_lines:
        col2.append(f"{a}{art_l}{r}")

    col2.append("")
    col2.append(f"{BOLD}Forecast:{r}")
    for fc in weather.get("forecast", [])[:3]:
        col2.append(f" • {fc['day']}: {fc['high']} / {fc['low']}")

    clock_info = get_clock_info()
    cal_lines = get_calendar_lines()

    col3 = [
        f"{BOLD}{a}TIME: {clock_info['time']}{r}",
        f"{t}{clock_info['date']}{r}",
        f"{m}{clock_info['week']}{r}",
        ""
    ]
    for cl in cal_lines:
        col3.append(f"{t}{cl}{r}")

    # Dynamically cap rows based on terminal window height
    display_rows = min(max_visible_rows, max(len(col1), len(col2), len(col3)))

    for idx in range(display_rows):
        c1 = col1[idx] if idx < len(col1) else ""
        c2 = col2[idx] if idx < len(col2) else ""
        c3 = col3[idx] if idx < len(col3) else ""

        p_c1 = truncate_and_pad(c1, col_w)
        p_c2 = truncate_and_pad(c2, col_w + 2)
        p_c3 = truncate_and_pad(c3, col_w)

        lines.append(f"{b}│{r} {p_c1} {b}│{r} {p_c2} {b}│{r} {p_c3} {b}│{r}")

    lines.append(f"{b}└{'─' * col_w}┴{'─' * (col_w + 2)}┴{'─' * col_w}┘{r}")

    return "\n".join(lines)
