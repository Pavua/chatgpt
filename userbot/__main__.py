from pathlib import Path
from .bot import main
from .utils import ensure_dependencies, init_logging
from .llm import load_config

if __name__ == '__main__':
    import asyncio, os
    ensure_dependencies()
    cfg = load_config()
    log_path = Path(os.getenv('USERBOT_APP_LOG', cfg.get('app_log_file', 'logs/userbot.log')))
    init_logging(log_path)
    asyncio.run(main())
