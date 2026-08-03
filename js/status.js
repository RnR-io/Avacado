/**
 * macOS Hardware Status Manager
 * Interacts with native macOS server daemon (/api/system) or falls back to Web APIs.
 */
class StatusManager {
  constructor() {
    this.timer = null;
  }

  startPolling(intervalMs = 2000) {
    if (this.timer) clearInterval(this.timer);
    this.fetchStatus();
    this.timer = setInterval(() => this.fetchStatus(), intervalMs);
  }

  async fetchStatus() {
    let data = null;
    const useNative = window.settingsManager?.config?.useNativeApi ?? true;

    if (useNative) {
      try {
        const res = await fetch('/api/system', { cache: 'no-store' });
        if (res.ok) {
          data = await res.json();
        }
      } catch (e) {
        // Server daemon offline or running in standalone static browser mode
      }
    }

    if (!data) {
      data = await this.getFallbackWebStatus();
    }

    this.renderStatus(data);
  }

  async getFallbackWebStatus() {
    const cores = navigator.hardwareConcurrency || 8;
    const memory = navigator.deviceMemory || 16;
    
    // Dynamic simulated CPU load variation
    const cpuLoad = (12 + Math.random() * 25).toFixed(1);
    const ramUsed = (memory * 0.45 + Math.random() * 0.8).toFixed(1);
    const ramPct = ((ramUsed / memory) * 100).toFixed(0);

    let battPct = 98;
    let isCharging = true;

    if ('getBattery' in navigator) {
      try {
        const batt = await navigator.getBattery();
        battPct = Math.round(batt.level * 100);
        isCharging = batt.charging;
      } catch (e) {}
    }

    return {
      model: "MacBook Pro (Apple Silicon)",
      os: "macOS Sonoma (Web Bridge)",
      cpu_cores: cores,
      cpu_usage: parseFloat(cpuLoad),
      total_ram_gb: memory,
      used_ram_gb: parseFloat(ramUsed),
      ram_pct: parseFloat(ramPct),
      batt_pct: battPct,
      is_charging: isCharging,
      power_source: isCharging ? "AC Power" : "Battery Power",
      disk_total: "926 GB",
      disk_avail: "834 GB",
      disk_pct: 10,
      uptime: "Up 3h 12m"
    };
  }

  renderStatus(data) {
    const elModel = document.getElementById('sysModel');
    const elBadge = document.getElementById('osBadge');
    const elCores = document.getElementById('cpuCoresVal');
    const elCpuVal = document.getElementById('cpuUsageVal');
    const elCpuBar = document.getElementById('cpuBar');
    const elRamTotal = document.getElementById('ramTotalVal');
    const elRamVal = document.getElementById('ramUsageVal');
    const elRamBar = document.getElementById('ramBar');
    const elDiskTotal = document.getElementById('diskTotalVal');
    const elDiskAvail = document.getElementById('diskAvailVal');
    const elDiskBar = document.getElementById('diskBar');
    const elBattState = document.getElementById('battState');
    const elUptime = document.getElementById('uptimeState');

    if (elModel) elModel.textContent = `${data.model}`;
    if (elBadge) elBadge.textContent = `${data.os}`;
    if (elCores) elCores.textContent = `${data.cpu_cores}`;
    if (elCpuVal) elCpuVal.textContent = `${data.cpu_usage}%`;
    if (elCpuBar) elCpuBar.style.width = `${Math.min(data.cpu_usage, 100)}%`;

    if (elRamTotal) elRamTotal.textContent = `${data.total_ram_gb} GB`;
    if (elRamVal) elRamVal.textContent = `${data.used_ram_gb} GB (${data.ram_pct}%)`;
    if (elRamBar) elRamBar.style.width = `${Math.min(data.ram_pct, 100)}%`;

    if (elDiskTotal) elDiskTotal.textContent = `${data.disk_total}`;
    if (elDiskAvail) elDiskAvail.textContent = `${data.disk_avail} Free`;
    if (elDiskBar) elDiskBar.style.width = `${data.disk_pct}%`;

    if (elBattState) {
      const icon = data.is_charging ? '⚡' : '🔋';
      elBattState.textContent = `${icon} ${data.batt_pct}% (${data.power_source})`;
    }

    if (elUptime) elUptime.textContent = `⏱ ${data.uptime}`;

    // Top menu bar updates
    const topBattVal = document.getElementById('topBattVal');
    if (topBattVal) topBattVal.textContent = `${data.batt_pct}%`;
  }
}

window.statusManager = new StatusManager();
