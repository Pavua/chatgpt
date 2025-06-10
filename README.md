# Telegram LLM Userbot Skeleton

This repository contains a minimal userbot powered by a local large language model.
It is not a full application, but a starting point for further development.

## Features

- Connects to Telegram using **Telethon**.
- Sends messages to a local LLM server (e.g. Ollama, LM Studio).
- Reads a system prompt from `userbot/prompts/system_prompt.txt` on every message.
- Logs conversations to `userbot/logs/history.jsonl`.
- Simple whitelist/blacklist via `userbot/config.yaml`.

## Setup

1. Create a Telegram API application to obtain `api_id` and `api_hash`.
2. Edit `userbot/config.yaml` with your credentials and LLM endpoint.
3. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the bot:

   ```bash
   python -m userbot.bot
   ```

The bot will start a new session on first launch and listen for incoming messages.
Only users allowed by the whitelist will receive responses.

## Notes

- The project is a simplified example and lacks the GUI and fine-tuning tools
  described in the original specification.
- LLM requests are sent to the configured HTTP endpoint; adjust the payload in
  `userbot/llm.py` for your model.
- Prompts can be hot-reloaded by editing the text file while the bot is running.

Contributions are welcome!
