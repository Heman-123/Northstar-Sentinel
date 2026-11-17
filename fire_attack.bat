@echo off
setlocal enabledelayedexpansion

echo ==========================================================
echo  NORTHSTAR SENTINEL: LIVE ATTACK DISPATCHER (WINDOWS)
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

echo [+] Using Python: %PYCMD%
%PYCMD% simulation\fire_live_attack.py

pause
