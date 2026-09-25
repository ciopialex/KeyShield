#!/usr/bin/env bash
# ==============================================================================
#  Aethelark MicShield - 1-Click Installer (Linux & macOS)
#  Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
# ==============================================================================
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "======================================================================"
echo "  AETHELARK MICSHIELD // SETUP ASSISTANT"
echo "  Copyright (c) 2026 Cioponea Alexandru (Shenny)"
echo "======================================================================"

# 1. Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "[-] Error: Python 3 is required. Please install Python 3.9+."
    exit 1
fi

# 2. Setup Virtual Environment if not present
if [ ! -d ".venv" ]; then
    echo "[+] Initializing environment in .venv..."
    python3 -m venv .venv
    .venv/bin/pip install --quiet --upgrade pip
    .venv/bin/pip install --quiet -r requirements.txt
    .venv/bin/pip install --quiet -e .
fi

# 3. Register System Icon for Taskbar / Dock on Linux
if [ "$(uname -s)" = "Linux" ]; then
    ICON_DIR="$HOME/.local/share/icons/hicolor/scalable/apps"
    APP_DIR="$HOME/.local/share/applications"
    mkdir -p "$ICON_DIR" "$APP_DIR"
    
    if [ -f "$DIR/keyshield/assets/aethelark-micshield.svg" ]; then
        cp "$DIR/keyshield/assets/aethelark-micshield.svg" "$ICON_DIR/aethelark-micshield.svg"
        cp "$DIR/keyshield/assets/aethelark-micshield.svg" "$ICON_DIR/aethelark-micshield-setup.svg"
        command -v gtk-update-icon-cache &>/dev/null && gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
    fi

    # Create setup desktop launcher
    cat << EOF > "$APP_DIR/aethelark-micshield-setup.desktop"
[Desktop Entry]
Version=1.0
Type=Application
Name=Aethelark MicShield Setup
Comment=Acoustic Keystroke Defense Setup Assistant
Exec=$DIR/.venv/bin/python $DIR/setup_gui.py
Icon=aethelark-micshield-setup
StartupWMClass=aethelark-micshield-setup
Terminal=false
Categories=Utility;Security;Audio;
StartupNotify=true
EOF
fi

# 4. Launch Graphical Setup Assistant
echo "[+] Opening Aethelark MicShield Setup Assistant..."
if [ -n "$DISPLAY" ] || [ "$(uname -s)" = "Darwin" ]; then
    exec "$DIR/.venv/bin/python" "$DIR/setup_gui.py" "$@"
else
    # Headless fallback
    bash "$DIR/install.sh"
fi
