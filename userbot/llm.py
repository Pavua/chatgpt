import requests
from pathlib import Path
import yaml
import asyncio
import os

DEFAULT_CONFIG = Path(__file__).resolve().parent / 'config.yaml'

def config_path() -> Path:
    """Return the path to the configuration file allowing override via env."""
    override = os.getenv("USERBOT_CONFIG")
    return Path(override) if override else DEFAULT_CONFIG


def load_config():
    """Load configuration from ``USERBOT_CONFIG`` path or default."""
    path = config_path()
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def save_config(config):
    """Save configuration to ``USERBOT_CONFIG`` path or default."""
    path = config_path()
    with open(path, 'w') as f:
        yaml.safe_dump(config, f)


def current_model(config):
    name = config['llm'].get('current')
    models = {m['name']: m for m in config['llm'].get('models', [])}
    return models.get(name)


def generate(prompt: str, config, temperature: float | None = None) -> str:
    model_cfg = current_model(config)
    if not model_cfg:
        return "[No model configured]"
    if temperature is None:
        temperature = float(config['llm'].get('temperature', 0.7))
    max_tokens = int(config['llm'].get('max_tokens', 512))
    top_p = float(config['llm'].get('top_p', 0.95))
    data = {
        "model": model_cfg.get('name'),
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": top_p,
        "stream": False,
    }
    try:
        resp = requests.post(model_cfg['endpoint'], json=data, timeout=60)
        resp.raise_for_status()
        res = resp.json()
        return res.get('response') or res.get('choices', [{}])[0].get('text', '')
    except Exception as e:
        return f"[LLM error: {e}]"


async def generate_async(prompt: str, config, temperature: float | None = None) -> str:
    """Asynchronously call ``generate`` in a thread."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, generate, prompt, config, temperature)
