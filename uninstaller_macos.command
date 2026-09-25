#!/usr/bin/env bash
# ==============================================================================
#  Aethelark MicShield - macOS Double-Clickable Uninstaller (.command)
#  Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
# ==============================================================================
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
exec bash "$DIR/uninstaller_linux_mac.sh" "$@"
