import json
from pathlib import Path

CONFIG_FILE = "config.json"

config = {
    "url": None,
    "port": 80,
    "wordlist": None,
    "extensions": ["php", "zip", "sql", "bak", "rar"],
    "threads": 10,
    "status_codes": [200, 301, 302, 403],
    "recurse": False,
    "depth": 1,
    "headers": {"User-Agent": "budir/1.0"},
}

def cargar_config():
    if Path(CONFIG_FILE).exists():
        with open(CONFIG_FILE, "r") as f:
            config.update(json.load(f))

def guardar_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
