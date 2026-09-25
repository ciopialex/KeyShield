#!/usr/bin/env python3
"""KeyShield Standalone Executable Builder.
======================================================================
Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
Licensed for personal, non-commercial use only.

Bundles KeyShield into a single zero-dependency native executable
for Linux, macOS, or Windows using PyInstaller.
"""
from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_ROOT / "keyshield" / "models" / "silero_vad.onnx"
MAIN_PATH = PROJECT_ROOT / "keyshield" / "main.py"


def build():
    print("=" * 65)
    print("  KEYSHIELD STANDALONE PACKAGER")
    print("  Copyright (c) 2026 Cioponea Alexandru (Shenny)")
    print("=" * 65)

    if not MODEL_PATH.exists():
        print(f"[-] Error: ONNX model missing at {MODEL_PATH}")
        sys.exit(1)

    os_name = platform.system().lower()
    sep = ";" if os_name == "windows" else ":"
    model_data = f"{MODEL_PATH}{sep}keyshield/models"
    assets_path = PROJECT_ROOT / "keyshield" / "assets"
    assets_data = f"{assets_path}{sep}keyshield/assets"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=KeyShield",
        "--onefile",
        "--noconsole",
        f"--add-data={model_data}",
        f"--add-data={assets_data}",
        "--clean",
        str(MAIN_PATH),
    ]

    print(f"[+] Building single standalone binary for {platform.system()}...")
    print(f"    Command: {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=str(PROJECT_ROOT))

    print("\n" + "=" * 65)
    print("  [✓] Build complete!")
    dist_dir = PROJECT_ROOT / "dist"
    print(f"  Single-file executable generated at: {dist_dir}")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    build()
