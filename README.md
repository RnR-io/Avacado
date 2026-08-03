# 🥑 Avocado: Native macOS Terminal Dashboard & CLI App

> A pure native macOS terminal dashboard and control center application (CLI & TUI) built for macOS Terminal, iTerm2, Kitty, Alacritty, or zsh/bash. **Zero web servers, zero browsers, zero third-party dependencies required!**

---

## 🖥 Terminal Dashboard Preview (Clean 3-Column Equal Split Layout)

```
┌───────────────────────────────────┬─────────────────────────────────────┬───────────────────────────────────┐
│ 💻 HARDWARE TELEMETRY             │ 🌦 ASCII WEATHER                    │ 📅 CALENDAR & 12H TIME            │
├───────────────────────────────────┼─────────────────────────────────────┼───────────────────────────────────┤
│ Model: Mac16,8                    │ Kollam                              │ TIME: 04:32:44 PM                 │
│ OS: macOS 26.6                    │ Temp: 26°C (Patchy rain nearby)     │ Monday, August 03, 2026           │
│ Kernel: Darwin 25.6.0 (arm64)     │ Wind: 19 km/h                       │ Week 31                           │
│ GPU: Apple M4 Pro                 │                                     │                                   │
│ CPU: Apple M4 Pro (14 Cores)      │          .--.                       │ 📅 August 2026                     │
│ CPU Load: [█░░░░░░░░░] 11.7%      │       .-(    ).                     │    Su Mo Tu We Th Fr Sa           │
│ Load Avg: 1.72, 2.26, 1.92        │      (___.__.__)                    │                       1           │
│ RAM: [██████████] 22.8/24.0GB     │       /  /  /  /                    │     2 [ 3] 4  5  6  7  8          │
│ RAM Free: 1.2GB | Swap: 0.00M     │      /  /  /  /                     │     9 10 11 12 13 14 15           │
│ Disk: [░░░░░░░░░░] 834Gi Free     │                                     │    16 17 18 19 20 21 22           │
│ Battery: 🔋 86% (Battery Power)   │ Forecast:                           │    23 24 25 26 27 28 29           │
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

## 🌟 Key Features (v1.7.0)

1. **🎨 24-bit TrueColor Image Graphics Engine**:
   - Converts image assets (`assets/avocado_logo.png`) into TrueColor 24-bit RGB Half-Block Matrix (`▄`) or native iTerm2/Kitty graphics protocol, working in 100% of terminal emulators including Apple Terminal.app!

2. **💻 Full-Screen Hardware Telemetry & Real-Time Area Graphs (`avocado --hardware`)**:
   - Multi-line CPU load area chart (`▃▅▂█▅▂▃▄`), load averages (1m/5m/15m), RAM breakdown (used, free, wired, swap), GPU Metal 3 specs, APFS disk capacity, and battery runtime.

3. **📐 Resilient Auto-Scaling Layout Engine**:
   - **Wide Terminals (`cols >= 95`)**: 3-Column Equal Split Layout with strict ANSI truncation.
   - **Compact Terminals (`cols < 95`)**: Stacked Single-Panel Layout to eliminate line wrap and border clipping.

4. **🎮 Interactive Arrow-Key TUI Menu & Settings**:
   - Navigate options with **Up/Down/Left/Right** Arrow keys and **Enter**.
   - Theme customizer (*Avocado*, *Matrix*, *Dracula*, *Ocean*, *Amber*).

5. **🔍 Google Search Launcher**:
   - Search Google directly from terminal (`google <query>` or `g <query>`) in your default browser.

---

## 📄 License

Distributed under the MIT License.
