Anomaly Signal Emitter（A-Level）
模組定位

Anomaly Signal Emitter 是一個
唯讀、被動、證據導向 的異常警報觸發模組。

它的唯一目的，是在既有的「報告與紀錄」基礎上，
將「人類會停下來注意的狀態不一致」轉換成明確、可回溯的警示訊號。

設計原則（不可變）

本模組 不做決策

本模組 不修復問題

本模組 不自動重跑任務

本模組 不修改任何資料

本模組 不假設「正確做法」

人類負責判斷，系統只負責提醒。

本模組是什麼

一個可被排程執行的 一次性檢查工具

一個基於既有輸出物（report / log）的 異常訊號產生器

一個提供「可讀證據」的可靠性元件

本模組不是什麼

❌ 監控 daemon

❌ 自動修復器

❌ Health checker with actions

❌ 決策引擎

❌ 長駐背景服務

支援的異常類型（A 級）

本模組僅檢查 靜態、可列舉、低風險 的異常條件。

1. 應有報告不存在

今日未產生 Daily Snapshot

本週（週一）未產生 Weekly Activity Report

本月初（前 3 天）未產生 Monthly Report

僅檢查「是否存在」，
不解析內容、不評估品質。

2. 排程與實際執行不一致

scheduler_log.txt 中有「任務建立紀錄」

但 task_log.txt 中找不到對應的實際執行證據

此類異常通常代表：

排程成功但未實際執行

或執行失敗但未被人注意

輸出行為

當模組執行時，會產生以下輸出：

1. anomaly_report.txt

每次執行都會重新產生

內容包含：

產生時間

異常列表（若存在）

明確、可閱讀的描述

2. anomaly.log（append-only）

永不覆寫

每次執行皆留下紀錄

作為長期追蹤與稽核依據

3. Console 輸出

[OK] No anomalies detected.

或 [WARN] Anomalies detected...

4. Exit Code

0：未偵測到異常

1：偵測到至少一項異常

Exit code 僅作為「訊號」，
不代表系統狀態已被處理。

檔案結構假設
office_microservices/
├─ reports/
│  ├─ DailySnapshot/
│  ├─ WeeklyActivity/
│  ├─ MonthlyActivity/
│
├─ logs/
│  ├─ scheduler_log.txt
│  ├─ task_log.txt
│
├─ anomaly_emitter.py
├─ anomaly.log
└─ anomaly_report.txt

使用方式
python anomaly_emitter.py


建議使用情境：

所有報告與排程任務完成後

作為每日 / 每週的「最後一道檢查」

可由排程器或批次檔呼叫

設計哲學說明（重要）

本模組刻意 不嘗試變聰明。

它不推測原因、不計算趨勢、不提供建議行動，
只做一件事：

把「系統狀態不一致」轉成「人類可注意的訊號」。

這是為了避免：

自動化過度

錯誤被放大

責任歸屬模糊

不建議的使用方式（請勿）

❌ 將本模組作為自動修復觸發器

❌ 依據異常結果直接刪檔 / 重跑 / 更改狀態

❌ 在未理解異常原因前忽略警告

❌ 將本模組當作「健康 OK 的保證」

適用對象

重視 可回溯性 的個人或小型團隊

不希望系統「偷偷幫忙決定」的使用者

偏好「慢一點，但不出事」的自動化風格

結語

Anomaly Signal Emitter
不是為了讓系統更聰明，
而是為了讓人類 不被系統蒙蔽。

當系統開始能提醒人，
而不是替人決定，
可靠性才真正成立。