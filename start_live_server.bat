@echo off
setlocal enabledelayedexpansion

echo ==========================================================
echo  NORTHSTAR SENTINEL: LIVE MONITORING SERVER (WINDOWS)
echo ==========================================================

:: 1. Locate Python
set PYCMD=py
where py >nul 2>nul
if %errorlevel% neq 0 (
    set PYCMD=python
    where python >nul 2>nul
    if %errorlevel% neq 0 (
        if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
            set PYCMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        )
    )
)

echo [+] Launching Sentinel Hardened Proxy on http://127.0.0.1:8765...
%PYCMD% simulation\mock_api_server.py --mode hardened

pause
