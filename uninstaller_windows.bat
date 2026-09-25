@echo off
REM ==============================================================================
REM  Aethelark MicShield - 1-Click Uninstaller (Windows)
REM  Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
REM ==============================================================================
title Aethelark MicShield Uninstaller

echo ======================================================================
echo   AETHELARK MICSHIELD // UNINSTALLER (WINDOWS)
echo   Copyright (c) 2026 Cioponea Alexandru (Shenny)
echo ======================================================================

cd /d "%~dp0"

REM Run PowerShell uninstaller if available
where powershell >nul 2>&1
if %errorlevel% equ 0 (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0uninstall.ps1"
    pause
    exit /b 0
)

REM Fallback batch cleanup if powershell is absent
taskkill /F /IM pythonw.exe /FI "WINDOWTITLE eq Aethelark*" >nul 2>&1
taskkill /F /IM pythonw.exe /FI "WINDOWTITLE eq KeyShield*" >nul 2>&1

set DESKTOP_DIR=%USERPROFILE%\Desktop
if exist "%DESKTOP_DIR%\KeyShield.lnk" del /F /Q "%DESKTOP_DIR%\KeyShield.lnk"
if exist "%DESKTOP_DIR%\Aethelark-MicShield.lnk" del /F /Q "%DESKTOP_DIR%\Aethelark-MicShield.lnk"

set TARGET_DIR=%LOCALAPPDATA%\Aethelark\MicShield
if exist "%TARGET_DIR%" rmdir /S /Q "%TARGET_DIR%"

echo.
echo ======================================================================
echo   [✓] Aethelark MicShield has been uninstalled from Windows.
echo ======================================================================
pause
exit /b 0
