#!/usr/bin/env bash
# ==============================================================================
#  KeyShield - Automated Uninstaller (Linux & macOS)
#  Intellectual Property (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
# ==============================================================================
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================================================"
echo "  KEYSHIELD // UNINSTALLER"
echo "======================================================================"

# 1. Stop any running instances
echo "[+] Stopping any running KeyShield processes..."
pkill -f "keyshield.main" 2>/dev/null || true
pkill -f "pw-loopback.*KeyShield" 2>/dev/null || true

# 2. Remove binary launcher
LAUNCHER="$HOME/.local/bin/keyshield"
if [ -f "$LAUNCHER" ]; then
    echo "[+] Removing launcher: $LAUNCHER"
    rm -f "$LAUNCHER"
fi

# 3. Remove Desktop & Autostart entries
DESKTOP_ENTRY="$HOME/.local/share/applications/keyshield.desktop"
AUTOSTART_ENTRY="$HOME/.config/autostart/keyshield.desktop"

if [ -f "$DESKTOP_ENTRY" ]; then
    echo "[+] Removing desktop launcher: $DESKTOP_ENTRY"
    rm -f "$DESKTOP_ENTRY"
fi

if [ -f "$AUTOSTART_ENTRY" ]; then
    echo "[+] Removing autostart entry: $AUTOSTART_ENTRY"
    rm -f "$AUTOSTART_ENTRY"
fi

# 4. Remove virtual environment
if [ -d "$DIR/.venv" ]; then
    echo "[+] Removing virtual environment in $DIR/.venv..."
    rm -rf "$DIR/.venv"
fi

# 5. Remove build/egg artifacts
rm -rf "$DIR/build" "$DIR/dist" "$DIR/*.egg-info" "$DIR/keyshield.egg-info" 2>/dev/null || true

echo ""
echo "======================================================================"
echo "  [✓] KeyShield has been completely uninstalled from your system."
echo "======================================================================"
