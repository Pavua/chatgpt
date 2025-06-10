import asyncio
import json
from pathlib import Path
from datetime import datetime

from telethon import TelegramClient, events
import yaml

from .llm import generate, load_config


CONFIG_PATH = Path(__file__).resolve().parent / 'config.yaml'
PROMPT_PATH = Path(__file__).resolve().parent / 'prompts' / 'system_prompt.txt'


def read_prompt() -> str:
    try:
        with open(PROMPT_PATH, 'r') as f:
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

        text = event.raw_text
        prompt = read_prompt() + "\n" + text
        response = generate(prompt)
        await event.reply(response)
        log_interaction(sender_id, text, response, log_file)

    async with client:
        print("Userbot started. Press Ctrl+C to stop.")
        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
