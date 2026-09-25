# ==============================================================================
#  KeyShield - Automated Uninstaller (Windows PowerShell)
#  Intellectual Property (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
# ==============================================================================

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  KEYSHIELD // UNINSTALLER (WINDOWS)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Stop any running instances
Stop-Process -Name "pythonw" -ErrorAction SilentlyContinue

# 2. Remove desktop shortcut
$desktopPath = [System.Environment]::GetFolderPath('Desktop')
$shortcutPath = "$desktopPath\KeyShield.lnk"
if (Test-Path $shortcutPath) {
    Write-Host "[+] Removing Desktop shortcut: $shortcutPath" -ForegroundColor Gray
    Remove-Item -Force $shortcutPath
}

# 3. Remove virtual environment
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Test-Path "$scriptDir\.venv") {
    Write-Host "[+] Removing virtual environment in $scriptDir\.venv..." -ForegroundColor Gray
    Remove-Item -Recurse -Force "$scriptDir\.venv"
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "  [✓] KeyShield has been completely uninstalled from Windows." -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
