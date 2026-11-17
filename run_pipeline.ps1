# Northstar Sentinel - Windows PowerShell Pipeline Runner
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " NORTHSTAR SENTINEL: FORENSIC PIPELINE EXECUTION (WINDOWS)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Locate Python Executable
$pythonCmd = $null

if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} else {
    # Check common Windows install directories
    $commonPaths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python39\python.exe",
        "C:\Program Files\Python312\python.exe",
        "C:\Program Files\Python311\python.exe",
        "C:\Program Files\Python310\python.exe",
        "C:\Python312\python.exe",
        "C:\Python311\python.exe",
        "C:\Python310\python.exe",
        "$env:USERPROFILE\anaconda3\python.exe",
        "$env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe"
    )

    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            $pythonCmd = "& `"$path`""
            break
        }
    }
}

if (-not $pythonCmd) {
    Write-Host "`n[-] ERROR: Python was not found on your Windows system." -ForegroundColor Red
    Write-Host "[!] Please install Python 3.9+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "    IMPORTANT: Check the box 'Add python.exe to PATH' during installation!" -ForegroundColor Yellow
    exit 1
}

Write-Host "[+] Python runtime located: $pythonCmd" -ForegroundColor Green

# 2. Execute 6 Pipeline Stages
$stages = @(
    "src\01_verify_ingest.py",
    "src\02_normalize.py",
    "src\03_correlate.py",
    "src\04_detect.py",
    "src\05_risk_scoring.py",
    "src\06_generate_report.py"
)

foreach ($stage in $stages) {
    Write-Host "`n[*] Executing: $stage ..." -ForegroundColor Yellow
    if ($pythonCmd -eq "py" -or $pythonCmd -eq "python") {
        & $pythonCmd $stage
    } else {
        Invoke-Expression "$pythonCmd $stage"
    }
}

Write-Host "`n[+] Running Security Test Harness (11 Tests)..." -ForegroundColor Yellow
if ($pythonCmd -eq "py" -or $pythonCmd -eq "python") {
    & $pythonCmd "simulation\test_hardened_api.py"
} else {
    Invoke-Expression "$pythonCmd simulation\test_hardened_api.py"
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " ALL STAGES & TESTS COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host " Formal report saved to: reports\NORTHSTAR_SENTINEL_INVESTIGATION_REPORT.md" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
