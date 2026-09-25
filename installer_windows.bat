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

REM 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [-] Python 3 not found. Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

REM 2. Virtual Environment Setup
if not exist ".venv" (
    echo [+] Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\pip.exe install --quiet --upgrade pip
    call .venv\Scripts\pip.exe install --quiet -r requirements.txt
    call .venv\Scripts\pip.exe install --quiet -e .
)

REM 3. Launch Graphical Setup Assistant
echo [+] Launching Setup Assistant...
start "" ".venv\Scripts\pythonw.exe" setup_gui.py

exit /b 0
