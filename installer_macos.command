#!/usr/bin/env bash
# ==============================================================================
#  Aethelark MicShield - macOS Double-Clickable Launcher (.command)
#  Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
# ==============================================================================
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
exec bash "$DIR/installer_linux_mac.sh" "$@"
