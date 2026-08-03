/**
 * Interactive zsh Terminal CLI Command Interpreter
 */
class TerminalCLI {
  constructor() {
    this.history = [];
    this.historyIdx = -1;
  }

  init() {
    this.bindEvents();
  }

  bindEvents() {
    const form = document.getElementById('cliForm');
    const input = document.getElementById('cliInput');

    if (form && input) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const cmd = input.value.trim();
        if (cmd) {
          this.executeCommand(cmd);
          this.history.push(cmd);
          this.historyIdx = this.history.length;
          input.value = '';
          if (window.terminalAudio) window.terminalAudio.playEnterClick();
        }
      });

      input.addEventListener('keydown', (e) => {
        if (window.terminalAudio && e.key.length === 1) {
          window.terminalAudio.playKeyClick();
        }

        if (e.key === 'ArrowUp') {
          e.preventDefault();
          if (this.historyIdx > 0) {
            this.historyIdx--;
            input.value = this.history[this.historyIdx];
          }
        } else if (e.key === 'ArrowDown') {
          e.preventDefault();
          if (this.historyIdx < this.history.length - 1) {
            this.historyIdx++;
            input.value = this.history[this.historyIdx];
          } else {
            this.historyIdx = this.history.length;
            input.value = '';
          }
        }
      });
    }
  }

  executeCommand(cmdStr) {
    this.appendLog(`user@macbook-pro ~ % ${cmdStr}`, 'prompt');
    const parts = cmdStr.split(/\s+/);
    const cmd = parts[0].toLowerCase();
    const args = parts.slice(1);

    switch (cmd) {
      case 'help':
        this.appendLog(`Available Terminal Commands:
  • neofetch / macfetch - Display Apple ASCII logo and system info
  • status             - Print detailed hardware system status
  • weather [city]     - Search weather forecast for city
  • news [category]    - Load latest tech or world news
  • apps               - List all installed favorite app shortcuts
  • open [name|index]  - Launch favorite app by name or shortcut number
  • settings           - Open Preferences & Customization modal
  • theme              - Cycle through macOS Terminal color themes
  • crt                - Toggle CRT scanline visual effect
  • matrix             - Launch Matrix digital rain screensaver (press Esc to exit)
  • clear              - Clear terminal output buffer
  • date / time        - Display current system date & time`, 'output');
        break;

      case 'neofetch':
      case 'macfetch':
        this.renderNeofetch();
        break;

      case 'status':
        if (window.statusManager) {
          window.statusManager.fetchStatus();
          this.appendLog('Refreshing macOS system hardware metrics...', 'output');
        }
        break;

      case 'weather':
        const city = args.join(' ') || 'San Francisco';
        if (window.weatherManager) {
          window.weatherManager.fetchWeather(city);
          this.appendLog(`Fetching weather for '${city}'...`, 'output');
        }
        break;

      case 'news':
        const cat = args[0] || 'tech';
        if (window.newsManager) {
          window.newsManager.fetchNews(cat);
          this.appendLog(`Loading news feed for '${cat}'...`, 'output');
        }
        break;

      case 'apps':
        if (window.appSwitcherManager) {
          const list = window.appSwitcherManager.apps.map((a, i) => ` [${i + 1}] ${a.icon} ${a.title} -> ${a.url}`).join('\n');
          this.appendLog(`Installed App Shortcuts:\n${list}`, 'output');
        }
        break;

      case 'open':
        const target = args.join(' ');
        if (!target) {
          this.appendLog('Usage: open [app_name | shortcut_number]', 'output');
        } else if (window.appSwitcherManager) {
          const app = window.appSwitcherManager.openAppByName(target);
          if (app) {
            this.appendLog(`Launching ${app.icon} ${app.title} (${app.url})...`, 'output');
          } else {
            this.appendLog(`App shortcut '${target}' not found. Type 'apps' to see all.`, 'output');
          }
        }
        break;

      case 'settings':
        const modal = document.getElementById('settingsModal');
        if (modal) modal.classList.add('open');
        this.appendLog('Opened Terminal Settings & Preferences panel.', 'output');
        break;

      case 'theme':
        if (window.themeManager) {
          const name = window.themeManager.cycleTheme();
          this.appendLog(`Switched theme to '${name}'`, 'output');
        }
        break;

      case 'crt':
        if (window.themeManager) {
          const isCrt = window.themeManager.toggleCrt();
          this.appendLog(`CRT scanline effect ${isCrt ? 'ENABLED' : 'DISABLED'}`, 'output');
        }
        break;

      case 'matrix':
        this.startMatrixRain();
        this.appendLog('Matrix digital rain active. Press [Esc] to exit.', 'output');
        break;

      case 'clear':
        const log = document.getElementById('cliLog');
        if (log) log.innerHTML = '';
        break;

      case 'date':
      case 'time':
        this.appendLog(new Date().toString(), 'output');
        break;

      default:
        this.appendLog(`zsh: command not found: ${cmd}. Type 'help' for available commands.`, 'output');
        break;
    }

    this.scrollToBottom();
  }

  renderNeofetch() {
    const art = `
    <span style="color:#ff5f56">                .o888a</span>          user@macbook-pro
    <span style="color:#ff5f56">              a8888"</span>            ----------------
    <span style="color:#27c93f">             888888</span>             OS: macOS Sonoma 26.6 (arm64)
    <span style="color:#27c93f">             888888888a</span>         Host: MacBook Pro 16" (Mac16,8)
    <span style="color:#ffbd2e">     a8888888888888888888</span>       Kernel: Darwin 23.5.0
    <span style="color:#ffbd2e">   .888888888888888888888</span>       Uptime: 2 hours, 15 mins
    <span style="color:#007aff">  .8888888888888888888888</span>       Shell: zsh 5.9
    <span style="color:#007aff">  88888888888888888888888</span>       CPU: Apple M3 Max (14 Cores)
    <span style="color:#af52de">  88888888888888888888888</span>       Memory: 11.2 GB / 24.0 GB
    <span style="color:#af52de">   "8888888888888888888"</span>        Battery: 99% (AC Power)
    <span style="color:#34c759">     "888888888888888"</span>          Terminal: Antigravity Terminal v2.0
    `;
    this.appendLog(art, 'output');
  }

  startMatrixRain() {
    const canvas = document.getElementById('matrixCanvas');
    if (!canvas) return;

    canvas.classList.remove('hidden');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const chars = '0123456789ABCDEFｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ';
    const fontSize = 14;
    const columns = Math.floor(canvas.width / fontSize);
    const drops = Array(columns).fill(1);

    const draw = () => {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = '#00ff66';
      ctx.font = `${fontSize}px monospace`;

      for (let i = 0; i < drops.length; i++) {
        const text = chars.charAt(Math.floor(Math.random() * chars.length));
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    };

    const interval = setInterval(draw, 33);

    const exitMatrix = (e) => {
      if (e.key === 'Escape') {
        clearInterval(interval);
        canvas.classList.add('hidden');
        window.removeEventListener('keydown', exitMatrix);
      }
    };
    window.addEventListener('keydown', exitMatrix);
  }

  appendLog(msg, type = 'output') {
    const log = document.getElementById('cliLog');
    if (!log) return;

    const line = document.createElement('div');
    line.className = `cli-line ${type}`;
    if (type === 'output' && msg.includes('<span')) {
      line.innerHTML = `<pre style="font-family:inherit;margin:0;">${msg}</pre>`;
    } else {
      line.textContent = msg;
    }
    log.appendChild(line);
  }

  scrollToBottom() {
    const container = document.getElementById('cliOutputContainer');
    if (container) container.scrollTop = container.scrollHeight;
  }
}

window.terminalCLI = new TerminalCLI();
