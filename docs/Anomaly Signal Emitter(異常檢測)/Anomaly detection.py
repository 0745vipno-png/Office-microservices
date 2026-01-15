#!/usr/bin/env python3
"""
==================================================
Anomaly Signal Emitter (A-Level)
==================================================

- 唯讀、被動式異常偵測
- 僅產生「異常訊號」與證據
- 不修復、不重跑、不決策

設計原則：
- 人類判斷，系統提醒
- 所有輸出皆可回溯
"""

import os
from datetime import datetime, date, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

REPORT_DIR = os.path.join(BASE_DIR, "reports")
LOG_DIR = os.path.join(BASE_DIR, "logs")

ANOMALY_LOG = os.path.join(BASE_DIR, "anomaly.log")
ANOMALY_REPORT = os.path.join(BASE_DIR, "anomaly_report.txt")


def log(msg: str):
    with open(ANOMALY_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")


def latest_file_in(dir_path: str):
    if not os.path.isdir(dir_path):
        return None
    files = [
        os.path.join(dir_path, f)
        for f in os.listdir(dir_path)
        if f.endswith(".txt")
    ]
    return max(files, key=os.path.getmtime) if files else None


def check_expected_reports():
    today = date.today()
    anomalies = []

    daily = latest_file_in(os.path.join(REPORT_DIR, "DailySnapshot"))
    weekly = latest_file_in(os.path.join(REPORT_DIR, "WeeklyActivity"))
    monthly = latest_file_in(os.path.join(REPORT_DIR, "MonthlyActivity"))

    if not daily:
        anomalies.append("Daily report missing")

    if not weekly and today.weekday() == 0:
        anomalies.append("Weekly report missing (Monday check)")

    if not monthly and today.day <= 3:
        anomalies.append("Monthly report missing (early-month check)")

    return anomalies


def check_scheduler_vs_task():
    scheduler_log = os.path.join(LOG_DIR, "scheduler_log.txt")
    task_log = os.path.join(LOG_DIR, "task_log.txt")

    if not os.path.isfile(scheduler_log) or not os.path.isfile(task_log):
        return []

    with open(scheduler_log, encoding="utf-8") as f:
        scheduler_lines = f.readlines()

    with open(task_log, encoding="utf-8") as f:
        task_lines = f.readlines()

    anomalies = []

    for line in scheduler_lines[-10:]:
        if "Created task" in line:
            task_name = line.strip()
            matched = any(task_name in t for t in task_lines)
            if not matched:
                anomalies.append(f"Scheduled task has no execution record: {task_name}")

    return anomalies


def emit_report(anomalies):
    timestamp = datetime.now().isoformat()

    with open(ANOMALY_REPORT, "w", encoding="utf-8") as f:
        f.write("Anomaly Signal Report\n")
        f.write("=" * 30 + "\n")
        f.write(f"Generated at: {timestamp}\n\n")

        if not anomalies:
            f.write("No anomalies detected.\n")
        else:
            f.write("Detected anomalies:\n")
            for a in anomalies:
                f.write(f"- {a}\n")

    log(f"Anomaly report generated with {len(anomalies)} issue(s)")


def main():
    anomalies = []

    anomalies.extend(check_expected_reports())
    anomalies.extend(check_scheduler_vs_task())

    emit_report(anomalies)

    if anomalies:
        print("[WARN] Anomalies detected. Please review anomaly_report.txt")
        for a in anomalies:
            print(f" - {a}")
        exit(1)

    print("[OK] No anomalies detected.")


if __name__ == "__main__":
    main()
