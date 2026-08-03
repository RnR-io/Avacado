/**
 * Settings & Preferences Manager
 */
class SettingsManager {
  constructor() {
    this.defaults = {
      fontFamily: "'JetBrains Mono', monospace",
      fontSize: 14,
      bgOpacity: 90,
      accentColor: "#34c759",
      crtEffect: true,
      refreshRate: 2000,
      tempUnit: "F",
      defaultCity: "San Francisco",
      audioEnabled: true,
      audioVolume: 50,
      useNativeApi: true
    };
    this.config = { ...this.defaults };
  }

  init() {
    this.loadFromStorage();
    this.bindEvents();
    this.applyAllSettings();
  }

  loadFromStorage() {
    const saved = localStorage.getItem('mac_terminal_settings');
    if (saved) {
      try {
        this.config = { ...this.defaults, ...JSON.parse(saved) };
      } catch (e) {}
    }
  }

  saveToStorage() {
    localStorage.setItem('mac_terminal_settings', JSON.stringify(this.config));
  }

  applyAllSettings() {
    const root = document.documentElement;
    root.style.setProperty('--font-family', this.config.fontFamily);
    root.style.setProperty('--font-size', `${this.config.fontSize}px`);
    root.style.setProperty('--accent-color', this.config.accentColor);
    root.style.setProperty('--terminal-bg', `rgba(18, 22, 31, ${this.config.bgOpacity / 100})`);

    if (this.config.crtEffect) {
      document.body.classList.add('crt-effect');
    } else {
      document.body.classList.remove('crt-effect');
    }

    if (window.terminalAudio) {
      window.terminalAudio.enabled = this.config.audioEnabled;
      window.terminalAudio.volume = this.config.audioVolume / 100;
    }

    this.updateFormUI();
  }

  updateFormUI() {
    const elFont = document.getElementById('settingFontFamily');
    const elSize = document.getElementById('settingFontSize');
    const elSizeVal = document.getElementById('fontSizeVal');
    const elOpacity = document.getElementById('settingBgOpacity');
    const elOpacityVal = document.getElementById('bgOpacityVal');
    const elAccent = document.getElementById('settingAccentColor');
    const elCrt = document.getElementById('settingCrtEffect');
    const elRefresh = document.getElementById('settingRefreshRate');
    const elTemp = document.getElementById('settingTempUnit');
    const elCity = document.getElementById('settingDefaultCity');
    const elAudio = document.getElementById('settingAudioEnabled');
    const elVol = document.getElementById('settingAudioVolume');
    const elVolVal = document.getElementById('audioVolVal');
    const elNative = document.getElementById('settingUseNativeApi');

    if (elFont) elFont.value = this.config.fontFamily;
    if (elSize) { elSize.value = this.config.fontSize; if (elSizeVal) elSizeVal.textContent = `${this.config.fontSize}px`; }
    if (elOpacity) { elOpacity.value = this.config.bgOpacity; if (elOpacityVal) elOpacityVal.textContent = `${this.config.bgOpacity}%`; }
    if (elAccent) elAccent.value = this.config.accentColor;
    if (elCrt) elCrt.checked = this.config.crtEffect;
    if (elRefresh) elRefresh.value = this.config.refreshRate;
    if (elTemp) elTemp.value = this.config.tempUnit;
    if (elCity) elCity.value = this.config.defaultCity;
    if (elAudio) elAudio.checked = this.config.audioEnabled;
    if (elVol) { elVol.value = this.config.audioVolume; if (elVolVal) elVolVal.textContent = `${this.config.audioVolume}%`; }
    if (elNative) elNative.checked = this.config.useNativeApi;
  }

  bindEvents() {
    // Modal open / close
    const modal = document.getElementById('settingsModal');
    const btnOpen = document.getElementById('btnSettingsOpen');
    const btnClose = document.getElementById('btnCloseSettings');
    const menuTrigger = document.getElementById('menuSettingsTrigger');

    const openModal = () => modal.classList.add('open');
    const closeModal = () => modal.classList.remove('open');

    if (btnOpen) btnOpen.addEventListener('click', openModal);
    if (menuTrigger) menuTrigger.addEventListener('click', openModal);
    if (btnClose) btnClose.addEventListener('click', closeModal);

    // Tab Switcher
    const tabBtns = document.querySelectorAll('.settings-tabs .tab-btn');
    tabBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const targetTab = btn.dataset.tab;
        document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
        const activeContent = document.getElementById(`tab-${targetTab}`);
        if (activeContent) activeContent.classList.add('active');
      });
    });

    // Save & Reset
    const btnSave = document.getElementById('btnSaveSettings');
    const btnReset = document.getElementById('btnResetSettings');

    if (btnSave) {
      btnSave.addEventListener('click', () => {
        this.config.fontFamily = document.getElementById('settingFontFamily').value;
        this.config.fontSize = parseInt(document.getElementById('settingFontSize').value, 10);
        this.config.bgOpacity = parseInt(document.getElementById('settingBgOpacity').value, 10);
        this.config.accentColor = document.getElementById('settingAccentColor').value;
        this.config.crtEffect = document.getElementById('settingCrtEffect').checked;
        this.config.refreshRate = parseInt(document.getElementById('settingRefreshRate').value, 10);
        this.config.tempUnit = document.getElementById('settingTempUnit').value;
        this.config.defaultCity = document.getElementById('settingDefaultCity').value;
        this.config.audioEnabled = document.getElementById('settingAudioEnabled').checked;
        this.config.audioVolume = parseInt(document.getElementById('settingAudioVolume').value, 10);
        this.config.useNativeApi = document.getElementById('settingUseNativeApi').checked;

        this.saveToStorage();
        this.applyAllSettings();
        closeModal();

        if (window.weatherManager) window.weatherManager.fetchWeather(this.config.defaultCity);
        if (window.statusManager) window.statusManager.startPolling(this.config.refreshRate);
      });
    }

    if (btnReset) {
      btnReset.addEventListener('click', () => {
        this.config = { ...this.defaults };
        this.saveToStorage();
        this.applyAllSettings();
      });
    }

    // Input slider label updates
    const elSize = document.getElementById('settingFontSize');
    if (elSize) elSize.addEventListener('input', e => {
      document.getElementById('fontSizeVal').textContent = `${e.target.value}px`;
    });

    const elOpacity = document.getElementById('settingBgOpacity');
    if (elOpacity) elOpacity.addEventListener('input', e => {
      document.getElementById('bgOpacityVal').textContent = `${e.target.value}%`;
    });

    const elVol = document.getElementById('settingAudioVolume');
    if (elVol) elVol.addEventListener('input', e => {
      document.getElementById('audioVolVal').textContent = `${e.target.value}%`;
    });
  }
}

window.settingsManager = new SettingsManager();
