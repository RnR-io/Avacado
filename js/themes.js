/**
 * Themes & CRT Effects Manager
 */
class ThemeManager {
  constructor() {
    this.themes = [
      { id: 'macos-pro', name: 'macOS Pro Dark', bg: '#0b0d12', accent: '#34c759' },
      { id: 'homebrew', name: 'Homebrew Green', bg: '#000000', accent: '#00ff66' },
      { id: 'dracula', name: 'Dracula Cyber', bg: '#1e1e2e', accent: '#cba6f7' },
      { id: 'ocean', name: 'Ocean Blue', bg: '#0f172a', accent: '#38bdf8' },
      { id: 'amber', name: 'Retro Amber', bg: '#0d0d0d', accent: '#ffb000' }
    ];
    this.currentIdx = 0;
  }

  setTheme(themeId) {
    const theme = this.themes.find(t => t.id === themeId) || this.themes[0];
    document.body.className = `theme-${theme.id} ${document.body.classList.contains('crt-effect') ? 'crt-effect' : ''}`;
    document.documentElement.style.setProperty('--accent-color', theme.accent);
    document.documentElement.style.setProperty('--accent-glow', `${theme.accent}4d`);
    this.currentIdx = this.themes.indexOf(theme);
    localStorage.setItem('mac_terminal_theme', theme.id);
  }

  cycleTheme() {
    this.currentIdx = (this.currentIdx + 1) % this.themes.length;
    this.setTheme(this.themes[this.currentIdx].id);
    return this.themes[this.currentIdx].name;
  }

  toggleCrt() {
    document.body.classList.toggle('crt-effect');
    const isCrt = document.body.classList.contains('crt-effect');
    localStorage.setItem('mac_terminal_crt', isCrt ? 'true' : 'false');
    return isCrt;
  }
}

window.themeManager = new ThemeManager();
