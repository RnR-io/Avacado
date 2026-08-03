/**
 * App Switcher & Favorites Launcher Manager
 */
class AppSwitcherManager {
  constructor() {
    this.defaults = [
      { id: '1', title: 'GitHub', url: 'https://github.com', icon: '🐙' },
      { id: '2', title: 'VS Code', url: 'https://vscode.dev', icon: '💻' },
      { id: '3', title: 'ChatGPT', url: 'https://chatgpt.com', icon: '🤖' },
      { id: '4', title: 'YouTube', url: 'https://youtube.com', icon: '▶️' },
      { id: '5', title: 'Spotify', url: 'https://open.spotify.com', icon: '🎵' },
      { id: '6', title: 'Gmail', url: 'https://mail.google.com', icon: '✉️' },
      { id: '7', title: 'X / Twitter', url: 'https://x.com', icon: '🐦' },
      { id: '8', title: 'Figma', url: 'https://figma.com', icon: '🎨' },
      { id: '9', title: 'Notion', url: 'https://notion.so', icon: '📝' }
    ];
    this.apps = [];
  }

  init() {
    this.loadFromStorage();
    this.bindEvents();
    this.renderDock();
  }

  loadFromStorage() {
    const saved = localStorage.getItem('mac_terminal_apps');
    if (saved) {
      try {
        this.apps = JSON.parse(saved);
      } catch (e) {
        this.apps = [...this.defaults];
      }
    } else {
      this.apps = [...this.defaults];
    }
  }

  saveToStorage() {
    localStorage.setItem('mac_terminal_apps', JSON.stringify(this.apps));
  }

  renderDock() {
    const dock = document.getElementById('appsDock');
    if (!dock) return;

    dock.innerHTML = '';
    this.apps.forEach((app, idx) => {
      const card = document.createElement('a');
      card.className = 'app-card';
      card.href = app.url;
      card.target = '_blank';
      card.rel = 'noopener noreferrer';
      card.innerHTML = `
        <span class="app-badge">${idx + 1}</span>
        <span class="app-icon">${app.icon || '🌐'}</span>
        <span class="app-title">${app.title}</span>
      `;
      card.addEventListener('click', () => {
        if (window.terminalAudio) window.terminalAudio.playKeyClick();
      });
      dock.appendChild(card);
    });
  }

  bindEvents() {
    const modal = document.getElementById('addAppModal');
    const btnTrigger = document.getElementById('btnAddAppTrigger');
    const btnClose = document.getElementById('btnCloseAddApp');
    const btnCancel = document.getElementById('btnCancelAddApp');
    const form = document.getElementById('addAppForm');

    const openModal = () => modal.classList.add('open');
    const closeModal = () => modal.classList.remove('open');

    if (btnTrigger) btnTrigger.addEventListener('click', openModal);
    if (btnClose) btnClose.addEventListener('click', closeModal);
    if (btnCancel) btnCancel.addEventListener('click', closeModal);

    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const title = document.getElementById('newAppName').value.trim();
        const url = document.getElementById('newAppUrl').value.trim();
        const icon = document.getElementById('newAppIcon').value.trim() || '🌐';

        if (title && url) {
          this.apps.push({
            id: String(this.apps.length + 1),
            title,
            url,
            icon
          });
          this.saveToStorage();
          this.renderDock();
          form.reset();
          closeModal();
        }
      });
    }

    // Number key shortcuts (1-9) to launch favorite app
    window.addEventListener('keydown', (e) => {
      // Ignore keybindings if typing inside input / textarea
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) return;
      if (e.key >= '1' && e.key <= '9') {
        const idx = parseInt(e.key, 10) - 1;
        if (idx < this.apps.length) {
          window.open(this.apps[idx].url, '_blank');
        }
      }
    });
  }

  openAppByName(nameOrIndex) {
    if (!nameOrIndex) return false;
    const query = nameOrIndex.toLowerCase();
    
    // Check by number index
    if (/^\d+$/.test(query)) {
      const idx = parseInt(query, 10) - 1;
      if (idx >= 0 && idx < this.apps.length) {
        window.open(this.apps[idx].url, '_blank');
        return this.apps[idx];
      }
    }

    // Check by app title matching
    const match = this.apps.find(a => a.title.toLowerCase().includes(query));
    if (match) {
      window.open(match.url, '_blank');
      return match;
    }
    return null;
  }
}

window.appSwitcherManager = new AppSwitcherManager();
