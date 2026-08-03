"""
Avocado Configuration Manager
Persists user settings in ~/.config/avocado/config.json
"""
import os
import json

CONFIG_DIR = os.path.expanduser("~/.config/avocado")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "theme": "avocado", # avocado, matrix, dracula, ocean, amber, monokai
    "temp_unit": "F",
    "default_city": "San Francisco",
    "refresh_rate": 2,
    "news_category": "tech",
    "favorite_apps": [
        {"name": "GitHub", "url": "https://github.com", "icon": "🐙"},
        {"name": "VS Code", "url": "https://vscode.dev", "icon": "💻"},
        {"name": "ChatGPT", "url": "https://chatgpt.com", "icon": "🤖"},
        {"name": "YouTube", "url": "https://youtube.com", "icon": "▶️"},
        {"name": "Spotify", "url": "https://open.spotify.com", "icon": "🎵"},
        {"name": "Gmail", "url": "https://mail.google.com", "icon": "✉️"},
        {"name": "X / Twitter", "url": "https://x.com", "icon": "🐦"},
        {"name": "Figma", "url": "https://figma.com", "icon": "🎨"},
        {"name": "Notion", "url": "https://notion.so", "icon": "📝"}
    ]
}

def load_config():
    if not os.path.exists(CONFIG_DIR):
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
        except Exception:
            pass

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
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")
