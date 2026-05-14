# FILE CONVERTOR — PowerShell Launcher
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Try .exe in root first
$ExePath = Join-Path $ScriptDir "FileConvertor.exe"
if (Test-Path $ExePath) {
    Write-Host "Starting FileConvertor..." -ForegroundColor Green
    Start-Process -FilePath $ExePath
    exit
}

# Fallback to Python src/main.py
$MainPy = Join-Path $ScriptDir "src\main.py"
if (Test-Path $MainPy) {
    try {
        python --version | Out-Null
        Write-Host "Starting FileConvertor via Python..." -ForegroundColor Green
        python $MainPy
        exit
    } catch {
        Write-Host "Python not found!" -ForegroundColor Red
    }
}

Write-Host "[ERROR] FileConvertor.exe not found and Python is not available." -ForegroundColor Red
Write-Host ""
Write-Host "Options:" -ForegroundColor Yellow
Write-Host "  1. Download .exe from: https://github.com/username/FileConvertor/releases"
Write-Host "  2. Install Python from: https://python.org"
Write-Host ""
Read-Host "Press Enter to exit"
