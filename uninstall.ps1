# ==============================================================================
#  Aethelark MicShield - Automated Uninstaller (Windows PowerShell)
#  Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
# ==============================================================================

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  AETHELARK MICSHIELD // UNINSTALLER (WINDOWS)" -ForegroundColor Cyan
Write-Host "  Copyright (c) 2026 Cioponea Alexandru (Shenny)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Stop any running instances safely
Get-Process | Where-Object { $_.ProcessName -like "*python*" -and ($_.MainWindowTitle -like "*Aethelark*" -or $_.MainWindowTitle -like "*KeyShield*") } | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Check and remove installed program folder from config
$configDir = "$HOME\.config\aethelark-micshield"
if (Test-Path "$configDir\install_dir") {
    $targetDir = Get-Content "$configDir\install_dir"
    if ($targetDir -and (Test-Path $targetDir)) {
        Write-Host "[+] Removing installed program folder: $targetDir" -ForegroundColor Gray
        Remove-Item -Recurse -Force $targetDir -ErrorAction SilentlyContinue
    }
    Remove-Item -Recurse -Force $configDir -ErrorAction SilentlyContinue
}

# Fallback default Windows target
$defaultTarget = "$env:LOCALAPPDATA\Aethelark\MicShield"
if (Test-Path $defaultTarget) {
    Write-Host "[+] Removing default target directory: $defaultTarget" -ForegroundColor Gray
    Remove-Item -Recurse -Force $defaultTarget -ErrorAction SilentlyContinue
}

# 3. Remove desktop shortcut
$desktopPath = [System.Environment]::GetFolderPath('Desktop')
foreach ($name in @("KeyShield.lnk", "Aethelark-MicShield.lnk")) {
    $shortcutPath = "$desktopPath\$name"
    if (Test-Path $shortcutPath) {
        Write-Host "[+] Removing Desktop shortcut: $shortcutPath" -ForegroundColor Gray
        Remove-Item -Force $shortcutPath -ErrorAction SilentlyContinue
    }
}

# 4. Remove local virtual environment if present
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Test-Path "$scriptDir\.venv") {
    Write-Host "[+] Removing virtual environment in $scriptDir\.venv..." -ForegroundColor Gray
    Remove-Item -Recurse -Force "$scriptDir\.venv" -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "  [✓] Aethelark MicShield has been completely uninstalled from Windows." -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
