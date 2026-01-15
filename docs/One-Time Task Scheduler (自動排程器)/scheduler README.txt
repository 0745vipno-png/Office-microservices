5. One-Time Task Scheduler (Optional)

scheduler.py

Purpose
在 Windows 環境下建立「只跑一次」的排程任務。

Characteristics

不常駐

不高權限

每次建立行為都有 log 紀錄

Configuration (Optional)

部分工具支援外部 JSON 設定檔：

daily_snapshot_config.json

可調整項目：

關心的檔案副檔名（如 .docx, .xlsx）

忽略的暫存或系統檔案（如 .tmp, .DS_Store)

若設定檔不存在或格式錯誤，工具會自動使用安全預設值。

Safety & Responsibility

本工具組 不保證結果正確性

僅負責「列出當下檔案狀態」

所有刪除、修改、清理行為，應由使用者自行判斷並執行

使用前請自行備份重要資料

Who Is This For?

一人公司 / 接案工作者

需要留下工作證據的工程師

想降低日常辦公摩擦，但不想引入複雜系統的人