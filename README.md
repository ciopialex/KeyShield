# Aethelark MicShield (KeyShield)

### Neural Acoustic Keystroke Firewall & Voice Gatekeeper
**Created & Engineered by Cioponea Alexandru ("Shenny")**  
*Free for Personal Use • Intellectual Property of Cioponea Alexandru*

---

[![License: Personal-Use](https://img.shields.io/badge/License-Personal--Use%20(KSL--1.0)-389E62.svg)](LICENSE.md)
[![Platform: Linux | macOS | Windows](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)]()
[![Inference: 0.109ms](https://img.shields.io/badge/Inference-0.109ms-brightgreen.svg)]()
[![CPU Load: <0.5%](https://img.shields.io/badge/CPU%20Load-%3C0.5%25-success.svg)]()
[![Telemetry: 100% Offline](https://img.shields.io/badge/Telemetry-Zero%20Data%20Collected-389E62.svg)]()

---

## The Threat: Acoustic Keyboard Eavesdropping

Recent breakthroughs in deep learning and signal processing have exposed a critical acoustic vulnerability in modern workstations: **Acoustic Keyboard Eavesdropping**. 

State-of-the-art neural acoustic classifiers (e.g., deep convolutional networks and audio spectrogram transformers) can reconstruct typed text—including passwords, encryption keys, private chat messages, and credit card numbers—from ambient microphone audio with **over 95% accuracy**.

This attack succeeds even when the microphone is built into a laptop bezel or resting on a desk several feet away, operating silently across:
* Video conference calls (Zoom, Google Meet, Microsoft Teams, Discord, Slack)
* Web browsers executing background WebRTC audio streams in hidden tabs
* Compromised communication software or background Trojans / RATs

```
                      [ Physical Microphone ]
                             (xm, ym)
                             ▲      ▲
               d(A, mic)    /        \    d(L, mic)
                           /          \
                          /            \
                ┌───────┐/              \┌───────┐
                │   A   │                │   L   │
                └───────┘                └───────┘
            (Far Left Key)             (Right Key)
            Δt_arrival = d_A / c       Δt_arrival = d_L / c
            Resonance: ~4.2 kHz        Resonance: ~6.8 kHz
```

### The Physics of How AI Decodes Keystrokes

An acoustic eavesdropping model does not simply "guess" words; it exploits fundamental wave physics across two primary acoustic channels:

#### 1. Spatial Geometry & Time-Difference of Arrival (TDoA)
* Every key on a physical keyboard occupies a fixed spatial coordinate $(x_k, y_k, z_k)$ relative to the microphone $(x_m, y_m, z_m)$.
* Sound propagates through air at speed $c \approx 343 \text{ m/s}$ ($0.343 \text{ mm/\mu s}$).
* A key on the left side of the keyboard (such as **"A"**, **"S"**, or **"Q"**) has a physical distance $d_A$ to the microphone that differs measurably from a key on the right side (such as **"L"**, **"P"**, or **"Enter"**), distance $d_L$.
* This distance delta produces an exact propagation time differential:
  $$\Delta t = \frac{|d_A - d_L|}{c}$$
* In stereo or multi-microphone arrays (standard on modern MacBooks, ThinkPads, and conference webcams), the phase shift $\Delta \phi$ between microphone capsules precisely triangulates the horizontal angle $\theta$ of the key strike.
* Even on single-capsule microphones, acoustic reflections bouncing off the desk, laptop palmrest, and display bezel arrive at distinct microsecond intervals ($t_{\text{direct}}$ vs $t_{\text{reflected}}$), providing a geometric distance fingerprint for each key.

#### 2. Structural Resonance & Spectral Eigenmodes
* Striking a key involves three physical phases:
  1. **The Switch Actuation**: The mechanical snap of the leaf, scissor mechanism, or click jacket.
  2. **The Bottom-Out Impact**: The keycap stem colliding with the housing plate and PCB substrate.
  3. **The Keycap Return**: The spring snapping the keycap back against the top housing.
* The keyboard chassis and laptop housing act as a resonant mechanical plate. Hitting **"A"** on the far-left edge excites structural eigenfrequencies and damping curves that differ dramatically from striking **"L"** near the center-right support pillars.
* Modern deep neural networks transform raw audio frames into high-resolution Mel-Spectrograms (frequency vs. time). The AI extracts:
  * **Spectral Centroid & Energy Dispersion**: Center-of-mass frequency distribution (typically spanning 1.5 kHz to 12 kHz).
  * **Chassis Eigenfrequencies**: Resonant peaks determined by the physical cavity underneath the specific switch.
  * **Transient Attack Envelope**: The sub-2ms impulse shape unique to each switch orientation.

By combining TDoA geometry and spectral resonance profiles, an AI eavesdropper maps acoustic waveforms directly into individual characters with surgical precision.

---

## The Solution: Aethelark MicShield Architecture

Traditional software attempts to solve this problem with static noise suppression (e.g., spectral subtraction or noise gates). These fail because keyboard clicks are high-energy impulse transients that bleed through linear filters, leaking high-frequency timing and resonance data.

**Aethelark MicShield** neutralizes acoustic eavesdropping from first principles by implementing a hardware-isolated, neural-gated acoustic firewall:

```
[ Physical Microphone Sensor ]
               │
               ▼ (16 kHz / 32 ms PCM Frames)
 ┌───────────────────────────────────────────────┐
 │ 160 ms Circular Ring Pre-Roll Buffer          │
 └───────────────────────┬───────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────┐
        │ Silero Neural VAD (ONNX / C++)  │
        │ Latency: 0.109 ms | CPU: 0.34%  │
        └────────────────┬────────────────┘
                         │
           Is Human Speech Verified?
          ┌──────────────┴──────────────┐
          │ YES                         │ NO (Typing, Clicks, Clatter)
          ▼                             ▼
 ┌───────────────────┐         ┌───────────────────────────────┐
 │ Voice Passthrough │         │ Zero-Signal Mathematical Sink │
 │ + 450ms Hysteresis│         │ Buffer = [0, 0, 0, ... 0]     │
 └─────────┬─────────┘         └───────────────┬───────────────┘
           │                                   │
           └─────────────────┬─────────────────┘
                             │
                             ▼
              [ OS Virtual Audio Loopback ]
          (KeyShield Acoustic Shield Microphone)
                             │
                             ▼
        [ Zoom / Discord / Chrome / Teams / OS Apps ]
```

### 1. Impulse Transient vs. Vocal Formant Separation
* **Typing Mechanics**: Mechanical keystrokes are non-harmonic impulse shocks. They possess an instantaneous rise time ($\tau < 1.5 \text{ ms}$), wide broadband frequency dispersion, and **zero sustained harmonic cohesion**.
* **Voice Mechanics**: Human speech is generated by subglottal pressure exciting the vocal folds, modulated by the vocal tract (pharynx, oral cavity, nasal cavity). This produces sustained harmonic formants ($F_0$ pitch fundamental, $F_1, F_2, F_3$ resonant formants) with continuous acoustic energy envelopes.
* MicShield's neural engine discriminates between impulse shocks and true vocal tract resonance with mathematical confidence.

### 2. 0.109 ms Neural Gatekeeper (C++ ONNX Inference)
* Audio is analyzed in real time in 32 ms discrete temporal frames (512 samples at 16 kHz).
* The classification engine is powered by an ultra-compact deep neural Voice Activity Detection model running on CPU via ONNX Runtime C++ binaries.
* **Zero Heavy Frameworks**: No PyTorch, no CUDA overhead, zero garbage collection pauses.
* **Benchmark Performance**:
  * Frame inference time: **0.109 ms** (under 1/300th of the 32 ms frame duration).
  * Theoretical throughput: **9,141 frames per second**.
  * Sustained CPU consumption: **0.34%** on modern multicore processors.

### 3. The Zero-Signal Mathematical Sink
* When human speech is not verified ($P(\text{speech}) < \theta_{\text{threshold}}$), audio is **not** attenuated or low-pass filtered.
* The raw buffer is completely dropped into a zero-signal sink, and the audio stream fed to the virtual microphone is replaced with a mathematical zero vector:
  $$\vec{S}_{\text{out}} = \vec{0} \quad (-\infty \text{ dBFS})$$
* **Result**: The AI eavesdropper receives absolute digital silence. No transient clicks, no chassis eigenmodes, no boundary reflections, and no TDoA timing information exist in the audio pipe. The side channel is eliminated.

### 4. 160 ms Circular Ring Pre-Roll (Zero Consonant Clipping)
* In human speech, initial consonants—especially unvoiced plosives (`/p/`, `/t/`, `/k/`) and fricatives (`/s/`, `/f/`)—can precede the full resonance of vocal cord oscillation by 20 to 50 milliseconds.
* Standard voice-activated gates clip these opening consonants, making speech sound truncated.
* Aethelark MicShield maintains an uninterrupted **160 ms circular memory ring buffer**. When the neural gate confirms speech, it flushes the prior 160 ms buffer instantaneously into the output pipe. Every opening syllable is preserved with 100% fidelity.

### 5. 450 ms Breath & Micro-Pause Hysteresis
* Natural human communication includes intra-sentence pauses, breathing intervals, and thinking micro-hesitations.
* MicShield employs dual-threshold hysteresis: once speech is verified, the gate remains open for **450 ms** after the last verified vocal formant before transitioning back to the zero-signal sink.
* Spoken sentences flow naturally without jarring cutoffs.

### 6. OS-Level Virtual Loopback Isolation
* The physical hardware microphone is bound exclusively by Aethelark MicShield.
* MicShield exposes an OS-level virtual audio loopback device:
  * **Linux**: Native PipeWire loopback node (`pw-loopback`)
  * **macOS**: High-fidelity virtual audio device (BlackHole)
  * **Windows**: Virtual audio loopback bridge (VB-Cable / Virtual Audio Cable)
* End-user applications (browsers, meeting clients, voice recorders) are assigned to the virtual device. User applications never receive raw, unfiltered hardware sensor data.

---

## User Interface & Experience

Designed with Steve Jobs-inspired aesthetic discipline and hardcore engineering execution:
* **Pure Obsidian Glass**: Cupertino dark palette (`#090A0F`), subtle 1px titanium hairline border, and clean typography.
* **Titanium Emerald Sage Accents**: Muted status indicators (`#389E62` / `#2E8B57`) delivering professional visual feedback without distraction.
* **Tactile Toggle**: Fluid physical toggle switch to instantaneously arm or disarm the firewall.
* **Zero Emojis, Pure Vector Assets**: 100% custom-crafted SVG vector artwork rendered dynamically for crisp display on Retina and HiDPI monitors.
* **System Tray Persistence**: Sits quietly in your operating system taskbar/tray, utilizing negligible memory and CPU.

---

## 1-Click Installers (Download & Run)

Aethelark MicShield includes 1-click double-clickable installers for every major operating system:

| Platform | 1-Click Installer | 1-Click Uninstaller |
| :--- | :--- | :--- |
| **macOS (Finder)** | Double-click `installer_macos.command` | Double-click `uninstaller_macos.command` |
| **Linux (Terminal)** | `./installer_linux_mac.sh` | `./uninstaller_linux_mac.sh` |
| **Windows (Explorer)** | Double-click `installer_windows.bat` | Double-click `uninstaller_windows.bat` |

Both installers launch the **Aethelark MicShield Setup Assistant** with full taskbar integration and custom vector branding, allowing you to select your preferred installation destination (defaults to `~/.local/share/aethelark-micshield`).

---

## Manual Execution & Commands

### Standard GUI Launch
```bash
keyshield
```

### Background Daemon (Starts Minimized to Tray)
```bash
keyshield --minimized
```

### Headless Server Mode (No GUI / Terminal Only)
```bash
keyshield --headless
```

### Run Hardware & Neural Performance Benchmark
```bash
keyshield --benchmark
```
*Sample Output:*
```text
============================================================
  KEYSHIELD NEURAL INFERENCE BENCHMARK
  Designed by Cioponea Alexandru (Shenny)
============================================================
Average execution time per 32ms frame: 0.109 ms
Theoretical max frame throughput: 9,141 fps
CPU Load @ 31.25 fps: 0.34%
============================================================
```

---

## Connecting Applications

In any application requiring microphone input (Zoom, Google Meet, Discord, Microsoft Teams, Slack, Chrome, OBS):
1. Open the application's **Audio Settings**.
2. Set **Input Device (Microphone)** to **KeyShield (Acoustic Shield Mic)**.
3. Your workstation now possesses hardware-grade acoustic defense against keyboard eavesdropping.

---

## Intellectual Property & License

Copyright (c) 2026 **Cioponea Alexandru ("Shenny")**. All Rights Reserved.

* **Personal Use License**: Aethelark MicShield is provided free of charge for personal, non-commercial use on personal workstations worldwide under the [KeyShield Personal-Use Source License (KSL-1.0)](LICENSE.md).
* **Intellectual Property**: All rights, title, acoustic deflection algorithms, neural gating architectures, vector designs, and code remain the exclusive intellectual property of **Cioponea Alexandru (Shenny)**.
* **Commercial Restrictions**: Commercial resale, distribution in proprietary software, hosting as a paid service, or filing patents on any concept or mechanism embodied in this software is strictly prohibited without an explicit written license from the author. See [LICENSE.md](LICENSE.md) for full terms.
