import os
from datetime import datetime
import traceback

# =========================================================
# 被 Windows Task Scheduler 執行的腳本
#
# 設計目標：
# - 不依賴 stdout / console
# - 不假設使用者登入
# - 只做一件事：留下「確實被執行」的證據
#
# 這個檔案的存在目的：
# - 驗證排程真的有跑
# - 區分「排程成功」與「實際執行成功」
# =========================================================

# 取得此檔案所在資料夾
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 強制將 working directory 固定在這裡
# 避免 Scheduler 預設使用 C:\Windows\System32
os.chdir(BASE_DIR)

# 執行紀錄檔（append-only）
LOG_PATH = os.path.join(BASE_DIR, "task_log.txt")


def log(msg: str):
    """
    寫入執行結果。
    不清檔、不覆寫，確保每次執行都有痕跡。
    """
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")


if __name__ == "__main__":
    try:
        # 正常執行路徑
        log(f"[OK] Ran at {datetime.now()}")

    except Exception:
        # 若未來加邏輯而發生錯誤
        # 也必須留下可追查的訊息
        log(f"[FAIL] {datetime.now()}")
        log(traceback.format_exc())
