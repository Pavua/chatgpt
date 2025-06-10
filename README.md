# Telegram LLM Userbot Skeleton

This repository contains a minimal userbot powered by a local large language model.
It now includes simple runtime controls for switching models and reloading the configuration.

## Features

- Connects to Telegram using **Telethon**.
- Sends messages to a local LLM server (e.g. Ollama, LM Studio).
- Reads a system prompt from the selected style file on every message.
- Logs conversations to `userbot/logs/history.jsonl`.
- Simple whitelist/blacklist via `userbot/config.yaml`.
- Runtime command `!model <name>` to switch between configured models.
- Runtime command `!style <name>` to change the prompt style.
- `!reload` reloads `config.yaml` without restarting the bot.

## Setup

1. Create a Telegram API application to obtain `api_id` and `api_hash`.
2. Edit `userbot/config.yaml` with your credentials and LLM endpoint.
   The file also defines available prompt styles.
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
At runtime you can send commands to the bot from an allowed account:

```
!model <name>   # switch to a different model from config.yaml
!reload         # reload configuration without restart
!style <name>   # switch system prompt style
```

## Notes

- The project is a simplified example and lacks the GUI and fine-tuning tools
  described in the original specification.
- LLM requests are sent to the configured HTTP endpoint; adjust the payload in
  `userbot/llm.py` for your model.
- Prompts can be hot-reloaded by editing the text file while the bot is running.

Contributions are welcome!
