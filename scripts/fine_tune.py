from pathlib import Path
import argparse

from userbot.fine_tune import fine_tune_from_history, run_ollama_fine_tune
from userbot.llm import load_config, save_config


def main():
    parser = argparse.ArgumentParser(description="Launch fine-tuning with Ollama")
    parser.add_argument("--log", default="logs/history.jsonl", help="Path to history file")
    parser.add_argument("--base", required=True, help="Base model name")
    parser.add_argument("--name", required=True, help="Name for the new model")
    args = parser.parse_args()

    log = Path(args.log)
    dataset = log.with_suffix(".dataset.json")
    fine_tune_from_history(log, dataset)

    if run_ollama_fine_tune(dataset, args.base, args.name):
        config = load_config()
        models = config.setdefault("llm", {}).setdefault("models", [])
        models.append({"name": args.name, "endpoint": config["llm"]["models"][0]["endpoint"]})
        config["llm"]["current"] = args.name
        save_config(config)
        print(f"Fine-tuning complete. Model '{args.name}' added to config.")
    else:
        print("Fine-tuning failed")

    dataset.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
