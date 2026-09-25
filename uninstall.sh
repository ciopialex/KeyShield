#!/usr/bin/env bash
# ==============================================================================
#  Aethelark MicShield - Automated Uninstaller (Linux & macOS)
#  Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
# ==============================================================================
set -e

echo "======================================================================"
echo "  AETHELARK MICSHIELD // UNINSTALLER"
echo "======================================================================"

# 1. Stop any running instances
echo "[+] Stopping any running KeyShield processes..."
pkill -9 -f "keyshield.main" 2>/dev/null || true
pkill -9 -f "pw-loopback.*KeyShield" 2>/dev/null || true

# 2. Check and delete the installed program directory
CONFIG_DIR="$HOME/.config/aethelark-micshield"
if [ -f "$CONFIG_DIR/install_dir" ]; then
    INSTALLED_TARGET="$(cat "$CONFIG_DIR/install_dir")"
    if [ -n "$INSTALLED_TARGET" ] && [ -d "$INSTALLED_TARGET" ]; then
        echo "[+] Removing installed program folder: $INSTALLED_TARGET"
        rm -rf "$INSTALLED_TARGET"
    fi
    rm -rf "$CONFIG_DIR"
fi

# Fallback default locations if config wasn't saved
if [ -d "$HOME/.local/share/aethelark-micshield" ]; then
    echo "[+] Removing default directory: $HOME/.local/share/aethelark-micshield"
    rm -rf "$HOME/.local/share/aethelark-micshield"
fi
if [ -d "$HOME/Applications/Aethelark MicShield" ]; then
    echo "[+] Removing macOS directory: $HOME/Applications/Aethelark MicShield"
    rm -rf "$HOME/Applications/Aethelark MicShield"
fi

# 3. Remove binary launcher
LAUNCHER="$HOME/.local/bin/keyshield"
if [ -f "$LAUNCHER" ]; then
    echo "[+] Removing launcher: $LAUNCHER"
    rm -f "$LAUNCHER"
fi

# 4. Remove Desktop & Autostart entries
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

echo ""
echo "======================================================================"
echo "  [✓] Aethelark MicShield has been completely uninstalled from your system."
echo "======================================================================"
