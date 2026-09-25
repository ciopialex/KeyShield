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

REM 1. Terminate running background instances
taskkill /F /IM pythonw.exe /FI "WINDOWTITLE eq Aethelark*" >nul 2>&1

REM 2. Remove Desktop shortcut
set DESKTOP_DIR=%USERPROFILE%\Desktop
if exist "%DESKTOP_DIR%\KeyShield.lnk" del /F /Q "%DESKTOP_DIR%\KeyShield.lnk"
if exist "%DESKTOP_DIR%\Aethelark-MicShield.lnk" del /F /Q "%DESKTOP_DIR%\Aethelark-MicShield.lnk"

echo.
echo ======================================================================
echo   [✓] Aethelark MicShield has been uninstalled from Windows.
echo ======================================================================
pause
exit /b 0
