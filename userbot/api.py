from pathlib import Path
from aiohttp import web

from .llm import save_config, generate_async
from .bot import read_prompt
from .utils import tail_history
from .fine_tune import dataset_from_history


def create_app(config, log_file: Path, prompts_dir: Path):
    app = web.Application()

    async def get_status(request):
        return web.json_response({
            "model": config["llm"].get("current"),
            "style": config.get("styles", {}).get("current"),
            "temperature": config["llm"].get("temperature"),
        })

    async def get_options(request):
        models = [
            {
                "name": m["name"],
                "type": m.get("type", ""),
                "endpoint": m.get("endpoint", ""),
            }
            for m in config["llm"].get("models", [])
        ]
        styles = [s["name"] for s in config.get("styles", {}).get("prompts", [])]
        return web.json_response({"models": models, "styles": styles})

    async def post_model(request):
        data = await request.json()
        name = data.get("name")
        models = {m["name"] for m in config["llm"].get("models", [])}
        if name in models:
            config["llm"]["current"] = name
            save_config(config)
            return web.json_response({"status": "ok"})
        return web.json_response({"error": "unknown model"}, status=400)

    async def post_model_config(request):
        data = await request.json()
        name = data.get("name")
        for m in config["llm"].get("models", []):
            if m["name"] == name:
                if "endpoint" in data:
                    m["endpoint"] = data["endpoint"]
                if "type" in data:
                    m["type"] = data["type"]
                save_config(config)
                return web.json_response({"status": "ok"})
        return web.json_response({"error": "unknown model"}, status=400)

    async def post_style(request):
        data = await request.json()
        name = data.get("name")
        styles = {s["name"] for s in config.get("styles", {}).get("prompts", [])}
        if name in styles:
            config["styles"]["current"] = name
            save_config(config)
            return web.json_response({"status": "ok"})
        return web.json_response({"error": "unknown style"}, status=400)

    async def get_history(request):
        limit = int(request.query.get("limit", 10))
        entries = tail_history(log_file, limit)
        return web.json_response(entries)

    async def get_dataset(request):
        limit = request.query.get("limit")
        limit = int(limit) if limit else None
        data = dataset_from_history(log_file, limit)
        return web.json_response(data)

    async def get_prompt(request):
        return web.Response(text=read_prompt(config, prompts_dir))

    async def post_prompt(request):
        data = await request.json()
        text = data.get("text", "")
        prompts = {p['name']: p['file'] for p in config.get('styles', {}).get('prompts', [])}
        current = config.get('styles', {}).get('current')
        path = prompts_dir / prompts.get(current, '')
        path.write_text(text)
        return web.json_response({"status": "ok"})

    async def post_chat(request):
        data = await request.json()
        message = data.get('message', '')
        style = data.get('style')
        prompt = read_prompt(config, prompts_dir, style) + "\n" + message
        resp = await generate_async(prompt, config)
        return web.json_response({"response": resp})

    async def get_access(request):
        return web.json_response({
            "whitelist": config.get("telegram", {}).get("whitelist", []),
            "blacklist": config.get("telegram", {}).get("blacklist", []),
        })

    async def post_access(request):
        data = await request.json()
        wl = data.get("whitelist", [])
        bl = data.get("blacklist", [])
        config.setdefault("telegram", {})["whitelist"] = wl
        config.setdefault("telegram", {})["blacklist"] = bl
        save_config(config)
        return web.json_response({"status": "ok"})

    app.add_routes([
        web.get('/status', get_status),
        web.post('/model', post_model),
        web.post('/modelconfig', post_model_config),
        web.post('/style', post_style),
        web.get('/options', get_options),
        web.get('/history', get_history),
        web.get('/dataset', get_dataset),
        web.get('/prompt', get_prompt),
        web.post('/prompt', post_prompt),
        web.post('/chat', post_chat),
        web.get('/access', get_access),
        web.post('/access', post_access),
    ])
    return app


async def start_api(config, log_file: Path, prompts_dir: Path):
    app = create_app(config, log_file, prompts_dir)
    host = config.get('api', {}).get('host', '127.0.0.1')
    port = int(config.get('api', {}).get('port', 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    print(f"API running on http://{host}:{port}")
    return runner
