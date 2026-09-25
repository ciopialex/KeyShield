"""Bespoke Vector SVG Assets for Aethelark MicShield.
======================================================================
Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
Strictly zero emojis. Ultra-precise agency-grade line geometry.
"""
from __future__ import annotations

from PyQt6.QtCore import QByteArray, QRectF, Qt
from PyQt6.QtGui import QIcon, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer

# 1. Master Aethelark Shield Emblem (High-end geometric faceted shield with inner acoustic core)
SVG_AETHELARK_SHIELD = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" fill="none">
  <defs>
    <radialGradient id="shieldGlow" cx="50%" cy="45%" r="50%">
      <stop offset="0%" stop-color="#34C759" stop-opacity="0.35"/>
      <stop offset="60%" stop-color="#30D158" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="shieldBorder" x1="0" y1="0" x2="120" y2="120" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#34C759"/>
      <stop offset="50%" stop-color="#30D158" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0A84FF" stop-opacity="0.3"/>
    </linearGradient>
    <linearGradient id="facetHighlight" x1="30" y1="20" x2="60" y2="90" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.0"/>
    </linearGradient>
  </defs>

  <!-- Ambient Radiant Halo -->
  <circle cx="60" cy="58" r="50" fill="url(#shieldGlow)"/>

  <!-- Outer Protective Armor Contour -->
  <path d="M60 16L94 28.5C94 62 80 89 60 102C40 89 26 62 26 28.5L60 16Z" 
        fill="#0D110F" 
        stroke="url(#shieldBorder)" 
        stroke-width="2.5" 
        stroke-linejoin="round"/>

  <!-- Chamfered Facet Highlight (Physical Machined Depth) -->
  <path d="M60 19L91 30.5C91 58 79 83 60 97V19Z" fill="url(#facetHighlight)"/>

  <!-- Inner Neural Core Aperture -->
  <path d="M60 32L78 40C78 61 70 77 60 84C50 77 42 61 42 40L60 32Z" 
        fill="#070908" 
        stroke="#34C759" 
        stroke-width="1.2" 
        stroke-opacity="0.6"/>

  <!-- Center Waveform Spine (Vocal Resonance Gateway) -->
  <line x1="60" y1="46" x2="60" y2="70" stroke="#34C759" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="53" y1="51" x2="53" y2="65" stroke="#34C759" stroke-width="2" stroke-linecap="round" stroke-opacity="0.8"/>
  <line x1="67" y1="51" x2="67" y2="65" stroke="#34C759" stroke-width="2" stroke-linecap="round" stroke-opacity="0.8"/>
  <line x1="47" y1="55" x2="47" y2="61" stroke="#34C759" stroke-width="1.5" stroke-linecap="round" stroke-opacity="0.4"/>
  <line x1="73" y1="55" x2="73" y2="61" stroke="#34C759" stroke-width="1.5" stroke-linecap="round" stroke-opacity="0.4"/>
</svg>"""

# 2. Keystroke Deflection Vector Icon (Acoustic impulse transient reflected at shield barrier)
SVG_KEYSTROKE_DEFLECT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <!-- Keycap base -->
  <rect x="3" y="11" width="8" height="8" rx="2" stroke="#8E8E93" stroke-width="1.5"/>
  <path d="M4.5 11V8.5C4.5 7.67 5.17 7 6 7H8C8.83 7 9.5 7.67 9.5 8.5V11" stroke="#8E8E93" stroke-width="1.5"/>
  <!-- Sound spikes coming off keycap -->
  <path d="M12 12.5L14 11.5M12 16.5L14 17.5" stroke="#FF9F0A" stroke-width="1.5" stroke-linecap="round"/>
  <!-- Energy Shield Deflection Wall -->
  <path d="M17 5V19" stroke="#34C759" stroke-width="2" stroke-linecap="round"/>
  <!-- Deflected trajectory -->
  <path d="M14.5 14.5L16.5 14.5L14.5 12" stroke="#FF9F0A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M21 9L18.5 12L21 15" stroke="#34C759" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="2 2"/>
</svg>"""

# 3. Biometric Vocal Resonance Vector Icon (Formant harmonics flowing unobstructed)
SVG_VOCAL_RESONANCE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <!-- Dynamic Vocal Wave Bands -->
  <path d="M3 12C4.5 10 5.5 10 7 12C8.5 14 9.5 14 11 12C12.5 10 13.5 10 15 12C16.5 14 17.5 14 19 12C20 10.5 21 11 22 12" 
        stroke="#34C759" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M5 8C6.5 6.5 7.5 6.5 9 8C10.5 9.5 11.5 9.5 13 8C14.5 6.5 15.5 6.5 17 8" 
        stroke="#34C759" stroke-width="1.4" stroke-linecap="round" stroke-opacity="0.6"/>
  <path d="M5 16C6.5 17.5 7.5 17.5 9 16C10.5 14.5 11.5 14.5 13 16C14.5 17.5 15.5 17.5 17 16" 
        stroke="#34C759" stroke-width="1.4" stroke-linecap="round" stroke-opacity="0.6"/>
</svg>"""

# 4. Zero-Cloud Local Hardware Enclave Vector Icon
SVG_HARDWARE_ENCLAVE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
  <!-- Silicon Processor Package -->
  <rect x="5" y="5" width="14" height="14" rx="2.5" stroke="#34C759" stroke-width="1.5" fill="#0E120F"/>
  <!-- Enclave Lock core -->
  <rect x="9" y="11" width="6" height="5" rx="1" stroke="#34C759" stroke-width="1.3"/>
  <path d="M10 11V9.5C10 8.4 10.9 7.5 12 7.5C13.1 7.5 14 8.4 14 9.5V11" stroke="#34C759" stroke-width="1.3"/>
  <!-- Disconnected Air-Gap Pins (Zero cloud egress) -->
  <line x1="9" y1="2" x2="9" y2="4.5" stroke="#636366" stroke-width="1.2" stroke-linecap="round"/>
  <line x1="15" y1="2" x2="15" y2="4.5" stroke="#636366" stroke-width="1.2" stroke-linecap="round"/>
  <line x1="9" y1="19.5" x2="9" y2="22" stroke="#636366" stroke-width="1.2" stroke-linecap="round"/>
  <line x1="15" y1="19.5" x2="15" y2="22" stroke="#636366" stroke-width="1.2" stroke-linecap="round"/>
  <line x1="2" y1="9" x2="4.5" y2="9" stroke="#636366" stroke-width="1.2" stroke-linecap="round"/>
  <line x1="2" y1="15" x2="4.5" y2="15" stroke="#636366" stroke-width="1.2" stroke-linecap="round"/>
  <line x1="19.5" y1="9" x2="22" y2="9" stroke="#636366" stroke-width="1.2" stroke-linecap="round"/>
  <line x1="19.5" y1="15" x2="22" y2="15" stroke="#636366" stroke-width="1.2" stroke-linecap="round"/>
</svg>"""

# 5. Checkmark Glyph (1.5px clean geometric check)
SVG_CHECKMARK = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none">
  <path d="M3.5 8.5L6.5 11.5L12.5 5" stroke="#34C759" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

# 6. Action Arrow Button Glyph
SVG_ARROW_RIGHT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none">
  <path d="M6 3.5L10.5 8L6 12.5" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""


def render_svg_pixmap(svg_str: str, width: int, height: int) -> QPixmap:
    """Renders any vector SVG string into an ultra-sharp anti-aliased QPixmap."""
    renderer = QSvgRenderer(QByteArray(svg_str.encode("utf-8")))
    pixmap = QPixmap(width, height)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(painter, QRectF(0, 0, width, height))
    painter.end()

    return pixmap


def get_aethelark_icon() -> QIcon:
    """Generates high-DPI multi-resolution QIcon for desktop taskbar & docks."""
    icon = QIcon()
    for size in (16, 24, 32, 48, 64, 128, 256):
        icon.addPixmap(render_svg_pixmap(SVG_AETHELARK_SHIELD, size, size))
    return icon
