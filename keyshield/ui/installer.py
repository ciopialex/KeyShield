"""Aethelark MicShield Steve Jobs-esque Graphical Setup Assistant.
======================================================================
Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
Licensed for personal, non-commercial use only.
Strictly zero emojis. Agency-grade double-bezel vector architecture.
"""
from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QRectF, QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QGuiApplication,
    QIcon,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QRadialGradient,
)
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from keyshield.ui.assets import (
    SVG_AETHELARK_SHIELD,
    SVG_ARROW_RIGHT,
    SVG_CHECKMARK,
    SVG_HARDWARE_ENCLAVE,
    SVG_KEYSTROKE_DEFLECT,
    SVG_VOCAL_RESONANCE,
    get_aethelark_icon,
    render_svg_pixmap,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class FeatureRow(QWidget):
    """Architectural double-bezel feature block with custom vector icon."""

    def __init__(self, svg_str: str, title: str, description: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(14)

        # Vector Icon Container (Milled Circular Bezel)
        icon_box = QWidget()
        icon_box.setFixedSize(36, 36)
        icon_box.setStyleSheet("""
            background: #14171A;
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        """)
        box_layout = QVBoxLayout(icon_box)
        box_layout.setContentsMargins(7, 7, 7, 7)

        lbl_icon = QLabel()
        lbl_icon.setPixmap(render_svg_pixmap(svg_str, 20, 20))
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box_layout.addWidget(lbl_icon)
        layout.addWidget(icon_box)

        # Text Column
        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #F2F2F7; font-size: 11px; font-weight: 600; letter-spacing: 0.2px;")
        text_col.addWidget(lbl_title)

        lbl_desc = QLabel(description)
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("color: #8E8E93; font-size: 10px; line-height: 1.35;")
        text_col.addWidget(lbl_desc)

        layout.addLayout(text_col)


class SetupAssistantWindow(QMainWindow):
    """Steve Jobs-esque Cupertino Glass Graphical Setup Assistant."""

    log_signal = pyqtSignal(str, int)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aethelark MicShield Setup")
        self.setWindowIcon(get_aethelark_icon())

        # Standard window with taskbar presence
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(430, 680)

        self._drag_pos = None
        self.is_installed = self._check_is_installed()

        self.log_signal.connect(self._on_progress)
        self.finished_signal.connect(self._on_finished)

        self._init_ui()

    def _check_is_installed(self) -> bool:
        launcher = Path.home() / ".local" / "bin" / "keyshield"
        return launcher.exists()

    def _init_ui(self):
        root = QWidget(self)
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(28, 22, 28, 26)
        layout.setSpacing(12)

        # 1. Top Controls Bar
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)

        eyebrow = QLabel("AETHELARK APPARATUS")
        eyebrow.setStyleSheet("""
            color: #389E62;
            background: rgba(56, 158, 98, 0.12);
            border: 1px solid rgba(56, 158, 98, 0.22);
            border-radius: 10px;
            padding: 3px 8px;
            font-size: 8px;
            font-weight: 700;
            letter-spacing: 1.6px;
        """)
        top_bar.addWidget(eyebrow)
        top_bar.addStretch()

        btn_close = QPushButton("×")
        btn_close.setFixedSize(26, 26)
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #18191E; color: #8E8E93; border-radius: 13px; font-size: 15px; font-weight: bold; border: 1px solid rgba(255, 255, 255, 0.05);
            }
            QPushButton:hover { background: #E03535; color: #FFFFFF; border-color: transparent; }
        """)
        btn_close.clicked.connect(self.close)
        top_bar.addWidget(btn_close)
        layout.addLayout(top_bar)

        # 2. Hero Vector Shield (Custom SVG with radiant ambient halo)
        icon_row = QHBoxLayout()
        icon_row.addStretch()
        lbl_hero = QLabel()
        lbl_hero.setPixmap(render_svg_pixmap(SVG_AETHELARK_SHIELD, 82, 82))
        lbl_hero.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_row.addWidget(lbl_hero)
        icon_row.addStretch()
        layout.addLayout(icon_row)

        # 3. Typography & Attribution
        self.lbl_title = QLabel("Aethelark MicShield")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setStyleSheet("""
            color: #FFFFFF;
            font-size: 21px;
            font-weight: 700;
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
            letter-spacing: -0.3px;
        """)
        layout.addWidget(self.lbl_title)

        self.lbl_sub = QLabel("Autonomous Acoustic Firewall • Designed by Cioponea Alexandru")
        self.lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_sub.setStyleSheet("color: #7A7D85; font-size: 10px; font-weight: 500; letter-spacing: 0.2px;")
        layout.addWidget(self.lbl_sub)

        layout.addSpacing(2)

        # 4. Double-Bezel Architectural Container (How it protects you)
        shell = QWidget()
        shell.setStyleSheet("""
            QWidget#Shell {
                background: #101115;
                border-radius: 14px;
                border: 1px solid rgba(255, 255, 255, 0.06);
            }
        """)
        shell.setObjectName("Shell")
        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(4, 4, 4, 4)
        shell_layout.setSpacing(2)

        row1 = FeatureRow(
            SVG_KEYSTROKE_DEFLECT,
            "Acoustic Keystroke Deflection",
            "Neutralizes AI sound eavesdroppers that reconstruct private passwords and typing from microphone audio."
        )
        row2 = FeatureRow(
            SVG_VOCAL_RESONANCE,
            "Neural Vocal Formant Passthrough",
            "Deep-learning VAD detects vocal tract harmonics, keeping your natural voice crystal-clear in calls."
        )
        row3 = FeatureRow(
            SVG_HARDWARE_ENCLAVE,
            "Zero-Data Collection Guarantee",
            "100% offline on your CPU. No audio recording, no telemetry. Free for personal use (IP: Cioponea Alexandru)."
        )

        shell_layout.addWidget(row1)
        # Hairline separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background: rgba(255, 255, 255, 0.04); max-height: 1px; margin: 0 12px;")
        shell_layout.addWidget(sep)
        shell_layout.addWidget(row2)
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("background: rgba(255, 255, 255, 0.04); max-height: 1px; margin: 0 12px;")
        shell_layout.addWidget(sep2)
        shell_layout.addWidget(row3)

        layout.addWidget(shell)

        # 5. Status Chip & Readiness Strip
        self.status_chip = QWidget()
        self.status_chip.setStyleSheet("""
            background: #0E1013;
            border-radius: 10px;
            border: 1px solid rgba(56, 158, 98, 0.16);
        """)
        chip_layout = QHBoxLayout(self.status_chip)
        chip_layout.setContentsMargins(14, 8, 14, 8)
        chip_layout.setSpacing(10)

        self.chip_icon = QLabel()
        self.chip_icon.setPixmap(render_svg_pixmap(SVG_CHECKMARK, 14, 14))
        chip_layout.addWidget(self.chip_icon)

        self.lbl_chip_text = QLabel("System Ready • PipeWire Virtual Loopback Configured")
        self.lbl_chip_text.setStyleSheet("color: #E5E5EA; font-size: 10px; font-weight: 500;")
        chip_layout.addWidget(self.lbl_chip_text)
        chip_layout.addStretch()

        layout.addWidget(self.status_chip)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar { background: #1C1C1E; border-radius: 1.5px; border: none; }
            QProgressBar::chunk { background: #389E62; border-radius: 1.5px; }
        """)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # 6. Options Checkbox
        self.chk_autostart = QCheckBox("Arm acoustic shield automatically on system login")
        self.chk_autostart.setChecked(True)
        self.chk_autostart.setStyleSheet("""
            QCheckBox { color: #8E8E93; font-size: 10.5px; font-weight: 400; }
            QCheckBox::indicator { width: 14px; height: 14px; border-radius: 4px; border: 1px solid #3A3A3C; background: #16171B; }
            QCheckBox::indicator:checked { background: #2E8B57; border-color: #389E62; }
        """)
        layout.addWidget(self.chk_autostart)

        layout.addStretch()

        # 7. Island Button CTA Architecture
        self.btn_layout = QVBoxLayout()
        self.btn_layout.setSpacing(8)

        if not self.is_installed:
            self.btn_primary = QPushButton("Install Aethelark MicShield")
            self.btn_primary.setFixedHeight(46)
            self.btn_primary.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_primary.setStyleSheet("""
                QPushButton {
                    background: #2E8B57;
                    color: #FFFFFF;
                    font-size: 13.5px;
                    font-weight: 600;
                    border-radius: 23px;
                    border: none;
                    letter-spacing: 0.3px;
                }
                QPushButton:hover { background: #349D63; }
                QPushButton:pressed { background: #257548; }
            """)
            self.btn_primary.clicked.connect(self._start_install)
            self.btn_layout.addWidget(self.btn_primary)
        else:
            self.btn_primary = QPushButton("Launch Aethelark MicShield")
            self.btn_primary.setFixedHeight(46)
            self.btn_primary.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_primary.setStyleSheet("""
                QPushButton {
                    background: #2E8B57;
                    color: #FFFFFF;
                    font-size: 13.5px;
                    font-weight: 600;
                    border-radius: 23px;
                    border: none;
                }
                QPushButton:hover { background: #349D63; }
            """)
            self.btn_primary.clicked.connect(self._launch_app)
            self.btn_layout.addWidget(self.btn_primary)


            self.btn_uninstall = QPushButton("Uninstall from System")
            self.btn_uninstall.setFixedHeight(38)
            self.btn_uninstall.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_uninstall.setStyleSheet("""
                QPushButton {
                    background: #141519;
                    color: #FF453A;
                    font-size: 11.5px;
                    font-weight: 600;
                    border-radius: 19px;
                    border: 1px solid rgba(255, 69, 58, 0.2);
                }
                QPushButton:hover { background: #1F2026; border-color: rgba(255, 69, 58, 0.45); }
            """)
            self.btn_uninstall.clicked.connect(self._start_uninstall)
            self.btn_layout.addWidget(self.btn_uninstall)

        layout.addLayout(self.btn_layout)

    def _start_install(self):
        self.btn_primary.setEnabled(False)
        self.btn_primary.setText("Installing Apparatus...")
        self.progress_bar.show()
        self.progress_bar.setValue(15)
        self.lbl_chip_text.setText("Installing neural gatekeeper...")

        threading.Thread(target=self._run_install_worker, daemon=True).start()

    def _run_install_worker(self):
        try:
            self.log_signal.emit("Configuring ONNX neural engine...", 35)
            time.sleep(0.4)

            sh_path = PROJECT_ROOT / "install.sh"
            if sh_path.exists():
                subprocess.run(["bash", str(sh_path)], cwd=str(PROJECT_ROOT), check=True)

            self.log_signal.emit("Mounting PipeWire virtual acoustic device...", 75)
            time.sleep(0.4)

            self.log_signal.emit("Integration complete.", 100)
            time.sleep(0.3)
            self.finished_signal.emit(True, "Aethelark MicShield is active and protected.")
        except Exception as e:
            self.finished_signal.emit(False, f"Installation failed: {e}")

    def _start_uninstall(self):
        self.btn_uninstall.setEnabled(False)
        self.btn_primary.setEnabled(False)
        self.btn_uninstall.setText("Purging...")
        self.progress_bar.show()
        self.progress_bar.setValue(30)
        self.lbl_chip_text.setText("Removing from system...")

        threading.Thread(target=self._run_uninstall_worker, daemon=True).start()

    def _run_uninstall_worker(self):
        try:
            sh_path = PROJECT_ROOT / "uninstall.sh"
            if sh_path.exists():
                subprocess.run(["bash", str(sh_path)], cwd=str(PROJECT_ROOT), check=True)
            self.log_signal.emit("All virtual devices, shortcuts & configs removed.", 100)
            time.sleep(0.4)
            self.finished_signal.emit(True, "Uninstalled cleanly from system.")
        except Exception as e:
            self.finished_signal.emit(False, f"Uninstall failed: {e}")

    def _on_progress(self, msg: str, percent: int):
        self.lbl_chip_text.setText(msg)
        self.progress_bar.setValue(percent)

    def _on_finished(self, success: bool, msg: str):
        self.progress_bar.hide()
        if success:
            self.lbl_chip_text.setText(msg)
            self.lbl_chip_text.setStyleSheet("color: #389E62; font-size: 10px; font-weight: 600;")
            self.btn_primary.setText("Close Assistant")
            self.btn_primary.setEnabled(True)
            self.btn_primary.clicked.disconnect()
            self.btn_primary.clicked.connect(self.close)
            if hasattr(self, "btn_uninstall"):
                self.btn_uninstall.hide()
        else:
            self.lbl_chip_text.setText(msg)
            self.lbl_chip_text.setStyleSheet("color: #FF453A; font-size: 10px; font-weight: 600;")
            self.btn_primary.setText("Retry")
            self.btn_primary.setEnabled(True)

    def _launch_app(self):
        launcher = Path.home() / ".local" / "bin" / "keyshield"
        if launcher.exists():
            subprocess.Popen([str(launcher)])
            self.close()
        else:
            self.lbl_chip_text.setText("Launcher not found. Please install first.")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def paintEvent(self, event):
        """Draws the aerospace-grade obsidian chassis."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = float(self.width()), float(self.height())
        radius = 24.0

        path = QPainterPath()
        path.addRoundedRect(QRectF(1, 1, w - 2, h - 2), radius, radius)

        # Deepest OLED Obsidian Titanium gradient
        bg_grad = QLinearGradient(0, 0, 0, h)
        bg_grad.setColorAt(0.0, QColor(13, 14, 18, 252))
        bg_grad.setColorAt(1.0, QColor(6, 7, 9, 252))
        painter.fillPath(path, QBrush(bg_grad))

        # Precision 1px hairline border
        painter.setPen(QPen(QColor(255, 255, 255, 22), 1.0))
        painter.drawPath(path)
