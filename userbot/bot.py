import asyncio
import json
from pathlib import Path
from datetime import datetime

from telethon import TelegramClient, events

from .llm import generate, load_config, save_config

PROMPTS_DIR = Path(__file__).resolve().parent / 'prompts'


def read_prompt(config) -> str:
    """Return the currently selected system prompt."""
    prompts = {p['name']: p['file'] for p in config.get('styles', {}).get('prompts', [])}
    current = config.get('styles', {}).get('current')
    path = PROMPTS_DIR / prompts.get(current, '')
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return ""


def log_interaction(user_id: int, message: str, response: str, log_file: Path):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "message": message,
        "response": response,
    }
    with open(log_file, 'a') as lf:
        lf.write(json.dumps(log_entry) + "\n")


async def main():
    config = load_config()
    api_id = config['telegram']['api_id']
    api_hash = config['telegram']['api_hash']
    session = config['telegram']['session']

    log_file = Path(config['log_file'])
    log_file.parent.mkdir(parents=True, exist_ok=True)

    client = TelegramClient(session, api_id, api_hash)

    whitelist = set(config['telegram'].get('whitelist', []))
    blacklist = set(config['telegram'].get('blacklist', []))

    @client.on(events.NewMessage(outgoing=False))
    async def handler(event):
        sender = await event.get_sender()
        sender_id = sender.id
        if blacklist and sender_id in blacklist:
            return
        if whitelist and sender_id not in whitelist:
            return

        text = event.raw_text.strip()

        if text.startswith('!model '):
            model_name = text.split(' ', 1)[1]
            models = {m['name'] for m in config['llm'].get('models', [])}
            if model_name in models:
                config['llm']['current'] = model_name
                save_config(config)
                await event.reply(f"\ud83d\udcbe Model switched to {model_name}")
            else:
                await event.reply("Unknown model")
            return

        if text.startswith('!style '):
            style_name = text.split(' ', 1)[1]
            styles = {s['name'] for s in config.get('styles', {}).get('prompts', [])}
            if style_name in styles:
                config['styles']['current'] = style_name
                save_config(config)
                await event.reply(f"\ud83c\udf73 Style switched to {style_name}")
            else:
                await event.reply("Unknown style")
            return

        if text == '!reload':
            config.update(load_config())
            await event.reply("Configuration reloaded")
            return

        prompt = read_prompt(config) + "\n" + text
        response = generate(prompt, config)
        await event.reply(response)
        log_interaction(sender_id, text, response, log_file)

    async with client:
        print("Userbot started. Press Ctrl+C to stop.")
        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
