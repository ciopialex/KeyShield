#!/usr/bin/env bash
# ==============================================================================
#  Aethelark MicShield - Automated Installer (Linux & macOS)
#  Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
# ==============================================================================
set -e

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Target installation directory (default or user-specified)
if [ "$(uname -s)" = "Darwin" ]; then
    DEFAULT_INSTALL="$HOME/Applications/Aethelark MicShield"
else
    DEFAULT_INSTALL="$HOME/.local/share/aethelark-micshield"
fi
INSTALL_TARGET="${1:-$DEFAULT_INSTALL}"
AUTOSTART_FLAG="${2:-autostart}"

echo "======================================================================"
echo "  AETHELARK MICSHIELD // INSTALLER"
echo "  Designed & Engineered by Cioponea Alexandru (Shenny)"
echo "======================================================================"
echo "[+] Source folder: $SOURCE_DIR"
echo "[+] Install destination: $INSTALL_TARGET"

OS="$(uname -s)"
echo "[+] Detected Operating System: $OS"

# 1. Verify Python 3
if ! command -v python3 &>/dev/null; then
    echo "[-] Error: Python 3 is required. Please install Python 3.9+."
    exit 1
fi

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "[+] Using Python $PY_VER"

# 2. Check virtual audio subsystem
if [ "$OS" = "Linux" ]; then
    if command -v pw-loopback &>/dev/null; then
        echo "[+] PipeWire virtual audio subsystem detected (pw-loopback ready)."
    elif command -v pactl &>/dev/null; then
        echo "[+] PulseAudio subsystem detected (pactl ready)."
    else
        echo "[!] Note: pw-loopback or pactl recommended for virtual microphone."
    fi
elif [ "$OS" = "Darwin" ]; then
    if system_profiler SPAudioDataType 2>/dev/null | grep -i "BlackHole" &>/dev/null; then
        echo "[+] macOS BlackHole virtual audio driver detected."
    else
        echo "[!] Recommended for macOS: brew install blackhole-2ch"
    fi
fi

# 3. Create isolated installation directory & copy files
echo "[+] Installing payload into $INSTALL_TARGET..."
mkdir -p "$INSTALL_TARGET"
cp -r "$SOURCE_DIR/keyshield" "$INSTALL_TARGET/"
cp "$SOURCE_DIR/setup.py" "$INSTALL_TARGET/" 2>/dev/null || true
cp "$SOURCE_DIR/requirements.txt" "$INSTALL_TARGET/"
cp "$SOURCE_DIR/LICENSE.md" "$INSTALL_TARGET/" 2>/dev/null || true
cp "$SOURCE_DIR/README.md" "$INSTALL_TARGET/" 2>/dev/null || true

# 4. Create virtual environment inside the destination directory
if [ ! -d "$INSTALL_TARGET/.venv" ]; then
    echo "[+] Creating dedicated virtual environment in $INSTALL_TARGET/.venv..."
    python3 -m venv "$INSTALL_TARGET/.venv"
fi

echo "[+] Installing neural dependencies..."
"$INSTALL_TARGET/.venv/bin/pip" install --quiet --upgrade pip
"$INSTALL_TARGET/.venv/bin/pip" install --quiet -r "$INSTALL_TARGET/requirements.txt"
"$INSTALL_TARGET/.venv/bin/pip" install --quiet -e "$INSTALL_TARGET"

# 5. Record installation directory for clean uninstaller
CONFIG_DIR="$HOME/.config/aethelark-micshield"
mkdir -p "$CONFIG_DIR"
echo "$INSTALL_TARGET" > "$CONFIG_DIR/install_dir"

# 6. Create local user launcher script
LAUNCHER_DIR="$HOME/.local/bin"
mkdir -p "$LAUNCHER_DIR"

cat << EOF > "$LAUNCHER_DIR/keyshield"
#!/usr/bin/env bash
cd "$INSTALL_TARGET"
exec "$INSTALL_TARGET/.venv/bin/python" -m keyshield.main "\$@"
EOF
chmod +x "$LAUNCHER_DIR/keyshield"
echo "[+] Created executable command: $LAUNCHER_DIR/keyshield"

# 7. Desktop & Icon Integration
if [ "$OS" = "Linux" ]; then
    ICON_DIR="$HOME/.local/share/icons/hicolor/scalable/apps"
    APP_DIR="$HOME/.local/share/applications"
    AUTOSTART_DIR="$HOME/.config/autostart"
    mkdir -p "$ICON_DIR" "$APP_DIR" "$AUTOSTART_DIR"

    if [ -f "$INSTALL_TARGET/keyshield/assets/aethelark-micshield.svg" ]; then
        cp "$INSTALL_TARGET/keyshield/assets/aethelark-micshield.svg" "$ICON_DIR/aethelark-micshield.svg"
        command -v gtk-update-icon-cache &>/dev/null && gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
    fi

    DESKTOP_ENTRY="[Desktop Entry]
Name=Aethelark MicShield
GenericName=Acoustic Keystroke Defense
Comment=Blocks acoustic keyboard eavesdropping while preserving human speech
Exec=$LAUNCHER_DIR/keyshield
Icon=aethelark-micshield
StartupWMClass=aethelark-micshield
Terminal=false
Type=Application
Categories=Utility;Security;Audio;
StartupNotify=true
"
    echo "$DESKTOP_ENTRY" > "$APP_DIR/keyshield.desktop"
    chmod +x "$APP_DIR/keyshield.desktop"
    if [ "$AUTOSTART_FLAG" != "no-autostart" ]; then
        echo "$DESKTOP_ENTRY" > "$AUTOSTART_DIR/keyshield.desktop"
        echo "[+] Created Desktop Application & Autostart entries."
    else
        echo "[+] Created Desktop Application entry (Autostart disabled)."
    fi
fi

echo ""
echo "======================================================================"
echo "  [✓] Aethelark MicShield successfully installed!"
echo "  Installed at: $INSTALL_TARGET"
echo "  Launcher: $LAUNCHER_DIR/keyshield"
echo "======================================================================"
