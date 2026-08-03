"""
Installed macOS Native Applications Scanner & Launcher
Hardened against input sanitization & argument injection attacks.
"""
import os
import subprocess
import re

DEFAULT_MAC_APPS = [
    "Safari", "Google Chrome", "ChatGPT", "WhatsApp", 
    "Terminal", "Calendar", "Notes", "Calculator", 
    "System Settings", "Music", "Preview"
]

def sanitize_app_name(name):
    """Sanitizes application name input to prevent argument/flag injection."""
    if not name or not isinstance(name, str):
        return ""
    # Strip dangerous shell characters & leading hyphens (which could trigger flag injection)
    sanitized = re.sub(r'[;&|`$><]', '', name).strip()
    while sanitized.startswith('-'):
        sanitized = sanitized[1:].strip()
    return sanitized

def get_installed_mac_apps():
    found_apps = []
    dirs_to_scan = [
        "/Applications",
        "/System/Applications",
        "/System/Applications/Utilities",
        "/Applications/Utilities",
        os.path.expanduser("~/Applications")
    ]

    for d in dirs_to_scan:
        if os.path.exists(d):
            try:
                for f in os.listdir(d):
                    if f.endswith('.app') and not f.startswith('.'):
                        app_name = f[:-4]
                        if app_name not in found_apps:
                            found_apps.append(app_name)
            except Exception:
                continue

    priority_order = [
        "Safari", "Google Chrome", "ChatGPT", "WhatsApp", "Visual Studio Code",
        "Terminal", "Calendar", "Notes", "Calculator", "System Settings",
        "Music", "Spotify", "Finder", "Preview", "Mail", "Messages"
    ]

    selected = []
    for prio in priority_order:
        if prio in found_apps:
            selected.append(prio)

    for app in found_apps:
        if app not in selected and len(selected) < 12:
            selected.append(app)

    return selected if selected else DEFAULT_MAC_APPS

def launch_mac_app(app_name_or_idx, installed_apps):
    if not app_name_or_idx:
        return False, "No app specified."

    target = str(app_name_or_idx).strip()

    # Check by number index (1-based)
    if target.isdigit():
        idx = int(target) - 1
        if 0 <= idx < len(installed_apps):
            app_name = installed_apps[idx]
            return _exec_open_app(app_name)

    # Check by name matching in installed list
    target_clean = sanitize_app_name(target)
    if not target_clean:
        return False, "Invalid app name provided."

    target_lower = target_clean.lower()
    for app_name in installed_apps:
        if target_lower in app_name.lower():
            return _exec_open_app(app_name)

    return _exec_open_app(target_clean)

def _exec_open_app(app_name):
    clean_name = sanitize_app_name(app_name)
    if not clean_name:
        return False, "Invalid app name."

    try:
        # Use '--' to prevent flag injection (e.g. open -a -- "AppName")
        res = subprocess.run(["open", "-a", "--", clean_name], capture_output=True, text=True, timeout=5)
        if res.returncode == 0:
            return True, f"🚀 Launched native macOS app: [{clean_name}]"
        else:
            # Fallback to standard open with double hyphens
            subprocess.Popen(["open", "--", clean_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True, f"Opening [{clean_name}]..."
    except Exception as e:
        return False, f"Failed to launch app '{clean_name}': {e}"
