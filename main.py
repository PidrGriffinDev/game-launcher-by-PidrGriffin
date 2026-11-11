import sys
import os
import subprocess
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QMessageBox, QFileDialog, QDialog,
    QComboBox, QRadioButton, QButtonGroup, QScrollArea, QFrame,
    QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QColor, QLinearGradient, QPainter, QPainter


class Localization:
    """Localization system for multi-language support."""

    def __init__(self):
        self.current_language = "Russian"
        self.translations = {
            "English": {
                "play": "PLAY",
                "update": "UPDATE",
                "up_to_date": "Up to Date",
                "size": "Size",
                "version": "Version",
                "launching": "LAUNCHING...",
                "settings": "Settings",
                "language": "Language",
                "window_mode": "Window Mode",
                "window": "Window",
                "fullscreen": "Fullscreen",
                "save_close": "Save & Close",
                "settings_saved": "Settings saved!",
                "title": "PetterGriffinDev Launcher"
            },
            "Russian": {
                "play": "ИГРАТЬ",
                "update": "ОБНОВИТЬ",
                "up_to_date": "Актуально",
                "size": "Размер",
                "version": "Версия",
                "launching": "ЗАПУСК...",
                "settings": "Настройки",
                "language": "Язык",
                "window_mode": "Режим окна",
                "window": "Оконный",
                "fullscreen": "Полный экран",
                "save_close": "Сохранить и закрыть",
                "settings_saved": "Настройки сохранены!",
                "title": "PetterGriffinDev Launcher"
            },
            "Spanish": {
                "play": "JUGAR",
                "update": "ACTUALIZAR",
                "up_to_date": "Actualizado",
                "size": "Tamaño",
                "version": "Versión",
                "launching": "INICIANDO...",
                "settings": "Configuración",
                "language": "Idioma",
                "window_mode": "Modo de ventana",
                "window": "Ventana",
                "fullscreen": "Pantalla completa",
                "save_close": "Guardar y cerrar",
                "settings_saved": "¡Configuración guardada!",
                "title": "PetterGriffinDev Launcher"
            }
        }

    def get(self, key):
        return self.translations[self.current_language].get(key, key)

    def set_language(self, language):
        self.current_language = language


class AnimatedButton(QPushButton):
    """Button with simple hover scale animation."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._scale = 1.0

    def enterEvent(self, event):
        """Smooth scale up on hover."""
        self._animate_scale(1.05, 200)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Smooth scale down on leave."""
        self._animate_scale(1.0, 200)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Smooth scale down on press."""
        self._animate_scale(0.95, 100)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Smooth scale up on release."""
        if self.underMouse():
            self._animate_scale(1.05, 200)
        else:
            self._animate_scale(1.0, 200)
        super().mouseReleaseEvent(event)

    def _animate_scale(self, target_scale, duration):
        """Animate scale."""
        self.anim = QPropertyAnimation(self, b"scale")
        self.anim.setDuration(duration)
        self.anim.setStartValue(self._scale)
        self.anim.setEndValue(target_scale)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()

    def scale(self):
        return self._scale

    def setScale(self, value):
        self._scale = value
        self.update()

    scale = pyqtProperty(float, scale, setScale)

    def paintEvent(self, event):
        """Override paint to apply scale transformation."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(self._scale, self._scale)
        painter.translate(-self.width() / 2, -self.height() / 2)
        super().paintEvent(event)


class SettingsDialog(QDialog):
    """Settings dialog with window mode and language options."""

    def __init__(self, parent=None, current_language="English", current_mode="Window"):
        super().__init__(parent)
        self.current_language = current_language
        self.current_mode = current_mode
        self.setup_ui()

    def setup_ui(self):
        """Setup settings UI with VITE GLASS style."""
        self.setWindowTitle("Настройки")
        self.setFixedSize(500, 400)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(20, 20, 20, 240),
                    stop:1 rgba(40, 40, 40, 240));
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(100, 100, 255, 200),
                    stop:1 rgba(150, 100, 255, 200));
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(100, 100, 255, 240),
                    stop:1 rgba(150, 100, 255, 240));
            }
            QRadioButton {
                color: white;
                font-size: 14px;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                background: rgba(255, 255, 255, 0.05);
            }
            QRadioButton::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(100, 100, 255, 200),
                    stop:1 rgba(150, 100, 255, 200));
                border: 2px solid rgba(150, 150, 255, 255);
            }
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 8px 12px;
                color: white;
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("⚙ Настройки")
        title.setStyleSheet("font-size: 24px; font-weight: 800; color: white;")
        layout.addWidget(title)

        # Window Mode Section
        mode_label = QLabel("Режим окна:")
        mode_label.setStyleSheet("font-size: 16px; font-weight: 700; color: rgba(255,255,255,200);")
        layout.addWidget(mode_label)

        mode_group = QButtonGroup(self)

        self.window_radio = QRadioButton("Оконный режим")
        self.window_radio.setChecked(self.current_mode == "Window")
        mode_group.addButton(self.window_radio, 1)
        layout.addWidget(self.window_radio)

        self.fullscreen_radio = QRadioButton("Полный экран")
        self.fullscreen_radio.setChecked(self.current_mode == "Fullscreen")
        mode_group.addButton(self.fullscreen_radio, 2)
        layout.addWidget(self.fullscreen_radio)

        # Language Section
        lang_label = QLabel("Язык:")
        lang_label.setStyleSheet("font-size: 16px; font-weight: 700; color: rgba(255,255,255,200);")
        layout.addWidget(lang_label)

        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "Russian", "Spanish"])
        self.lang_combo.setCurrentText(self.current_language)
        layout.addWidget(self.lang_combo)

        layout.addStretch()

        # Close button
        close_btn = QPushButton("Сохранить и закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def get_settings(self):
        """Return selected settings."""
        mode = "Fullscreen" if self.fullscreen_radio.isChecked() else "Window"
        language = self.lang_combo.currentText()
        return {"mode": mode, "language": language}


class GameCard(QFrame):
    """Game display card with VITE GLASS style."""

    def __init__(self, parent=None, localization=None):
        super().__init__(parent)
        self.game_data = None
        self.localization = localization
        self.setup_ui()

    def setup_ui(self):
        """Setup card UI with VITE GLASS design."""
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(40, 40, 50, 220),
                    stop:1 rgba(50, 50, 60, 220));
                border-radius: 28px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # Game icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.08),
                    stop:1 rgba(255, 255, 255, 0.12));
                border-radius: 28px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """)
        layout.addWidget(self.icon_label, 0, Qt.AlignmentFlag.AlignCenter)

        # Game title
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 38px;
                font-weight: 900;
                color: white;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 0.06),
                    stop:1 rgba(255, 255, 255, 0.1));
                padding: 18px 35px;
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        layout.addWidget(self.title_label, 0, Qt.AlignmentFlag.AlignCenter)

        # Game info
        info_layout = QHBoxLayout()
        info_layout.setSpacing(35)

        self.size_label = QLabel()
        self.size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.size_label.setStyleSheet("""
            QLabel {
                font-size: 19px;
                font-weight: 700;
                color: rgba(255, 255, 255, 220);
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.18));
                padding: 12px 25px;
                border-radius: 14px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
        """)
        info_layout.addWidget(self.size_label, 1)

        self.version_label = QLabel()
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setStyleSheet("""
            QLabel {
                font-size: 19px;
                font-weight: 700;
                color: rgba(255, 255, 255, 220);
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.18));
                padding: 12px 25px;
                border-radius: 14px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
        """)
        info_layout.addWidget(self.version_label, 1)

        layout.addLayout(info_layout, 0)

        # Update status
        self.update_status_label = QLabel()
        self.update_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_status_label.setStyleSheet("""
            QLabel {
                font-size: 17px;
                font-weight: 800;
                color: rgba(52, 199, 89, 255);
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(52, 199, 89, 0.25),
                    stop:1 rgba(52, 199, 89, 0.35));
                padding: 10px 28px;
                border-radius: 14px;
                border: 1px solid rgba(52, 199, 89, 0.4);
            }
        """)
        layout.addWidget(self.update_status_label, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(30)

        # Play button with animation
        self.play_button = AnimatedButton()
        self.play_button.setMinimumHeight(85)
        self.play_button.setMinimumWidth(300)
        self.play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(52, 199, 89, 240),
                    stop:1 rgba(32, 199, 89, 240));
                color: white;
                border: none;
                border-radius: 22px;
                padding: 22px 70px;
                font-size: 26px;
                font-weight: 900;
                letter-spacing: 3px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(52, 199, 89, 255),
                    stop:1 rgba(32, 199, 89, 255));
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(52, 199, 89, 220),
                    stop:1 rgba(32, 199, 89, 220));
            }
        """)
        layout.addWidget(self.play_button, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(20)

        # Update button with animation
        self.update_button = AnimatedButton()
        self.update_button.setMinimumHeight(50)
        self.update_button.setMinimumWidth(240)
        self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_button.hide()
        self.update_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 122, 255, 220),
                    stop:1 rgba(0, 122, 255, 220));
                color: white;
                border: none;
                border-radius: 14px;
                padding: 14px 30px;
                font-size: 16px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 122, 255, 250),
                    stop:1 rgba(0, 122, 255, 250));
            }
        """)
        layout.addWidget(self.update_button, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)

    def set_game(self, game_data):
        """Update card with game info."""
        self.game_data = game_data

        # Update icon
        from PyQt6.QtGui import QIcon
        icon = QIcon(game_data.get('icon', ''))
        if not icon.isNull():
            self.icon_label.setPixmap(icon.pixmap(130, 130))

        # Update text with localization
        if self.localization:
            self.title_label.setText(game_data['title'])
            self.size_label.setText(f"{self.localization.get('size')}: {game_data['size']}")
            self.version_label.setText(f"{self.localization.get('version')}: {game_data['version']}")
            self.update_status_label.setText(game_data['status'])

            # Update buttons with localization
            self.play_button.setText(f"▶ {self.localization.get('play')} ▶")
            self.update_button.setText(self.localization.get('update'))
        else:
            self.title_label.setText(game_data['title'])
            self.size_label.setText(f"Размер: {game_data['size']}")
            self.version_label.setText(f"Версия: {game_data['version']}")
            self.update_status_label.setText(game_data['status'])
            self.play_button.setText(f"▶ ИГРАТЬ ▶")
            self.update_button.setText("ОБНОВИТЬ")

        # Show/hide update button
        if game_data['needs_update']:
            self.update_button.show()
        else:
            self.update_button.hide()

    def update_language(self):
        """Update all text when language changes."""
        if self.game_data and self.localization:
            self.set_game(self.game_data)


class ModernLauncher(QMainWindow):
    """Modern launcher with VITE GLASS style."""

    def __init__(self):
        super().__init__()
        self.setMinimumSize(1400, 900)
        self.resize(1600, 1000)

        # Localization
        self.localization = Localization()

        # Settings
        self.window_mode = "Window"

        # Game paths
        self.game_paths = {}
        self.load_config()

        # All games data
        self.games = self.get_all_games()

        self.setup_ui()
        self.apply_theme()

    def get_all_games(self):
        """Return all games with their data."""
        return [
            {
                "title": "WRC 10",
                "size": "45.2 GB",
                "version": "1.2.5",
                "status": "Актуально",
                "needs_update": False,
                "icon": "icons/wrc10.png",
                "theme": "white"
            },
            {
                "title": "WRC 9",
                "size": "42.8 GB",
                "version": "1.1.3",
                "status": "Актуально",
                "needs_update": False,
                "icon": "icons/wrc9.png",
                "theme": "dark"
            },
            {
                "title": "Forza Horizon 6",
                "size": "118.5 GB",
                "version": "2.0.1",
                "status": "ОБНОВИТЬ",
                "needs_update": True,
                "icon": "icons/forza.png",
                "theme": "orange"
            },
            {
                "title": "Dead Island 2",
                "size": "67.3 GB",
                "version": "1.5.0",
                "status": "Актуально",
                "needs_update": False,
                "icon": "icons/dead_island.png",
                "theme": "green"
            },
            {
                "title": "WRC Generations",
                "size": "48.7 GB",
                "version": "1.3.2",
                "status": "Актуально",
                "needs_update": False,
                "icon": "icons/wrc_generations.png",
                "theme": "blue"
            },
            {
                "title": "Teardown",
                "size": "1.2 GB",
                "version": "1.4.0",
                "status": "ОБНОВИТЬ",
                "needs_update": True,
                "icon": "icons/teardown.png",
                "theme": "yellow"
            },
            {
                "title": "Assetto Corsa EVO",
                "size": "55.4 GB",
                "version": "0.9.5",
                "status": "Актуально",
                "needs_update": False,
                "icon": "icons/assetto_corsa.png",
                "theme": "purple"
            },
            {
                "title": "Assetto Corsa Competizione",
                "size": "62.1 GB",
                "version": "1.8.2",
                "status": "Актуально",
                "needs_update": False,
                "icon": "icons/assetto_corsa_comp.png",
                "theme": "red"
            },
            {
                "title": "Project Cars 3",
                "size": "72.5 GB",
                "version": "1.0.5",
                "status": "Актуально",
                "needs_update": False,
                "icon": "icons/project_cars3.png",
                "theme": "cyan"
            },
            {
                "title": "Need For Speed Heat",
                "size": "54.8 GB",
                "version": "2.3.1",
                "status": "Актуально",
                "needs_update": False,
                "icon": "icons/nfs_heat.png",
                "theme": "orange_red"
            },
            {
                "title": "The Last Of Us Part 1 Remastered",
                "size": "79.3 GB",
                "version": "1.0.8",
                "status": "Актуально",
                "needs_update": False,
                "icon": "icons/tlou_remastered.png",
                "theme": "brown"
            },
            {
                "title": "Watch Dogs 2",
                "size": "58.6 GB",
                "version": "1.2.4",
                "status": "Актуально",
                "needs_update": False,
                "icon": "icons/watch_dogs2.png",
                "theme": "teal"
            },
            {
                "title": "Bodycam",
                "size": "8.4 GB",
                "version": "0.5.2",
                "status": "ОБНОВИТЬ",
                "needs_update": True,
                "icon": "icons/bodycam.png",
                "theme": "gray"
            }
        ]

    def setup_ui(self):
        """Setup main UI with VITE GLASS style."""
        self.setWindowTitle(self.localization.get('title'))
        # Central widget
        central = QWidget()
        central.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(15, 15, 20, 255),
                    stop:1 rgba(25, 25, 35, 255));
            }
        """)
        self.setCentralWidget(central)

        # Main vertical layout
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Top bar
        self.setup_top_bar(main_layout)

        # Content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(content_layout, 1)

        # Sidebar
        self.setup_sidebar(content_layout)

        # Game card area
        self.setup_game_area(content_layout)

    def setup_top_bar(self, parent_layout):
        """Setup top bar with VITE GLASS style."""
        top_bar = QFrame()
        top_bar.setFixedHeight(80)
        top_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(20, 20, 30, 240),
                    stop:1 rgba(30, 30, 40, 240));
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            }
        """)

        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(25, 0, 25, 0)

        # Title
        title = QLabel(self.localization.get('title'))
        title.setStyleSheet("font-size: 24px; font-weight: 900; color: white;")
        layout.addWidget(title)
        layout.addStretch()

        # Language combo
        lang_label = QLabel(f"{self.localization.get('language')}:")
        lang_label.setStyleSheet("color: rgba(255,255,255,200); font-size: 15px; font-weight: 700;")
        layout.addWidget(lang_label)

        self.lang_combo = QComboBox()
        self.lang_combo.setMinimumWidth(160)
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 12px;
                padding: 10px 18px;
                color: white;
                font-size: 15px;
                font-weight: 700;
            }
        """)
        self.lang_combo.addItems(["English", "Russian", "Spanish"])
        self.lang_combo.setCurrentText(self.localization.current_language)
        self.lang_combo.currentTextChanged.connect(self.change_language)
        layout.addWidget(self.lang_combo)

        # Settings button
        settings_btn = AnimatedButton()
        settings_btn.setText(f"⚙ {self.localization.get('settings')}")
        settings_btn.setFixedSize(140, 45)
        settings_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(100, 100, 255, 220),
                    stop:1 rgba(150, 100, 255, 220));
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 15px;
                font-weight: 800;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(100, 100, 255, 250),
                    stop:1 rgba(150, 100, 255, 250));
            }
        """)
        settings_btn.clicked.connect(self.open_settings)
        layout.addWidget(settings_btn)

        # Store reference for language updates
        self.top_layout = layout

        parent_layout.addWidget(top_bar)

    def setup_sidebar(self, parent_layout):
        """Setup sidebar with VITE GLASS style."""
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(320)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(18, 18, 25, 250),
                    stop:1 rgba(25, 25, 35, 250));
                border: none;
                border-right: 1px solid rgba(255, 255, 255, 0.08);
                padding: 18px;
            }
            QListWidget::item {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 0.06),
                    stop:1 rgba(255, 255, 255, 0.1));
                border-radius: 14px;
                padding: 18px 22px;
                margin: 10px 0px;
                color: white;
                font-size: 17px;
                font-weight: 700;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }
            QListWidget::item:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.2));
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            QListWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(100, 100, 255, 0.5),
                    stop:1 rgba(150, 100, 255, 0.5));
                border: 2px solid rgba(150, 150, 255, 0.7);
            }
        """)

        for game in self.games:
            item = QListWidgetItem(game['title'])
            item.setData(Qt.ItemDataRole.UserRole, game)
            self.sidebar.addItem(item)

        self.sidebar.itemClicked.connect(self.on_game_selected)
        parent_layout.addWidget(self.sidebar)

    def setup_game_area(self, parent_layout):
        """Setup game card area."""
        game_area = QWidget()
        game_area.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(20, 20, 30, 240),
                    stop:1 rgba(30, 30, 40, 240));
            }
        """)
        game_layout = QVBoxLayout(game_area)
        game_layout.setContentsMargins(35, 35, 35, 35)
        game_layout.setSpacing(25)

        self.game_card = GameCard(localization=self.localization)
        self.game_card.setMinimumSize(600, 700)
        self.game_card.play_button.clicked.connect(self.launch_game)
        self.game_card.update_button.clicked.connect(self.update_game)

        game_layout.addWidget(self.game_card)
        game_layout.addStretch()

        parent_layout.addWidget(game_area, 1)

    def apply_theme(self):
        """Apply VITE GLASS theme."""
        pass  # Theme is applied via stylesheets

    def load_config(self):
        """Load game paths from config."""
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {game: data.get('executable', '') for game, data in config.get('games', {}).items()}
            except Exception as e:
                print(f"Error loading config: {e}")
        return {}

    def save_config(self):
        """Save game paths to config."""
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        try:
            config = {"games": {}}
            for game, path in self.game_paths.items():
                config["games"][game] = {"executable": path, "description": f"Path to {game}"}

            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def on_game_selected(self, item):
        """Handle game selection."""
        game_data = item.data(Qt.ItemDataRole.UserRole)
        if game_data:
            self.game_card.set_game(game_data)

    def change_language(self, language):
        """Change language and update all UI."""
        self.localization.set_language(language)

        # Update window title
        self.setWindowTitle(self.localization.get('title'))

        # Update top bar labels and buttons
        for i in range(self.top_layout.count()):
            item = self.top_layout.itemAt(i)
            if item:
                widget = item.widget()
                if isinstance(widget, QLabel):
                    current_text = widget.text()
                    if ":" in current_text and ("Язык" in current_text or "Language" in current_text or "Idioma" in current_text):
                        widget.setText(f"{self.localization.get('language')}:")
                elif isinstance(widget, QPushButton):
                    widget.setText(f"⚙ {self.localization.get('settings')}")

        # FORCE update game card buttons
        if self.game_card and self.game_card.game_data:
            self.game_card.set_game(self.game_card.game_data)

        print(f"Language changed to: {language}")

    def open_settings(self):
        """Open settings dialog."""
        dialog = SettingsDialog(self, self.localization.current_language, self.window_mode)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            settings = dialog.get_settings()
            self.localization.set_language(settings['language'])
            self.window_mode = settings['mode']

            # Apply window mode
            if self.window_mode == "Fullscreen":
                self.showFullScreen()
            else:
                self.showNormal()

            # Update language combo
            self.lang_combo.setCurrentText(self.localization.current_language)

            # Update all UI text
            self.change_language(self.localization.current_language)

            QMessageBox.information(self, self.localization.get('launch_success'), self.localization.get('settings_saved'))

    def launch_game(self):
        """Launch the selected game."""
        if not self.game_card.game_data:
            return

        game_name = self.game_card.game_data['title']
        executable_path = self.game_paths.get(game_name, "")

        self.game_card.play_button.setText(f"⏳ {self.localization.get('launching')}")
        self.game_card.play_button.setEnabled(False)

        if executable_path and os.path.exists(executable_path):
            try:
                subprocess.Popen([executable_path], shell=True)
                self.game_card.play_button.setText(f"▶ {self.localization.get('play')} ▶")
                self.game_card.play_button.setEnabled(True)
                QMessageBox.information(self, self.localization.get('launch_success'), self.localization.get('launch_success_text').format(game_name))
            except Exception as e:
                self.game_card.play_button.setText(f"▶ {self.localization.get('play')} ▶")
                self.game_card.play_button.setEnabled(True)
                QMessageBox.critical(self, self.localization.get('launch_error'), self.localization.get('launch_error_text').format(e))
        else:
            self.game_card.play_button.setText(f"▶ {self.localization.get('play')} ▶")
            self.game_card.play_button.setEnabled(True)
            self.ask_for_game_path(game_name)

    def ask_for_game_path(self, game_name):
        """Ask user to select game executable."""
        msg = QMessageBox()
        msg.setWindowTitle("Путь не настроен")
        msg.setText(f"Путь к игре '{game_name}' не настроен.\n\nХотите выбрать путь к исполняемому файлу?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setStyleSheet("background-color: rgb(30, 30, 30); color: white;")

        result = msg.exec()

        if result == QMessageBox.StandardButton.Yes:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                f"Выберите исполняемый файл для {game_name}",
                "",
                "Executable files (*.exe)"
            )

            if file_path:
                self.game_paths[game_name] = file_path
                self.save_config()

                success_msg = QMessageBox()
                success_msg.setWindowTitle("Успешно")
                success_msg.setText(f"Путь к '{game_name}' сохранён:\n{file_path}\n\nТеперь можно запустить игру!")
                success_msg.setStyleSheet("background-color: rgb(30, 30, 30); color: white;")
                success_msg.exec()

                self.launch_game()

    def update_game(self):
        """Update game."""
        if self.game_card.game_data:
            QMessageBox.information(self, "Обновление", f"Обновление {self.game_card.game_data['title']}...")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = ModernLauncher()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
