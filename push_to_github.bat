@echo off
setlocal enabledelayedexpansion

echo ======================================================================
echo   NORTHSTAR SENTINEL - GIT PUSH RUNNER
echo   Repository: https://github.com/Heman-123/Northstar-Sentinel.git
echo ======================================================================
echo.

:: Detect and set Git path
set "GIT_CMD="
if exist "C:\Program Files\Git\cmd\git.exe" (
    set "GIT_CMD=C:\Program Files\Git\cmd\git.exe"
    set "PATH=%PATH%;C:\Program Files\Git\cmd;C:\Program Files\Git\bin"
) else if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Git\cmd\git.exe" (
    set "GIT_CMD=C:\Users\%USERNAME%\AppData\Local\Programs\Git\cmd\git.exe"
    set "PATH=%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Git\cmd"
) else (
    where git >nul 2>&1
    if !errorlevel! equ 0 (
        set "GIT_CMD=git"
    )
)

if "%GIT_CMD%"=="" (
    echo [ERROR] Git was not found in standard directories.
    echo Please install Git or ensure git.exe is in your PATH.
    pause
    exit /b 1
)

echo [*] Using Git at: %GIT_CMD%
echo.

cd /d "%~dp0"
echo [*] Working Directory: %CD%
echo.

echo [*] Initializing Git repository...
"%GIT_CMD%" init

echo [*] Setting branch to main...
"%GIT_CMD%" branch -M main

echo [*] Configuring remote origin...
"%GIT_CMD%" remote remove origin 2>nul
"%GIT_CMD%" remote add origin https://github.com/Heman-123/Northstar-Sentinel.git

echo [*] Staging all files...
"%GIT_CMD%" add .

echo [*] Committing deliverables and codebase...
"%GIT_CMD%" commit -m "feat: complete Northstar Sentinel platform for CRIMEATHON '26 (Case NS-26-014)" -m "Includes Deliverables 1-4, 6-stage DFIR pipeline, Zero-Trust PEP gateway, Splunk ES dashboard, 15 unit tests passing 100%, and executive forensic reports."

echo.
echo ======================================================================
echo [*] Pushing to GitHub (https://github.com/Heman-123/Northstar-Sentinel.git)...
echo ======================================================================
"%GIT_CMD%" push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo [!] Standard push was rejected (remote may contain an initial commit from GitHub).
    echo [!] Attempting force push to overwrite with complete project...
    echo.
    set /p choice="Do you want to force push to overwrite with the full project? (Y/N): "
    if /i "!choice!"=="Y" (
        "%GIT_CMD%" push -u origin main --force
    )
)

echo.
echo ======================================================================
echo Done! Check your repository at:
echo https://github.com/Heman-123/Northstar-Sentinel
echo ======================================================================
pause
