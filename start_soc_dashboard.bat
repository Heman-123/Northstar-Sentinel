@echo off
setlocal enabledelayedexpansion

echo ==========================================================
echo  NORTHSTAR SENTINEL: ENTERPRISE SOC COMMAND CENTER LAUNCH
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
echo [+] Starting Sentinel Live Telemetry and PEP Proxy on port 8765...

:: 2. Launch mock_api_server.py in a minimized background CMD window
start /min "Sentinel PEP Proxy Server" %PYCMD% simulation\mock_api_server.py --mode hardened

:: 3. Wait 1 second for port binding
timeout /t 1 /nobreak >nul

:: 4. Launch the SOC Command Center in the default browser
echo [+] Launching Enterprise SOC Dashboard in your default browser...
start http://127.0.0.1:8765

echo.
echo ==========================================================
echo  SUCCESS: SOC WORKBENCH IS NOW ACTIVE!
echo  URL: http://127.0.0.1:8765
echo.
echo  To trigger simulated live attacks, run:
echo    .\fire_attack.bat
echo ==========================================================
echo.
pause
