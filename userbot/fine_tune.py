import json
from pathlib import Path
import argparse


def dataset_from_history(log_file: Path, limit: int | None = None):
    """Return a list of prompt/response pairs from the history file."""
    data = []
    if log_file.exists():
        with open(log_file, "r") as fh:
            for line in fh:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                data.append({
                    "prompt": entry.get("message", ""),
                    "completion": entry.get("response", "")
                })
    if limit:
        data = data[-limit:]
    return data


def fine_tune_from_history(log_file: Path, output: Path) -> None:
    """Write ``dataset_from_history`` output to ``output`` file."""
    dataset = dataset_from_history(log_file)
    with open(output, "w") as out:
        json.dump(dataset, out, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Create dataset from history for fine-tuning")
    parser.add_argument("--log", default="logs/history.jsonl", help="Path to history file")
    parser.add_argument("--out", required=True, help="Output dataset JSON file")
    args = parser.parse_args()
    fine_tune_from_history(Path(args.log), Path(args.out))


if __name__ == "__main__":
    main()
