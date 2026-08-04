"""
Avocado Terminal Dashboard Main CLI Entry Point v2.0.0
Features Responsive Full-Window Layout, 2-Column Hardware Telemetry View,
Arrow-Key TUI Menu, Google Search Launcher, and GitHub Repo Info.
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
from avocado.status import get_macos_status, render_fullscreen_hardware_page
from avocado.weather import get_weather
from avocado.calendar_clock import get_calendar_lines, get_clock_info
from avocado.github_info import get_github_info, open_github_in_browser
from avocado.ui import render_dashboard, render_neofetch, clear_screen, get_theme, RESET, BOLD, DIM

HISTORY_FILE = os.path.join(CONFIG_DIR, "history")
COMMANDS = ["help", "status", "hardware", "weather", "calendar", "google", "github", "neofetch", "settings", "theme", "version", "v", "clear", "quit", "exit"]

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
        print(f"\n{BOLD}🔍 GOOGLE SEARCH LAUNCHER{RESET}")
        query = input("Enter Google search query: ").strip()

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
  • \033[1mVersion Tag:\033[0m  v2.0.0
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
    from avocado.menu import run_menu
    opts = [
        f"Theme: {config.get('theme')} (avocado/matrix/dracula/ocean/amber)",
        f"Temperature Unit: {config.get('temp_unit')} (C/F)",
        f"Location: {config.get('default_city')} ('auto' for IP)",
        "Back to Dashboard"
    ]
    idx = run_menu("⚙️ TERMINAL SETTINGS & PREFERENCES", opts)
    if idx == 0:
        t_idx = run_menu("Select Theme", ["avocado", "matrix", "dracula", "ocean", "amber"])
        config['theme'] = ["avocado", "matrix", "dracula", "ocean", "amber"][t_idx]
        save_config(config)
    elif idx == 1:
        u_idx = run_menu("Select Temperature Unit", ["Celsius (°C)", "Fahrenheit (°F)"])
        config['temp_unit'] = "C" if u_idx == 0 else "F"
        save_config(config)
    elif idx == 2:
        city_choice = input("\nEnter location/city name (or 'auto'): ").strip()
        if city_choice:
            config['default_city'] = city_choice
            save_config(config)

def run_tui_menu_navigation(config):
    from avocado.menu import run_menu
    opts = [
        "1. Dashboard View (Auto-Scaled Window Boundaries)",
        "2. Hardware Telemetry Page",
        "3. Google Search Launcher",
        "4. GitHub Repository Info & About",
        "5. Terminal Settings & Preferences",
        "6. Calendar & Time",
        "7. Weather Forecast & ASCII Art",
        "8. Neofetch Summary",
        "9. Exit Avocado"
    ]
    idx = run_menu("🥑 AVOCADO INTERACTIVE TUI MENU", opts)
    if idx == 0: return "dashboard"
    if idx == 1: return "hardware"
    if idx == 2: return "google"
    if idx == 3: return "github"
    if idx == 4: return "settings"
    if idx == 5: return "calendar"
    if idx == 6: return "weather"
    if idx == 7: return "neofetch"
    if idx == 8: return "quit"
    return "dashboard"

def main():
    parser = argparse.ArgumentParser(description="Avocado: Native macOS Terminal Dashboard & CLI App v2.0.0")
    parser.add_argument("-v", "-V", "--version", action="store_true", help="Print Avocado version info and exit")
    parser.add_argument("--status", action="store_true", help="Print expanded laptop hardware telemetry and exit")
    parser.add_argument("--hardware", action="store_true", help="Launch Full-Screen Hardware Telemetry & Graphs View")
    parser.add_argument("--weather", type=str, help="Get weather forecast for a city")
    parser.add_argument("--calendar", action="store_true", help="Print monthly calendar and 12-hour system time")
    parser.add_argument("--neofetch", action="store_true", help="Render macOS system neofetch ASCII art")
    parser.add_argument("--github", action="store_true", help="Display GitHub repository info and about page")
    parser.add_argument("--google", type=str, help="Search Google in default browser")
    parser.add_argument("--menu", action="store_true", help="Launch interactive Arrow-Key TUI Menu")
    parser.add_argument("--settings", action="store_true", help="Open terminal settings configuration")
    parser.add_argument("--once", action="store_true", help="Render dashboard once and exit")

    args = parser.parse_args()

    if args.version:
        print("🥑 Avocado v2.0.0 (Native macOS Terminal Dashboard)")
        return

    config = load_config()

    colors = get_theme(config.get("theme", "avocado"))

    if args.hardware:
        clear_screen()
        print(render_fullscreen_hardware_page(colors))
        return

    if args.google:
        run_google_search(args.google)
        return

    if args.github:
        render_github_page()
        return

    if args.neofetch:
        print(render_neofetch(colors))
        return

    if args.status:
        st = get_macos_status()
        batt = st.get('batt', {'pct': 100, 'power_src': 'AC Power'})
        print(f"Model: {st['model']} ({st['os']})")
        print(f"Chip: {st['chip_brand']} | GPU: {st['gpu']}")
        print(f"CPU Load: {st['cpu_usage']}% | Load Avg: {st['load_str']}")
        print(f"RAM: {st['used_ram_gb']}GB / {st['total_ram_gb']}GB ({st['ram_pct']}%) [Free: {st['free_ram_gb']}GB | Cache: {st['cache_ram_gb']}GB]")
        print(f"Disk: {st['disk_used_gb']}G / {st['disk_total_gb']}G ({st['disk_free_gb']}G Free)")
        print(f"Battery: {batt['pct']}% ({batt['power_src']})")
        print(f"Network IP: {st['local_ip']}")
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
        if choice == "hardware":
            clear_screen()
            print(render_fullscreen_hardware_page(colors))
            input("\nPress Enter to return...")
            return
        elif choice == "google": run_google_search()
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

        print(f"\nQuick Keys: {BOLD}[m]{r}enu (arrow keys)  {BOLD}[h]{r}ardware page  {BOLD}[g]{r}oogle search  {BOLD}[i]{r}nfo github  {BOLD}[s]{r}ettings  {BOLD}[r]{r}efresh  {BOLD}[q]{r}uit")
        print(f"{DIM}Press 'm' for Arrow-Key TUI Menu | Type 'hardware' for Full-Screen Telemetry | Tab autocomplete{RESET}")

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
        elif cmd in ["m", "menu"]:
            choice = run_tui_menu_navigation(config)
            if choice == "hardware":
                clear_screen()
                print(render_fullscreen_hardware_page(colors))
                input("\nPress Enter to return...")
            elif choice == "google": run_google_search()
            elif choice == "github": render_github_page()
            elif choice == "settings": run_settings_prompt(config)
            elif choice == "neofetch":
                clear_screen()
                print(render_neofetch(colors, status))
                input("\nPress Enter to return...")
            elif choice == "quit": break
        elif cmd in ["h", "hardware", "telemetry"]:
            clear_screen()
            print(render_fullscreen_hardware_page(colors))
            input("\nPress Enter to return to dashboard...")
        elif cmd in ["g", "google"]:
            query = " ".join(sub_args)
            run_google_search(query)
        elif cmd in ["i", "info", "github"]:
            render_github_page()
            input("\nPress Enter to return...")
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
        elif cmd in ["help", "?"]:
            print("""
Available Avocado Navigation & Commands:
  • Hardware Page: Type 'hardware' or 'h' for Full-Screen Telemetry & Graphs
  • TUI Menu:      Type 'm' or run 'avocado --menu' for Arrow-Key + Enter TUI menu
  • Single Keys:   [m]enu  [h]ardware  [g]oogle  [i]nfo github  [r]efresh  [s]ettings  [c]alendar  [w]eather  [n]eofetch  [q]uit
  • Google:        Type 'google <query>' or 'g <query>' to search Google in browser
  • GitHub:        Type 'info' or 'i' to view repository details
  • Arrows:        UP / DOWN arrows cycle through typed command history
  • Tab:           Tab autocompletes command names
""")
            input("\nPress Enter to return to dashboard...")
        elif cmd == "theme":
            if sub_args and sub_args[0].lower() in ['avocado', 'matrix', 'dracula', 'ocean', 'amber']:
                config['theme'] = sub_args[0].lower()
                save_config(config)
                print(f"Theme updated to '{sub_args[0]}'!")
                time.sleep(1)
        elif cmd in ["v", "version", "-v", "--version"]:
            print(f"\n{BOLD}🥑 Avocado Terminal App v2.0.0{RESET}")
            print("Native macOS Hardware Telemetry & Dashboard Control Center")
            print("Repository: https://github.com/RnR-io/Avacado")
            print("License: MIT")
            input("\nPress Enter to return to dashboard...")
        elif cmd == "clear":
            clear_screen()
        else:
            print(f"Unknown command: {cmd}. Type 'help' for shortcuts.")
            time.sleep(1)

if __name__ == "__main__":
    main()
