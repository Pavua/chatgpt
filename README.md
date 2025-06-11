# Telegram LLM Userbot Skeleton

This repository contains a minimal userbot powered by a local large language model.
It now includes runtime controls for switching models and styles, adjusting temperature
and managing access lists.

## Features

- Connects to Telegram using **Telethon**.
- Sends messages to a local LLM server (e.g. Ollama, LM Studio).
- Reads a system prompt from the selected style file on every message.
- Logs conversations to `userbot/logs/history.jsonl`.
- Simple whitelist/blacklist via `userbot/config.yaml`.
- Runtime commands `!model <name>` and `!style <name>` to switch models and styles.
- `!temp <value>` sets the generation temperature.
- `!allow <id>` / `!block <id>` modify white/blacklists.
- `!reload` reloads `config.yaml` without restarting the bot.
- `!export` and `!import` handle conversation history.
- `!status` shows the active model, style and temperature.
- `!train` creates a fine-tuning dataset from history.
- `!stop` gracefully shuts down the bot.
- `!help` lists available commands.
- LLM requests are performed in a background thread to keep the bot responsive.

## Setup

1. Create a Telegram API application to obtain `api_id` and `api_hash`.
2. Edit `userbot/config.yaml` with your credentials and LLM endpoint.
   The file also defines available prompt styles.
3. (Optional) install requirements manually:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the bot. Missing packages will be installed automatically on first run:

   ```bash
   python -m userbot
   ```

The bot will start a new session on first launch and listen for incoming messages.
Only users allowed by the whitelist will receive responses.
At runtime you can send commands to the bot from an allowed account:

```
!model <name>    # switch to a different model
!style <name>    # switch system prompt style
!temp <value>    # set generation temperature
!allow <id>      # add user to whitelist
!block <id>      # add user to blacklist
!export          # export history file
!import <file>   # import history from uploaded file
!history [n]     # show last n history entries
!reload          # reload configuration
!status          # show current settings
!train           # create dataset for fine-tuning
!stop            # stop the bot
!help            # list commands
```

## Notes

- The project is a simplified example and lacks the GUI and fine-tuning tools
 described in the original specification.
- LLM requests are sent to the configured HTTP endpoint; adjust the payload in
  `userbot/llm.py` for your model.
- Dependencies will be installed automatically when running `python -m userbot`.
- Prompts can be hot-reloaded by editing the text file while the bot is running.
- Use `!history [n]` to quickly preview recent conversations.
- Generate a dataset for fine-tuning with `python -m userbot.fine_tune --out data.json` or the `!train` command.

### Packaging

Use `scripts/package.py` to create a zip archive for distribution:

```bash
python scripts/package.py --output userbot.zip
```

Contributions are welcome!
