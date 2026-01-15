import subprocess
import os
from datetime import datetime

# =========================================================
# 一次性排程器（One-Time Task Scheduler）
#
# 設計目標：
# - 只建立「跑一次」的 Windows 排程
# - 不使用高權限、不常駐、不自動重試
# - 每一次建立行為都留下證據（log）
#
# 適用情境：
# - 個人自動化
# - 可驗證、可回溯
# - 防止自己亂排程、忘記排過什麼
# =========================================================

# 取得目前這個檔案所在的資料夾
# 所有 log 都固定寫在這裡，避免 working directory 問題
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 排程建立行為的永久紀錄（append-only）
LOG_PATH = os.path.join(BASE_DIR, "scheduler_log.txt")


def log(msg: str):
    """
    將排程建立相關事件寫入 log。
    不覆寫、不清空，確保歷史行為可追溯。
    """
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")


def create_task(task_name: str, script_path: str, run_time: str):
    """
    建立一個「只跑一次」的 Windows 排程任務。

    注意事項（給未來的自己）：
    - 使用 schtasks CLI，而非 COM API（簡單、可預期）
    - /tr 參數必須是一整條 command string（不能拆）
    - 不指定 /ru /rl，避免權限風險
    """

    # 使用目前執行這個 scheduler 的 Python 解譯器
    # 確保 virtualenv / 版本一致
    python_exe = os.sys.executable

    # 驗證時間格式（錯就直接 fail）
    # schtasks 本身對錯誤時間的回饋不可靠
    datetime.strptime(run_time, "%H:%M")

    # /tr 需要的是完整 command line
    # 這裡必須自行處理引號，避免路徑含空白出錯
    task_command = f'"{python_exe}" "{script_path}"'

    # schtasks 參數：
    # /sc once  → 只跑一次
    # /st HH:MM → 當天指定時間
    # /tn       → 任務名稱
    # /tr       → 要執行的指令
    # /f        → 若已存在則覆蓋（避免卡住）
    cmd = [
        "schtasks",
        "/create",
        "/sc", "once",
        "/st", run_time,
        "/tn", task_name,
        "/tr", task_command,
        "/f"
    ]

    # 不使用 shell=True，避免不必要風險
    subprocess.run(cmd, check=True)

    # 成功後寫入 log，作為「建立證據」
    log(f"Created task '{task_name}' at {run_time} -> {script_path}")

    print(f"[OK] Task '{task_name}' scheduled at {run_time}")


if __name__ == "__main__":
    print("=== One-Time Task Scheduler ===")

    # 讓使用者（自己）明確指定要被排程的 Python 腳本
    script = input("Python script path: ").strip().strip('"')
    if not os.path.isfile(script):
        print("[ERROR] Script not found")
        exit(1)

    # 排程任務名稱（會顯示在 Windows 排程器）
    task_name = input("Task name: ").strip()

    # 執行時間（24 小時制）
    run_time = input("Run time (HH:MM): ").strip()

    # 最後一道人為確認
    # 防止手滑或複製貼上造成意外排程
    confirm = input("Create ONE-TIME task? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Aborted.")
        exit(0)

    try:
        create_task(task_name, script, run_time)
    except Exception as e:
        # 若建立失敗，也要留下紀錄
        log(f"[ERROR] Failed to create task: {e}")
        print("[ERROR] Failed to create scheduled task")
