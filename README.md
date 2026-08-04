# 🥑 Avocado: Native macOS Terminal Dashboard & CLI App (v2.0.0)

> **Developer:** RnR-io | **Repository:** [https://github.com/RnR-io/Avacado](https://github.com/RnR-io/Avacado)

A pure native macOS terminal dashboard and control center application (CLI & TUI) built for macOS Terminal, iTerm2, Kitty, Alacritty, or zsh/bash. **Zero web servers, zero browsers, zero third-party dependencies required!**

---

## 🖥 Terminal Dashboard Preview (Clean Auto-Scaling Layout)

```
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
│ .---.   GUACA CONTROL CENTER                                                                  │
│ ( (O) ) v2.0.0 | Guaca Mode Active 🥑                                                         │
├──────────────────────────────┬────────────────────────────────┬────────────────────────────────┤
│ Guaca Telemetry                │ Weather                          │ Calendar & Time                  │
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
🥑 Avocado v2.0.0 · Guaca Mode Active · Developer: RnR-io · Repository: https://github.com/RnR-io/Avacado
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

## 🌟 Key Features (v2.0.0)

1. **🥑 Guaca Telemetry & Textured Teardrop Graphic**:
   - Features symmetrical **Avocado Teardrop Shape** ASCII logo filled with organic texture patterns (`---`, `::-::-::`, `░`, `~~~`) and theme-reactive colors.

2. **⚡ Real-Time Live Data Polling (1.0s)**:
   - Full-screen hardware telemetry view polls system load, RAM, APFS disk, battery health/temp, and processes live every 1 second.

3. **🌦 IP Geolocation & Live Weather**:
   - Auto-detects location via IP geolocation and fetches live weather conditions, wind speeds, and dynamic forecast dates.

4. **📐 Full-Window Box Boundary Auto-Scaling**:
   - Outer and inner box grid borders auto-expand to fill full terminal window width (`cols`) smoothly.

---

## 📄 Development & License

- **Developer:** RnR-io
- **Status:** Official v2.0.0 Release (Guaca Mode Active 🥑)
- **License:** Distributed under the MIT License.


