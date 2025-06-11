# Telegram LLM Userbot Skeleton

This repository contains a minimal userbot powered by a local large language model.
It now includes runtime controls for switching models and styles, adjusting temperature
and managing access lists.

## Features

- Connects to Telegram using **Telethon**.
- Sends messages to a local LLM server (e.g. Ollama, LM Studio).
- Reads a system prompt from the selected style file on every message.
- Logs conversations to `userbot/logs/history.jsonl`.
- Writes detailed events to `userbot/logs/userbot.log`.
- Paths can be overridden via environment variables.
- Simple whitelist/blacklist via `userbot/config.yaml`.
- Runtime commands `!model <name>` and `!style <name>` to switch models and styles.
- `!temp <value>` adjusts generation temperature.
- `!tokens <n>` and `!top_p <value>` control generation limits.
- Optional conversation context per chat with `!context on|off`.
- Per-chat style overrides with `!stylefor <id> <style>`.
- Simulated typing with configurable delay before replies.
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
- Optional automatic fine-tuning when enough history is accumulated.
- Optional HTTP API for GUI integration is available on the configured port.
- Automatic updates via `git pull` and remote configuration sync when `update`
  options are set.
- Drop python files in `userbot/plugins` to add custom commands.
- Use `!plugins` to list plugin commands and `!reloadplugins` to reload them.
- Models are defined in `config.yaml` with `type` (e.g. `mlx` or `gguf`) and
  custom endpoint URLs.
- Minimal Electron GUI for adjusting settings, browsing history and access lists.
  It also lets you edit the endpoint and type of the active model.
- The GUI includes a simple chat window for sending messages to the LLM without Telegram.
- Native SwiftUI client available in `swiftui/` with macOS notifications and optional autostart

## Setup

1. Create a Telegram API application to obtain `api_id` and `api_hash`.
2. Edit `userbot/config.yaml` with your credentials and LLM settings.
   By default it points to LM Studio running on `http://localhost:1234`.
   Start LM Studio and enable the local server before launching the bot.
   The file also defines available prompt styles and model types.
   Options like `typing_delay` and `autotrain` fine-tuning settings can be adjusted there.
   You can override the location of this file by setting the `USERBOT_CONFIG`
   environment variable.
    The log file path, application log path and prompts directory can be
    changed with `USERBOT_LOG_FILE`, `USERBOT_APP_LOG` and
    `USERBOT_PROMPTS_DIR`.
  Plugins are loaded from the directory specified by `plugins_dir`.
  When `update.repo` or `update.config_url` are set in `config.yaml` the bot
  will run `git pull` and fetch an updated configuration on startup.
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
!stylefor <id> <style> # set style for a specific user
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
!autotrain on|off # toggle automatic fine-tuning
!plugins         # list plugin commands
!reloadplugins   # reload plugins at runtime
!stop            # stop the bot
!help            # list commands
```

### HTTP API

When the configuration's `api.enabled` option is true, the bot also starts an HTTP service (default `127.0.0.1:8080`).
`GET /options` returns available models with their types and endpoints so the GUI can populate dropdowns.
Basic endpoints include:

```
GET  /status           # current model, style and temperature
POST /model {name}     # switch model
POST /style {name}     # switch style
GET  /options          # list available models and styles
POST /modelconfig      # update endpoint or type for a model
GET  /history?limit=n  # return last n log entries
GET  /dataset?limit=n  # download dataset JSON
GET  /prompt           # show current prompt text
POST /prompt {text}    # replace current prompt
GET  /access           # view whitelist and blacklist
POST /access {lists}   # replace access lists
POST /chat {message, style?}   # talk to the LLM directly
```

### Plugins

Plugins add custom runtime commands. Drop a `.py` file into `userbot/plugins`
defining a `register(add_command)` function. Within it call
`add_command(name, handler)` where ``handler(event, arg, config)`` is an async
function. Use `!reloadplugins` to reload plugins without restarting and
`!plugins` to see which commands are available.

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
The "Model Settings" area shows the endpoint and type of the selected model, so you can update them without editing YAML.


### SwiftUI Client

Для macOS и iOS доступно минимальное приложение на SwiftUI. Оно подключается к HTTP API бота и позволяет переключать модель и стиль.

```bash
cd swiftui
swift build -c release
```

Запуск требует macOS 12+ или iOS 15+.

Приложение уведомляет о смене модели и стиля через системные уведомления.
Для автозапуска можно установить LaunchAgent из `swiftui/launch_agent.plist`.

Чтобы получить полноценный `.app` и проект для Xcode, запустите
`scripts/package_swiftui.sh` на macOS. Скрипт соберёт приложение и создаст
архив `dist/UserbotApp.zip`, который можно развернуть как обычную программу.
При необходимости проект можно открыть в Xcode командой `open Package.swift`.
Можно также выполнить `scripts/generate_xcodeproj.sh`, чтобы заранее сгенерировать файл `UserbotApp.xcodeproj`.

## Notes

- The project includes basic Electron and SwiftUI GUIs along with a simple
  fine-tuning helper.
- LLM requests are sent to the configured HTTP endpoint; adjust the payload in
  `userbot/llm.py` for your model.
- Dependencies will be installed automatically when running `python -m userbot`.
- When `update.repo` is defined the bot will run `git pull` on startup and
  `update.config_url` can point to a remote YAML file that will be merged into
  the local configuration.
- Prompts can be hot-reloaded by editing the text file while the bot is running.
- Use `!history [n]` to quickly preview recent conversations.
- Each log entry includes a session ID, model and style for easier analysis.
- Generate a dataset for fine-tuning with `python -m userbot.fine_tune --out data.json` or the `!train` command`.
- Launch local training with `python scripts/fine_tune.py --base llama2 --name my-model` or via `!finetune my-model`.

### Packaging

Use `scripts/package.py` to create release archives.
Run it without options to simply zip the repository or pass `--binary` to build
a standalone executable via PyInstaller:

```bash
python scripts/package.py --output userbot.zip       # source archive
python scripts/package.py --binary --output userbot  # creates userbot.zip with an executable
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

For a native macOS build of the SwiftUI client run:

```bash
scripts/package_swiftui.sh  # creates dist/UserbotApp.zip
```


Contributions are welcome!

See [ROADMAP.md](ROADMAP.md) for planned features.
