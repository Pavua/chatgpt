#!/usr/bin/env python3
"""Create a zip archive of the project for distribution."""
from pathlib import Path
import shutil
import argparse


def main():
    parser = argparse.ArgumentParser(description="Package the userbot into a zip archive")
    parser.add_argument("--output", default="userbot_package.zip", help="Output zip file name")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    base_name = Path(args.output).with_suffix("")
    archive_path = shutil.make_archive(base_name=str(base_name), format="zip", root_dir=root)
    print(f"Archive created at {archive_path}")


if __name__ == "__main__":
    main()
