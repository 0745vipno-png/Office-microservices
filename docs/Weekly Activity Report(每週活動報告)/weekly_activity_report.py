#!/usr/bin/env python3
"""
==================================================
Weekly Activity Report
==================================================

- 掃描最近 7 天的檔案活動
- 列出每日新增 / 修改的檔案
- 輸出為一般上班族可閱讀的文字報告

注意事項：
- 本工具為唯讀，不會修改或刪除任何檔案
- 請自行確保重要資料已有備份
"""

import os
import sys
import json
from datetime import datetime, date, timedelta
from collections import defaultdict
from typing import Dict, List, Set

LOG_FILE = "weekly_activity_report.log"
CONFIG_FILE = "daily_snapshot_config.json"

DAYS = 7  # 固定 7 天，刻意不做成參數，避免複雜化

# ===== 安全預設設定 =====

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


def scan_weekly_activity(base_dir: str) -> Dict[date, Dict[str, List[str]]]:
    today = date.today()
    start_day = today - timedelta(days=DAYS - 1)

    activity: Dict[date, Dict[str, List[str]]] = defaultdict(
        lambda: {"new": [], "modified": []}
    )

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

            if start_day <= created <= today:
                activity[created]["new"].append(rel_path)
            elif start_day <= modified <= today:
                activity[modified]["modified"].append(rel_path)

    log(
        f"Scanned={scanned}, Ignored={ignored}, "
        f"Days={DAYS}"
    )

    return activity


def print_report(base_dir: str, activity: Dict[date, Dict[str, List[str]]]) -> None:
    today = date.today()
    start_day = today - timedelta(days=DAYS - 1)

    print("=" * 40)
    print("Weekly Activity Report")
    print(f"Period : {start_day} ~ {today}")
    print(f"Folder : {base_dir}")
    print("=" * 40)
    print()

    total_new = sum(len(v["new"]) for v in activity.values())
    total_modified = sum(len(v["modified"]) for v in activity.values())

    print("[Summary]")
    print(f"- Days scanned        : {DAYS}")
    print(f"- New files created   : {total_new}")
    print(f"- Files modified      : {total_modified}")
    print(f"- Total activity      : {total_new + total_modified} files")
    print()

    print("[Daily Breakdown]")
    print()

    for day in sorted(activity.keys()):
        day_data = activity[day]
        if not day_data["new"] and not day_data["modified"]:
            continue

        print(f"{day}")
        if day_data["new"]:
            print("- New:")
            for f in sorted(day_data["new"]):
                print(f"  - {f}")
        if day_data["modified"]:
            print("- Modified:")
            for f in sorted(day_data["modified"]):
                print(f"  - {f}")
        print()

    print("[Note]")
    print("- Temporary and system files are ignored.")
    print("- Only common office document formats are listed.")
    print("- This report is read-only.")
    print()


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python weekly_activity_report.py <folder_path>")
        sys.exit(1)

    base_dir = sys.argv[1]

    if not os.path.isdir(base_dir):
        print("[ERROR] Folder not found.")
        sys.exit(1)

    activity = scan_weekly_activity(base_dir)
    print_report(base_dir, activity)


if __name__ == "__main__":
    main()
