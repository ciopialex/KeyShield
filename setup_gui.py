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

from PyQt6.QtWidgets import QApplication
from keyshield.ui.installer import SetupAssistantWindow
from keyshield.ui.assets import get_aethelark_icon


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Aethelark MicShield Setup")
    app.setApplicationDisplayName("Aethelark MicShield Setup")
    app.setDesktopFileName("aethelark-micshield-setup")
    app.setWindowIcon(get_aethelark_icon())

    window = SetupAssistantWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
