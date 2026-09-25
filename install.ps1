# ==============================================================================
#  Aethelark MicShield - Automated Installer (Windows PowerShell)
#  Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
# ==============================================================================
param(
    [string]$InstallTarget = "$env:LOCALAPPDATA\Aethelark\MicShield",
    [string]$Autostart = "autostart"
)

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  AETHELARK MICSHIELD // WINDOWS INSTALLER" -ForegroundColor Cyan
Write-Host "  Designed & Engineered by Cioponea Alexandru (Shenny)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Verify Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command py -ErrorAction SilentlyContinue
}
if (-not $pythonCmd) {
    Write-Host "[-] Python 3 not found. Please install Python 3.9+ from python.org or Microsoft Store." -ForegroundColor Red
    Exit 1
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 2. Virtual Audio driver check
Write-Host "[+] Checking virtual audio devices..." -ForegroundColor Gray
$vbCable = Get-PnpDevice -FriendlyName "*CABLE*" -ErrorAction SilentlyContinue
if (-not $vbCable) {
    Write-Host "[!] Tip: Install free VB-CABLE to route filtered audio into Zoom/Discord/Teams:" -ForegroundColor Yellow
    Write-Host "    https://vb-audio.com/Cable/" -ForegroundColor Yellow
}

# 3. Create isolated installation directory & copy files
Write-Host "[+] Installing payload into $InstallTarget..." -ForegroundColor Gray
New-Item -ItemType Directory -Force -Path $InstallTarget | Out-Null
Copy-Item -Recurse -Force "$scriptDir\keyshield" "$InstallTarget\"
Copy-Item -Force "$scriptDir\requirements.txt" "$InstallTarget\"
if (Test-Path "$scriptDir\setup.py") { Copy-Item -Force "$scriptDir\setup.py" "$InstallTarget\" }
if (Test-Path "$scriptDir\LICENSE.md") { Copy-Item -Force "$scriptDir\LICENSE.md" "$InstallTarget\" }
if (Test-Path "$scriptDir\README.md") { Copy-Item -Force "$scriptDir\README.md" "$InstallTarget\" }

# 4. Virtual environment setup inside destination directory
$targetVenv = "$InstallTarget\.venv"
if (-not (Test-Path $targetVenv)) {
    Write-Host "[+] Creating virtual environment in $targetVenv..." -ForegroundColor Gray
    & $pythonCmd.Source -m venv $targetVenv
}

Write-Host "[+] Installing neural dependencies..." -ForegroundColor Gray
& "$targetVenv\Scripts\pip.exe" install --quiet --upgrade pip
& "$targetVenv\Scripts\pip.exe" install --quiet -r "$InstallTarget\requirements.txt"
& "$targetVenv\Scripts\pip.exe" install --quiet -e "$InstallTarget"

# 5. Save config directory
$configDir = "$HOME\.config\aethelark-micshield"
New-Item -ItemType Directory -Force -Path $configDir | Out-Null
Set-Content -Path "$configDir\install_dir" -Value $InstallTarget

# 6. Create Desktop Shortcut
$desktopPath = [System.Environment]::GetFolderPath('Desktop')
$wshShell = New-Object -ComObject WScript.Shell
$shortcut = $wshShell.CreateShortcut("$desktopPath\Aethelark-MicShield.lnk")
$shortcut.TargetPath = "$targetVenv\Scripts\pythonw.exe"
$shortcut.Arguments = "-m keyshield.main"
$shortcut.WorkingDirectory = "$InstallTarget"
$shortcut.Description = "Aethelark MicShield - Acoustic Keystroke Defense"
$shortcut.Save()

# 7. Optional Autostart Shortcut
if ($Autostart -ne "no-autostart") {
    $startupFolder = [System.Environment]::GetFolderPath('Startup')
    $autoShortcut = $wshShell.CreateShortcut("$startupFolder\Aethelark-MicShield.lnk")
    $autoShortcut.TargetPath = "$targetVenv\Scripts\pythonw.exe"
    $autoShortcut.Arguments = "-m keyshield.main --minimized"
    $autoShortcut.WorkingDirectory = "$InstallTarget"
    $autoShortcut.Description = "Aethelark MicShield Background Guard"
    $autoShortcut.Save()
    Write-Host "[+] Added to Windows Startup." -ForegroundColor Gray
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "  [✓] Aethelark MicShield successfully installed on Windows!" -ForegroundColor Green
Write-Host "  Destination: $InstallTarget" -ForegroundColor Green
Write-Host "  Desktop shortcut: Aethelark-MicShield.lnk" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
