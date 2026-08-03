"""
Avocado Terminal Dashboard Main CLI Entry Point
Features readline command history (Up/Down arrow navigation), tab completion, and single-key shortcuts.
"""
import sys
import os
import argparse
import time

try:
    import readline
    HAVE_READLINE = True
except ImportError:
    HAVE_READLINE = False

from avocado.config import load_config, save_config, CONFIG_DIR
from avocado.status import get_macos_status
from avocado.weather import get_weather
from avocado.calendar_clock import get_calendar_lines, get_clock_info
from avocado.ui import render_dashboard, render_neofetch, clear_screen, get_theme, RESET, BOLD, DIM

HISTORY_FILE = os.path.join(CONFIG_DIR, "history")
COMMANDS = ["help", "status", "weather", "calendar", "neofetch", "settings", "theme", "clear", "quit", "exit"]

def setup_readline():
    """Configures readline for Up/Down arrow history navigation & tab completion."""
    if not HAVE_READLINE:
        return

    # Load history
    if os.path.exists(HISTORY_FILE):
        try:
            readline.read_history_file(HISTORY_FILE)
        except Exception:
            pass

    # Save history on exit
    import atexit
    atexit.register(save_readline_history)

    # Enable autocompletion
    def completer(text, state):
        options = [c for c in COMMANDS if c.startswith(text.lower())]
        if state < len(options):
            return options[state]
        return None

    readline.set_completer(completer)
    if "libedit" in readline.__doc__ if readline.__doc__ else False:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

def save_readline_history():
    if HAVE_READLINE:
        try:
            readline.set_history_length(100)
            readline.write_history_file(HISTORY_FILE)
        except Exception:
            pass

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

def main():
    parser = argparse.ArgumentParser(description="Avocado: Native macOS Terminal Dashboard & CLI App")
    parser.add_argument("--status", action="store_true", help="Print expanded laptop hardware telemetry and exit")
    parser.add_argument("--weather", type=str, help="Get weather forecast for a city")
    parser.add_argument("--calendar", action="store_true", help="Print monthly calendar and system time")
    parser.add_argument("--neofetch", action="store_true", help="Render macOS system neofetch ASCII art")
    parser.add_argument("--settings", action="store_true", help="Open terminal settings configuration")
    parser.add_argument("--once", action="store_true", help="Render dashboard once and exit")

    args = parser.parse_args()
    config = load_config()

    if args.neofetch:
        colors = get_theme(config.get("theme", "avocado"))
        print(render_neofetch(colors))
        return

    if args.status:
        st = get_macos_status()
        print(f"Model: {st['model']} ({st['os']})")
        print(f"Kernel: {st['kernel']}")
        print(f"CPU: {st['cpu_brand']} - Load: {st['cpu_usage']}% (User: {st['cpu_user']}% | Sys: {st['cpu_sys']}%)")
        print(f"RAM: {st['used_ram_gb']}GB / {st['total_ram_gb']}GB ({st['ram_pct']}%) [Free: {st['free_ram_gb']}GB]")
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

    status = get_macos_status()
    weather = get_weather(config.get("default_city", "auto"), config.get("temp_unit", "C"))

    if args.once:
        print(render_dashboard(status, weather, config))
        return

    # Setup Readline for Up/Down arrow history & Tab Completion
    setup_readline()

    # Main Interactive Command Loop
    while True:
        clear_screen()
        print(render_dashboard(status, weather, config))

        colors = get_theme(config.get("theme", "avocado"))
        p = colors["primary"]
        r = RESET

        print(f"\nQuick Keys: {BOLD}[r]{r}efresh  {BOLD}[s]{r}ettings  {BOLD}[c]{r}alendar  {BOLD}[w]{r}eather  {BOLD}[n]{r}eofetch  {BOLD}[q]{r}uit")
        print(f"{m if 'm' in locals() else DIM}Use UP/DOWN arrows for history | Tab to autocomplete commands{RESET}")

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

        # Single-key & Full Command Shortcuts
        if cmd in ["q", "quit", "exit"]:
            print("Exiting Avocado Terminal App. Have a great day!")
            break
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
            print(render_neofetch(colors))
            input("\nPress Enter to return to dashboard...")
        elif cmd in ["h", "help", "?"]:
            print("""
Available Avocado Navigation & Commands:
  • Single Keys:  [r]efresh  [s]ettings  [c]alendar  [w]eather  [n]eofetch  [q]uit
  • Arrows:       UP / DOWN arrows cycle through typed command history
  • Tab:          Tab autocompletes command names
  • Full Commands:
      status             - Refresh laptop telemetry
      weather [city]     - Search weather for any city
      calendar           - Show monthly calendar grid
      settings           - Open preferences editor
      theme [name]       - Change theme (avocado, matrix, dracula, ocean, amber)
      clear              - Clear terminal screen
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
