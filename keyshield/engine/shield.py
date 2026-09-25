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
    CHUNK_SIZE = 512      # 32ms per frame @ 16kHz
    CHANNELS = 1
    LOOKAHEAD_FRAMES = 4  # 128ms deterministic lookahead buffer

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
        self._in_channels = 1
        self._out_channels = 1

        self._prev_voice_state = False
        self.total_keystrokes_blocked = 0

        # Delay-line lookahead FIFO
        self._delay_fifo = collections.deque(maxlen=self.LOOKAHEAD_FRAMES)
        self._fade_samples = 32  # 2ms smooth anti-click crossfade
        self._fade_in_curve = np.linspace(0.0, 1.0, self._fade_samples, dtype=np.float32)
        self._fade_out_curve = np.linspace(1.0, 0.0, self._fade_samples, dtype=np.float32)

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
        self._reset_delay_fifo()

    def _reset_delay_fifo(self):
        self._delay_fifo.clear()
        zeros = np.zeros(self.CHUNK_SIZE, dtype=np.int16)
        for _ in range(self.LOOKAHEAD_FRAMES):
            self._delay_fifo.append(zeros.copy())

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

    def _write_to_out(self, frame: np.ndarray):
        """Writes frame with automatic mono-to-stereo channel upmixing if needed."""
        if self._out_stream is None:
            return
        try:
            if self._out_channels > 1:
                stereo_frame = np.column_stack([frame, frame])
                self._out_stream.write(stereo_frame)
            else:
                self._out_stream.write(frame)
        except Exception:
            pass

    def _run_loop(self):
        """Audio streaming loop with zero-allocation buffers and deterministic delay-line lookahead."""
        in_idx, out_idx = self.router.find_target_devices()

        # Open input stream: try mono, fall back to stereo if hardware requires it
        self._in_stream = None
        for ch in (1, 2):
            try:
                self._in_stream = sd.InputStream(
                    samplerate=self.SAMPLE_RATE,
                    channels=ch,
                    dtype="int16",
                    blocksize=self.CHUNK_SIZE,
                    device=in_idx,
                )
                self._in_stream.start()
                self._in_channels = ch
                break
            except Exception as e:
                if ch == 2:
                    print(f"[KeyShield] Error opening input stream on device {in_idx}: {e}")
                    self._running = False
                    return

        # Open output stream: detect max channels and configure accordingly
        if out_idx is not None:
            out_ch = 1
            try:
                out_info = sd.query_devices(out_idx)
                if out_info.get("max_output_channels", 1) >= 2:
                    out_ch = 2
            except Exception:
                pass

            for ch in (out_ch, 1 if out_ch == 2 else 2):
                try:
                    self._out_stream = sd.OutputStream(
                        samplerate=self.SAMPLE_RATE,
                        channels=ch,
                        dtype="int16",
                        blocksize=self.CHUNK_SIZE,
                        device=out_idx,
                    )
                    self._out_stream.start()
                    self._out_channels = ch
                    break
                except Exception as e:
                    self._out_stream = None

        zeros_chunk = np.zeros(self.CHUNK_SIZE, dtype=np.int16)
        self._reset_delay_fifo()
        self._prev_voice_state = False

        while self._running:
            try:
                data, overflowed = self._in_stream.read(self.CHUNK_SIZE)
                if self._in_channels > 1 and data.ndim == 2 and data.shape[1] > 1:
                    samples = data[:, 0].copy()
                else:
                    samples = data.flatten()

                # Defensively guarantee exact frame size
                if len(samples) != self.CHUNK_SIZE:
                    if len(samples) < self.CHUNK_SIZE:
                        samples = np.pad(samples, (0, self.CHUNK_SIZE - len(samples)))
                    else:
                        samples = samples[:self.CHUNK_SIZE]

                if not self.is_armed:
                    # Pass-through unfiltered without acoustic gating
                    self._write_to_out(samples)
                    if self.on_telemetry:
                        raw_rms = float(np.sqrt(np.mean(samples.astype(np.float32) ** 2)))
                        self.on_telemetry(True, 1.0, raw_rms, "DISARMED", self.total_keystrokes_blocked, False)
                    continue

                # Push incoming frame into delay FIFO and pop delayed candidate frame
                self._delay_fifo.append(samples)
                delayed_frame = self._delay_fifo.popleft()

                # Run neural voice activity and keystroke transient classifier on current frame
                is_voice, prob, rms, sys_state, key_blocked = self.vad.process_frame(samples)

                if key_blocked:
                    self.total_keystrokes_blocked += 1

                # Deterministic frame forwarding with micro-crossfade on transitions
                if is_voice:
                    out_frame = delayed_frame.copy()
                    if not self._prev_voice_state:
                        # Smooth 2ms fade-in eliminates DC click on gate opening
                        out_frame[:self._fade_samples] = (
                            out_frame[:self._fade_samples].astype(np.float32) * self._fade_in_curve
                        ).astype(np.int16)
                else:
                    if self._prev_voice_state:
                        # Smooth 2ms fade-out eliminates abrupt cut on gate closing
                        out_frame = delayed_frame.copy()
                        out_frame[:self._fade_samples] = (
                            out_frame[:self._fade_samples].astype(np.float32) * self._fade_out_curve
                        ).astype(np.int16)
                        out_frame[self._fade_samples:] = 0
                    else:
                        out_frame = zeros_chunk

                self._prev_voice_state = is_voice
                self._write_to_out(out_frame)

                if self.on_telemetry:
                    self.on_telemetry(is_voice, prob, rms, sys_state, self.total_keystrokes_blocked, key_blocked)

            except Exception as e:
                if self._running:
                    time.sleep(0.02)
