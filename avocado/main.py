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
from avocado.news import get_top_news
from avocado.apps import open_app
from avocado.ui import render_dashboard, render_neofetch, clear_screen, get_theme, RESET, BOLD, DIM

def run_settings_prompt(config):
    colors = get_theme(config.get("theme", "avocado"))
    p = colors["primary"]
    r = RESET

    print(f"\n{BOLD}⚙️  AVOCADO TERMINAL SETTINGS & PREFERENCES{r}")
    print("--------------------------------------------------")
    print(f"1. Theme: {config.get('theme')} (options: avocado, matrix, dracula, ocean, amber)")
    print(f"2. Temperature Unit: {config.get('temp_unit')} (options: F, C)")
    print(f"3. Default City: {config.get('default_city')}")
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
        unit_choice = input(f"Enter temp unit (F/C): ").strip().upper()
        if unit_choice in ['F', 'C']:
            config['temp_unit'] = unit_choice
            save_config(config)
            print(f"Temperature unit set to '{unit_choice}'!")
    elif choice == '3':
        city_choice = input(f"Enter default city name: ").strip()
        if city_choice:
            config['default_city'] = city_choice
            save_config(config)
            print(f"Default city updated to '{city_choice}'!")

def main():
    parser = argparse.ArgumentParser(description="🥑 Avocado: Native macOS Terminal Dashboard & CLI App")
    parser.add_argument("--status", action="store_true", help="Print laptop hardware status and exit")
    parser.add_argument("--weather", type=str, help="Get weather forecast for a city")
    parser.add_argument("--news", action="store_true", help="Get top tech news headlines")
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
        print(f"💻 Model: {st['model']} ({st['os']})")
        print(f"🧠 CPU: {st['cpu_brand']} - Load: {st['cpu_usage']}%")
        print(f"💾 RAM: {st['used_ram_gb']}GB / {st['total_ram_gb']}GB ({st['ram_pct']}%)")
        print(f"🔋 Battery: {st['batt_pct']}% ({st['power_source']})")
        print(f"⏱ Uptime: {st['uptime']}")
        return

    if args.weather:
        w = get_weather(args.weather, config.get("temp_unit", "F"))
        print(f"🌦 Weather for {w['city']}: {w['icon']} {w['temp']} - {w['desc']} (Wind: {w['wind']})")
        return

    if args.news:
        news = get_top_news(count=5)
        print("📰 Top Hacker News Headlines:")
        for idx, n in enumerate(news):
            print(f"  {idx+1}. {n['title']} (▲{n['score']}) -> {n['url']}")
        return

    if args.settings:
        run_settings_prompt(config)
        return

    # Interactive Dashboard CLI Mode
    status = get_macos_status()
    weather = get_weather(config.get("default_city", "San Francisco"), config.get("temp_unit", "F"))
    news = get_top_news()

    if args.once:
        print(render_dashboard(status, weather, news, config))
        return

    # Main Interactive Prompt Loop
    while True:
        clear_screen()
        print(render_dashboard(status, weather, news, config))

        colors = get_theme(config.get("theme", "avocado"))
        p = colors["primary"]
        r = RESET

        print(f"\nType {BOLD}'help'{r}, {BOLD}'neofetch'{r}, {BOLD}'weather [city]'{r}, {BOLD}'news'{r}, {BOLD}'open [1-9]'{r}, {BOLD}'settings'{r}, or {BOLD}'quit'{r}.")
        try:
            cmd_str = input(f"\n{p}🥑 avocado > {r}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Avocado Terminal App. Have a great day! 🥑")
            break

        if not cmd_str:
            status = get_macos_status()
            continue

        parts = cmd_str.split()
        cmd = parts[0].lower()
        sub_args = parts[1:]

        if cmd in ["quit", "exit", "q"]:
            print("Exiting Avocado Terminal App. Goodbye! 🥑")
            break
        elif cmd == "help":
            print("""
Available Avocado Commands:
  • neofetch           - Display Apple ASCII logo and hardware specs
  • status             - Refresh and show detailed laptop metrics
  • weather [city]     - Search weather forecast for city
  • news               - Fetch latest tech & Hacker News items
  • apps               - List favorite app shortcuts
  • open [name|idx]    - Launch favorite app by name or index (e.g. open 1 or open github)
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
            city = " ".join(sub_args) if sub_args else config.get("default_city", "San Francisco")
            weather = get_weather(city, config.get("temp_unit", "F"))
        elif cmd == "news":
            news = get_top_news()
        elif cmd == "apps":
            print("\nInstalled Favorite Apps:")
            for idx, a in enumerate(config.get("favorite_apps", [])):
                print(f" [{idx+1}] {a.get('icon', '🌐')} {a['name']} -> {a['url']}")
            input("\nPress Enter to return...")
        elif cmd == "open":
            target = " ".join(sub_args)
            success, msg = open_app(target, config.get("favorite_apps", []))
            print(f"\n{msg}")
            time.sleep(1)
        elif cmd == "settings":
            run_settings_prompt(config)
            config = load_config()
            status = get_macos_status()
            weather = get_weather(config.get("default_city", "San Francisco"), config.get("temp_unit", "F"))
        elif cmd == "theme":
            if sub_args and sub_args[0].lower() in ['avocado', 'matrix', 'dracula', 'ocean', 'amber']:
                config['theme'] = sub_args[0].lower()
                save_config(config)
                print(f"Theme updated to {sub_args[0]}!")
                time.sleep(1)
        elif cmd == "clear":
            clear_screen()
        else:
            print(f"Unknown command: {cmd}. Type 'help' for available commands.")
            time.sleep(1)

if __name__ == "__main__":
    main()
