"""
Terminal UI Utilities (ANSI Colors & 3-Column Equal 1/3 Split Grid Layout)
Renders a clean 3-Column Dashboard: Left 1/3 (Hardware Stats), Middle 1/3 (ASCII Weather), Right 1/3 (Calendar & Clock).
"""
import os
import sys
from avocado.calendar_clock import get_calendar_lines, get_clock_info

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

def make_progress_bar(pct, length=12, fill_char="█", empty_char="░"):
    filled = int(round(length * (pct / 100.0)))
    return fill_char * filled + empty_char * (length - filled)

def pad_str(text, width):
    """Pads string with spaces to exact width while respecting ANSI color codes."""
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    plain = ansi_escape.sub('', text)
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

    art = f"""
{a}      ( \\              avocado-cli{r}        user@macbook-pro
{a}     /   \\             -----------{r}        ----------------
{p}    ( (O) )            {t}OS:{r}                {status['os']}
{p}     \\___/             {t}Host:{r}              {status['model']}
{p}                       {t}Kernel:{r}            {status['kernel']}
{m}                       {t}GPU:{r}               {status['gpu']}
{m}                       {t}Uptime:{r}            {status['uptime']}
{m}                       {t}Load Avg:{r}          {status['load_avg']}
{m}                       {t}CPU:{r}               {status['cpu_brand']} ({status['cpu_cores']} Cores)
{m}                       {t}Memory:{r}            {status['used_ram_gb']} GB / {status['total_ram_gb']} GB (Swap: {status['swap_used']})
{m}                       {t}Battery:{r}           🔋 {status['batt_pct']}% ({status['power_source']})
{m}                       {t}Network:{r}           {status['local_ip']} ({status['net_if']})
"""
    return art

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
        cols, rows = 115, 30

    w = max(100, cols - 2)
    # Calculate 1/3 column width
    col_w = max(30, (w - 6) // 3)
    total_inner_w = col_w * 3 + 4

    lines = []

    # 1. Header Box
    lines.append(f"{b}┌{'─' * (total_inner_w)}┐{r}")
    title_str = " [AVOCADO] MAC OS TERMINAL DASHBOARD "
    lines.append(f"{b}│{r} {a}( \\{r}  {BOLD}{p}{title_str}{r}{' ' * max(0, total_inner_w - 9 - len(title_str))}{b}│{r}")
    lines.append(f"{b}│{r} {p}( (O) ){r} {m}Native Hardware Telemetry & Interactive Control Center{r}{' ' * max(0, total_inner_w - 55)}{b}│{r}")
    lines.append(f"{b}├{'─' * col_w}┬{'─' * (col_w + 2)}┬{'─' * col_w}┤{r}")

    # Column Headers (1/3 Hardware, 1/3 Weather, 1/3 Calendar & Time)
    c1_h = pad_str(f"{BOLD}{h}💻 HARDWARE TELEMETRY{r}", col_w)
    c2_h = pad_str(f"{BOLD}{h}🌦 ASCII WEATHER{r}", col_w + 2)
    c3_h = pad_str(f"{BOLD}{h}📅 CALENDAR & 12H TIME{r}", col_w)

    lines.append(f"{b}│{r} {c1_h} {b}│{r} {c2_h} {b}│{r} {c3_h} {b}│{r}")
    lines.append(f"{b}├{'─' * col_w}┼{'─' * (col_w + 2)}┼{'─' * col_w}┤{r}")

    # 2. Build Column Content Lists
    # Column 1 (Hardware Telemetry)
    cpu_bar = make_progress_bar(status['cpu_usage'], 10)
    ram_bar = make_progress_bar(status['ram_pct'], 10)
    disk_bar = make_progress_bar(status['disk_pct'], 10)

    col1 = [
        f"{t}Model:{r} {status['model']}",
        f"{t}OS:{r} {status['os']}",
        f"{t}Kernel:{r} {status['kernel'][:20]}",
        f"{t}GPU:{r} {status['gpu'][:22]}",
        f"{t}CPU:{r} {status['cpu_brand'][:20]}",
        f"{t}CPU Load:{r} [{a}{cpu_bar}{r}] {status['cpu_usage']}%",
        f"{t}Load Avg:{r} {status['load_avg']}",
        f"{t}RAM:{r} [{a}{ram_bar}{r}] {status['used_ram_gb']}/{status['total_ram_gb']}GB",
        f"{m}RAM Free:{r} {status['free_ram_gb']}GB | {m}Swap:{r} {status['swap_used']}",
        f"{t}Disk:{r} [{a}{disk_bar}{r}] {status['disk_avail']} Free",
        f"{t}Battery:{r} 🔋 {status['batt_pct']}% ({status['power_source'][:8]})",
        f"{t}IP:{r} {status['local_ip']}",
        f"{t}Uptime:{r} {status['uptime']}"
    ]

    # Column 2 (Weather & Forecast)
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

    # Column 3 (Calendar & 12-Hour Digital Clock)
    clock_info = get_clock_info()
    cal_lines = get_calendar_lines()
    banner = clock_info["large_banner"]

    col3 = [
        f"{BOLD}{a}TIME: {clock_info['time']}{r}",
        f"{t}{clock_info['date']}{r}",
        ""
    ]
    for b_l in banner:
        col3.append(f"{a}{b_l}{r}")

    col3.append("")
    for cl in cal_lines[:6]:
        col3.append(f"{t}{cl}{r}")

    # Zip rows across 3 columns
    max_rows = max(len(col1), len(col2), len(col3))

    for idx in range(max_rows):
        c1 = col1[idx] if idx < len(col1) else ""
        c2 = col2[idx] if idx < len(col2) else ""
        c3 = col3[idx] if idx < len(col3) else ""

        p_c1 = pad_str(c1, col_w)
        p_c2 = pad_str(c2, col_w + 2)
        p_c3 = pad_str(c3, col_w)

        lines.append(f"{b}│{r} {p_c1} {b}│{r} {p_c2} {b}│{r} {p_c3} {b}│{r}")

    lines.append(f"{b}└{'─' * col_w}┴{'─' * (col_w + 2)}┴{'─' * col_w}┘{r}")

    return "\n".join(lines)
