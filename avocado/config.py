"""
Avocado Configuration Manager
Persists user settings in ~/.config/avocado/config.json with strict permissions (0700/0600).
"""
import os
import json

CONFIG_DIR = os.path.expanduser("~/.config/avocado")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "theme": "avocado",
    "temp_unit": "C",           # Celsius as default
    "default_city": "auto",     # Auto location detection
    "refresh_rate": 2
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
        content = json.dumps(config, indent=2).encode("utf-8")
        fd = os.open(CONFIG_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with open(fd, "wb") as f:
            f.write(content)
    except Exception as e:
        print(f"Error saving config: {e}")

