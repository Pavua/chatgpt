import requests
from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).resolve().parent / 'config.yaml'


def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)


def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
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
    data = {
        "model": model_cfg.get('name'),
        "prompt": prompt,
        "temperature": temperature,
        "stream": False,
    }
    try:
        resp = requests.post(model_cfg['endpoint'], json=data, timeout=60)
        resp.raise_for_status()
        res = resp.json()
        return res.get('response') or res.get('choices', [{}])[0].get('text', '')
    except Exception as e:
        return f"[LLM error: {e}]"
