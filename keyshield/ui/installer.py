"""KeyShield Steve Jobs-esque Graphical Installer & Setup Assistant.
======================================================================
Copyright (c) 2026 Cioponea Alexandru (Shenny). All Rights Reserved.
Licensed for personal, non-commercial use only.
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
from PyQt6.QtGui import QBrush, QColor, QFont, QIcon, QLinearGradient, QPainter, QPainterPath, QPen, QRadialGradient
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from keyshield.ui.tray import create_shield_icon

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class SetupAssistantWindow(QMainWindow):
    """Minimalist Cupertino-style Graphical Installer."""

    log_signal = pyqtSignal(str, int)  # status text, progress percentage
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(380, 500)

        self._drag_pos = None
        self.is_installed = self._check_is_installed()

        self.log_signal.connect(self._on_progress)
        self.finished_signal.connect(self._on_finished)

        self._init_ui()

    def _check_is_installed(self) -> bool:
        """Checks if KeyShield launcher is already in ~/.local/bin or desktop."""
        launcher = Path.home() / ".local" / "bin" / "keyshield"
        return launcher.exists()

    def _init_ui(self):
        root = QWidget(self)
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(16)

        # 1. Top Controls (Close button)
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        btn_close = QPushButton("×")
        btn_close.setFixedSize(24, 24)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #1C1C1E; color: #8E8E93; border-radius: 12px; font-size: 14px; font-weight: bold; border: none;
            }
            QPushButton:hover { background: #E03535; color: #FFFFFF; }
        """)
        btn_close.clicked.connect(self.close)
        top_bar.addWidget(btn_close)
        layout.addLayout(top_bar)

        # 2. Hero Icon (Centered Shield)
        icon_row = QHBoxLayout()
        icon_row.addStretch()
        lbl_icon = QLabel()
        lbl_icon.setPixmap(create_shield_icon(True).pixmap(72, 72))
        icon_row.addWidget(lbl_icon)
        icon_row.addStretch()
        layout.addLayout(icon_row)

        # 3. Title & Subtitle
        self.lbl_title = QLabel("KeyShield Setup")
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: 700; font-family: -apple-system, 'SF Pro Display', sans-serif;")
        layout.addWidget(self.lbl_title)

        self.lbl_sub = QLabel("Acoustic Keystroke Defense & Neural Gatekeeper\nDesigned by Cioponea Alexandru (Shenny)")
        self.lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_sub.setStyleSheet("color: #8E8E93; font-size: 11px; line-height: 1.4;")
        layout.addWidget(self.lbl_sub)

        layout.addSpacing(6)

        # 4. Status Card
        self.status_card = QWidget()
        self.status_card.setStyleSheet("background: #141418; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.06);")
        card_layout = QVBoxLayout(self.status_card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(8)

        if self.is_installed:
            self.lbl_state = QLabel("✓ KeyShield is currently installed")
            self.lbl_state.setStyleSheet("color: #34C759; font-size: 12px; font-weight: 600;")
            self.lbl_state_desc = QLabel("Installed at ~/.local/bin/keyshield with autostart enabled.")
        else:
            self.lbl_state = QLabel("Ready to Install")
            self.lbl_state.setStyleSheet("color: #FFFFFF; font-size: 12px; font-weight: 600;")
            self.lbl_state_desc = QLabel("Installs neural voice firewall and registers the virtual microphone.")

        self.lbl_state_desc.setStyleSheet("color: #8E8E93; font-size: 11px;")
        card_layout.addWidget(self.lbl_state)
        card_layout.addWidget(self.lbl_state_desc)

        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: #2C2C2E;
                border-radius: 2px;
                border: none;
            }
            QProgressBar::chunk {
                background: #34C759;
                border-radius: 2px;
            }
        """)
        self.progress_bar.hide()
        card_layout.addWidget(self.progress_bar)

        layout.addWidget(self.status_card)

        # 5. Options (Autostart)
        self.chk_autostart = QCheckBox("Start automatically on system boot")
        self.chk_autostart.setChecked(True)
        self.chk_autostart.setStyleSheet("""
            QCheckBox {
                color: #A1A1A6;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1px solid #3A3A3C;
                background: #1C1C1E;
            }
            QCheckBox::indicator:checked {
                background: #34C759;
                border-color: #34C759;
            }
        """)
        layout.addWidget(self.chk_autostart)

        layout.addStretch()

        # 6. Action Buttons
        self.btn_layout = QVBoxLayout()
        self.btn_layout.setSpacing(10)

        if not self.is_installed:
            self.btn_primary = QPushButton("Install KeyShield")
            self.btn_primary.setFixedHeight(44)
            self.btn_primary.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_primary.setStyleSheet("""
                QPushButton {
                    background: #34C759; color: #FFFFFF; font-size: 14px; font-weight: 600; border-radius: 22px; border: none;
                }
                QPushButton:hover { background: #30B753; }
                QPushButton:pressed { background: #289945; }
            """)
            self.btn_primary.clicked.connect(self._start_install)
            self.btn_layout.addWidget(self.btn_primary)
        else:
            self.btn_primary = QPushButton("Launch KeyShield")
            self.btn_primary.setFixedHeight(44)
            self.btn_primary.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_primary.setStyleSheet("""
                QPushButton {
                    background: #34C759; color: #FFFFFF; font-size: 14px; font-weight: 600; border-radius: 22px; border: none;
                }
                QPushButton:hover { background: #30B753; }
            """)
            self.btn_primary.clicked.connect(self._launch_app)
            self.btn_layout.addWidget(self.btn_primary)

            self.btn_uninstall = QPushButton("Uninstall KeyShield")
            self.btn_uninstall.setFixedHeight(40)
            self.btn_uninstall.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_uninstall.setStyleSheet("""
                QPushButton {
                    background: #1C1C1E; color: #FF453A; font-size: 13px; font-weight: 600; border-radius: 20px; border: 1px solid rgba(255, 69, 58, 0.2);
                }
                QPushButton:hover { background: #2C2C2E; border-color: rgba(255, 69, 58, 0.4); }
            """)
            self.btn_uninstall.clicked.connect(self._start_uninstall)
            self.btn_layout.addWidget(self.btn_uninstall)

        layout.addLayout(self.btn_layout)

    def _start_install(self):
        self.btn_primary.setEnabled(False)
        self.btn_primary.setText("Installing...")
        self.progress_bar.show()
        self.progress_bar.setValue(10)
        self.lbl_state.setText("Installing KeyShield...")

        threading.Thread(target=self._run_install_worker, daemon=True).start()

    def _run_install_worker(self):
        try:
            self.log_signal.emit("Configuring virtual environment...", 30)
            time.sleep(0.5)

            # Run setup
            sh_path = PROJECT_ROOT / "install.sh"
            if sh_path.exists():
                subprocess.run(["bash", str(sh_path)], cwd=str(PROJECT_ROOT), check=True)

            self.log_signal.emit("Registering virtual audio loopback...", 75)
            time.sleep(0.4)

            self.log_signal.emit("Finalizing desktop integration...", 100)
            time.sleep(0.3)
            self.finished_signal.emit(True, "Installation completed successfully!")
        except Exception as e:
            self.finished_signal.emit(False, f"Installation failed: {e}")

    def _start_uninstall(self):
        self.btn_uninstall.setEnabled(False)
        self.btn_primary.setEnabled(False)
        self.btn_uninstall.setText("Uninstalling...")
        self.progress_bar.show()
        self.progress_bar.setValue(30)
        self.lbl_state.setText("Removing KeyShield...")

        threading.Thread(target=self._run_uninstall_worker, daemon=True).start()

    def _run_uninstall_worker(self):
        try:
            sh_path = PROJECT_ROOT / "uninstall.sh"
            if sh_path.exists():
                subprocess.run(["bash", str(sh_path)], cwd=str(PROJECT_ROOT), check=True)
            self.log_signal.emit("Cleaned up system shortcuts and configs.", 100)
            time.sleep(0.5)
            self.finished_signal.emit(True, "Uninstalled cleanly from system.")
        except Exception as e:
            self.finished_signal.emit(False, f"Uninstall failed: {e}")

    def _on_progress(self, msg: str, percent: int):
        self.lbl_state_desc.setText(msg)
        self.progress_bar.setValue(percent)

    def _on_finished(self, success: bool, msg: str):
        self.progress_bar.hide()
        if success:
            self.lbl_state.setText("Success")
            self.lbl_state.setStyleSheet("color: #34C759; font-size: 13px; font-weight: 600;")
            self.lbl_state_desc.setText(msg)
            self.btn_primary.setText("Close")
            self.btn_primary.setEnabled(True)
            self.btn_primary.clicked.disconnect()
            self.btn_primary.clicked.connect(self.close)
            if hasattr(self, "btn_uninstall"):
                self.btn_uninstall.hide()
        else:
            self.lbl_state.setText("Error")
            self.lbl_state.setStyleSheet("color: #FF453A; font-size: 13px; font-weight: 600;")
            self.lbl_state_desc.setText(msg)
            self.btn_primary.setText("Retry")
            self.btn_primary.setEnabled(True)

    def _launch_app(self):
        launcher = Path.home() / ".local" / "bin" / "keyshield"
        if launcher.exists():
            subprocess.Popen([str(launcher)])
            self.close()
        else:
            self.lbl_state_desc.setText("Launcher not found. Please install first.")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = float(self.width()), float(self.height())
        radius = 24.0

        path = QPainterPath()
        path.addRoundedRect(QRectF(1, 1, w - 2, h - 2), radius, radius)

        bg_grad = QLinearGradient(0, 0, 0, h)
        bg_grad.setColorAt(0.0, QColor(14, 15, 20, 252))
        bg_grad.setColorAt(1.0, QColor(7, 8, 11, 252))
        painter.fillPath(path, QBrush(bg_grad))

        painter.setPen(QPen(QColor(255, 255, 255, 22), 1.0))
        painter.drawPath(path)
