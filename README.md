# Avocado: Native macOS Terminal Dashboard & CLI App

> A pure native macOS terminal dashboard application (CLI & TUI) that runs directly inside macOS Terminal, iTerm2, Kitty, Alacritty, or zsh/bash. **Zero web servers, zero browsers, zero third-party dependencies required!**

---

## 🌟 Key Features

1. **💻 Expanded macOS System Hardware Telemetry**:
   - Queries official macOS shell APIs (`sysctl`, `pmset`, `vm_stat`, `df`, `sw_vers`, `uname`).
   - Displays real-time **CPU load % (User vs Sys)**, **Apple M-Series / Intel Model**, **Memory RAM Usage, Free RAM & Swap**, **APFS Storage**, **Battery % & Power State**, **Local Network IP (`en0`)**, **Kernel Version & Arch (`arm64`)**, and **System Uptime**.

2. **🌦 ASCII Weather Forecast & Auto Location**:
   - Auto-detects location via IP Geolocation API (`auto`).
   - Default temperature unit in **Celsius (°C)** (configurable to Fahrenheit).
   - Multi-line ASCII Art weather banners (Sun, Cloud, Rain, Thunderstorm, Snow, Fog).

3. **📅 Monthly Calendar & System Time**:
   - Terminal monthly calendar grid highlighting today's date, current time, date, and week number.

4. **⚙️ Terminal Settings & Config**:
   - Configure ANSI color themes (*Avocado Green*, *Matrix*, *Dracula*, *Ocean*, *Amber*), temperature units (°C / °F), and location saved securely in `~/.config/avocado/config.json`.

---

## 📦 Homebrew Installation

```bash
# 1. Tap the repository
brew tap RnR-io/Avacado https://github.com/RnR-io/Avacado.git

# 2. Install avocado
brew install avocado

# 3. Launch from any terminal prompt!
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
| `./bin/avocado --status` | Print expanded hardware telemetry summary |
| `./bin/avocado --neofetch` | Display Apple ASCII logo and hardware specs |
| `./bin/avocado --weather "Tokyo"` | Get weather forecast for any city |
| `./bin/avocado --calendar` | Display monthly calendar and system time |
| `./bin/avocado --settings` | Open interactive settings editor |

---

## 📄 License

Distributed under the MIT License.
