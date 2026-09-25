# KeyShield 🛡️

### Neural Acoustic Keystroke Firewall & Voice Gatekeeper
**Created & Engineered by Cioponea Alexandru ("Shenny")**  
*Free for Personal Use • Intellectual Property of Cioponea Alexandru*

---

[![License: Personal-Use](https://img.shields.io/badge/License-Personal--Use%20(KSL--1.0)-emerald.svg)](LICENSE.md)
[![Platform: Linux | macOS | Windows](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)]()
[![Inference: 0.109ms](https://img.shields.io/badge/Inference-0.109ms-brightgreen.svg)]()
[![CPU Load: <0.5%](https://img.shields.io/badge/CPU%20Load-%3C0.5%25-success.svg)]()

---

## 💡 The Threat: Acoustic Keyboard Eavesdropping

Recent cybersecurity research has proven that modern deep learning models can reconstruct passwords, PINs, private keys, and confidential messages from ambient microphone audio with **over 95% accuracy**. 

Whether from background apps, browser tabs running malicious WebRTC scripts, compromised meeting software, or malware:
* Every mechanical switch, laptop scissor switch, and membrane keyboard produces unique acoustic time-difference and resonance signatures.
* Simply muting yourself manually is friction-heavy, prone to human error, and impossible during live calls.

## 🚀 The Solution: First-Principles Acoustic Isolation

**KeyShield** solves this at the physical acoustic layer:
1. **Physical Sound vs. Vocal Formants:** Human speech produces distinct vocal tract harmonic formants ($F_0, F_1, F_2$) driven by vocal cord oscillation. Keyboard clicks are abrupt impulse transients with steep rise times (< 2 ms) and zero harmonic formant cohesion.
2. **Neural Gatekeeper:** KeyShield passes each 32ms audio frame into an ultra-compact neural network running in C++ on CPU via ONNX Runtime (**0.109 ms latency**, **0.34% CPU usage**, zero PyTorch).
3. **Zero Consonant Clipping:** Employs a circular ring buffer maintaining a continuous **160 ms pre-roll**. When you speak, the opening plosive or vowel (`p`, `t`, `s`, `k`) is flushed instantaneously into the virtual microphone without clipping.
4. **450 ms Breath Hysteresis:** Natural breathing pauses and micro-hesitations within sentences are maintained smoothly without jarring cuts.
5. **100% Keystroke Deflection:** When your voice is silent, typing sounds, desk knocks, and chair creaks are mathematically wiped from the stream. The microphone capability is never altered or degraded.

```
[ Physical Mic ]
       │
       ▼ (32ms frames @ 16kHz)
[ KeyShield Neural VAD ] ────── (Typing / Clicks detected) ────► [ Zero-Signal Sink ] (BLOCKED)
       │
       ▼ (Human Speech Verified)
[ 160ms Pre-Roll + Voice Stream ]
       │
       ▼
[ KeyShield Virtual Microphone ] ───► Zoom / Discord / Chrome / OS Apps
```

---

## 🎨 The Experience: Steve Jobs-esque Simplicity

* **Install Once, Forget Forever:** Sits quietly in your system tray. Automatically starts at boot.
* **Pure Obsidian Glass:** Minimalist Cupertino dark aesthetic (`#090A0F`), subtle 1px hairline border, and typography inspired by Apple design language.
* **Tactile Toggle:** Fluid iOS-style physical toggle switch to arm or disarm the firewall.
* **Ambient Breathing Orb:** Visual status indicator displaying real-time speech verification, transient rejection sparks, and blocked keystroke telemetry.

---

## 📦 1-Click Installers (Download & Run)

Users can simply clone or download the repository and double-click their platform installer:

### 🍏 Linux & macOS
* **macOS Finder (Double-Click):** Double-click `installer_macos.command` (to install) or `uninstaller_macos.command` (to uninstall).
* **Linux / Terminal:**
  * **Install:** Run `./installer_linux_mac.sh` (or `./installer_linux\&mac.sh`)
  * **Uninstall:** Run `./uninstaller_linux_mac.sh` (or `./uninstaller_linux\&mac.sh`)

### 🪟 Windows
* **Install:** Double-click `installer_windows.bat` in File Explorer.
* **Uninstall:** Double-click `uninstaller_windows.bat` in File Explorer.


Both installers launch the **Aethelark MicShield Setup Assistant** GUI with full taskbar integration and custom vector icons.


---

## 🛠️ Usage

### Standard Launch (GUI)
```bash
keyshield
```

### Background Daemon (System Tray)
```bash
keyshield --minimized
```

### Headless Server Mode (No GUI)
```bash
keyshield --headless
```

### Run Performance Benchmark
```bash
keyshield --benchmark
```
*Output:*
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

## 🔌 Connecting Applications

In any application requiring voice input (Zoom, Google Meet, Discord, Microsoft Teams, Slack, Chrome):
1. Open the application's **Audio Settings**.
2. Select **KeyShield (Acoustic Shield Mic)** as your Input Microphone.
3. Your microphone now has hardware-grade acoustic defense enabled.

---

## ⚖️ Intellectual Property & License

Copyright (c) 2026 **Cioponea Alexandru ("Shenny")**. All Rights Reserved.

* **Personal Use:** Free of charge for personal, non-commercial use on personal computers.
* **Intellectual Property:** All rights, titles, inventions, acoustic deflection algorithms, and designs remain the exclusive intellectual property of **Cioponea Alexandru (Shenny)**.
* **Commercial Restrictions:** Commercial resale, commercial hosting, proprietary bundling, or unauthorized patent filings are strictly prohibited without an explicit written license. See [LICENSE.md](LICENSE.md) for full terms.
