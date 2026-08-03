# 🥑 Avocado: Native macOS Terminal Dashboard & CLI App

> A pure native macOS terminal dashboard application (CLI & TUI) that runs directly inside macOS Terminal, iTerm2, Kitty, Alacritty, or zsh/bash. **Zero web servers, zero browsers, zero third-party dependencies required!**

---

## ⚡ 1-Step Quick Installation

### Option 1: One-Line Curl Install (Simplest — Works Anywhere)

Copy & paste this single command into your terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/RnR-io/Avacado/main/install.sh | bash
```

---

### Option 2: One-Line Homebrew Install

```bash
brew install RnR-io/Avacado/avocado
```

Once installed, simply run **`avocado`** in any terminal window!

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

4. **⚡ Seamless Keyboard Navigation**:
   - **Up/Down Arrow History**: Cycle through all typed commands (`readline`).
   - **Tab Autocompletion**: Autocomplete command names.
   - **Single-Key Shortcuts**: Quick keys `[r]`efresh, `[s]`ettings, `[c]`alendar, `[w]`eather, `[n]`eofetch, `[q]`uit.

5. **⚙️ Terminal Settings & Config**:
   - Configure ANSI color themes (*Avocado Green*, *Matrix*, *Dracula*, *Ocean*, *Amber*), temperature units (°C / °F), and location saved securely in `~/.config/avocado/config.json`.

---

## 🚀 Terminal Commands & Usage

| Command | Description |
| :--- | :--- |
| `avocado` | Launch interactive terminal dashboard |
| `avocado --once` | Print dashboard layout once and exit |
| `avocado --status` | Print expanded hardware telemetry summary |
| `avocado --neofetch` | Display Apple ASCII logo and hardware specs |
| `avocado --weather "Tokyo"` | Get weather forecast for any city |
| `avocado --calendar` | Display monthly calendar grid and system time |
| `avocado --settings` | Open interactive settings editor |

---

## 📄 License

Distributed under the MIT License.
