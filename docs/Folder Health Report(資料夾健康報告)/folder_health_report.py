#!/usr/bin/env python3
"""
==================================================
Folder Health Report
==================================================

- 檢查資料夾健康狀態
- 列出空資料夾、大型檔案、久未修改的檔案
- 僅產出報告，不會修改或刪除任何資料

注意事項：
- 本工具為唯讀
- 請自行確保重要資料已有備份
"""

import os
import sys
from datetime import datetime, date, timedelta
from typing import List, Tuple

LOG_FILE = "folder_health_report.log"

# ===== 健康檢查門檻（刻意寫死，避免過度複雜） =====

LARGE_FILE_MB = 50
STALE_DAYS = 180


def log(msg: str) -> None:
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")


def is_empty_folder(path: str) -> bool:
    try:
        return not any(os.scandir(path))
    except OSError:
        return False


def scan_folder_health(base_dir: str) -> Tuple[List[str], List[Tuple[str, float]], List[Tuple[str, date]]]:
    empty_folders: List[str] = []
    large_files: List[Tuple[str, float]] = []
    stale_files: List[Tuple[str, date]] = []

    today = date.today()
    stale_threshold = today - timedelta(days=STALE_DAYS)

    scanned_files = 0
    scanned_dirs = 0

    for root, dirs, files in os.walk(base_dir):
        scanned_dirs += 1

        # 檢查空資料夾
        if is_empty_folder(root):
            rel_dir = os.path.relpath(root, base_dir)
            if rel_dir != ".":
                empty_folders.append(rel_dir)

        for name in files:
            scanned_files += 1
            path = os.path.join(root, name)

            try:
                stat = os.stat(path)
            except OSError:
                continue

            size_mb = stat.st_size / (1024 * 1024)
            modified_date = datetime.fromtimestamp(stat.st_mtime).date()

            rel_path = os.path.relpath(path, base_dir)

            if size_mb >= LARGE_FILE_MB:
                large_files.append((rel_path, size_mb))

            if modified_date <= stale_threshold:
                stale_files.append((rel_path, modified_date))

    log(
        f"Scanned_dirs={scanned_dirs}, "
        f"Scanned_files={scanned_files}, "
        f"Empty={len(empty_folders)}, "
        f"Large={len(large_files)}, "
        f"Stale={len(stale_files)}"
    )

    return empty_folders, large_files, stale_files


def print_report(
    base_dir: str,
    empty_folders: List[str],
    large_files: List[Tuple[str, float]],
    stale_files: List[Tuple[str, date]],
) -> None:
    today_str = date.today().isoformat()

    print("=" * 40)
    print("Folder Health Report")
    print(f"Scan Date : {today_str}")
    print(f"Folder    : {base_dir}")
    print("=" * 40)
    print()

    print("[Summary]")
    print(f"- Empty folders            : {len(empty_folders)}")
    print(f"- Large files (>= {LARGE_FILE_MB} MB)   : {len(large_files)}")
    print(f"- Stale files (>= {STALE_DAYS} days) : {len(stale_files)}")
    print()

    if empty_folders:
        print("[Empty Folders]")
        for d in sorted(empty_folders):
            print(f"- {d}")
        print()

    if large_files:
        print("[Large Files]")
        for path, size in sorted(large_files, key=lambda x: -x[1]):
            print(f"- {path} ({size:.1f} MB)")
        print()

    if stale_files:
        print("[Stale Files]")
        for path, mdate in sorted(stale_files, key=lambda x: x[1]):
            print(f"- {path} (last modified: {mdate})")
        print()

    print("[Note]")
    print("- This report is read-only.")
    print("- No files or folders were modified.")
    print("- Please review carefully before taking any action.")
    print()


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python folder_health_report.py <folder_path>")
        sys.exit(1)

    base_dir = sys.argv[1]

    if not os.path.isdir(base_dir):
        print("[ERROR] Folder not found.")
        sys.exit(1)

    empty_folders, large_files, stale_files = scan_folder_health(base_dir)
    print_report(base_dir, empty_folders, large_files, stale_files)


if __name__ == "__main__":
    main()
