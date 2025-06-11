#!/usr/bin/env python3
"""Create distributable archives of the userbot."""
from pathlib import Path
import shutil
import argparse
import subprocess
import sys
import os


def main():
    parser = argparse.ArgumentParser(description="Package the userbot for distribution")
    parser.add_argument("--output", default="userbot_package.zip", help="Output archive name")
    parser.add_argument("--binary", action="store_true", help="Build standalone binary using PyInstaller")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    base_name = Path(args.output).with_suffix("")

    if args.binary:
        try:
            import PyInstaller  # type: ignore
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        subprocess.check_call([
            sys.executable,
            "-m",
            "PyInstaller",
            "--onefile",
            "-n",
            "userbot",
            str(root / "userbot" / "__main__.py"),
        ])
        dist = root / "dist"
        binary = dist / ("userbot.exe" if os.name == "nt" else "userbot")
        archive_path = shutil.make_archive(base_name=str(base_name), format="zip", root_dir=dist, base_dir=binary.name)
    else:
        archive_path = shutil.make_archive(base_name=str(base_name), format="zip", root_dir=root)
    print(f"Archive created at {archive_path}")


if __name__ == "__main__":
    main()
