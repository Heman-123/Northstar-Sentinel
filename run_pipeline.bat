@echo off
setlocal enabledelayedexpansion

echo ==========================================================
echo  NORTHSTAR SENTINEL: FORENSIC PIPELINE EXECUTION (WINDOWS)
echo ==========================================================

:: 1. Check for 'py' command (Windows Python Launcher)
where py >nul 2>nul
if %errorlevel% equ 0 (
    set PYCMD=py
    goto RUN
)

:: 2. Check for 'python' command
where python >nul 2>nul
if %errorlevel% equ 0 (
    set PYCMD=python
    goto RUN
)

:: 3. Check AppData Python paths
for %%v in (Python312 Python311 Python310 Python39) do (
    if exist "%LOCALAPPDATA%\Programs\Python\%%v\python.exe" (
        set PYCMD="%LOCALAPPDATA%\Programs\Python\%%v\python.exe"
        goto RUN
    )
    if exist "C:\Program Files\Python\%%v\python.exe" (
        set PYCMD="C:\Program Files\Python\%%v\python.exe"
        goto RUN
    )
    if exist "C:\%%v\python.exe" (
        set PYCMD="C:\%%v\python.exe"
        goto RUN
    )
)

echo.
echo [!] ERROR: Python is not found or not registered in PATH.
echo [!] Please install Python from https://www.python.org/downloads/
echo     (Make sure to check "Add python.exe to PATH" during installation)
pause
exit /b 1

:RUN
echo [+] Using Python: %PYCMD%
echo.

echo [*] Stage 1: Ingesting and Verifying Hashes...
%PYCMD% src\01_verify_ingest.py
echo.

echo [*] Stage 2: Normalizing Logs to OCSF Schema...
%PYCMD% src\02_normalize.py
echo.

echo [*] Stage 3: Correlating Cross-Source Events...
%PYCMD% src\03_correlate.py
echo.

echo [*] Stage 4: Running Behavioral Detection Rules...
%PYCMD% src\04_detect.py
echo.

echo [*] Stage 5: Computing Decoupled Risk Scores...
%PYCMD% src\05_risk_scoring.py
echo.

echo [*] Stage 6: Generating Formal DFIR Report...
%PYCMD% src\06_generate_report.py
echo.

echo [*] Running 11 Automated Security Tests...
%PYCMD% simulation\test_hardened_api.py
echo.

echo [*] Running Comprehensive Pipeline Unit Tests...
%PYCMD% tests\test_pipeline.py
echo.

echo ==========================================================
echo  ALL STAGES AND TESTS COMPLETED SUCCESSFULLY!
echo  Check reports\NORTHSTAR_SENTINEL_INVESTIGATION_REPORT.md
echo ==========================================================
pause
