"""
GitHub Repository Info & About Page Module
Fetches repository metadata from GitHub API or formats offline fallback info.
"""
import urllib.request
import json
import subprocess
import webbrowser

REPO_URL = "https://github.com/RnR-io/Avacado"
API_URL = "https://api.github.com/repos/RnR-io/Avacado"

def get_github_info():
    try:
        req = urllib.request.Request(
            API_URL,
            headers={"User-Agent": "AvocadoTerminalApp/1.1"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return {
                "name": data.get("name", "Avacado"),
                "full_name": data.get("full_name", "RnR-io/Avacado"),
                "description": data.get("description", "Native macOS Terminal Dashboard & CLI App"),
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "issues": data.get("open_issues_count", 0),
                "license": data.get("license", {}).get("name", "MIT License") if data.get("license") else "MIT",
                "html_url": data.get("html_url", REPO_URL),
                "owner": data.get("owner", {}).get("login", "RnR-io"),
                "updated_at": data.get("updated_at", "2026-08-03")[:10]
            }
    except Exception:
        return {
            "name": "Avacado",
            "full_name": "RnR-io/Avacado",
            "description": "Native macOS Terminal Dashboard & CLI App",
            "stars": 1,
            "forks": 0,
            "issues": 0,
            "license": "MIT License",
            "html_url": REPO_URL,
            "owner": "RnR-io",
            "updated_at": "2026-08-03"
        }

def open_github_in_browser():
    try:
        subprocess.Popen(["open", REPO_URL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        try:
            webbrowser.open(REPO_URL)
        except Exception:
            pass
