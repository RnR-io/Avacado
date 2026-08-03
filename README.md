# 🥑 Avocado: Native macOS Terminal Dashboard & CLI App

> A pure native macOS terminal dashboard application (CLI & TUI) that runs directly inside macOS Terminal, iTerm2, Kitty, Alacritty, or zsh/bash. **Zero web servers, zero browsers, zero third-party dependencies required!**

---

## 🌟 Key Features

1. **💻 Native macOS System Hardware Telemetry**:
   - Queries official macOS shell APIs (`sysctl`, `pmset`, `vm_stat`, `df`, `sw_vers`) securely using `shell=False`.
   - Displays real-time **CPU load %**, **Apple Silicon / Intel model**, **Memory RAM usage**, **APFS Disk storage**, **Battery % (AC / Battery state)**, and **System Uptime**.

2. **🌦 ASCII Weather Forecast**:
   - Live weather via Open-Meteo API formatted directly into ASCII art banners.
   - Shows current temperature (°F / °C), condition art, wind speed, and 3-day forecast.

3. **📅 Monthly Calendar & System Time**:
   - Terminal monthly calendar grid highlighting today's date, date, timezone, and uptime.

4. **🚀 Installed macOS Native Apps Dock**:
   - Auto-discovers and launches native macOS applications installed on your Mac (`open -a`).

5. **⚙️ Terminal Settings & Config**:
   - Configure ANSI color themes (*Avocado Green*, *Matrix*, *Dracula*, *Ocean*, *Amber*), temperature units, and default city saved securely in `~/.config/avocado/config.json` with `0700/0600` permissions.

6. **🔒 Hardened & Secure**:
   - Sanitized input parameters against argument injection and command hijacking.
   - Enforces HTTPS-only weather requests.

---

## 📦 Homebrew Installation

```bash
# Tap the repository
brew tap RnR-io/Avacado

# Install avocado
brew install avocado

# Launch Avocado terminal app
avocado
```

---

## 🚀 Quick Start (Local Setup)

```bash
# Clone the repository
git clone https://github.com/RnR-io/Avacado.git
cd Avacado

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
| `./bin/avocado --calendar` | Display monthly calendar and system time |
| `./bin/avocado --apps` | List installed macOS native applications |
| `./bin/avocado --settings` | Open interactive settings editor |

---

## 📄 License

Distributed under the MIT License.
