#!/usr/bin/env bash
# ==============================================================================
#  KeyShield - Automated Installer (Linux & macOS)
#  Intellectual Property (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
# ==============================================================================
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "======================================================================"
echo "  KEYSHIELD // ACOUSTIC KEYSTROKE DEFENSE"
echo "  Designed & Engineered by Cioponea Alexandru (Shenny)"
echo "======================================================================"

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
        echo "[!] Note: Neither pw-loopback nor pactl was found."
        echo "    KeyShield will run in direct monitor mode."
    fi
elif [ "$OS" = "Darwin" ]; then
    if system_profiler SPAudioDataType 2>/dev/null | grep -i "BlackHole" &>/dev/null; then
        echo "[+] macOS BlackHole virtual audio driver detected."
    else
        echo "[!] Recommended: Install BlackHole 2ch for seamless virtual microphone routing:"
        echo "    brew install blackhole-2ch"
    fi
fi

# 3. Create isolated virtual environment
if [ ! -d ".venv" ]; then
    echo "[+] Creating virtual environment in .venv..."
    python3 -m venv .venv
fi

echo "[+] Installing KeyShield dependencies..."
.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt
.venv/bin/pip install --quiet -e .

# 4. Create local user launcher script
LAUNCHER_DIR="$HOME/.local/bin"
mkdir -p "$LAUNCHER_DIR"

cat << EOF > "$LAUNCHER_DIR/keyshield"
#!/usr/bin/env bash
cd "$DIR"
exec "$DIR/.venv/bin/python" -m keyshield.main "\$@"
EOF
chmod +x "$LAUNCHER_DIR/keyshield"
echo "[+] Created executable command: $LAUNCHER_DIR/keyshield"

# 5. Linux Desktop Integration (.desktop file)
if [ "$OS" = "Linux" ]; then
    APP_DIR="$HOME/.local/share/applications"
    AUTOSTART_DIR="$HOME/.config/autostart"
    mkdir -p "$APP_DIR" "$AUTOSTART_DIR"

    DESKTOP_ENTRY="[Desktop Entry]
Name=KeyShield
GenericName=Acoustic Keystroke Defense
Comment=Blocks acoustic keyboard eavesdropping while preserving human speech
Exec=$LAUNCHER_DIR/keyshield
Terminal=false
Type=Application
Categories=Utility;Security;Audio;
StartupNotify=true
"
    echo "$DESKTOP_ENTRY" > "$APP_DIR/keyshield.desktop"
    echo "$DESKTOP_ENTRY" > "$AUTOSTART_DIR/keyshield.desktop"
    chmod +x "$APP_DIR/keyshield.desktop"
    echo "[+] Created Desktop Application & Autostart entries."
fi

echo ""
echo "======================================================================"
echo "  [✓] KeyShield successfully installed!"
echo "  "
echo "  To launch KeyShield:"
echo "    $LAUNCHER_DIR/keyshield"
echo "  "
echo "  Or start in background tray:"
echo "    $LAUNCHER_DIR/keyshield --minimized"
echo "======================================================================"
