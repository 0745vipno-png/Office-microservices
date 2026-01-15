# Office Utility CLI Toolkit

一組一次性執行、只讀、以「人類可讀報告」為核心的辦公室輔助 CLI 工具集合。

本專案專注於將日常工作中可觀測的事實（檔案活動、資料夾狀態）
轉換為可回溯、可閱讀、可審閱的文字報告，
而不是建立長期服務、背景程序或自動決策系統。

本工具組的核心目標是：
降低日常工作摩擦，而不是替人做判斷。

設計原則如下：
- 所有工具皆為一次性執行（one-shot CLI）
- 不常駐、不背景執行
- 不修改、不刪除任何使用者資料
- 不進行自動判斷或決策
- 輸出內容以一般上班族可直接閱讀的文字為主
- 所有行為皆可回溯（log 與報告檔案）

這是一套「留下證據，而不是承諾結果」的工具集合。

本工具組包含以下模組：

Daily Activity Snapshot  
用於列出指定資料夾中「今天新增與修改的檔案」。  
適合下班前快速回顧當日實際檔案活動。  

執行方式：
python daily_snapshot.py <folder_path>

Weekly Activity Report  
彙整最近 7 天的檔案活動，依日期列出新增與修改紀錄。  
適合週報整理或短期工作回顧，不進行任何效率或進度判斷。  

執行方式：
python weekly_activity_report.py <folder_path>

Monthly Activity Report  
回顧指定月份內的長期檔案活動輪廓。  
用於觀察長期行為模式，僅提供事實彙整，不適用於績效評估或自動化決策。  

執行方式：
python monthly_activity_report.py <folder_path> <year> <month>

Folder Health Report  
盤點資料夾結構狀態與潛在風險，例如空資料夾、過大檔案、久未修改檔案。  
僅產出報告，不進行任何清理或修改。  

執行方式：
python folder_health_report.py <folder_path>

Report Archiver  
將任何 CLI 工具的文字輸出內容，依時間轉為不可變的歷史報告檔案。  
僅從 STDIN 接收內容，不解析、不理解、不修改輸入資料。  

使用方式：
python some_report.py ... | python report_archiver.py <report_name>

Report Inventory  
盤點目前實際存在的報告檔案。  
僅掃描 reports 目錄結構，列出「實際存在的報告事實」，不推論完整性、不補跑、不做判斷。  

執行方式：
python report_inventory.py

One-Time Task Scheduler（可選）  
在 Windows 環境下建立「只跑一次」的排程任務。  
僅負責建立排程並留下審計紀錄，不執行、不解讀任何業務邏輯。  
所有工具皆可手動執行，本模組僅在需要排程證據時使用。

系統架構、責任邊界與非目標說明，請參考 architecture.md  
設計原則與風險約束，請參考 design-principles.md  
各模組的詳細行為與限制，請參考各資料夾內的 README 文件。

本工具組僅提供：
「在某一時間尺度下，檔案系統實際發生了什麼」。

如何解讀這些結果、是否採取行動，以及行動後果，
皆需由使用者自行判斷並承擔。
