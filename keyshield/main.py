"""KeyShield: Acoustic Keystroke Defense & Neural Voice Gatekeeper.
======================================================================
Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
Licensed for personal, non-commercial use only.
"""
from __future__ import annotations

import argparse
import signal
import sys
import time
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from keyshield.engine import AcousticShield
from keyshield.ui.tray import create_shield_icon

__version__ = "1.0.0"
__author__ = "Cioponea Alexandru (Shenny)"


def run_benchmark():
    """Runs a 1000-iteration inference benchmark to verify 0.25ms CPU latency."""
    import numpy as np
    from keyshield.engine.vad import SileroNeuralGate

    print("\n" + "=" * 60)
    print("  KEYSHIELD NEURAL INFERENCE BENCHMARK")
    print(f"  Designed by {__author__}")
    print("=" * 60)

    print("Initializing ONNX Runtime session...")
    gate = SileroNeuralGate()
    dummy_frame = np.zeros(512, dtype=np.int16)

    # Warmup
    for _ in range(50):
        gate.process_frame(dummy_frame)

    iterations = 1000
    start = time.perf_counter()
    for _ in range(iterations):
        gate.process_frame(dummy_frame)
    elapsed = time.perf_counter() - start

    avg_ms = (elapsed / iterations) * 1000.0
    print(f"Total time for {iterations} frames: {elapsed:.4f}s")
    print(f"Average execution time per 32ms frame: {avg_ms:.3f} ms")
    print(f"Theoretical max frame throughput: {int(1000.0 / avg_ms):,} fps")
    print(f"CPU Load @ 31.25 fps: {(avg_ms / 32.0) * 100.0:.2f}%")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description=f"KeyShield v{__version__} - Acoustic Keystroke Defense by {__author__}"
    )
    parser.add_argument("--benchmark", action="store_true", help="Run neural VAD performance benchmark")
    parser.add_argument("--headless", action="store_true", help="Run background daemon without UI")
    parser.add_argument("--minimized", action="store_true", help="Start directly in system tray")
    parser.add_argument("--version", action="version", version=f"KeyShield {__version__} by {__author__}")

    args = parser.parse_args()

    if args.benchmark:
        run_benchmark()
        return

    # Initialize acoustic engine
    shield_engine = AcousticShield()

    if args.headless:
        print("\n" + "=" * 65)
        print(f"  KeyShield v{__version__} // Headless Acoustic Shield Daemon")
        print(f"  Intellectual Property (c) 2026 {__author__}")
        print("=" * 65)
        print("  [+] Starting acoustic firewall...")
        shield_engine.start()
        print("  [✓] Defense active. Acoustic keystrokes deflected.")
        print("  [!] Press Ctrl+C to terminate.\n")

        def _sig_handler(sig, frame):
            print("\nShutting down KeyShield...")
            shield_engine.stop()
            sys.exit(0)

        signal.signal(signal.SIGINT, _sig_handler)
        signal.signal(signal.SIGTERM, _sig_handler)

        while True:
            time.sleep(1)

    # GUI Mode (PyQt6)
    from PyQt6.QtWidgets import QApplication
    from keyshield.ui.app import KeyShieldWindow
    from keyshield.ui.tray import KeyShieldTray

    app = QApplication(sys.argv)
    app.setApplicationName("KeyShield")
    app.setWindowIcon(create_shield_icon(True))
    app.setQuitOnLastWindowClosed(False)

    shield_engine.start()

    window = KeyShieldWindow(shield_engine)
    tray = KeyShieldTray(window, shield_engine)
    tray.show()

    if not args.minimized:
        window.show()

    # Clean exit hook
    app.aboutToQuit.connect(shield_engine.stop)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
