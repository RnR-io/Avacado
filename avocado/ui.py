"""
Terminal UI Utilities (ANSI Colors & Box-Drawing Grid)
"""
import os
import sys

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

def render_neofetch(colors):
    p = colors["primary"]
    a = colors["accent"]
    t = colors["text"]
    m = colors["muted"]
    r = RESET

    art = f"""
{a}                 🥑 avocado {r}       user@macbook-pro
{p}               .o888a{r}             ----------------
{p}             a8888"{r}               OS: macOS Sonoma 26.6 (arm64)
{p}            888888{r}                Host: MacBook Pro 16" (Mac16,8)
{p}            888888888a{r}            Kernel: Darwin 23.5.0
{a}    a8888888888888888888{r}          Uptime: 3 days, 2 hours
{a}  .888888888888888888888{r}          Shell: zsh / avocado-cli v2.0
{a} .8888888888888888888888{r}          CPU: Apple M3 Max (14 Cores)
{p} 88888888888888888888888{r}          Memory: 11.2 GB / 24.0 GB
{p} "8888888888888888888"{r}           Battery: 99% (AC Power)
{p}    "888888888888888"{r}             App: Avocado Terminal Dashboard
"""
    return art

def render_dashboard(status, weather, news, config):
    colors = get_theme(config.get("theme", "avocado"))
    p = colors["primary"]
    a = colors["accent"]
    h = colors["header"]
    t = colors["text"]
    m = colors["muted"]
    b = colors["border"]
    r = RESET

    # Calculate terminal dimensions
    try:
        cols, rows = os.get_terminal_size()
    except Exception:
        cols, rows = 80, 24

    w = max(78, min(cols - 2, 110))

    lines = []
    
    # Header box
    lines.append(f"{b}┌{'─' * (w - 2)}┐{r}")
    title_str = f" 🥑 AVOCADO MAC OS TERMINAL DASHBOARD "
    lines.append(f"{b}│{r} {BOLD}{p}{title_str}{r}{' ' * (w - 4 - len(title_str))}{b}│{r}")
    lines.append(f"{b}├{'─' * (w - 2)}┤{r}")

    # Section 1: Laptop Hardware Status
    lines.append(f"{b}│{r} {BOLD}{h}💻 LAPTOP HARDWARE STATUS{r} {m}({status['os']}){r}{' ' * (w - 32 - len(status['os']))}{b}│{r}")
    lines.append(f"{b}│{r}  {t}Model:{r} {status['model']}  |  {t}CPU:{r} {status['cpu_brand']}")
    
    cpu_bar = make_progress_bar(status['cpu_usage'], 14)
    ram_bar = make_progress_bar(status['ram_pct'], 14)
    disk_bar = make_progress_bar(status['disk_pct'], 14)

    lines.append(f"{b}│{r}  {t}CPU Load:{r} [{a}{cpu_bar}{r}] {status['cpu_usage']}%  |  {t}RAM:{r} [{a}{ram_bar}{r}] {status['used_ram_gb']}GB / {status['total_ram_gb']}GB ({status['ram_pct']}%)")
    lines.append(f"{b}│{r}  {t}Storage:{r} [{a}{disk_bar}{r}] {status['disk_avail']} Free  |  {t}Battery:{r} 🔋 {status['batt_pct']}% ({status['power_source']})")
    lines.append(f"{b}│{r}  {t}Uptime:{r} {status['uptime']}")
    lines.append(f"{b}├{'─' * (w - 2)}┤{r}")

    # Section 2: Weather & News Side-by-Side or Stacked
    lines.append(f"{b}│{r} {BOLD}{h}🌦 LIVE WEATHER{r} {m}({weather.get('city', 'San Francisco')}){r}{' ' * (w - 26 - len(weather.get('city', 'San Francisco')))}{b}│{r}")
    lines.append(f"{b}│{r}  {weather.get('icon', '🌤')} {BOLD}{t}{weather.get('temp', '68°F')}{r} - {weather.get('desc', 'Partly Cloudy')}  |  Wind: {weather.get('wind', '8 km/h')}")

    f_str = ""
    for f in weather.get("forecast", []):
        f_str += f"{f['day']}: {f['icon']}{f['high']}  "
    if f_str:
        lines.append(f"{b}│{r}  {t}Forecast:{r} {f_str}")
    lines.append(f"{b}├{'─' * (w - 2)}┤{r}")

    # Section 3: Tech & World News
    lines.append(f"{b}│{r} {BOLD}{h}📰 HACKER NEWS HEADLINES{r}{' ' * (w - 24)}{b}│{r}")
    for idx, item in enumerate(news[:4]):
        title = item['title']
        if len(title) > w - 12:
            title = title[:w - 15] + "..."
        lines.append(f"{b}│{r}  {a}{idx+1}.{r} {t}{title}{r} {m}(▲{item.get('score', 0)}){r}")
    lines.append(f"{b}├{'─' * (w - 2)}┤{r}")

    # Section 4: Favorite App Launcher
    lines.append(f"{b}│{r} {BOLD}{h}🚀 FAVORITE APPS LAUNCHER{r} {m}(Type 'open 1' or press key to launch){r}{' ' * (w - 63)}{b}│{r}")
    dock_line = "  "
    for idx, app in enumerate(config.get("favorite_apps", [])[:6]):
        dock_line += f"[{a}{idx+1}{r}] {app.get('icon', '🌐')} {app['name']}   "
    lines.append(f"{b}│{r}{dock_line}")

    lines.append(f"{b}└{'─' * (w - 2)}┘{r}")

    return "\n".join(lines)
