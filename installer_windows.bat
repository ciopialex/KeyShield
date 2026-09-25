@echo off
REM ==============================================================================
REM  Aethelark MicShield - 1-Click Installer (Windows)
REM  Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
REM ==============================================================================
title Aethelark MicShield Setup Assistant

echo ======================================================================
echo   AETHELARK MICSHIELD // SETUP ASSISTANT (WINDOWS)
echo   Copyright (c) 2026 Cioponea Alexandru (Shenny)
echo ======================================================================

cd /d "%~dp0"

REM 1. Detect Python (try python, then py launcher)
set "PY_CMD="
where python >nul 2>&1 && set "PY_CMD=python"
if not defined PY_CMD (
    where py >nul 2>&1 && set "PY_CMD=py"
)

if not defined PY_CMD (
    echo [-] Python 3 not detected on this system.
    echo [+] Please install Python 3.9+ from https://python.org or the Microsoft Store.
    echo     (Make sure to check "Add Python to PATH" during installation)
    echo.
    pause
    exit /b 1
)

echo [+] Using Python interpreter: %PY_CMD%

REM 2. Virtual Environment Setup
if not exist ".venv" (
    echo [+] Creating virtual environment in .venv...
    %PY_CMD% -m venv .venv
    call .venv\Scripts\pip.exe install --quiet --upgrade pip
    call .venv\Scripts\pip.exe install --quiet -r requirements.txt
    call .venv\Scripts\pip.exe install --quiet -e .
)

REM 3. Launch Graphical Setup Assistant
echo [+] Launching Setup Assistant...
start "" ".venv\Scripts\pythonw.exe" setup_gui.py

exit /b 0
