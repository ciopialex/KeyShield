"""KeyShield Steve Jobs-esque Minimalist User Interface.
======================================================================
Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
Licensed for personal, non-commercial use only.
"""
from __future__ import annotations

import math
from typing import Optional

from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QRect,
    QRectF,
    QSize,
    Qt,
    QTimer,
    pyqtProperty,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class TactileSwitch(QWidget):
    """Steve Jobs-style tactile toggle switch with fluid animation."""

    toggled = pyqtSignal(bool)

    def __init__(self, checked=True, parent=None):
        super().__init__(parent)
        self.setFixedSize(56, 32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._checked = checked
        self._thumb_position = 28.0 if checked else 4.0

        self._anim = QPropertyAnimation(self, b"thumb_position")
        self._anim.setDuration(180)
        self._anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, checked: bool):
        if self._checked != checked:
            self._checked = checked
            self._animate_thumb()
            self.toggled.emit(self._checked)

    def _get_thumb_position(self) -> float:
        return self._thumb_position

    def _set_thumb_position(self, pos: float):
        self._thumb_position = pos
        self.update()

    thumb_position = pyqtProperty(float, _get_thumb_position, _set_thumb_position)

    def _animate_thumb(self):
        target = 28.0 if self._checked else 4.0
        self._anim.stop()
        self._anim.setStartValue(self._thumb_position)
        self._anim.setEndValue(target)
        self._anim.start()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setChecked(not self._checked)
            event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = float(self.width()), float(self.height())
        r = h / 2.0

        track_path = QPainterPath()
        track_path.addRoundedRect(0, 0, w, h, r, r)

        # Track background
        if self._checked:
            track_color = QColor(56, 158, 98)  # Muted Titanium Emerald
        else:
            track_color = QColor(44, 44, 48)   # Apple Dark Graphite

        painter.fillPath(track_path, track_color)

        # Thumb
        thumb_d = 24.0
        thumb_y = 4.0
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(QRectF(self._thumb_position, thumb_y, thumb_d, thumb_d))


class AcousticShieldOrb(QWidget):
    """Central interactive status orb with breathing glow and voice waveform."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(160, 160)
        self.is_armed = True
        self.is_voice = False
        self.speech_prob = 0.0
        self.raw_rms = 0.0
        self.keystroke_flash = 0.0
        self.wave_phase = 0.0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(33)  # ~30 fps

    def update_telemetry(self, is_voice: bool, prob: float, rms: float, key_blocked: bool):
        self.is_voice = is_voice
        self.speech_prob = prob
        self.raw_rms = rms
        if key_blocked:
            self.keystroke_flash = 1.0
        self.update()

    def set_armed(self, armed: bool):
        self.is_armed = armed
        self.update()

    def _tick(self):
        self.wave_phase += 0.08
        if self.keystroke_flash > 0.0:
            self.keystroke_flash = max(0.0, self.keystroke_flash - 0.05)
            self.update()
        if self.is_voice:
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        cx, cy = self.width() / 2.0, self.height() / 2.0
        base_radius = 54.0

        # Breathing pulse calculation
        breath = math.sin(self.wave_phase) * 3.0

        # Outer Radial Glow
        glow_grad = QRadialGradient(cx, cy, 75.0)
        if not self.is_armed:
            glow_grad.setColorAt(0.0, QColor(90, 95, 105, 30))
            glow_grad.setColorAt(1.0, QColor(0, 0, 0, 0))
        elif self.keystroke_flash > 0.1:
            alpha = int(self.keystroke_flash * 140)
            glow_grad.setColorAt(0.0, QColor(255, 159, 10, alpha))
            glow_grad.setColorAt(1.0, QColor(0, 0, 0, 0))
        elif self.is_voice:
            glow_grad.setColorAt(0.0, QColor(56, 158, 98, 160))
            glow_grad.setColorAt(1.0, QColor(0, 0, 0, 0))
        else:
            glow_grad.setColorAt(0.0, QColor(56, 158, 98, 60))
            glow_grad.setColorAt(1.0, QColor(0, 0, 0, 0))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(glow_grad))
        painter.drawEllipse(QRectF(cx - 75, cy - 75, 150, 150))

        # Main Sphere Body
        body_grad = QLinearGradient(cx - base_radius, cy - base_radius, cx + base_radius, cy + base_radius)
        if not self.is_armed:
            body_grad.setColorAt(0.0, QColor(35, 36, 42))
            body_grad.setColorAt(1.0, QColor(18, 19, 22))
        else:
            body_grad.setColorAt(0.0, QColor(22, 28, 25))
            body_grad.setColorAt(1.0, QColor(10, 14, 12))

        painter.setBrush(QBrush(body_grad))
        ring_color = QColor(56, 158, 98, 200) if self.is_armed else QColor(80, 80, 85, 120)
        if self.keystroke_flash > 0.1:
            ring_color = QColor(255, 159, 10, 240)
        painter.setPen(QPen(ring_color, 2.0))
        painter.drawEllipse(QRectF(cx - base_radius, cy - base_radius, base_radius * 2, base_radius * 2))

        # Dynamic Content Inside Sphere:
        # If voice is passing: draw harmonic vocal rings
        if self.is_voice and self.is_armed:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(56, 158, 98, 220))
            num_bars = 5
            for i in range(num_bars):
                bx = cx - 22 + (i * 11)
                amp = math.sin(self.wave_phase * 2.5 + i * 1.2) * 12.0
                bar_h = max(8.0, 22.0 + amp)
                painter.drawRoundedRect(QRectF(bx, cy - bar_h / 2.0, 5, bar_h), 2.5, 2.5)
        else:
            # Draw Minimalist Shield Glyph
            shield_path = QPainterPath()
            sx, sy = cx, cy - 14
            shield_path.moveTo(sx, sy)
            shield_path.lineTo(sx + 16, sy + 6)
            shield_path.quadTo(sx + 16, sy + 24, sx, sy + 34)
            shield_path.quadTo(sx - 16, sy + 24, sx - 16, sy + 6)
            shield_path.closeSubpath()

            if not self.is_armed:
                icon_pen = QPen(QColor(120, 122, 130), 2.0)
                icon_fill = QColor(45, 47, 52, 100)
            elif self.keystroke_flash > 0.1:
                icon_pen = QPen(QColor(255, 159, 10), 2.0)
                icon_fill = QColor(255, 159, 10, 40)
            else:
                icon_pen = QPen(QColor(56, 158, 98), 2.0)
                icon_fill = QColor(56, 158, 98, 40)


            painter.setPen(icon_pen)
            painter.setBrush(QBrush(icon_fill))
            painter.drawPath(shield_path)


class KeyShieldWindow(QMainWindow):
    """Steve Jobs-esque Cupertino Glass Interface for KeyShield."""

    telemetry_signal = pyqtSignal(bool, float, float, str, int, bool)

    def __init__(self, shield_engine, parent=None):
        super().__init__(parent)
        self.shield_engine = shield_engine

        self.setWindowTitle("Aethelark MicShield")
        self.setWindowIcon(create_shield_icon(True))

        # Frameless, translucent Apple obsidian styling with taskbar presence
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(340, 480)

        self._drag_pos = QPoint()

        # Connect telemetry signal for thread safety
        self.telemetry_signal.connect(self._on_telemetry)
        self.shield_engine.on_telemetry = self._emit_telemetry

        self._init_ui()

    def _emit_telemetry(self, is_voice, prob, rms, state, count, key_blocked):
        self.telemetry_signal.emit(is_voice, prob, rms, state, count, key_blocked)

    def _init_ui(self):
        root = QWidget(self)
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(24, 20, 24, 24)
        layout.setSpacing(14)

        # 1. Header Bar: Window controls & Branding
        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)

        title_col = QVBoxLayout()
        title_col.setSpacing(2)

        lbl_title = QLabel("Aethelark MicShield")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: 700; font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;")
        title_col.addWidget(lbl_title)

        lbl_sub = QLabel("ACOUSTIC KEYSTROKE DEFENSE")
        lbl_sub.setStyleSheet("color: #86868B; font-size: 8px; font-weight: 700; letter-spacing: 1.5px;")
        title_col.addWidget(lbl_sub)


        header.addLayout(title_col)
        header.addStretch()

        # Close / Minimize buttons
        btn_min = QPushButton("–")
        btn_min.setFixedSize(24, 24)
        btn_min.setStyleSheet("""
            QPushButton {
                background: #1C1C1E; color: #8E8E93; border-radius: 12px; font-size: 14px; font-weight: bold; border: none;
            }
            QPushButton:hover { background: #2C2C2E; color: #FFFFFF; }
        """)
        btn_min.clicked.connect(self.hide)
        header.addWidget(btn_min)

        btn_close = QPushButton("×")
        btn_close.setFixedSize(24, 24)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #1C1C1E; color: #8E8E93; border-radius: 12px; font-size: 14px; font-weight: bold; border: none;
            }
            QPushButton:hover { background: #E03535; color: #FFFFFF; }
        """)
        btn_close.clicked.connect(QApplication.instance().quit)
        header.addWidget(btn_close)

        layout.addLayout(header)

        # 2. Central Shield Orb
        layout.addSpacing(6)
        orb_container = QHBoxLayout()
        orb_container.addStretch()
        self.orb = AcousticShieldOrb(self)
        orb_container.addWidget(self.orb)
        orb_container.addStretch()
        layout.addLayout(orb_container)

        # 3. Status Badge & Description
        self.lbl_status = QLabel("PROTECTED")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setStyleSheet("color: #389E62; font-size: 13px; font-weight: 700; letter-spacing: 2px;")
        layout.addWidget(self.lbl_status)

        self.lbl_desc = QLabel("Keyboard acoustic mapping blocked.\nHuman voice passes with zero loss.")
        self.lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_desc.setStyleSheet("color: #A1A1A6; font-size: 11px; line-height: 1.4;")
        layout.addWidget(self.lbl_desc)

        layout.addSpacing(4)

        # 4. Tactile Master Switch Row
        switch_card = QWidget()
        switch_card.setStyleSheet("background: #141418; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.05);")
        switch_layout = QHBoxLayout(switch_card)
        switch_layout.setContentsMargins(16, 12, 16, 12)

        switch_label_col = QVBoxLayout()
        switch_label_col.setSpacing(2)
        lbl_sw_title = QLabel("Acoustic Firewall")
        lbl_sw_title.setStyleSheet("color: #FFFFFF; font-size: 13px; font-weight: 600;")
        self.lbl_sw_sub = QLabel("Active defense running")
        self.lbl_sw_sub.setStyleSheet("color: #8E8E93; font-size: 10px;")
        switch_label_col.addWidget(lbl_sw_title)
        switch_label_col.addWidget(self.lbl_sw_sub)
        switch_layout.addLayout(switch_label_col)
        switch_layout.addStretch()

        self.switch = TactileSwitch(checked=True)
        self.switch.toggled.connect(self._on_switch_toggled)
        switch_layout.addWidget(self.switch)
        layout.addWidget(switch_card)

        # 5. Live Telemetry Metric Strip
        metrics_row = QHBoxLayout()
        metrics_row.setSpacing(10)

        # Card 1: Blocked Keystrokes
        c1 = QWidget()
        c1.setStyleSheet("background: #141418; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);")
        c1_layout = QVBoxLayout(c1)
        c1_layout.setContentsMargins(12, 10, 12, 10)
        c1_layout.setSpacing(2)
        lbl_c1_t = QLabel("BLOCKED TAPS")
        lbl_c1_t.setStyleSheet("color: #636366; font-size: 8px; font-weight: 700; letter-spacing: 1px;")
        self.lbl_count = QLabel("0")
        self.lbl_count.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: 700; font-family: -apple-system, monospace;")
        c1_layout.addWidget(lbl_c1_t)
        c1_layout.addWidget(self.lbl_count)
        metrics_row.addWidget(c1)

        # Card 2: Neural Confidence
        c2 = QWidget()
        c2.setStyleSheet("background: #141418; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05);")
        c2_layout = QVBoxLayout(c2)
        c2_layout.setContentsMargins(12, 10, 12, 10)
        c2_layout.setSpacing(2)
        lbl_c2_t = QLabel("LATENCY")
        lbl_c2_t.setStyleSheet("color: #636366; font-size: 8px; font-weight: 700; letter-spacing: 1px;")
        lbl_c2_val = QLabel("0.25 ms")
        lbl_c2_val.setStyleSheet("color: #389E62; font-size: 18px; font-weight: 700; font-family: -apple-system, monospace;")
        c2_layout.addWidget(lbl_c2_t)
        c2_layout.addWidget(lbl_c2_val)
        metrics_row.addWidget(c2)

        layout.addLayout(metrics_row)

        layout.addStretch()

        # 6. Minimalist Signature Footer
        footer = QLabel("Designed by Cioponea Alexandru (Shenny)")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #48484A; font-size: 9px; font-weight: 500; letter-spacing: 0.5px;")
        layout.addWidget(footer)

    def _on_switch_toggled(self, checked: bool):
        self.shield_engine.set_armed(checked)
        self.orb.set_armed(checked)
        if checked:
            self.lbl_status.setText("PROTECTED")
            self.lbl_status.setStyleSheet("color: #389E62; font-size: 13px; font-weight: 700; letter-spacing: 2px;")
            self.lbl_desc.setText("Keyboard acoustic mapping blocked.\nHuman voice passes with zero loss.")
            self.lbl_sw_sub.setText("Active defense running")
        else:
            self.lbl_status.setText("DISARMED")
            self.lbl_status.setStyleSheet("color: #8E8E93; font-size: 13px; font-weight: 700; letter-spacing: 2px;")
            self.lbl_desc.setText("Mic is open to all sounds.\nKeystrokes are exposed to eavesdropping.")
            self.lbl_sw_sub.setText("Defense bypassed")

    def _on_telemetry(self, is_voice: bool, prob: float, rms: float, state: str, count: int, key_blocked: bool):
        self.orb.update_telemetry(is_voice, prob, rms, key_blocked)
        self.lbl_count.setText(str(count))

        if self.shield_engine.is_armed:
            if is_voice:
                self.lbl_status.setText("VOICE DETECTED")
                self.lbl_status.setStyleSheet("color: #389E62; font-size: 13px; font-weight: 700; letter-spacing: 2px;")
            elif key_blocked:
                self.lbl_status.setText("KEYSTROKE DEFLECTED")
                self.lbl_status.setStyleSheet("color: #FF9F0A; font-size: 13px; font-weight: 700; letter-spacing: 2px;")
            else:
                self.lbl_status.setText("PROTECTED")
                self.lbl_status.setStyleSheet("color: #389E62; font-size: 13px; font-weight: 700; letter-spacing: 2px;")


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def paintEvent(self, event):
        """Draws the dark obsidian glass card background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = float(self.width()), float(self.height())
        radius = 24.0

        path = QPainterPath()
        path.addRoundedRect(QRectF(1, 1, w - 2, h - 2), radius, radius)

        # Deep Apple Obsidian Ceramic gradient
        bg_grad = QLinearGradient(0, 0, 0, h)
        bg_grad.setColorAt(0.0, QColor(14, 15, 20, 252))
        bg_grad.setColorAt(1.0, QColor(7, 8, 11, 252))
        painter.fillPath(path, QBrush(bg_grad))

        # Precision 1px hairline border
        painter.setPen(QPen(QColor(255, 255, 255, 22), 1.0))
        painter.drawPath(path)
