"""
Avocado Configuration Manager
Persists user settings in ~/.config/avocado/config.json with strict file permissions (0700/0600).
"""
import os
import json

CONFIG_DIR = os.path.expanduser("~/.config/avocado")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "theme": "avocado",
    "temp_unit": "F",
    "default_city": "San Francisco",
    "refresh_rate": 2,
    "favorite_apps": [
        {"name": "Safari", "url": "Safari"},
        {"name": "Google Chrome", "url": "Google Chrome"},
        {"name": "ChatGPT", "url": "ChatGPT"},
        {"name": "Terminal", "url": "Terminal"},
        {"name": "Notes", "url": "Notes"}
    ]
}

def ensure_secure_dir():
    if not os.path.exists(CONFIG_DIR):
        try:
            os.makedirs(CONFIG_DIR, mode=0o700, exist_ok=True)
        except Exception:
            pass
    else:
        try:
            os.chmod(CONFIG_DIR, 0o700)
        except Exception:
            pass

def load_config():
    ensure_secure_dir()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                config = DEFAULT_CONFIG.copy()
                config.update(saved)
                return config
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    try:
        ensure_secure_dir()
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        os.chmod(CONFIG_FILE, 0o600)
    except Exception as e:
        print(f"Error saving config: {e}")
