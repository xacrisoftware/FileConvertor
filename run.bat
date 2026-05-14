@echo off
title FILE CONVERTOR

:: Try the .exe right next to this script
if exist "%~dp0FileConvertor.exe" (
    start "" "%~dp0FileConvertor.exe"
    exit /b
)

:: Fallback: run via Python from src/
if exist "%~dp0src\main.py" (
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        python "%~dp0src\main.py"
        exit /b
    )
)

:: Nothing works
echo [ERROR] FileConvertor.exe not found, and Python is not available.
echo.
echo Options:
echo   1. Download .exe from: https://github.com/username/FileConvertor/releases
echo   2. Install Python from: https://python.org
echo.
pause
