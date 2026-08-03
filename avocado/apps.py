"""
Favorite Apps & Terminal Launcher
"""
import subprocess
import webbrowser

def open_app(app_target, apps_list):
    if not app_target:
        return False, "No target provided."

    target = str(app_target).strip().lower()

    # Check by number index
    if target.isdigit():
        idx = int(target) - 1
        if 0 <= idx < len(apps_list):
            app = apps_list[idx]
            launch_url_or_app(app["url"])
            return True, f"Launched [{app['name']}] -> {app['url']}"

    # Check by name
    for app in apps_list:
        if target in app["name"].lower():
            launch_url_or_app(app["url"])
            return True, f"Launched [{app['name']}] -> {app['url']}"

    # Fallback to general open URL or search
    if target.startswith("http://") or target.startswith("https://"):
        launch_url_or_app(target)
        return True, f"Opened {target}"

    return False, f"Shortcut for '{target}' not found."

def launch_url_or_app(url_or_cmd):
    try:
        subprocess.Popen(["open", url_or_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        try:
            webbrowser.open(url_or_cmd)
        except Exception:
            pass
