import requests
from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).resolve().parent / 'config.yaml'


def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)


def generate(prompt: str, temperature: float = 0.7) -> str:
    config = load_config()
    data = {
        "model": config['llm']['model'],
        "prompt": prompt,
        "temperature": temperature,
        "stream": False,
    }
    try:
        resp = requests.post(config['llm']['endpoint'], json=data, timeout=60)
        resp.raise_for_status()
        res = resp.json()
        return res.get('response') or res.get('choices', [{}])[0].get('text', '')
    except Exception as e:
        return f"[LLM error: {e}]"
