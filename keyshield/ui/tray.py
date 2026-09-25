"""KeyShield System Tray Integration.
======================================================================
Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
Licensed for personal, non-commercial use only.
"""
from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QAction, QColor, QIcon, QPainter, QPainterPath, QPen, QPixmap
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon


def create_shield_icon(active: bool = True) -> QIcon:
    """Generates an Apple-style minimalist vector shield icon in memory."""
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    cx, cy = 32.0, 32.0
    path = QPainterPath()
    path.moveTo(cx, cy - 20)
    path.lineTo(cx + 18, cy - 10)
    path.quadTo(cx + 18, cy + 12, cx, cy + 24)
    path.quadTo(cx - 18, cy + 12, cx - 18, cy - 10)
    path.closeSubpath()

    color = QColor(56, 158, 98) if active else QColor(142, 142, 147)
    painter.setPen(QPen(color, 4.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(QColor(color.red(), color.green(), color.blue(), 60))
    painter.drawPath(path)
    painter.end()

    return QIcon(pixmap)


class KeyShieldTray(QSystemTrayIcon):
    """System tray controller for background protection."""

    def __init__(self, main_window, shield_engine, parent=None):
        super().__init__(create_shield_icon(True), parent)
        self.main_window = main_window
        self.shield_engine = shield_engine

        self.setToolTip("Aethelark MicShield — Acoustic Keystroke Defense Active")

        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #1C1C1E;
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 6px;
                font-family: -apple-system, sans-serif;
                font-size: 12px;
            }
            QMenu::item {
                padding: 6px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #2C2C2E;
                color: #389E62;
            }
        """)

        self.act_show = QAction("Open Aethelark MicShield", self)
        self.act_show.triggered.connect(self._toggle_window)
        menu.addAction(self.act_show)

        self.act_toggle_shield = QAction("Disable Defense", self)
        self.act_toggle_shield.triggered.connect(self._toggle_shield)
        menu.addAction(self.act_toggle_shield)

        menu.addSeparator()

        act_quit = QAction("Quit Aethelark MicShield", self)
        act_quit.triggered.connect(self._quit)
        menu.addAction(act_quit)

        self.setContextMenu(menu)
        self.activated.connect(self._on_activated)

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self._toggle_window()

    def _toggle_window(self):
        if self.main_window.isVisible():
            self.main_window.hide()
        else:
            self.main_window.show()
            self.main_window.activateWindow()

    def _toggle_shield(self):
        is_armed = not self.shield_engine.is_armed
        self.shield_engine.set_armed(is_armed)
        self.main_window.switch.setChecked(is_armed)
        self.setIcon(create_shield_icon(is_armed))
        if is_armed:
            self.act_toggle_shield.setText("Disable Defense")
            self.setToolTip("Aethelark MicShield — Acoustic Keystroke Defense Active")
        else:
            self.act_toggle_shield.setText("Enable Defense")
            self.setToolTip("Aethelark MicShield — Defense Paused")

    def _quit(self):
        self.shield_engine.stop()
        from PyQt6.QtWidgets import QApplication
        QApplication.instance().quit()
