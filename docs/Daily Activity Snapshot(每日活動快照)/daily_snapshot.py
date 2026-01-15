#!/usr/bin/env python3
# NOTE: Do not enable followlinks to avoid unexpected scans
"""
==================================================
Daily Activity Snapshot (Configurable)
==================================================

- 支援外部 JSON 設定檔
- 若設定檔不存在或錯誤，自動使用安全預設值
- 適合一般上班族與一人公司日常使用

注意事項：
- 本工具為唯讀，不會修改或刪除任何檔案
- 請自行確保重要資料已有備份
"""

import os
import sys
import json
from datetime import datetime, date
from typing import List, Tuple, Set

LOG_FILE = "daily_snapshot.log"
CONFIG_FILE = "daily_snapshot_config.json"

# ===== 安全預設值（永遠存在） =====

DEFAULT_ALLOWED_EXTENSIONS: Set[str] = {
    ".docx", ".xlsx", ".pptx", ".pdf", ".txt"
}

DEFAULT_IGNORED_EXTENSIONS: Set[str] = {
    ".tmp"
}

DEFAULT_IGNORED_FILENAMES: Set[str] = {
    ".DS_Store", "Thumbs.db"
}


def log(msg: str) -> None:
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")


def load_config() -> tuple[Set[str], Set[str], Set[str]]:
    """
    載入 JSON 設定檔。
    若檔案不存在或格式錯誤，回退至預設值。
    """
    if not os.path.isfile(CONFIG_FILE):
        log("Config file not found. Using default settings.")
        return (
            DEFAULT_ALLOWED_EXTENSIONS,
            DEFAULT_IGNORED_EXTENSIONS,
            DEFAULT_IGNORED_FILENAMES,
        )

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        allowed = {
            ext.lower() for ext in data.get("allowed_extensions", [])
        } or DEFAULT_ALLOWED_EXTENSIONS

        ignored_ext = {
            ext.lower() for ext in data.get("ignored_extensions", [])
        }

        ignored_names = set(data.get("ignored_filenames", []))

        log("Config file loaded successfully.")

        return allowed, ignored_ext, ignored_names

    except Exception as e:
        log(f"Failed to load config. Using defaults. Error: {e}")
        return (
            DEFAULT_ALLOWED_EXTENSIONS,
            DEFAULT_IGNORED_EXTENSIONS,
            DEFAULT_IGNORED_FILENAMES,
        )


def is_relevant_file(
    filename: str,
    allowed_ext: Set[str],
    ignored_ext: Set[str],
    ignored_names: Set[str],
) -> bool:
    name = os.path.basename(filename)

    if name in ignored_names:
        return False

    ext = os.path.splitext(name)[1].lower()

    if ext in ignored_ext:
        return False

    return ext in allowed_ext


def scan_today_activity(base_dir: str) -> Tuple[List[str], List[str]]:
    today = date.today()
    new_files: List[str] = []
    modified_files: List[str] = []

    allowed_ext, ignored_ext, ignored_names = load_config()

    scanned = 0
    ignored = 0

    for root, _, files in os.walk(base_dir):
        for name in files:
            scanned += 1

            if not is_relevant_file(name, allowed_ext, ignored_ext, ignored_names):
                ignored += 1
                continue

            path = os.path.join(root, name)
            try:
                stat = os.stat(path)
            except OSError:
                continue

            created = datetime.fromtimestamp(stat.st_ctime).date()
            modified = datetime.fromtimestamp(stat.st_mtime).date()

            rel_path = os.path.relpath(path, base_dir)

            if created == today:
                new_files.append(rel_path)
            elif modified == today:
                modified_files.append(rel_path)

    log(
        f"Scanned={scanned}, Ignored={ignored}, "
        f"New={len(new_files)}, Modified={len(modified_files)}"
    )

    return new_files, modified_files


def print_report(base_dir: str, new_files: List[str], modified_files: List[str]) -> None:
    today_str = date.today().isoformat()

    print("=" * 30)
    print("Daily Activity Snapshot")
    print(f"Date  : {today_str}")
    print(f"Folder: {base_dir}")
    print("=" * 30)
    print()

    print("[Summary]")
    print(f"- New files created   : {len(new_files)}")
    print(f"- Files modified      : {len(modified_files)}")
    print(f"- Total activity      : {len(new_files) + len(modified_files)} files")
    print()

    if new_files:
        print("[New Files]")
        for f in sorted(new_files):
            print(f"- {f}")
        print()

    if modified_files:
        print("[Modified Files]")
        for f in sorted(modified_files):
            print(f"- {f}")
        print()

    print("[Note]")
    print("File filtering rules are configurable via JSON config.")
    print("This report is read-only.")
    print("Please make sure important files are backed up manually.")
    print()


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python daily_snapshot.py <folder_path>")
        sys.exit(1)

    base_dir = sys.argv[1]

    if not os.path.isdir(base_dir):
        print("[ERROR] Folder not found.")
        sys.exit(1)

    new_files, modified_files = scan_today_activity(base_dir)
    print_report(base_dir, new_files, modified_files)


if __name__ == "__main__":
    main()
