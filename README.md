# 🥑 Avocado: Native macOS Terminal Dashboard & CLI App (v2.0.0 Public Beta)

> **Project Status: Public Beta Release (v2.0.0)**  
> **Developer:** RnR-io | **Repository:** [https://github.com/RnR-io/Avacado](https://github.com/RnR-io/Avacado)

A pure native macOS terminal dashboard and control center application (CLI & TUI) built for macOS Terminal, iTerm2, Kitty, Alacritty, or zsh/bash. **Zero web servers, zero browsers, zero third-party dependencies required!**

---

## 🖥 Terminal Dashboard Preview (Clean Auto-Scaling Layout)

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│ .---.   AVOCADO CONTROL CENTER [BETA]                                                         │
│ ( (O) ) v2.0.0 Beta Release | Live Native macOS Telemetry                                      │
├──────────────────────────────┬────────────────────────────────┬────────────────────────────────┤
│ Hardware Telemetry             │ Weather                          │ Calendar & Time                  │
├──────────────────────────────┼────────────────────────────────┼────────────────────────────────┤
│ Model: Mac16,8                 │ Kollam                           │ TIME: 12:23:56 PM                │
│ OS: macOS 26.6                 │ Temp: 27°C (Light rain shower)   │ Tuesday, August 04, 2026         │
│ Chip: Apple M4 Pro             │ Wind: 22 km/h                    │ Week 31                          │
│ GPU: Apple M4 Pro              │                                  │                                  │
│ CPU Load: [█░░░░░░░] 12.3%     │          .--.                    │ 📅 August 2026                    │
│ RAM: [█░░░░░░░] 3.6/24.0G      │       .-(    ).                  │    Su Mo Tu We Th Fr Sa          │
│ Free: 20.4G | Cache: 0.1G      │      (___.__.__)                 │                       1          │
│ Disk: [█░░░░░░░] 828.5G Free   │       /  /  /  /                 │     2  3 [ 4] 5  6  7  8         │
│ Battery: 🔋 51% (Discharging)   │      /  /  /  /                  │     9 10 11 12 13 14 15          │
│ IP: 192.168.101.113            │                                  │    16 17 18 19 20 21 22          │
│ Uptime: 4 days                 │ Forecast:                        │    23 24 25 26 27 28 29          │
│                                │  • 08-04: 27°C / 25°C            │    30 31                         │
│                                │  • 08-05: 27°C / 25°C            │                                  │
│                                │  • 08-06: 28°C / 25°C            │                                  │
└──────────────────────────────┴────────────────────────────────┴────────────────────────────────┘
🥑 Avocado v2.0.0 (Beta) · Developer: RnR-io · Repository: https://github.com/RnR-io/Avacado
```

---

## ⚡ Quick Installation & Launch

### Option 1: One-Line Homebrew Install

```bash
brew install RnR-io/Avacado/avocado
```

### Option 2: One-Line Curl Install

```bash
curl -fsSL https://raw.githubusercontent.com/RnR-io/Avacado/main/install.sh | bash
```

Once installed, run **`avocado`** (or **`avacado`**) in any terminal window!

---

## 🌟 Key Features (v2.0.0 Beta)

1. **💻 Live 2-Column Hardware Telemetry Page (`avocado --hardware`)**:
   - Displays real-time macOS system load, per-core CPU breakdown (`Core1`, `Core10`), Apple Silicon P+E core layout (`10P+4E`), Memory (Used, Free, Cache), APFS disk metrics, battery health (100%), power source, cycle count, temperature, top 3 real processes, network throughput (Down/Up MB/s), local IP, and a theme-colored Avocado ASCII top logo.

2. **🥑 Multi-Color Gradient ASCII Avocado Graphic**:
   - Custom high-density ASCII avocado logo featuring vertical multi-color gradient transitions (Green -> Lime -> Gold -> Red/Orange -> Purple -> Soft Blue).

3. **🌦 IP Geolocation & Live Weather**:
   - Auto-detects location via IP geolocation and fetches live weather conditions, wind speeds, and dynamic forecast dates.

4. **📐 Full-Window Box Boundary Auto-Scaling**:
   - Outer and inner box grid borders auto-expand to fill the full terminal window width (`cols`) smoothly when opened or resized.

5. **ℹ️ Version Info Command**:
   - Run `avocado -v` or `avocado --version` to display instant version and build information.

---

## 📄 Development & License

- **Developer:** RnR-io
- **Status:** Public Beta Project
- **License:** Distributed under the MIT License.

