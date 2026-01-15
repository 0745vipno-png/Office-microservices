#!/usr/bin/env python3
"""
==================================================
Monthly Activity Report
==================================================

- 掃描指定月份的檔案活動
- 列出該月每日新增 / 修改的檔案
- 輸出為人類可閱讀的文字報告

注意事項：
- 本工具為唯讀，不會修改或刪除任何檔案
- 不依賴 Daily / Weekly 是否曾執行
- 僅根據檔案系統現況推導
"""

import os
import sys
import json
from datetime import datetime, date, timedelta
from collections import defaultdict
from typing import Dict, List, Set

LOG_FILE = "monthly_activity_report.log"
CONFIG_FILE = "daily_snapshot_config.json"

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


def month_range(year: int, month: int) -> tuple[date, date]:
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(year, month + 1, 1) - timedelta(days=1)
    return start, end


def scan_monthly_activity(
    base_dir: str,
    year: int,
    month: int,
) -> Dict[date, Dict[str, List[str]]]:
    start_day, end_day = month_range(year, month)

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

            if start_day <= created <= end_day:
                activity[created]["new"].append(rel_path)
            elif start_day <= modified <= end_day:
                activity[modified]["modified"].append(rel_path)

    log(
        f"Scanned={scanned}, Ignored={ignored}, "
        f"Period={start_day}~{end_day}"
    )

    return activity


def print_report(
    base_dir: str,
    year: int,
    month: int,
    activity: Dict[date, Dict[str, List[str]]],
) -> None:
    start_day, end_day = month_range(year, month)

    print("=" * 45)
    print("Monthly Activity Report")
    print(f"Period : {start_day} ~ {end_day}")
    print(f"Folder : {base_dir}")
    print("=" * 45)
    print()

    total_new = sum(len(v["new"]) for v in activity.values())
    total_modified = sum(len(v["modified"]) for v in activity.values())

    print("[Summary]")
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

        print(day)
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
    print("- This report is read-only.")
    print("- Data is inferred from file timestamps.")
    print("- Creation time semantics may vary by OS.")
    print()


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: python monthly_activity_report.py <folder_path> <year> <month>")
        sys.exit(1)

    base_dir = sys.argv[1]
    year = int(sys.argv[2])
    month = int(sys.argv[3])

    if not os.path.isdir(base_dir):
        print("[ERROR] Folder not found.")
        sys.exit(1)

    if month < 1 or month > 12:
        print("[ERROR] Month must be 1-12.")
        sys.exit(1)

    activity = scan_monthly_activity(base_dir, year, month)
    print_report(base_dir, year, month, activity)


if __name__ == "__main__":
    main()
