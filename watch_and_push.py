#!/usr/bin/env python3
"""
Data Watcher - Zero Touch Automation
=====================================
Drop this running in the background in VS Code terminal.

What it does:
  1. Watches data/raw/ folder for any file change
  2. When CSV data changes it automatically:
       - git add (data + dvc files)
       - git commit with timestamp
       - git push
  3. GitHub Actions then:
       - Runs full pipeline (trains new model)
       - Commits new best_model.pkl back
       - Rebuilds Docker image
       - Pushes to Docker Hub

Usage:
  venv_mlops\\Scripts\\python.exe watch_and_push.py

Then just replace/modify any file in data/raw/
Everything else is fully automatic.
"""

import os
import sys
import time
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime


# ─────────────────────────────────────────
# Config
# ─────────────────────────────────────────
WATCH_DIR    = Path("data/raw")
POLL_SECONDS = 5          # check every 5 seconds
PROJECT_ROOT = Path(__file__).parent


def get_dir_hash(directory: Path) -> str:
    """Compute a hash of all files in a directory."""
    hasher = hashlib.md5()
    if not directory.exists():
        return ""
    for f in sorted(directory.rglob("*")):
        if f.is_file():
            hasher.update(f.name.encode())
            hasher.update(str(f.stat().st_mtime).encode())
            hasher.update(str(f.stat().st_size).encode())
    return hasher.hexdigest()


def run(cmd: str, desc: str = "") -> bool:
    """Run a shell command, print output."""
    if desc:
        print(f"  [{desc}]")
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True,
        cwd=str(PROJECT_ROOT)
    )
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr.strip()}")
        return False
    return True


def push_changes():
    """Stage, commit and push all data + model changes."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "="*55)
    print(f"  DATA CHANGE DETECTED at {timestamp}")
    print("  Starting automatic pipeline trigger...")
    print("="*55)

    # Stage the changed data files
    run("git add data/raw/", "Staging raw data")
    run("git add data/raw.dvc", "Staging DVC file")
    run("git add .dvc/", "Staging DVC cache refs")

    # Check if there's anything to commit
    result = subprocess.run(
        "git diff --staged --quiet",
        shell=True, cwd=str(PROJECT_ROOT)
    )

    if result.returncode == 0:
        print("  No changes to commit — already up to date.")
        return

    # Commit and push
    msg = f"data: update raw dataset [{timestamp}]"
    ok = run(f'git commit -m "{msg}"', "Committing")
    if not ok:
        print("  Commit failed — check git status manually.")
        return

    ok = run("git push", "Pushing to GitHub")
    if not ok:
        print("  Push failed — check your internet / credentials.")
        return

    print("\n" + "="*55)
    print("  PUSHED SUCCESSFULLY")
    print("  GitHub Actions is now running automatically:")
    print()
    print("  Step 1: MLOps Pipeline CI")
    print("          ingestion -> validation -> cleaning ->")
    print("          feature_engineering -> model_training ->")
    print("          model_selection")
    print("          -> commits new best_model.pkl to repo")
    print()
    print("  Step 2: Docker Build and Push")
    print("          builds new image with updated model")
    print("          pushes to dhrumi2910/mlops-churn-pipeline:latest")
    print()
    print("  Track progress:")
    print("  https://github.com/MDhrumi-2005/Customer-Churn-End-to-End-MLOps/actions")
    print("="*55 + "\n")


def main():
    print("="*55)
    print("  ZERO TOUCH DATA WATCHER")
    print("="*55)
    print(f"  Watching: {WATCH_DIR.absolute()}")
    print(f"  Poll interval: every {POLL_SECONDS} seconds")
    print()
    print("  Instructions:")
    print("  1. Keep this running in background")
    print("  2. Replace data/raw/*.csv with your new data")
    print("  3. Everything else is FULLY AUTOMATIC")
    print()
    print("  Press Ctrl+C to stop watching")
    print("="*55 + "\n")

    last_hash = get_dir_hash(WATCH_DIR)
    print(f"  Initial data hash: {last_hash[:12]}...")
    print("  Watching for changes...\n")

    try:
        while True:
            time.sleep(POLL_SECONDS)
            current_hash = get_dir_hash(WATCH_DIR)

            if current_hash != last_hash:
                last_hash = current_hash
                push_changes()
                print("  Watching for next change...\n")

    except KeyboardInterrupt:
        print("\n  Watcher stopped.")


if __name__ == "__main__":
    main()
