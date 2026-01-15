report_archiver.py

Purpose
將任何 CLI 工具的輸出內容，依時間自動存成報告檔案。

Usage

python some_report.py ... | python report_archiver.py <report_name>


Example

python daily_snapshot.py C:\work\projectA | python report_archiver.py daily_snapshot


Generated structure

reports/
├─ daily_snapshot/
│   └─ 2026-01-09_18-32-10.txt
├─ weekly_activity/
│   └─ 2026-01-09_18-35-44.txt
└─ folder_health/
    └─ 2026-01-09_18-38-02.txt