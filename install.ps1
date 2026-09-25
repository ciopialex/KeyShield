# ==============================================================================
#  KeyShield - Automated Installer (Windows PowerShell)
#  Intellectual Property (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
# ==============================================================================

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  KEYSHIELD // ACOUSTIC KEYSTROKE DEFENSE" -ForegroundColor Cyan
Write-Host "  Designed & Engineered by Cioponea Alexandru (Shenny)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Verify Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[-] Python 3 not found. Please install Python 3.9+ from python.org or Microsoft Store." -ForegroundColor Red
    Exit 1
}

# 2. Virtual Audio driver check
Write-Host "[+] Checking virtual audio devices..." -ForegroundColor Gray
$vbCable = Get-PnpDevice -FriendlyName "*CABLE*" -ErrorAction SilentlyContinue
if (-not $vbCable) {
    Write-Host "[!] Tip: Install free VB-CABLE to route filtered audio into Zoom/Discord/Teams:" -ForegroundColor Yellow
    Write-Host "    https://vb-audio.com/Cable/" -ForegroundColor Yellow
}

# 3. Virtual environment setup
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

if (-not (Test-Path ".venv")) {
    Write-Host "[+] Creating virtual environment in .venv..." -ForegroundColor Gray
    python -m venv .venv
}

Write-Host "[+] Installing KeyShield dependencies..." -ForegroundColor Gray
& .\.venv\Scripts\pip.exe install --quiet --upgrade pip
& .\.venv\Scripts\pip.exe install --quiet -r requirements.txt
& .\.venv\Scripts\pip.exe install --quiet -e .

# 4. Create Desktop Shortcut
$desktopPath = [System.Environment]::GetFolderPath('Desktop')
$wshShell = New-Object -ComObject WScript.Shell
$shortcut = $wshShell.CreateShortcut("$desktopPath\KeyShield.lnk")
$shortcut.TargetPath = "$scriptDir\.venv\Scripts\pythonw.exe"
$shortcut.Arguments = "-m keyshield.main"
$shortcut.WorkingDirectory = "$scriptDir"
$shortcut.Description = "KeyShield - Acoustic Keystroke Defense"
$shortcut.Save()

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "  [✓] KeyShield successfully installed on Windows!" -ForegroundColor Green
Write-Host "  Desktop shortcut created: KeyShield.lnk" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
