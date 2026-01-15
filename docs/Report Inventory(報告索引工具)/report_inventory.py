#!/usr/bin/env python3
"""
==================================================
Report Inventory
==================================================

- 掃描 reports 目錄
- 列出目前實際存在的報告檔案
- 僅整理與顯示，不做任何修改或判斷

注意事項：
- 本工具為唯讀
- 不推論「應該存在的報告」
- 不進行補齊、分類正確性或完整性判斷
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple

BASE_REPORT_DIR = "reports"


def parse_timestamp(filename: str) -> str:
    """
    嘗試從檔名解析時間戳。
    若失敗，僅回傳原始檔名。
    """
    name = os.path.splitext(filename)[0]
    try:
        dt = datetime.strptime(name, "%Y-%m-%d_%H-%M-%S")
        return dt.isoformat(sep=" ")
    except ValueError:
        return filename


def scan_reports(base_dir: str) -> Dict[str, List[Tuple[str, str]]]:
    """
    掃描 reports 目錄結構。

    回傳結構：
    {
        report_type: [
            (filename, parsed_time),
            ...
        ]
    }
    """
    inventory: Dict[str, List[Tuple[str, str]]] = {}

    if not os.path.isdir(base_dir):
        return inventory

    for report_type in sorted(os.listdir(base_dir)):
        type_dir = os.path.join(base_dir, report_type)
        if not os.path.isdir(type_dir):
            continue

        files: List[Tuple[str, str]] = []

        for name in sorted(os.listdir(type_dir)):
            path = os.path.join(type_dir, name)
            if not os.path.isfile(path):
                continue

            timestamp = parse_timestamp(name)
            files.append((name, timestamp))

        if files:
            inventory[report_type] = files

    return inventory


def print_report(inventory: Dict[str, List[Tuple[str, str]]]) -> None:
    print("=" * 40)
    print("Report Inventory")
    print("=" * 40)
    print()

    if not inventory:
        print("No reports found.")
        print()
        return

    for report_type, files in inventory.items():
        print(f"[{report_type}]")
        print(f"- Count: {len(files)}")

        for filename, timestamp in files:
            print(f"  - {filename} ({timestamp})")

        print()


def main() -> None:
    if len(sys.argv) > 2:
        print("Usage: python report_inventory.py [reports_dir]")
        sys.exit(1)

    base_dir = sys.argv[1] if len(sys.argv) == 2 else BASE_REPORT_DIR

    inventory = scan_reports(base_dir)
    print_report(inventory)


if __name__ == "__main__":
    main()
