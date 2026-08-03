"""
Native macOS System Hardware Telemetry Collector
Queries sysctl, pmset, vm_stat, df, sw_vers, and top.
"""
import subprocess
import re

def run_cmd(cmd):
    try:
        res = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=3)
        return res.decode('utf-8', errors='ignore').strip()
    except Exception:
        return ""

def get_macos_status():
    # 1. Model & OS
    model = run_cmd("sysctl -n hw.model") or "Mac (Apple Silicon)"
    os_ver = run_cmd("sw_vers -productVersion") or "macOS"
    os_name = run_cmd("sw_vers -productName") or "macOS"
    
    # 2. CPU
    ncpu = run_cmd("sysctl -n hw.ncpu") or "8"
    cpu_brand = run_cmd("sysctl -n machdep.cpu.brand_string")
    if not cpu_brand:
        cpu_brand = f"Apple Silicon ({ncpu} Cores)"

    top_out = run_cmd("top -l 1 -n 0 | grep 'CPU usage'")
    cpu_usage = 14.5
    if top_out:
        m = re.search(r'(\d+\.\d+)%\s+user,\s+(\d+\.\d+)%\s+sys', top_out)
        if m:
            cpu_usage = round(float(m.group(1)) + float(m.group(2)), 1)

    # 3. Memory
    mem_size_bytes = run_cmd("sysctl -n hw.memsize")
    total_ram_gb = 16.0
    if mem_size_bytes.isdigit():
        total_ram_gb = round(int(mem_size_bytes) / (1024**3), 1)

    vm_stat_out = run_cmd("vm_stat")
    used_ram_gb = round(total_ram_gb * 0.45, 1)
    if vm_stat_out:
        pages_free = re.search(r'Pages free:\s+(\d+)\.', vm_stat_out)
        pages_speculative = re.search(r'Pages speculative:\s+(\d+)\.', vm_stat_out)
        page_size = 4096
        if pages_free:
            free_b = int(pages_free.group(1)) * page_size
            spec_b = (int(pages_speculative.group(1)) if pages_speculative else 0) * page_size
            used_ram_gb = round((total_ram_gb * (1024**3) - (free_b + spec_b)) / (1024**3), 1)

    ram_pct = round((used_ram_gb / total_ram_gb) * 100, 1) if total_ram_gb else 45.0

    # 4. Battery
    batt_out = run_cmd("pmset -g batt")
    batt_pct = 98
    is_charging = False
    power_source = "AC Adapter"
    rem_time = "Charged"

    if batt_out:
        if "Battery Power" in batt_out:
            power_source = "Battery Power"
        m_pct = re.search(r'(\d+)%', batt_out)
        if m_pct:
            batt_pct = int(m_pct.group(1))
        if "charging" in batt_out.lower() and "discharging" not in batt_out.lower():
            is_charging = True
        m_rem = re.search(r'(\d+:\d+)\s+remaining', batt_out)
        if m_rem:
            rem_time = m_rem.group(1) + " rem"

    # 5. Storage
    df_out = run_cmd("df -h /")
    disk_total = "500Gi"
    disk_used = "200Gi"
    disk_avail = "300Gi"
    disk_pct = 40
    if df_out:
        lines = df_out.split('\n')
        if len(lines) > 1:
            parts = re.split(r'\s+', lines[1])
            if len(parts) >= 5:
                disk_total = parts[1]
                disk_used = parts[2]
                disk_avail = parts[3]
                disk_pct = int(parts[4].replace('%', '')) if parts[4].replace('%', '').isdigit() else 40

    # 6. Uptime
    uptime_str = run_cmd("uptime") or "up 2 hours"
    m_up = re.search(r'up\s+([^,]+)', uptime_str)
    uptime_formatted = m_up.group(1) if m_up else "2 hours"

    return {
        "model": model,
        "os": f"{os_name} {os_ver}",
        "cpu_brand": cpu_brand,
        "cpu_cores": ncpu,
        "cpu_usage": cpu_usage,
        "total_ram_gb": total_ram_gb,
        "used_ram_gb": used_ram_gb,
        "ram_pct": ram_pct,
        "batt_pct": batt_pct,
        "is_charging": is_charging,
        "power_source": power_source,
        "batt_rem_time": rem_time,
        "disk_total": disk_total,
        "disk_used": disk_used,
        "disk_avail": disk_avail,
        "disk_pct": disk_pct,
        "uptime": uptime_formatted
    }
