# 🥑 Avocado: Native macOS Terminal Dashboard & CLI App

> A pure native macOS terminal dashboard application (CLI & TUI) that runs directly inside macOS Terminal, iTerm2, Kitty, Alacritty, or zsh/bash. **Zero web servers, zero browsers, zero third-party dependencies required!**

---

## 🖥 Terminal Dashboard Preview (3-Column Equal Split Layout)

```
┌───────────────────────────────────┬─────────────────────────────────────┬───────────────────────────────────┐
│ 💻 HARDWARE TELEMETRY             │ 🌦 ASCII WEATHER                    │ 📅 CALENDAR & 12H TIME            │
├───────────────────────────────────┼─────────────────────────────────────┼───────────────────────────────────┤
│ Model: Mac16,8                    │ Kollam, IN                          │ TIME: 03:34:29 PM                 │
│ OS: macOS 26.6                    │ Temp: 28°C (Overcast)               │ Monday, August 03, 2026           │
│ Kernel: Darwin 25.6.0 (arm64)     │ Wind: 16.7 km/h                     │                                   │
│ GPU: Apple M4 Pro                 │                                     │  ┌─┐  ┌─┐     ┌─┐  ┐ ┌     ┌─┐    │
│ CPU: Apple M4 Pro (14 Cores)      │      .--.                           │  │ │   ─┤  🎃   ─┤  └─┤  🎃  ┌─┘    │
│ CPU Load: [█░░░░░░░░░] 11.7%      │   .-(    ).                         │  └─┘  └─┘     └─┘    ┴     └───    │
│ Load Avg: 1.56, 1.30, 1.42        │  (___.__.__)                        │                                   │
│ RAM: [██████████] 23.9/24.0GB     │                                     │ 📅 August 2026                     │
│ RAM Free: 0.1GB | Swap: 0.00M     │ Forecast:                           │    Su Mo Tu We Th Fr Sa           │
│ Disk: [░░░░░░░░░░] 834Gi Free     │  • 08-03: 28°C / 25°C               │                       1           │
│ Battery: 🔋 92% (Battery Power)   │  • 08-04: 29°C / 23°C               │     2 [ 3] 4  5  6  7  8          │
│ IP: 192.168.101.113               │  • 08-05: 28°C / 25°C               │     9 10 11 12 13 14 15           │
│ Uptime: 3 days                    │                                     │    16 17 18 19 20 21 22           │
└───────────────────────────────────┴─────────────────────────────────────┴───────────────────────────────────┘
```

---

## ⚡ 1-Step Quick Installation

### Option 1: One-Line Homebrew Install (Recommended)

```bash
brew install RnR-io/Avacado/avocado
```

---

### Option 2: One-Line Curl Install

```bash
curl -fsSL https://raw.githubusercontent.com/RnR-io/Avacado/main/install.sh | bash
```

Once installed, simply run **`avocado`** (or **`avacado`**) in any terminal window!

---

## 🌟 Key Features

1. **💻 3-Column Equal Split Grid (1/3 Hardware, 1/3 Weather, 1/3 Calendar)**:
   - **Left 1/3**: Laptop Hardware Telemetry (CPU Load, Load Avg, RAM & Swap, APFS Storage, GPU, Battery, Network IP, Uptime).
   - **Middle 1/3**: Live ASCII Weather & 3-Day Forecast.
   - **Right 1/3**: 12-Hour Digital Clock ASCII Banner & Monthly Calendar.

2. **🎮 Interactive Arrow-Key TUI Menu & Menu Settings**:
   - Navigate options with **Up/Down/Left/Right** Arrow keys and **Enter**.
   - Menu-driven settings editor for color themes, temperature units (°C / °F), and location.

3. **🔍 Google Search Launcher**:
   - Search Google directly from terminal (`google <query>` or `g <query>`) in your default browser.

4. **🥑 GitHub Repo Info**:
   - Dedicated repository metadata view (`info` or `github`).

---

## 📄 License

Distributed under the MIT License.
