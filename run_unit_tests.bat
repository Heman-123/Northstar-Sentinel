@echo off
setlocal enabledelayedexpansion

echo ==========================================================
echo  NORTHSTAR SENTINEL: MODULAR UNIT TEST SUITE (WINDOWS)
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
echo [+] Executing Modular Stage Unit Tests (tests/test_*.py)...
echo.

%PYCMD% -m unittest discover tests -v

echo.
echo ==========================================================
echo  UNIT TESTS COMPLETE!
echo ==========================================================
pause
