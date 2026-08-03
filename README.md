#  macOS Terminal Dashboard & Landing Page

> An authentic macOS terminal-themed dashboard and browser landing page displaying live laptop hardware metrics, real-time weather, tech news, digital clock, favorite app launcher dock, and an interactive `zsh` command line prompt.

---

## 🌟 Key Features

1. **Native macOS System Hardware Monitoring**:
   - Queries official macOS shell APIs (`pmset`, `sysctl`, `vm_stat`, `df`, `sw_vers`).
   - Displays real-time **CPU usage %**, **Apple Silicon / Intel model**, **Memory RAM usage**, **APFS Disk storage**, **Battery % (AC / Battery state)**, and **System Uptime**.

2. **Full Settings & Preferences Panel (`Cmd+,`)**:
   - **Font Customization**: Choose between `JetBrains Mono`, `Fira Code`, `Share Tech Mono` (Retro), `SF Mono` (macOS native), or `Courier New`.
   - **Font Size & Scale**: Slider adjustments from 11px to 22px.
   - **Terminal Opacity & Blur**: Glassmorphic blur slider (50% to 100%).
   - **Theme Palettes**: Switch between *macOS Pro Dark*, *Homebrew Matrix Green*, *Dracula Cyber*, *Ocean Blue*, and *Retro Amber*.
   - **Audio & Mechanical Keypress Sound FX**: Synthesized retro keypress audio feedback with volume controls.
   - **Weather Units**: Toggle between Fahrenheit (°F) and Celsius (°C).

3. **Live Weather Widget**:
   - Powered by Open-Meteo API (free, open, no API key required).
   - Global city search & 5-day weather forecasts with weather condition icons.

4. **Tech & World News Aggregator**:
   - Hacker News top stories feed & tech headlines.
   - Live search filter & direct article links.

5. **Favorite App Switcher & Dock Launcher**:
   - Quick launch cards for GitHub, VS Code, ChatGPT, YouTube, Spotify, Gmail, X, Figma, Notion.
   - Keyboard shortcuts (`1`–`9`) to launch any app instantly.
   - Custom app editor modal to add/remove your own web & app shortcuts.

6. **Interactive `zsh` CLI Prompt & Commands**:
   - Command prompt: `user@macbook-pro ~ %`
   - Commands: `help`, `neofetch`, `status`, `weather [city]`, `news [category]`, `apps`, `open [app]`, `settings`, `theme`, `crt`, `matrix`, `clear`.
   - Matrix digital rain screensaver (`matrix` command).

---

## 📦 Homebrew Installation

### Via Homebrew (Tap & Install)

```bash
# Tap the repository formula
brew tap RnR-io/mac-terminal-app

# Install mac-terminal-dashboard
brew install mac-terminal-dashboard

# Run the launcher CLI
mac-terminal-dashboard
```

---

## 🚀 Quick Start (Local Setup)

### Option 1: Direct Script Launch (Zero Dependencies)

```bash
# Clone repository
git clone https://github.com/RnR-io/mac-terminal-app.git
cd "mac terminal app"

# Run executable launcher
./bin/mac-terminal-app
```

The launcher will start the Python native system backend on `http://127.0.0.1:8765` and open your default browser.

### Option 2: Using NPM

```bash
npm start
```

---

## ⚙️ Interactive Terminal Commands

Inside the terminal command line prompt (`user@macbook-pro ~ %`):

| Command | Description |
| :--- | :--- |
| `help` | Display all available CLI commands |
| `neofetch` / `macfetch` | Render Apple ASCII logo with hardware specifications |
| `status` | Refresh and display laptop hardware metrics |
| `weather [city]` | Search and view weather forecast for any city |
| `news [category]` | Load latest headlines (`tech`, `hn`, `dev`) |
| `apps` | List all installed favorite app shortcuts |
| `open [app\|number]` | Launch favorite app by name or key index (`open 1` or `open github`) |
| `settings` | Open Settings & Preferences modal |
| `theme` | Cycle through terminal color themes |
| `crt` | Toggle CRT retro scanline effect |
| `matrix` | Launch full-screen Matrix rain animation |
| `clear` | Clear terminal console buffer |

---

## 🛠 Project Structure

```
.
├── Formula/
│   └── mac-terminal-dashboard.rb   # Homebrew Formula
├── bin/
│   └── mac-terminal-app            # Executable launcher binary
├── js/
│   ├── app.js                      # Core app initialization & timers
│   ├── audio.js                    # Web Audio mechanical key click synthesizer
│   ├── appswitcher.js              # Favorite app switcher dock & shortcut manager
│   ├── news.js                     # News aggregator feed
│   ├── settings.js                 # Settings & Preferences modal manager
│   ├── status.js                   # Hardware status (Native API + Web fallback)
│   ├── terminal.js                 # Interactive zsh CLI prompt & interpreter
│   ├── themes.js                   # Theme palettes & CRT scanline effects
│   └── weather.js                  # Open-Meteo weather API integration
├── index.html                      # Terminal dashboard HTML structure
├── index.css                       # macOS styling, glassmorphism & themes
├── server.py                       # Native macOS system API backend server
├── package.json                    # Package metadata & script targets
├── .gitignore                      # Git ignored files
└── README.md                       # Project documentation
```

---

## 📄 License

Distributed under the MIT License.
