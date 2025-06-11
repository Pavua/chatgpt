import importlib
import subprocess
import sys
from pathlib import Path
import yaml


def ensure_dependencies():
    """Install required packages if missing."""
    packages = {
        "telethon": "telethon>=1.29.0",
        "yaml": "PyYAML>=6.0",
        "requests": "requests>=2.31.0",
        "aiohttp": "aiohttp>=3.8.5",
        "PyInstaller": "pyinstaller>=6.4.0",
    }
    for module, package in packages.items():
        try:
            importlib.import_module(module)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def export_history(log_file: Path, dest: Path):
    dest.write_bytes(Path(log_file).read_bytes())


def import_history(src: Path, log_file: Path):
    with open(src, "rb") as f_in, open(log_file, "ab") as f_out:
        f_out.write(f_in.read())


def tail_history(log_file: Path, limit: int = 5):
    """Return the last ``limit`` entries from the history file."""
    from collections import deque
    import json

    entries = deque(maxlen=limit)
    if log_file.exists():
        with open(log_file, "r") as fh:
            for line in fh:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return list(entries)


def sync_config(config):
    """Fetch updated configuration from ``config['update']['config_url']`` if set."""
    import requests

    url = config.get('update', {}).get('config_url')
    if not url:
        return config
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        new_cfg = yaml.safe_load(resp.text)
        config.update(new_cfg or {})
    except Exception as exc:
        print(f"Config sync failed: {exc}")
    return config


def check_updates(config):
    """Run ``git pull`` if ``update_repo`` is configured."""
    repo = config.get('update', {}).get('repo')
    if not repo:
        return
    try:
        subprocess.run(['git', 'pull', repo], check=True)
    except Exception as exc:
        print(f"Update check failed: {exc}")
