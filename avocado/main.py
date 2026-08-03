"""
Avocado Terminal Dashboard Main CLI Entry Point
"""
import sys
import os
import argparse
import time

from avocado.config import load_config, save_config
from avocado.status import get_macos_status
from avocado.weather import get_weather
from avocado.calendar_clock import get_calendar_lines, get_clock_info
from avocado.ui import render_dashboard, render_neofetch, clear_screen, get_theme, RESET, BOLD, DIM

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

    # Main Interactive Command Loop
    while True:
        clear_screen()
        print(render_dashboard(status, weather, config))

        colors = get_theme(config.get("theme", "avocado"))
        p = colors["primary"]
        r = RESET

        print(f"\nType {BOLD}'help'{r}, {BOLD}'weather [city]'{r}, {BOLD}'calendar'{r}, {BOLD}'status'{r}, {BOLD}'settings'{r}, or {BOLD}'quit'{r}.")
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

        if cmd in ["quit", "exit", "q"]:
            print("Exiting Avocado Terminal App. Have a great day!")
            break
        elif cmd == "help":
            print("""
Available Avocado Commands:
  • neofetch           - Display Apple ASCII logo and hardware specs
  • status             - Refresh and show expanded laptop system metrics
  • weather [city]     - Search weather forecast for any city with ASCII art
  • calendar           - Show monthly calendar and digital clock
  • settings           - Open terminal settings configuration prompt
  • theme [name]       - Change theme (avocado, matrix, dracula, ocean, amber)
  • clear              - Clear screen
  • quit / exit        - Exit Avocado application
""")
            input("\nPress Enter to return to dashboard...")
        elif cmd in ["neofetch", "macfetch"]:
            clear_screen()
            print(render_neofetch(colors))
            input("\nPress Enter to return to dashboard...")
        elif cmd == "status":
            status = get_macos_status()
        elif cmd == "weather":
            city = " ".join(sub_args) if sub_args else config.get("default_city", "auto")
            weather = get_weather(city, config.get("temp_unit", "C"))
        elif cmd == "calendar":
            clear_screen()
            clock = get_clock_info()
            print(f"Time: {clock['time']} | {clock['date']}\n")
            for line in get_calendar_lines():
                print(line)
            input("\nPress Enter to return...")
        elif cmd == "settings":
            run_settings_prompt(config)
            config = load_config()
            status = get_macos_status()
            weather = get_weather(config.get("default_city", "auto"), config.get("temp_unit", "C"))
        elif cmd == "theme":
            if sub_args and sub_args[0].lower() in ['avocado', 'matrix', 'dracula', 'ocean', 'amber']:
                config['theme'] = sub_args[0].lower()
                save_config(config)
                print(f"Theme updated to '{sub_args[0]}'!")
                time.sleep(1)
        elif cmd == "clear":
            clear_screen()
        else:
            print(f"Unknown command: {cmd}. Type 'help' for available commands.")
            time.sleep(1)

if __name__ == "__main__":
    main()
