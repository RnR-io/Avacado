/**
 * Application Main Controller
 */
document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize Settings
  if (window.settingsManager) window.settingsManager.init();

  // 2. Initialize Hardware Status Monitoring
  if (window.statusManager) {
    const refreshRate = window.settingsManager?.config?.refreshRate || 2000;
    window.statusManager.startPolling(refreshRate);
  }

  // 3. Initialize Weather
  if (window.weatherManager) window.weatherManager.init();

  // 4. Initialize News Feed
  if (window.newsManager) window.newsManager.init();

  // 5. Initialize App Switcher Dock
  if (window.appSwitcherManager) window.appSwitcherManager.init();

  // 6. Initialize Terminal CLI
  if (window.terminalCLI) window.terminalCLI.init();

  // 7. Bind Quick Action Toolbar Buttons
  bindToolbarActions();

  // 8. Start Real-time Top Menu Bar Clock & Session Timer
  startClockAndTimers();

  // 9. Bind Global Shortcuts (Cmd+, Cmd+F)
  bindGlobalShortcuts();
});

function bindToolbarActions() {
  const btnTheme = document.getElementById('btnThemeToggle');
  const btnCrt = document.getElementById('btnCrtToggle');
  const btnAudio = document.getElementById('btnAudioToggle');
  const btnExpand = document.getElementById('btnExpandWindow');
  const btnClose = document.getElementById('btnCloseWindow');

  if (btnTheme) {
    btnTheme.addEventListener('click', () => {
      if (window.themeManager) {
        const name = window.themeManager.cycleTheme();
        if (window.terminalCLI) window.terminalCLI.appendLog(`Switched theme to ${name}`, 'output');
      }
    });
  }

  if (btnCrt) {
    btnCrt.addEventListener('click', () => {
      if (window.themeManager) {
        const active = window.themeManager.toggleCrt();
        if (window.terminalCLI) window.terminalCLI.appendLog(`CRT Effect ${active ? 'ON' : 'OFF'}`, 'output');
      }
    });
  }

  if (btnAudio) {
    btnAudio.addEventListener('click', () => {
      if (window.terminalAudio) {
        window.terminalAudio.enabled = !window.terminalAudio.enabled;
        btnAudio.textContent = window.terminalAudio.enabled ? '🔊 Sound' : '🔇 Muted';
      }
    });
  }

  if (btnExpand) {
    btnExpand.addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    });
  }

  if (btnClose) {
    btnClose.addEventListener('click', () => {
      alert("macOS Terminal Dashboard session active. Press Cmd+W or close browser tab to exit.");
    });
  }
}

function startClockAndTimers() {
  const sessionStartTime = Date.now();

  const updateClocks = () => {
    const now = new Date();

    // Top Menu Bar Date & Clock
    const topClock = document.getElementById('topClock');
    const topDate = document.getElementById('topDate');
    if (topClock) topClock.textContent = now.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' });
    if (topDate) topDate.textContent = now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });

    // Panel Large Digital Clock & Date
    const largeClock = document.getElementById('largeClock');
    const largeDate = document.getElementById('largeDate');
    const tzSelect = document.getElementById('tzSelect');

    const tz = (tzSelect && tzSelect.value !== 'local') ? tzSelect.value : undefined;
    if (largeClock) {
      largeClock.textContent = now.toLocaleTimeString('en-US', { timeZone: tz, hour12: false });
    }
    if (largeDate) {
      largeDate.textContent = now.toLocaleDateString('en-US', { timeZone: tz, weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
    }

    // Session Elapsed Timer
    const elapsedSecs = Math.floor((Date.now() - sessionStartTime) / 1000);
    const hrs = String(Math.floor(elapsedSecs / 3600)).padStart(2, '0');
    const mins = String(Math.floor((elapsedSecs % 3600) / 60)).padStart(2, '0');
    const secs = String(elapsedSecs % 60).padStart(2, '0');
    const sessionElapsed = document.getElementById('sessionElapsed');
    if (sessionElapsed) sessionElapsed.textContent = `${hrs}:${mins}:${secs}`;
  };

  updateClocks();
  setInterval(updateClocks, 1000);

  const tzSelect = document.getElementById('tzSelect');
  if (tzSelect) tzSelect.addEventListener('change', updateClocks);
}

function bindGlobalShortcuts() {
  window.addEventListener('keydown', (e) => {
    // Cmd + , (Open Settings)
    if ((e.metaKey || e.ctrlKey) && e.key === ',') {
      e.preventDefault();
      const modal = document.getElementById('settingsModal');
      if (modal) modal.classList.add('open');
    }
  });
}
