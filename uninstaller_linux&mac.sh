#!/usr/bin/env bash
# ==============================================================================
#  Aethelark MicShield - 1-Click Uninstaller (Linux & macOS)
#  Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
# ==============================================================================
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "======================================================================"
echo "  AETHELARK MICSHIELD // UNINSTALLER"
echo "======================================================================"

# 1. Stop running processes
echo "[+] Stopping any running Aethelark MicShield instances..."
pkill -9 -f "keyshield.main" 2>/dev/null || true
pkill -9 -f "setup_gui.py" 2>/dev/null || true
pkill -9 -f "pw-loopback.*KeyShield" 2>/dev/null || true

# 2. Remove binary launcher
LAUNCHER="$HOME/.local/bin/keyshield"
if [ -f "$LAUNCHER" ]; then
    echo "[+] Removing launcher: $LAUNCHER"
    rm -f "$LAUNCHER"
fi

# 3. Remove Desktop & Autostart entries
rm -f "$HOME/.local/share/applications/keyshield.desktop" 2>/dev/null || true
rm -f "$HOME/.local/share/applications/aethelark-micshield-setup.desktop" 2>/dev/null || true
rm -f "$HOME/.config/autostart/keyshield.desktop" 2>/dev/null || true
rm -f "$HOME/Desktop/Aethelark-MicShield*" 2>/dev/null || true
rm -f "$HOME/Desktop/KeyShield*" 2>/dev/null || true

# 4. Remove system icons
rm -f "$HOME/.local/share/icons/hicolor/scalable/apps/aethelark-micshield*.svg" 2>/dev/null || true

# 5. Clean build caches
rm -rf "$DIR/build" "$DIR/dist" "$DIR/*.egg-info" "$DIR/keyshield.egg-info" 2>/dev/null || true

echo ""
echo "======================================================================"
echo "  [✓] Aethelark MicShield has been completely uninstalled from your system."
echo "======================================================================"
