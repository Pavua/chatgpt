# Telegram LLM Userbot Skeleton

This repository contains a minimal userbot powered by a local large language model.
It now includes runtime controls for switching models and styles, adjusting temperature
and managing access lists.

## Features

- Connects to Telegram using **Telethon**.
- Sends messages to a local LLM server (e.g. Ollama, LM Studio).
- Reads a system prompt from the selected style file on every message.
- Logs conversations to `userbot/logs/history.jsonl`.
- Paths can be overridden via environment variables.
- Simple whitelist/blacklist via `userbot/config.yaml`.
- Runtime commands `!model <name>` and `!style <name>` to switch models and styles.
- `!temp <value>` adjusts generation temperature.
- `!tokens <n>` and `!top_p <value>` control generation limits.
- Optional conversation context per chat with `!context on|off`.
- `!allow <id>` / `!block <id>` modify white/blacklists.
- `!reload` reloads `config.yaml` without restarting the bot.
- `!export` and `!import` handle conversation history.
- `!status` shows the active model, style and temperature.
- `!train` creates a fine-tuning dataset from history.
- `!finetune <name>` launches a local fine-tuning job and switches to the new model.
- Dataset export is also available via the GUI's "Export Dataset" button.
- `!summary [n]` summarizes recent conversation entries.
- `!stop` gracefully shuts down the bot.
- `!help` lists available commands.
- LLM requests are performed in a background thread to keep the bot responsive.
- Optional HTTP API for GUI integration is available on the configured port.
- Minimal Electron GUI for adjusting settings, browsing history and access lists.
- Native SwiftUI client available in `swiftui/`

## Setup

1. Create a Telegram API application to obtain `api_id` and `api_hash`.
2. Edit `userbot/config.yaml` with your credentials and LLM endpoint.
   The file also defines available prompt styles.
   You can override the location of this file by setting the `USERBOT_CONFIG`
   environment variable.
   The log file path and prompts directory can be changed with
   `USERBOT_LOG_FILE` and `USERBOT_PROMPTS_DIR`.
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
!tokens <n>      # set maximum tokens
!top_p <value>   # set nucleus sampling p
!context on|off  # enable or disable persistent context
!allow <id>      # add user to whitelist
!block <id>      # add user to blacklist
!export          # export history file
!import <file>   # import history from uploaded file
!prompt          # show current system prompt
!setprompt ...   # replace current prompt
!history [n]     # show last n history entries
!summary [n]     # summarize last n history entries
!reload          # reload configuration
!status          # show current settings
!train           # create dataset for fine-tuning
!finetune <name> # fine-tune base model and switch
!stop            # stop the bot
!help            # list commands
```

### HTTP API

When the configuration's `api.enabled` option is true, the bot also starts an HTTP service (default `127.0.0.1:8080`).
Basic endpoints include:

```
GET  /status           # current model, style and temperature
POST /model {name}     # switch model
POST /style {name}     # switch style
GET  /history?limit=n  # return last n log entries
GET  /dataset?limit=n  # download dataset JSON
GET  /prompt           # show current prompt text
POST /prompt {text}    # replace current prompt
GET  /access           # view whitelist and blacklist
POST /access {lists}   # replace access lists
```

### Electron GUI

The repository ships with a minimal GUI located in the `gui/` directory. It
connects to the HTTP API and lets you change the active model or style,
edit the current prompt, manage access lists and browse recent history.

Install dependencies and start the interface with:

```bash
cd gui
npm install
npm start
```

Use the theme button to switch between light and dark modes.
The "Access Control" section lets you edit the whitelist and blacklist. Enter user IDs separated by spaces or newlines and click "Save Access".
Click "Export Dataset" in the History section to download a JSON file of recent conversations.


### SwiftUI Client

Для macOS и iOS доступно минимальное приложение на SwiftUI. Оно подключается к HTTP API бота и позволяет переключать модель и стиль.

```bash
cd swiftui
swift build -c release
```

Запуск требует macOS 12+ или iOS 15+

## Notes

- The project includes basic Electron and SwiftUI GUIs along with a simple
  fine-tuning helper.
- LLM requests are sent to the configured HTTP endpoint; adjust the payload in
  `userbot/llm.py` for your model.
- Dependencies will be installed automatically when running `python -m userbot`.
- Prompts can be hot-reloaded by editing the text file while the bot is running.
- Use `!history [n]` to quickly preview recent conversations.
- Each log entry includes a session ID, model and style for easier analysis.
- Generate a dataset for fine-tuning with `python -m userbot.fine_tune --out data.json` or the `!train` command`.
- Launch local training with `python scripts/fine_tune.py --base llama2 --name my-model` or via `!finetune my-model`.

### Packaging

Use `scripts/package.py` to create a zip archive for distribution:

```bash
python scripts/package.py --output userbot.zip
```

Archiving the repository typically completes within a few seconds.

To create standalone desktop packages of the GUI, run the packaging scripts
inside the `gui` directory. They rely on `electron-packager` and will build a
macOS or Windows bundle:

```bash
cd gui
npm install
npm run package-macos  # builds a .app on macOS
npm run package-win    # builds a Windows executable
```


Contributions are welcome!

See [ROADMAP.md](ROADMAP.md) for planned features.
