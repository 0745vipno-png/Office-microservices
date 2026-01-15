#!/usr/bin/env python3
"""
==================================================
Report Archiver
==================================================

- 從 STDIN 接收文字報告
- 依照報告類型與時間，自動存檔
- 不解析、不修改、不理解內容

使用方式：
python some_report.py ... | python report_archiver.py <report_name>
"""

import sys
import os
from datetime import datetime

BASE_REPORT_DIR = "reports"


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python report_archiver.py <report_name>")
        sys.exit(1)

    report_name = sys.argv[1].strip()
    if not report_name:
        print("[ERROR] Report name cannot be empty.")
        sys.exit(1)

    content = sys.stdin.read()
    if not content.strip():
        print("[ERROR] No input received from STDIN.")
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    report_dir = os.path.join(BASE_REPORT_DIR, report_name)
    os.makedirs(report_dir, exist_ok=True)

    report_path = os.path.join(report_dir, f"{timestamp}.txt")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] Report archived at: {report_path}")


if __name__ == "__main__":
    main()
