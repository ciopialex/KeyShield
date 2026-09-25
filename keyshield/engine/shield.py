"""KeyShield Orchestration Engine: Real-time Audio Stream Guard.
======================================================================
Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
Licensed for personal, non-commercial use only.
"""
from __future__ import annotations

import collections
import queue
import threading
import time
from typing import Callable, Optional

import numpy as np
import sounddevice as sd

from .router import AudioRouter
from .vad import SileroNeuralGate


class AcousticShield:
    """Real-time acoustic keystroke defense pipeline."""

    SAMPLE_RATE = 16000
    CHUNK_SIZE = 512  # 32ms per frame @ 16kHz
    CHANNELS = 1

    def __init__(
        self,
        on_telemetry: Optional[Callable[[bool, float, float, str, int, bool], None]] = None,
    ):
        self.router = AudioRouter()
        self.vad = SileroNeuralGate(sample_rate=self.SAMPLE_RATE, frame_samples=self.CHUNK_SIZE)
        self.on_telemetry = on_telemetry

        self.is_armed = True
        self._running = False
        self._worker_thread: Optional[threading.Thread] = None

        self._in_stream: Optional[sd.InputStream] = None
        self._out_stream: Optional[sd.OutputStream] = None

        self._prev_voice_state = False
        self.total_keystrokes_blocked = 0

    def start(self):
        """Initializes virtual routing and starts audio capture thread."""
        if self._running:
            return

        self._running = True

        # Setup virtual audio sink
        ok, msg = self.router.setup_virtual_device()
        print(f"[KeyShield Router] {msg}")

        self._worker_thread = threading.Thread(target=self._run_loop, daemon=True)
        self._worker_thread.start()

    def stop(self):
        """Stops audio capture and cleans up virtual audio devices."""
        self._running = False
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=1.5)

        self._close_streams()
        self.router.teardown()

    def set_armed(self, armed: bool):
        """Toggles active acoustic defense on or off."""
        self.is_armed = armed
        if not armed:
            self.vad.reset()

    def _close_streams(self):
        if self._in_stream:
            try:
                self._in_stream.stop()
                self._in_stream.close()
            except Exception:
                pass
            self._in_stream = None

        if self._out_stream:
            try:
                self._out_stream.stop()
                self._out_stream.close()
            except Exception:
                pass
            self._out_stream = None

    def _run_loop(self):
        """Audio streaming loop with zero-allocation buffers."""
        in_idx, out_idx = self.router.find_target_devices()

        try:
            self._in_stream = sd.InputStream(
                samplerate=self.SAMPLE_RATE,
                channels=self.CHANNELS,
                dtype="int16",
                blocksize=self.CHUNK_SIZE,
                device=in_idx,
            )
            self._in_stream.start()
        except Exception as e:
            print(f"[KeyShield] Error opening input stream: {e}")
            self._running = False
            return

        if out_idx is not None:
            try:
                self._out_stream = sd.OutputStream(
                    samplerate=self.SAMPLE_RATE,
                    channels=self.CHANNELS,
                    dtype="int16",
                    blocksize=self.CHUNK_SIZE,
                    device=out_idx,
                )
                self._out_stream.start()
            except Exception as e:
                print(f"[KeyShield] Warning: Output stream failed to open on device {out_idx}: {e}")
                self._out_stream = None

        zeros_chunk = np.zeros(self.CHUNK_SIZE, dtype=np.int16)

        while self._running:
            try:
                data, overflowed = self._in_stream.read(self.CHUNK_SIZE)
                samples = data.flatten()

                if not self.is_armed:
                    # Pass-through unfiltered
                    if self._out_stream:
                        self._out_stream.write(samples)
                    if self.on_telemetry:
                        raw_rms = float(np.sqrt(np.mean(samples.astype(np.float32) ** 2)))
                        self.on_telemetry(True, 1.0, raw_rms, "DISARMED", self.total_keystrokes_blocked, False)
                    continue

                # Run neural voice activity and keystroke transient classifier
                is_voice, prob, rms, sys_state, key_blocked = self.vad.process_frame(samples)

                if key_blocked:
                    self.total_keystrokes_blocked += 1

                # Audio forwarding logic
                if self._out_stream:
                    if is_voice:
                        # On rising edge of speech, flush pre-roll to catch opening plosive
                        if not self._prev_voice_state:
                            pre_roll = self.vad.get_pre_roll()
                            self._out_stream.write(pre_roll)
                        self._out_stream.write(samples)
                    else:
                        # Feed pure silence to virtual mic: keyboard sounds are wiped out!
                        self._out_stream.write(zeros_chunk)

                self._prev_voice_state = is_voice

                if self.on_telemetry:
                    self.on_telemetry(is_voice, prob, rms, sys_state, self.total_keystrokes_blocked, key_blocked)

            except Exception as e:
                if self._running:
                    time.sleep(0.02)
