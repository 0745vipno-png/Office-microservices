@echo off
REM ===================================================
REM run_all_reports.bat
REM 執行所有報告腳本，並將結果自動歸檔
REM ===================================================

SET BASE_DIR=%~dp0
SET WORK_FOLDER=C:\Your\Target\Folder\Path
SET PYTHON_EXE=python.exe

REM ---------------------------------------------------
REM 請修改上面的 WORK_FOLDER 為您要掃描的實際資料夾路徑
REM 例如: SET WORK_FOLDER=D:\Projects
REM ---------------------------------------------------

echo [Info] Starting all reports generation and archiving...
echo [Info] Scanning folder: %WORK_FOLDER%
echo.

REM ===================================================
REM 1. 執行每日快照 (Daily Snapshot)
REM ===================================================
echo === Running Daily Snapshot ===
call :run_script "%BASE_DIR%daily_snapshot.py" "DailySnapshot" "%WORK_FOLDER%"

REM ===================================================
REM 2. 執行每週活動報告 (Weekly Activity Report)
REM ===================================================
echo === Running Weekly Activity Report ===
call :run_script "%BASE_DIR%weekly_activity_report.py" "WeeklyActivity" "%WORK_FOLDER%"

REM ===================================================
REM 3. 執行資料夾健康報告 (Folder Health Report)
REM ===================================================
echo === Running Folder Health Report ===
call :run_script "%BASE_DIR%folder_health_report.py" "FolderHealth" "%WORK_FOLDER%"

REM ===================================================
REM 4. A 級異常警報觸發器（唯讀 / 被動）
REM ===================================================
echo === Running Anomaly Signal Emitter (A-Level) ===
%PYTHON_EXE% "%BASE_DIR%anomaly_emitter.py"

IF %ERRORLEVEL% NEQ 0 (
    echo [WARN] Anomalies detected. Please review anomaly_report.txt
) ELSE (
    echo [OK] No anomalies detected.
)

echo.
echo [Info] All report tasks finished.
echo [Info] Review anomaly_report.txt if warnings were shown.
pause
goto :eof


REM ===================================================
REM 子程序：執行報告並歸檔
REM ===================================================
:run_script
    SET SCRIPT_PATH=%1
    SET REPORT_NAME=%2
    SET FOLDER_PATH=%3

    echo [Info] Executing %REPORT_NAME%...

    REM 使用管道(|)將報告輸出導向 archiver.py
    %PYTHON_EXE% "%SCRIPT_PATH%" "%FOLDER_PATH%" | %PYTHON_EXE% "%BASE_DIR%report_archiver.py" "%REPORT_NAME%"

    IF %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to run %REPORT_NAME%. Check logs.
    ) ELSE (
        echo [OK] %REPORT_NAME% archived.
    )
    echo.
goto :eof
