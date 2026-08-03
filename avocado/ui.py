"""
Terminal UI Utilities (ANSI Colors & Box-Drawing Grid Layout)
Responsive 3-panel dashboard layout with dynamic window resizing and detailed ASCII graphics.
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

def make_progress_bar(pct, length=18, fill_char="█", empty_char="░"):
    filled = int(round(length * (pct / 100.0)))
    return fill_char * filled + empty_char * (length - filled)

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

    # Dynamic terminal width resizing
    try:
        cols, rows = os.get_terminal_size()
    except Exception:
        cols, rows = 85, 28

    w = max(82, cols - 2)
    lines = []

    # 1. Outer Header Box with Detailed ASCII Avocado Icon
    lines.append(f"{b}┌{'─' * (w - 2)}┐{r}")
    title_str = f" [AVOCADO] MAC OS TERMINAL DASHBOARD & CONTROL CENTER "
    lines.append(f"{b}│{r} {a}( \\{r}  {BOLD}{p}{title_str}{r}{' ' * max(0, w - 11 - len(title_str))}{b}│{r}")
    lines.append(f"{b}│{r} {p}( (O) ){r} {m}Native Hardware Telemetry | Press Arrow Keys or Numbers to Navigate{r}{' ' * max(0, w - 74)}{b}│{r}")
    lines.append(f"{b}├{'─' * (w - 2)}┤{r}")

    # 2. Expanded Laptop Hardware Telemetry Section
    lines.append(f"{b}│{r} {BOLD}{h}💻 LAPTOP HARDWARE TELEMETRY{r} {m}({status['os']}){r}{' ' * max(0, w - 35 - len(status['os']))}{b}│{r}")
    lines.append(f"{b}│{r}  {t}Model:{r} {status['model']}  |  {t}Kernel:{r} {status['kernel']}  |  {t}GPU:{r} {status['gpu']}")
    lines.append(f"{b}│{r}  {t}CPU:{r} {status['cpu_brand']} ({status['cpu_cores']} Cores)  |  {t}Load Avg:{r} {status['load_avg']}")

    bar_len = max(12, min(24, w - 65))
    cpu_bar = make_progress_bar(status['cpu_usage'], bar_len)
    ram_bar = make_progress_bar(status['ram_pct'], bar_len)
    disk_bar = make_progress_bar(status['disk_pct'], bar_len)

    lines.append(f"{b}│{r}  {t}CPU Load:{r} [{a}{cpu_bar}{r}] {status['cpu_usage']}% {m}(User: {status['cpu_user']}% | Sys: {status['cpu_sys']}%){r}")
    lines.append(f"{b}│{r}  {t}RAM Usage:{r} [{a}{ram_bar}{r}] {status['used_ram_gb']}GB / {status['total_ram_gb']}GB ({status['ram_pct']}%) {m}[Free: {status['free_ram_gb']}GB | Wired: {status['wired_ram_gb']}GB | Swap: {status['swap_used']}] {r}")
    lines.append(f"{b}│{r}  {t}APFS Disk:{r} [{a}{disk_bar}{r}] {status['disk_used']} / {status['disk_total']} {m}({status['disk_avail']} Free | {status['disk_pct']}% Used){r}")
    lines.append(f"{b}│{r}  {t}Battery:{r} 🔋 {status['batt_pct']}% ({status['power_source']})  |  {t}Network IP:{r} {status['local_ip']} ({status['net_if']})")
    lines.append(f"{b}│{r}  {t}System Uptime:{r} {status['uptime']}")
    lines.append(f"{b}├{'─' * (w - 2)}┤{r}")

    # 3. Weather & Forecast Section
    lines.append(f"{b}│{r} {BOLD}{h}🌦 ASCII WEATHER FORECAST{r} {m}({weather.get('city', 'Auto Location')}){r}{' ' * max(0, w - 32 - len(weather.get('city', 'Auto Location')))}{b}│{r}")

    art_lines = weather.get("art", [""])
    weather_info_header = f"Temp: {BOLD}{weather.get('temp', '22°C')}{r} ({weather.get('desc', 'Clear')}) | Wind: {weather.get('wind', '12 km/h')}"

    for art_l in art_lines:
        lines.append(f"{b}│{r}  {a}{art_l}{r}  |  {t}{weather_info_header}{r}")
        weather_info_header = ""

    fc_str = "  Forecast: "
    for fc in weather.get("forecast", []):
        fc_str += f"{fc['day']}: {fc['high']}/{fc['low']}  "
    lines.append(f"{b}│{r}  {t}{fc_str}{r}")

    lines.append(f"{b}├{'─' * (w - 2)}┤{r}")

    # 4. Monthly Calendar & 12-Hour Digital Clock Section
    lines.append(f"{b}│{r} {BOLD}{h}📅 MONTHLY CALENDAR & 12-HOUR SYSTEM TIME{r}{' ' * max(0, w - 44)}{b}│{r}")

    cal_lines = get_calendar_lines()
    clock_info = get_clock_info()

    lines.append(f"{b}│{r}  {BOLD}{a}TIME: {clock_info['time']}{r}  |  {t}{clock_info['date']} ({clock_info['week']}){r}")

    # Render 12-hour ASCII digital clock banner side-by-side with calendar if window width allows
    banner_lines = clock_info["large_banner"]
    lines.append(f"{b}│{r}  {a}{banner_lines[0]}{r}")
    lines.append(f"{b}│{r}  {a}{banner_lines[1]}{r}")
    lines.append(f"{b}│{r}  {a}{banner_lines[2]}{r}")

    for cl in cal_lines[:5]:
        lines.append(f"{b}│{r}  {t}{cl}{r}")

    lines.append(f"{b}└{'─' * (w - 2)}┘{r}")

    return "\n".join(lines)
