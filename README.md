# 🥑 Avocado: Native macOS Terminal Dashboard & CLI App

> A pure native macOS terminal dashboard application (CLI & TUI) that runs directly inside macOS Terminal, iTerm2, Kitty, Alacritty, or zsh/bash. **Zero web servers, zero browsers, zero third-party dependencies required!**

---

## 🖥 Terminal Dashboard Preview (Clean 3-Column Equal Split Layout)

```
┌───────────────────────────────────┬─────────────────────────────────────┬───────────────────────────────────┐
│ 💻 HARDWARE TELEMETRY             │ 🌦 ASCII WEATHER                    │ 📅 CALENDAR & 12H TIME            │
├───────────────────────────────────┼─────────────────────────────────────┼───────────────────────────────────┤
│ Model: Mac16,8                    │ Kollam                              │ TIME: 04:04:02 PM                 │
│ OS: macOS 26.6                    │ Temp: 26°C (Light rain shower)      │ Monday, August 03, 2026           │
│ Kernel: Darwin 25.6.0 (arm64)     │ Wind: 22 km/h                       │ Week 31                           │
│ GPU: Apple M4 Pro                 │                                     │                                   │
│ CPU: Apple M4 Pro (14 Cores)      │          .--.                       │ 📅 August 2026                     │
│ CPU Load: [█░░░░░░░░░] 10.8%      │       .-(    ).                     │    Su Mo Tu We Th Fr Sa           │
│ Load Avg: 1.20, 1.25, 1.32        │      (___.__.__)                    │                       1           │
│ RAM: [██████████] 23.7/24.0GB     │       /  /  /  /                    │     2 [ 3] 4  5  6  7  8          │
│ RAM Free: 0.3GB | Swap: 0.00M     │      /  /  /  /                     │     9 10 11 12 13 14 15           │
│ Disk: [░░░░░░░░░░] 834Gi Free     │                                     │    16 17 18 19 20 21 22           │
│ Battery: 🔋 90% (Battery Power)   │ Forecast:                           │    23 24 25 26 27 28 29           │
│ IP: 192.168.101.113               │  • 08-03: 26°C / 25°C               │    30 31                          │
│ Uptime: 3 days                    │  • 08-04: 25°C / 24°C               │                                   │
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

1. **🥑 Ultra-Detailed ASCII Avocado Art & Neofetch**:
   - High-density shaded ASCII Avocado Art with inner fruit core shading and seed pit center (`O` / `(O)`).

2. **📅 Clean Calendar Column**:
   - Clean 12-Hour system time display and monthly calendar grid without cluttered ASCII art numbers above the calendar.

3. **🎮 Interactive Arrow-Key TUI Menu & Menu Settings**:
   - Navigate options with **Up/Down/Left/Right** Arrow keys and **Enter**.
   - Menu-driven settings editor for color themes, temperature units (°C / °F), and location.

4. **🔍 Google Search Launcher**:
   - Search Google directly from terminal (`google <query>` or `g <query>`) in your default browser.

5. **🥑 GitHub Repo Info**:
   - Dedicated repository metadata view (`info` or `github`).

---

## 📄 License

Distributed under the MIT License.
