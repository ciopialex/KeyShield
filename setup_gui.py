#!/usr/bin/env python3
"""Aethelark MicShield Setup Assistant (Graphical Installer).
======================================================================
Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
Licensed for personal, non-commercial use only.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("aethelark.micshield.setup.1.0")
    except Exception:
        pass

from PyQt6.QtWidgets import QApplication
from keyshield.ui.installer import SetupAssistantWindow
from keyshield.ui.assets import get_aethelark_icon


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("aethelark-micshield-setup")
    app.setApplicationDisplayName("Aethelark MicShield Setup")
    app.setDesktopFileName("aethelark-micshield-setup")

    icon = get_aethelark_icon()
    app.setWindowIcon(icon)

    window = SetupAssistantWindow()
    window.setWindowIcon(icon)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
