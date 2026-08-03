#!/usr/bin/env python3
"""
macOS Terminal Dashboard Backend & Static Server
Provides native macOS system metrics via shell commands (pmset, sysctl, vm_stat, df, sw_vers)
and serves static web files.
"""

import http.server
import socketserver
import json
import subprocess
import re
import urllib.parse
import urllib.request
import os
import sys

PORT = 8765

def run_cmd(cmd):
    try:
        res = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=3)
        return res.decode('utf-8', errors='ignore').strip()
    except Exception as e:
        return ""

def get_macos_status():
    # 1. OS & Model
    model = run_cmd("sysctl -n hw.model") or "Mac (Apple Silicon/Intel)"
    os_ver = run_cmd("sw_vers -productVersion") or "macOS"
    os_name = run_cmd("sw_vers -productName") or "macOS"
    os_full = f"{os_name} {os_ver}"
    
    # 2. CPU
    ncpu = run_cmd("sysctl -n hw.ncpu") or "8"
    cpu_brand = run_cmd("sysctl -n machdep.cpu.brand_string")
    if not cpu_brand:
        cpu_brand = f"Apple Silicon ({ncpu} Cores)"
    
    # Simple CPU load estimation via top
    top_out = run_cmd("top -l 1 -n 0 | grep 'CPU usage'")
    cpu_usage = 15.0
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
    used_ram_gb = round(total_ram_gb * 0.45, 1) # Default sensible estimate
    if vm_stat_out:
        pages_free = re.search(r'Pages free:\s+(\d+)\.', vm_stat_out)
        pages_active = re.search(r'Pages active:\s+(\d+)\.', vm_stat_out)
        pages_inactive = re.search(r'Pages inactive:\s+(\d+)\.', vm_stat_out)
        pages_speculative = re.search(r'Pages speculative:\s+(\d+)\.', vm_stat_out)
        pages_wired = re.search(r'Pages wired down:\s+(\d+)\.', vm_stat_out)
        pages_compressed = re.search(r'Pages occupied by compressor:\s+(\d+)\.', vm_stat_out)
        
        page_size = 4096
        if pages_free and pages_active and pages_wired:
            free_b = int(pages_free.group(1)) * page_size
            spec_b = (int(pages_speculative.group(1)) if pages_speculative else 0) * page_size
            total_free_b = free_b + spec_b
            used_ram_gb = round((total_ram_gb * (1024**3) - total_free_b) / (1024**3), 1)

    ram_pct = round((used_ram_gb / total_ram_gb) * 100, 1) if total_ram_gb else 45.0

    # 4. Battery
    batt_out = run_cmd("pmset -g batt")
    batt_pct = 95
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
            rem_time = m_rem.group(1) + " remaining"

    # 5. Disk Storage
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
    uptime_formatted = m_up.group(1) if m_up else "1 hour"

    return {
        "model": model,
        "os": os_full,
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

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/system':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            data = get_macos_status()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return
        elif parsed.path == '/api/hn':
            # Proxy Hacker News top stories
            try:
                req = urllib.request.urlopen("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=4)
                ids = json.loads(req.read().decode('utf-8'))[:12]
                stories = []
                for item_id in ids[:8]:
                    try:
                        s_req = urllib.request.urlopen(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json", timeout=2)
                        s_data = json.loads(s_req.read().decode('utf-8'))
                        if s_data and 'title' in s_data:
                            stories.append({
                                'title': s_data.get('title'),
                                'url': s_data.get('url', f"https://news.ycombinator.com/item?id={item_id}"),
                                'by': s_data.get('by', 'hn'),
                                'score': s_data.get('score', 0)
                            })
                    except Exception:
                        continue
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(stories).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                return

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), DashboardHandler) as httpd:
        print(f"macOS Terminal Dashboard Server running on http://127.0.0.1:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == '__main__':
    main()
