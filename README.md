# 🥑 Avocado: Native macOS Terminal Dashboard & CLI App

> A pure native macOS terminal dashboard application (CLI & TUI) that runs directly inside macOS Terminal, iTerm2, Kitty, Alacritty, or zsh/bash. **Zero web servers, zero browsers, zero third-party dependencies required!**

---

## 🌟 Key Features

1. **💻 Native macOS System Hardware Telemetry**:
   - Queries official macOS shell APIs (`sysctl`, `pmset`, `vm_stat`, `df`, `sw_vers`).
   - Displays real-time **CPU load %**, **Apple Silicon / Intel model**, **Memory RAM usage**, **APFS Disk storage**, **Battery % (AC / Battery state)**, and **System Uptime**.

2. **🌦 Terminal Weather Forecast**:
   - Live weather via Open-Meteo API formatted directly into terminal text.
   - Shows current temperature (°F / °C), condition icon, wind speed, and multi-day forecast.

3. **📰 Hacker News Reader**:
   - Top 5 Hacker News headlines with points scores right inside the terminal layout.

4. **🚀 App Switcher & Favorite Launchers**:
   - Launch favorite apps/web links (`open 1` or `open github`).

5. **⚙️ Terminal Settings & Config**:
   - Configure ANSI color themes (*Avocado Green*, *Matrix*, *Dracula*, *Ocean*, *Amber*), temperature units, default city, and app shortcuts saved natively in `~/.config/avocado/config.json`.

6. **🥑 Interactive CLI Console**:
   - Prompt `avocado >` with support for commands: `neofetch`, `status`, `weather [city]`, `news`, `apps`, `open [app]`, `settings`, `theme`, `clear`, `help`, `quit`.

---

## 📦 Homebrew Installation

```bash
# Tap the repository
brew tap RnR-io/avocado

# Install avocado
brew install avocado

# Launch Avocado terminal app
avocado
```

---

## 🚀 Quick Start (Local Setup)

```bash
# Clone the repository
git clone https://github.com/RnR-io/avocado.git
cd "mac terminal app"

# Run the executable terminal binary
./bin/avocado
```

### CLI Command Options

| Command | Description |
| :--- | :--- |
| `./bin/avocado` | Launch interactive terminal dashboard |
| `./bin/avocado --once` | Print dashboard layout once and exit |
| `./bin/avocado --status` | Print laptop hardware status summary |
| `./bin/avocado --neofetch` | Display Apple ASCII logo and hardware specs |
| `./bin/avocado --weather "Tokyo"` | Get weather forecast for any city |
| `./bin/avocado --news` | Fetch latest Hacker News headlines |
| `./bin/avocado --settings` | Open interactive settings editor |

---

## 📄 License

Distributed under the MIT License.
