import importlib
import subprocess
import sys
from pathlib import Path


def ensure_dependencies():
    """Install required packages if missing."""
    packages = {
        "telethon": "telethon>=1.29.0",
        "yaml": "PyYAML>=6.0",
        "requests": "requests>=2.31.0",
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
