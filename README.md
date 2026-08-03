# 🥑 Avocado: Native macOS Terminal Dashboard & CLI App

> A pure native macOS terminal dashboard and control center application (CLI & TUI) built for macOS Terminal, iTerm2, Kitty, Alacritty, or zsh/bash. **Zero web servers, zero browsers, zero third-party dependencies required!**

---

## 🖥 Terminal Dashboard Preview (Clean 3-Column Equal Split Layout)

```
┌───────────────────────────────────┬─────────────────────────────────────┬───────────────────────────────────┐
│ 💻 HARDWARE TELEMETRY             │ 🌦 ASCII WEATHER                    │ 📅 CALENDAR & 12H TIME            │
├───────────────────────────────────┼─────────────────────────────────────┼───────────────────────────────────┤
│ Model: Mac16,8                    │ Kollam                              │ TIME: 04:08:06 PM                 │
│ OS: macOS 26.6                    │ Temp: 26°C (Light rain shower)      │ Monday, August 03, 2026           │
│ Kernel: Darwin 25.6.0 (arm64)     │ Wind: 22 km/h                       │ Week 31                           │
│ GPU: Apple M4 Pro                 │                                     │                                   │
│ CPU: Apple M4 Pro (14 Cores)      │          .--.                       │ 📅 August 2026                     │
│ CPU Load: [█░░░░░░░░░] 10.4%      │       .-(    ).                     │    Su Mo Tu We Th Fr Sa           │
│ Load Avg: 1.38, 1.41, 1.37        │      (___.__.__)                    │                       1           │
│ RAM: [██████████] 23.9/24.0GB     │       /  /  /  /                    │     2 [ 3] 4  5  6  7  8          │
│ RAM Free: 0.1GB | Swap: 0.00M     │      /  /  /  /                     │     9 10 11 12 13 14 15           │
│ Disk: [░░░░░░░░░░] 834Gi Free     │                                     │    16 17 18 19 20 21 22           │
│ Battery: 🔋 89% (Battery Power)   │ Forecast:                           │    23 24 25 26 27 28 29           │
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

## 🌟 Key Features (v1.5.0)

1. **💻 Full-Screen Hardware Telemetry & Real-Time Sparkline Graphs (`avocado --hardware`)**:
   - Detailed hardware metrics, real-time CPU sparkline load history graph (`▃▅▂█▅▂▃▄`), system load averages (1m, 5m, 15m), memory breakdown (wired, compressed, swap), GPU Metal 3 specs, APFS storage capacity, battery remaining runtime, and network IP.

2. **🥑 Ultra-Detailed High-Density ASCII Avocado Art & Neofetch**:
   - Multi-line shaded ASCII Avocado Art with inner fruit core shading and seed pit center (`(O)`).

3. **📐 3-Column Equal Split Grid (1/3 Hardware, 1/3 Weather, 1/3 Calendar)**:
   - Clean 3-panel split adapting dynamically to any terminal window size.

4. **🎮 Interactive Arrow-Key TUI Menu & Settings**:
   - Navigate options with **Up/Down/Left/Right** Arrow keys and **Enter**.
   - Menu-driven settings editor for color themes (*Avocado*, *Matrix*, *Dracula*, *Ocean*, *Amber*), temperature units (°C / °F), and location.

5. **🔍 Google Search Launcher**:
   - Search Google directly from terminal (`google <query>` or `g <query>`) in your default browser.

6. **🥑 GitHub Repo Info & About Page**:
   - Dedicated repository metadata view (`info` or `github`).

---

## 🚀 CLI Command Options

| Command | Description |
| :--- | :--- |
| `avocado` | Launch interactive terminal dashboard |
| `avocado --hardware` | Launch Full-Screen Hardware Telemetry & Real-Time Sparkline Graphs Page |
| `avocado --menu` | Launch Arrow-Key TUI Navigation Menu |
| `avocado --once` | Print 3-column dashboard once and exit |
| `avocado --status` | Print hardware telemetry summary |
| `avocado --neofetch` | Display detailed ASCII Avocado Art & system summary |
| `avocado --google "query"` | Search Google in default browser |
| `avocado --github` | Display GitHub repository info & about page |
| `avocado --weather "Tokyo"` | Get weather forecast for any city |
| `avocado --calendar` | Display monthly calendar grid and system time |
| `avocado --settings` | Open interactive settings editor |

---

## 📄 License

Distributed under the MIT License.
