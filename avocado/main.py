"""
Avocado Terminal Dashboard Main CLI Entry Point v1.1.0
Features interactive arrow-key TUI menu, Google Search launcher, GitHub Repo Info, 12-Hour clock, and expanded telemetry.
"""
import sys
import os
import argparse
import time
import urllib.parse
import webbrowser

try:
    import readline
    HAVE_READLINE = True
except ImportError:
    HAVE_READLINE = False

from avocado.config import load_config, save_config, CONFIG_DIR
from avocado.status import get_macos_status
from avocado.weather import get_weather
from avocado.calendar_clock import get_calendar_lines, get_clock_info
from avocado.github_info import get_github_info, open_github_in_browser
from avocado.ui import render_dashboard, render_neofetch, clear_screen, get_theme, RESET, BOLD, DIM

HISTORY_FILE = os.path.join(CONFIG_DIR, "history")
COMMANDS = ["help", "status", "weather", "calendar", "google", "github", "neofetch", "settings", "theme", "clear", "quit", "exit"]

def setup_readline():
    if not HAVE_READLINE: return
    if os.path.exists(HISTORY_FILE):
        try: readline.read_history_file(HISTORY_FILE)
        except Exception: pass

    import atexit
    atexit.register(save_readline_history)

    def completer(text, state):
        options = [c for c in COMMANDS if c.startswith(text.lower())]
        return options[state] if state < len(options) else None

    readline.set_completer(completer)
    if "libedit" in (readline.__doc__ or ""):
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

def save_readline_history():
    if HAVE_READLINE:
        try:
            readline.set_history_length(100)
            readline.write_history_file(HISTORY_FILE)
        except Exception: pass

def run_google_search(query=None):
    if not query:
        print(f"\n{BOLD}🔍 GOOGLE SEARCH LAUNCHER{r}")
        query = input(f"Enter Google search query: ").strip()

    if query:
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        print(f"Opening Google search for '{query}' in default browser...")
        try:
            webbrowser.open(search_url)
        except Exception as e:
            print(f"Error launching browser: {e}")
        time.sleep(1)

def render_github_page():
    clear_screen()
    info = get_github_info()
    print(f"""
\033[1;32m 🥑 GITHUB REPOSITORY INFO & ABOUT PAGE\033[0m
--------------------------------------------------
  • \033[1mRepository:\033[0m   {info['full_name']}
  • \033[1mDescription:\033[0m  {info['description']}
  • \033[1mAuthor:\033[0m       {info['owner']}
  • \033[1mVersion Tag:\033[0m  v1.1.0
  • \033[1mLicense:\033[0m      {info['license']}
  • \033[1mURL:\033[0m          {info['html_url']}
  • \033[1mUpdated:\033[0m      {info['updated_at']}
--------------------------------------------------
Options:
  [1] Open Repository in Browser
  [2] Return to Dashboard
""")
    choice = input("\033[1;32mavocado > \033[0m").strip()
    if choice == '1':
        open_github_in_browser()

def run_settings_prompt(config):
    colors = get_theme(config.get("theme", "avocado"))
    p = colors["primary"]
    r = RESET

    print(f"\n{BOLD}[SETTING] AVOCADO TERMINAL SETTINGS & PREFERENCES{r}")
    print("--------------------------------------------------")
    print(f"1. Theme: {config.get('theme')} (avocado, matrix, dracula, ocean, amber)")
    print(f"2. Temperature Unit: {config.get('temp_unit')} (C, F)")
    print(f"3. Default Location: {config.get('default_city')} ('auto' for IP location)")
    print("4. Back to Dashboard")
    print("--------------------------------------------------")

    choice = input(f"{p}Select setting to edit (1-4): {r}").strip()
    if choice == '1':
        theme_choice = input(f"Enter theme name (avocado/matrix/dracula/ocean/amber): ").strip().lower()
        if theme_choice in ['avocado', 'matrix', 'dracula', 'ocean', 'amber']:
            config['theme'] = theme_choice
            save_config(config)
            print(f"Theme updated to '{theme_choice}'!")
    elif choice == '2':
        unit_choice = input(f"Enter temp unit (C/F): ").strip().upper()
        if unit_choice in ['C', 'F']:
            config['temp_unit'] = unit_choice
            save_config(config)
            print(f"Temperature unit set to '{unit_choice}'!")
    elif choice == '3':
        city_choice = input(f"Enter location/city name (or 'auto'): ").strip()
        if city_choice:
            config['default_city'] = city_choice
            save_config(config)
            print(f"Location updated to '{city_choice}'!")

def run_tui_menu_navigation(config):
    """Interactive TUI menu allowing navigation with Arrow Keys & selection with Enter."""
    from avocado.menu import run_menu
    opts = [
        "1. Dashboard View",
        "2. Google Search Launcher",
        "3. GitHub Repository Info",
        "4. Monthly Calendar & 12H Clock",
        "5. Weather Forecast & ASCII Art",
        "6. Hardware Telemetry Summary",
        "7. Terminal Settings",
        "8. Exit Avocado"
    ]
    idx = run_menu("🥑 AVOCADO TUI MENU SELECTION", opts)
    if idx == 0: return "dashboard"
    if idx == 1: return "google"
    if idx == 2: return "github"
    if idx == 3: return "calendar"
    if idx == 4: return "weather"
    if idx == 5: return "status"
    if idx == 6: return "settings"
    if idx == 7: return "quit"
    return "dashboard"

def main():
    parser = argparse.ArgumentParser(description="Avocado: Native macOS Terminal Dashboard & CLI App v1.1.0")
    parser.add_argument("--status", action="store_true", help="Print expanded laptop hardware telemetry and exit")
    parser.add_argument("--weather", type=str, help="Get weather forecast for a city")
    parser.add_argument("--calendar", action="store_true", help="Print monthly calendar and 12-hour system time")
    parser.add_argument("--neofetch", action="store_true", help="Render macOS system neofetch ASCII art")
    parser.add_argument("--github", action="store_true", help="Display GitHub repository info and about page")
    parser.add_argument("--google", type=str, help="Search Google in default browser")
    parser.add_argument("--menu", action="store_true", help="Launch interactive Arrow-Key TUI Menu")
    parser.add_argument("--settings", action="store_true", help="Open terminal settings configuration")
    parser.add_argument("--once", action="store_true", help="Render dashboard once and exit")

    args = parser.parse_args()
    config = load_config()

    if args.google:
        run_google_search(args.google)
        return

    if args.github:
        render_github_page()
        return

    if args.neofetch:
        colors = get_theme(config.get("theme", "avocado"))
        print(render_neofetch(colors))
        return

    if args.status:
        st = get_macos_status()
        print(f"Model: {st['model']} ({st['os']})")
        print(f"Kernel: {st['kernel']} | GPU: {st['gpu']}")
        print(f"CPU: {st['cpu_brand']} - Load: {st['cpu_usage']}% (User: {st['cpu_user']}% | Sys: {st['cpu_sys']}%) [Load Avg: {st['load_avg']}]")
        print(f"RAM: {st['used_ram_gb']}GB / {st['total_ram_gb']}GB ({st['ram_pct']}%) [Free: {st['free_ram_gb']}GB | Wired: {st['wired_ram_gb']}GB | Swap: {st['swap_used']}]")
        print(f"Disk: {st['disk_used']} / {st['disk_total']} ({st['disk_avail']} Free)")
        print(f"Battery: {st['batt_pct']}% ({st['power_source']})")
        print(f"Network: {st['local_ip']} ({st['net_if']})")
        print(f"Uptime: {st['uptime']}")
        return

    if args.weather:
        w = get_weather(args.weather, config.get("temp_unit", "C"))
        print(f"Weather for {w['city']}: {w['temp']} - {w['desc']} (Wind: {w['wind']})")
        for line in w.get("art", []):
            print(line)
        return

    if args.calendar:
        clock = get_clock_info()
        print(f"Time: {clock['time']} | {clock['date']}")
        for line in get_calendar_lines():
            print(line)
        return

    if args.settings:
        run_settings_prompt(config)
        return

    if args.menu:
        choice = run_tui_menu_navigation(config)
        if choice == "google": run_google_search()
        elif choice == "github": render_github_page()
        elif choice == "settings": run_settings_prompt(config)
        elif choice == "quit": sys.exit(0)

    status = get_macos_status()
    weather = get_weather(config.get("default_city", "auto"), config.get("temp_unit", "C"))

    if args.once:
        print(render_dashboard(status, weather, config))
        return

    setup_readline()

    # Main Interactive Command Loop
    while True:
        clear_screen()
        print(render_dashboard(status, weather, config))

        colors = get_theme(config.get("theme", "avocado"))
        p = colors["primary"]
        r = RESET

        print(f"\nQuick Keys: {BOLD}[g]{r}oogle search  {BOLD}[i]{r}nfo github  {BOLD}[r]{r}efresh  {BOLD}[s]{r}ettings  {BOLD}[c]{r}alendar  {BOLD}[m]{r}enu  {BOLD}[q]{r}uit")
        print(f"{DIM}Use UP/DOWN arrows for command history | Type 'google <query>' to search | Tab autocomplete{RESET}")

        try:
            cmd_str = input(f"\n{p}avocado > {r}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Avocado Terminal App. Goodbye!")
            break

        if not cmd_str:
            status = get_macos_status()
            continue

        parts = cmd_str.split()
        cmd = parts[0].lower()
        sub_args = parts[1:]

        if cmd in ["q", "quit", "exit"]:
            print("Exiting Avocado Terminal App. Have a great day!")
            break
        elif cmd in ["g", "google"]:
            query = " ".join(sub_args)
            run_google_search(query)
        elif cmd in ["i", "info", "github"]:
            render_github_page()
            input("\nPress Enter to return...")
        elif cmd in ["m", "menu"]:
            choice = run_tui_menu_navigation(config)
            if choice == "google": run_google_search()
            elif choice == "github": render_github_page()
            elif choice == "settings": run_settings_prompt(config)
            elif choice == "quit": break
        elif cmd in ["r", "status", "refresh"]:
            status = get_macos_status()
        elif cmd in ["s", "settings"]:
            run_settings_prompt(config)
            config = load_config()
            status = get_macos_status()
            weather = get_weather(config.get("default_city", "auto"), config.get("temp_unit", "C"))
        elif cmd in ["c", "calendar"]:
            clear_screen()
            clock = get_clock_info()
            print(f"Time: {clock['time']} | {clock['date']}\n")
            for line in get_calendar_lines():
                print(line)
            input("\nPress Enter to return...")
        elif cmd in ["w", "weather"]:
            city = " ".join(sub_args) if sub_args else config.get("default_city", "auto")
            weather = get_weather(city, config.get("temp_unit", "C"))
        elif cmd in ["n", "neofetch", "macfetch"]:
            clear_screen()
            print(render_neofetch(colors, status))
            input("\nPress Enter to return to dashboard...")
        elif cmd in ["h", "help", "?"]:
            print("""
Available Avocado Navigation & Commands:
  • Single Keys:  [g]oogle  [i]nfo github  [m]enu  [r]efresh  [s]ettings  [c]alendar  [w]eather  [n]eofetch  [q]uit
  • Menu:         Type 'm' or run 'avocado --menu' for Arrow-Key + Enter TUI menu
  • Google:       Type 'google <query>' or 'g <query>' to search Google in browser
  • GitHub:       Type 'info' or 'i' to view repository details
  • Arrows:       UP / DOWN arrows cycle through typed command history
  • Tab:          Tab autocompletes command names
""")
            input("\nPress Enter to return to dashboard...")
        elif cmd == "theme":
            if sub_args and sub_args[0].lower() in ['avocado', 'matrix', 'dracula', 'ocean', 'amber']:
                config['theme'] = sub_args[0].lower()
                save_config(config)
                print(f"Theme updated to '{sub_args[0]}'!")
                time.sleep(1)
        elif cmd == "clear":
            clear_screen()
        else:
            print(f"Unknown command: {cmd}. Type 'h' or 'help' for shortcuts.")
            time.sleep(1)

if __name__ == "__main__":
    main()
