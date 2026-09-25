"""KeyShield Virtual Audio Router.
======================================================================
Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
Licensed for personal, non-commercial use only.

Cross-Platform Audio Routing Architecture:
- Linux: Native PipeWire `pw-loopback` or PulseAudio `module-null-sink`.
  Instantly creates "KeyShield (Acoustic Shield Mic)" without kernel drivers.
- macOS: CoreAudio loopback via BlackHole 2ch.
- Windows: WASAPI / DirectSound loopback via VB-Audio Virtual Cable.
"""
from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
import threading
import time
from typing import Optional, Tuple

import sounddevice as sd


class AudioRouter:
    """Manages the creation, lifecycle, and device selection of the virtual microphone."""

    def __init__(self):
        self.os_type = platform.system().lower()
        self._loopback_process: Optional[subprocess.Popen] = None
        self._pulse_module_ids: list[str] = []

    def setup_virtual_device(self) -> Tuple[bool, str]:
        """Creates or detects the virtual microphone device for the active OS."""
        if self.os_type == "linux":
            return self._setup_linux_device()
        elif self.os_type == "darwin":
            return self._setup_macos_device()
        elif self.os_type == "windows":
            return self._setup_windows_device()
        else:
            return False, f"Unsupported operating system: {self.os_type}"

    def _setup_linux_device(self) -> Tuple[bool, str]:
        """Sets up virtual sink and source on Linux via PipeWire or PulseAudio."""
        # 1. Try PipeWire pw-loopback (native, zero-package on modern distros)
        if shutil.which("pw-loopback"):
            try:
                cmd = [
                    "pw-loopback",
                    "--name=KeyShield_Daemon",
                    "--capture-props=media.class=Audio/Sink node.name=KeyShield_Sink node.description=\"KeyShield Virtual Sink\"",
                    "--playback-props=media.class=Audio/Source node.name=KeyShield_Mic node.description=\"KeyShield (Acoustic Shield Mic)\""
                ]
                self._loopback_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    preexec_fn=os.setpgrp if hasattr(os, "setpgrp") else None
                )
                time.sleep(0.3)
                if self._loopback_process.poll() is None:
                    return True, "PipeWire 'KeyShield (Acoustic Shield Mic)' created successfully."
            except Exception as e:
                pass

        # 2. Try pactl (PulseAudio or pipewire-pulse)
        if shutil.which("pactl"):
            try:
                out1 = subprocess.check_output([
                    "pactl", "load-module", "module-null-sink",
                    "sink_name=KeyShield_Sink",
                    "sink_properties=device.description=\"KeyShield_Virtual_Sink\""
                ], text=True).strip()
                if out1:
                    self._pulse_module_ids.append(out1)

                out2 = subprocess.check_output([
                    "pactl", "load-module", "module-remap-source",
                    "master=KeyShield_Sink.monitor",
                    "source_name=KeyShield_Mic",
                    "source_properties=device.description=\"KeyShield_(Acoustic_Shield_Mic)\""
                ], text=True).strip()
                if out2:
                    self._pulse_module_ids.append(out2)

                return True, "PulseAudio 'KeyShield (Acoustic Shield Mic)' mounted."
            except Exception as e:
                pass

        return False, "Could not automatically mount virtual audio device on Linux. pw-loopback or pactl required."

    def _setup_macos_device(self) -> Tuple[bool, str]:
        """Checks for BlackHole 2ch on macOS."""
        devices = sd.query_devices()
        has_blackhole = any("blackhole" in d["name"].lower() for d in devices)
        if has_blackhole:
            return True, "macOS BlackHole Virtual Audio Driver detected."
        return False, "BlackHole 2ch not detected. Install with: brew install blackhole-2ch"

    def _setup_windows_device(self) -> Tuple[bool, str]:
        """Checks for VB-CABLE on Windows."""
        devices = sd.query_devices()
        has_vbcable = any("cable" in d["name"].lower() for d in devices)
        if has_vbcable:
            return True, "Windows VB-CABLE Virtual Audio Device detected."
        return False, "VB-CABLE not detected. Download free from https://vb-audio.com/Cable/"

    def find_target_devices(self) -> Tuple[Optional[int], Optional[int]]:
        """Finds the best (physical_input_index, virtual_output_index).

        Returns:
            (input_idx, output_idx)
        """
        devices = sd.query_devices()
        input_idx = None
        output_idx = None

        # 1. Locate physical input microphone
        # Avoid our own virtual sinks as inputs
        default_in = sd.default.device[0]
        if default_in is not None and default_in >= 0:
            dev_name = devices[default_in]["name"].lower()
            if "keyshield" not in dev_name and "null" not in dev_name:
                input_idx = default_in

        if input_idx is None:
            for idx, dev in enumerate(devices):
                if dev["max_input_channels"] > 0:
                    name = dev["name"].lower()
                    if "keyshield" not in name and "blackhole" not in name and "cable" not in name:
                        input_idx = idx
                        break

        # 2. Locate virtual output sink
        for idx, dev in enumerate(devices):
            if dev["max_output_channels"] > 0:
                name = dev["name"].lower()
                if "keyshield_sink" in name or "keyshield virtual sink" in name or "keyshield" in name:
                    output_idx = idx
                    break
                elif self.os_type == "darwin" and "blackhole" in name:
                    output_idx = idx
                    break
                elif self.os_type == "windows" and "cable input" in name:
                    output_idx = idx
                    break

        return input_idx, output_idx

    def teardown(self):
        """Cleanly terminates virtual audio loopbacks and unmounts modules."""
        if self._loopback_process:
            try:
                self._loopback_process.terminate()
                self._loopback_process.wait(timeout=1.0)
            except Exception:
                try:
                    self._loopback_process.kill()
                except Exception:
                    pass
            self._loopback_process = None

        if self._pulse_module_ids and shutil.which("pactl"):
            for mod_id in self._pulse_module_ids:
                try:
                    subprocess.run(["pactl", "unload-module", str(mod_id)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except Exception:
                    pass
            self._pulse_module_ids.clear()
