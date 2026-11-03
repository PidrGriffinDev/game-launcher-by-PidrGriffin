import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QLabel, QPushButton,
    QFrame, QScrollArea, QComboBox, QGraphicsOpacityEffect,
    QGraphicsBlurEffect, QDialog
)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, pyqtProperty, QTimer, QPoint
from PyQt6.QtGui import QColor, QPainter, QBrush, QIcon, QFont, QLinearGradient
from typing import Optional
from localization import LocalizationManager
from theme_manager import ThemeManager
from game_data import Game, get_all_games
from game_scanner import GameScannerThread, GameLauncherThread


class GlassCard(QFrame):
    """Glass morphism card widget with blur effect."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(60, 60, 60, 120);
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
        """)


class AnimatedWidget(QWidget):
    """Widget with opacity animation support."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity = 1.0
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(self._opacity)

    def set_opacity(self, opacity: float):
        """Set widget opacity."""
        self._opacity = opacity
        self.opacity_effect.setOpacity(opacity)

    def get_opacity(self) -> float:
        """Get widget opacity."""
        return self._opacity

    opacity = pyqtProperty(float, get_opacity, set_opacity)

    def fade_in(self, duration: int = 300):
        """Fade in animation."""
        animation = QPropertyAnimation(self, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        animation.start()

    def fade_out(self, duration: int = 300):
        """Fade out animation."""
        animation = QPropertyAnimation(self, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        animation.start()


class GameCard(AnimatedWidget):
    """Game display card with glassmorphism."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.game: Optional[Game] = None
        self.setup_ui()

    def setup_ui(self):
        """Setup card UI."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Game icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(140, 140)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 0.08);
                border-radius: 24px;
                border: 2px solid rgba(255, 255, 255, 0.15);
            }
        """)
        layout.addWidget(self.icon_label, 0, Qt.AlignmentFlag.AlignCenter)

        # Spacer
        layout.addSpacing(15)

        # Game title
        self.title_label = QLabel()
        self.title_label.setObjectName("gameTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("""
            QLabel#gameTitle {
                font-size: 36px;
                font-weight: 800;
                color: white;
                background-color: rgba(255, 255, 255, 0.05);
                padding: 15px 30px;
                border-radius: 16px;
            }
        """)
        layout.addWidget(self.title_label, 0, Qt.AlignmentFlag.AlignCenter)

        # Spacer
        layout.addSpacing(10)

        # Game info container (size + version)
        info_layout = QHBoxLayout()
        info_layout.setSpacing(30)

        # Game size
        self.size_label = QLabel()
        self.size_label.setObjectName("gameSize")
        self.size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.size_label.setStyleSheet("""
            QLabel#gameSize {
                font-size: 18px;
                font-weight: 600;
                color: rgba(255, 255, 255, 200);
                background-color: rgba(255, 255, 255, 0.1);
                padding: 10px 20px;
                border-radius: 12px;
            }
        """)
        info_layout.addWidget(self.size_label, 1)

        # Game version
        self.version_label = QLabel()
        self.version_label.setObjectName("gameVersion")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setStyleSheet("""
            QLabel#gameVersion {
                font-size: 18px;
                font-weight: 600;
                color: rgba(255, 255, 255, 200);
                background-color: rgba(255, 255, 255, 0.1);
                padding: 10px 20px;
                border-radius: 12px;
            }
        """)
        info_layout.addWidget(self.version_label, 1)

        layout.addLayout(info_layout, 0)

        # Spacer
        layout.addSpacing(10)

        # Update status
        self.update_status_label = QLabel()
        self.update_status_label.setObjectName("updateStatus")
        self.update_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_status_label.setStyleSheet("""
            QLabel#updateStatus {
                font-size: 16px;
                font-weight: 700;
                color: rgba(52, 199, 89, 255);
                background-color: rgba(52, 199, 89, 0.2);
                padding: 8px 24px;
                border-radius: 12px;
            }
        """)
        layout.addWidget(self.update_status_label, 0, Qt.AlignmentFlag.AlignCenter)

        # Spacer
        layout.addSpacing(25)

        # Play button
        self.play_button = QPushButton()
        self.play_button.setObjectName("playButton")
        self.play_button.setMinimumHeight(80)
        self.play_button.setMinimumWidth(280)
        self.play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_button.setStyleSheet("""
            QPushButton#playButton {
                background-color: rgba(52, 199, 89, 240);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 20px 60px;
                font-size: 24px;
                font-weight: 800;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            QPushButton#playButton:hover {
                background-color: rgba(52, 199, 89, 255);
            }
            QPushButton#playButton:pressed {
                background-color: rgba(52, 199, 89, 220);
            }
        """)
        layout.addWidget(self.play_button, 0, Qt.AlignmentFlag.AlignCenter)

        # Spacer
        layout.addSpacing(15)

        # Update button
        self.update_button = QPushButton()
        self.update_button.setObjectName("updateButton")
        self.update_button.setMinimumHeight(45)
        self.update_button.setMinimumWidth(220)
        self.update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_button.hide()
        layout.addWidget(self.update_button, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)

    def set_game(self, game: Game, loc_manager: LocalizationManager):
        """Update card with game info."""
        self.game = game

        # Update icon
        icon = game.get_icon()
        if not icon.isNull():
            self.icon_label.setPixmap(icon.pixmap(120, 120, QIcon.Mode.Normal, QIcon.State.Off))

        # Update text
        self.title_label.setText(game.title)
        self.size_label.setText(f"{loc_manager.get('game_size')}: {game.get_display_size()}")
        self.version_label.setText(f"{loc_manager.get('game_version')}: {game.get_display_version()}")

        # Update status
        if game.update_required:
            self.update_status_label.setText(loc_manager.get("update"))
            self.update_button.setText(loc_manager.get("update"))
            self.update_button.show()
        else:
            self.update_status_label.setText(loc_manager.get("up_to_date"))
            self.update_button.hide()

        # Play button - make it very clear
        play_text = loc_manager.get("play")
        self.play_button.setText(f"▶ {play_text} ▶")
        self.play_button.setStyleSheet(f"""
            QPushButton#playButton {{
                background-color: rgba(52, 199, 89, 240);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 20px 60px;
                font-size: 24px;
                font-weight: 800;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}
            QPushButton#playButton:hover {{
                background-color: rgba(52, 199, 89, 255);
            }}
            QPushButton#playButton:pressed {{
                background-color: rgba(52, 199, 89, 220);
            }}
        """)

        # Trigger fade-in animation
        self.fade_in(300)


class MainWindow(QMainWindow):
    """Main launcher window."""

    def __init__(self):
        super().__init__()
        self.current_game: Optional[Game] = None
        self.games: list[Game] = []

        # Initialize managers
        self.loc_manager = LocalizationManager()
        self.theme_manager = ThemeManager()

        # Background scanner thread
        self.scanner_thread: Optional[GameScannerThread] = None
        self.launcher_thread: Optional[GameLauncherThread] = None

        # Background color for animation
        self.bg_color = QColor(30, 30, 30)
        self.target_bg_color = QColor(30, 30, 30)

        # Window dragging
        self.drag_position = None

        self.setup_ui()
        self.load_stylesheet()
        self.update_window_style()

        # Start game scanning
        self.scan_games()

        # Start background color animation timer
        self.anim_timer = QTimer()
        self.anim_timer.timeout.connect(self.animate_background)
        self.anim_timer.start(16)  # ~60 FPS

    def setup_ui(self):
        """Setup main window UI."""
        self.setWindowTitle(self.loc_manager.get("app_title"))
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Top bar with settings
        self.setup_top_bar(main_layout)

        # Content area (horizontal for sidebar + game card)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(content_layout, 1)

        # Sidebar
        self.setup_sidebar(content_layout)

        # Game card area
        self.setup_content_area(content_layout)

    def setup_sidebar(self, parent_layout):
        """Setup sidebar with game list."""
        sidebar = QListWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("""
            QListWidget#sidebar {
                background-color: rgba(20, 20, 20, 250);
                border: none;
                border-right: 2px solid rgba(255, 255, 255, 0.1);
                padding: 15px;
            }
            QListWidget#sidebar::item {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                padding: 15px 20px;
                margin: 8px 0px;
                color: white;
                font-size: 16px;
                font-weight: 600;
            }
            QListWidget#sidebar::item:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
            QListWidget#sidebar::item:selected {
                background-color: rgba(0, 122, 255, 0.4);
                border: 2px solid rgba(0, 122, 255, 0.6);
            }
        """)
        sidebar.itemClicked.connect(self.on_game_selected)

        parent_layout.addWidget(sidebar)
        self.sidebar = sidebar

    def setup_content_area(self, parent_layout):
        """Setup main content area."""
        # Container widget for right side
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: rgba(30, 30, 30, 240);")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Game card
        self.game_card = GameCard()
        self.game_card.setObjectName("gameCard")
        self.game_card.setMinimumSize(500, 600)
        self.game_card.setStyleSheet("""
            QFrame#gameCard {
                background-color: rgba(40, 40, 40, 230);
                border-radius: 24px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """)
        self.game_card.play_button.clicked.connect(self.launch_game)
        self.game_card.update_button.clicked.connect(self.update_game)

        content_layout.addWidget(self.game_card)
        content_layout.addStretch()

        parent_layout.addWidget(content_widget, 1)

    def setup_top_bar(self, parent_layout):
        """Setup top bar with language switcher."""
        top_bar = QFrame()
        top_bar.setFixedHeight(70)
        top_bar.setObjectName("topBar")
        top_bar.setStyleSheet("""
            QFrame#topBar {
                background-color: rgba(30, 30, 30, 240);
                border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            }
        """)

        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(20, 0, 20, 0)

        # Title
        title_label = QLabel(self.loc_manager.get("app_title"))
        title_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: 800;
                color: white;
            }
        """)
        layout.addWidget(title_label)

        layout.addStretch()

        # Language switcher
        lang_label = QLabel(f"{self.loc_manager.get('language')}:")
        lang_label.setStyleSheet("color: white; font-size: 15px; font-weight: 600;")
        layout.addWidget(lang_label)

        self.lang_combo = QComboBox()
        self.lang_combo.setObjectName("languageCombo")
        self.lang_combo.setMinimumWidth(150)
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                padding: 10px 15px;
                color: white;
                font-size: 14px;
                font-weight: 600;
            }
            QComboBox:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        for code, name in self.loc_manager.get_available_languages().items():
            self.lang_combo.addItem(name, code)
        self.lang_combo.setCurrentIndex(
            list(self.loc_manager.get_available_languages().keys()).index(self.loc_manager.current_language)
        )
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        layout.addWidget(self.lang_combo)

        # Settings button
        settings_button = QPushButton()
        settings_button.setObjectName("settingsButton")
        settings_button.setText("⚙ Настройки")
        settings_button.setFixedSize(120, 40)
        settings_button.setStyleSheet("""
            QPushButton#settingsButton {
                background-color: rgba(0, 122, 255, 200);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton#settingsButton:hover {
                background-color: rgba(0, 122, 255, 240);
            }
        """)
        settings_button.clicked.connect(self.open_settings)
        layout.addWidget(settings_button)

        # Add top bar to existing layout
        main_layout = self.centralWidget().layout()
        main_layout.insertWidget(0, top_bar)

    def load_stylesheet(self):
        """Load glassmorphism stylesheet."""
        style_path = os.path.join("styles", "glassmorphism.qss")
        if os.path.exists(style_path):
            with open(style_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())

    def update_window_style(self):
        """Update window background color."""
        theme = self.theme_manager.get_current_theme()
        self.target_bg_color = theme["background"]

    def animate_background(self):
        """Animate background color transition."""
        # Smoothly interpolate current color to target color
        r = self.bg_color.red() + (self.target_bg_color.red() - self.bg_color.red()) * 0.05
        g = self.bg_color.green() + (self.target_bg_color.green() - self.bg_color.green()) * 0.05
        b = self.bg_color.blue() + (self.target_bg_color.blue() - self.bg_color.blue()) * 0.05

        self.bg_color = QColor(int(r), int(g), int(b))

        # Update window background
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.bg_color.name()};
            }}
            {self.styleSheet()}
        """)

    def update_theme_colors(self, theme: dict):
        """Update dynamic theme colors."""
        # Update target background color for animation
        self.target_bg_color = theme["background"]

        # Update sidebar color
        self.sidebar.setStyleSheet(f"""
            QListWidget#sidebar {{
                background-color: rgba(20, 20, 20, 250);
                border: none;
                border-right: 2px solid rgba(255, 255, 255, 0.1);
                padding: 15px;
            }}
            QListWidget#sidebar::item {{
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                padding: 15px 20px;
                margin: 8px 0px;
                color: white;
                font-size: 16px;
                font-weight: 600;
            }}
            QListWidget#sidebar::item:hover {{
                background-color: rgba(255, 255, 255, 0.15);
            }}
            QListWidget#sidebar::item:selected {{
                background-color: {theme["accent"].name()};
                border: 2px solid {theme["accent"].name()};
            }}
        """)

        # Update play button color
        self.game_card.play_button.setStyleSheet(f"""
            QPushButton#playButton {{
                background-color: {theme["play_button"].name()};
                color: white;
                border: none;
                border-radius: 16px;
                padding: 16px 48px;
                font-size: 18px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            QPushButton#playButton:hover {{
                background-color: {theme["play_button_hover"].name()};
            }}
            QPushButton#playButton:pressed {{
                background-color: {theme["play_button"].name()};
            }}
            QPushButton#playButton:disabled {{
                background-color: rgba(128, 128, 128, 150);
                color: rgba(255, 255, 255, 150);
            }}
        """)

        # Update game card glassmorphism effect
        self.game_card.setStyleSheet(f"""
            QFrame#gameCard {{
                background-color: transparent;
                border-radius: 24px;
                border: none;
            }}
        """)

        # Update glass container
        self.glass_container.setStyleSheet(f"""
            QFrame#glassContainer {{
                background-color: rgba(40, 40, 40, 230);
                border-radius: 24px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }}
        """)

        # Update text colors
        self.game_card.title_label.setStyleSheet(f"""
            QLabel#gameTitle {{
                font-size: 32px;
                font-weight: 700;
                color: {theme["text"].name()};
            }}
        """)

        self.game_card.size_label.setStyleSheet(f"""
            QLabel#gameSize {{
                font-size: 15px;
                font-weight: 500;
                color: {theme["text_secondary"].name()};
            }}
        """)

        self.game_card.version_label.setStyleSheet(f"""
            QLabel#gameVersion {{
                font-size: 15px;
                font-weight: 500;
                color: {theme["text_secondary"].name()};
            }}
        """)

    def scan_games(self):
        """Start game scanning in background."""
        self.scanner_thread = GameScannerThread()
        self.scanner_thread.games_found.connect(self.on_games_found)
        self.scanner_thread.scan_complete.connect(self.on_scan_complete)
        self.scanner_thread.start()

    def on_games_found(self, games: list[Game]):
        """Handle games found from scanner."""
        self.games = games
        self.sidebar.clear()

        for game in games:
            item = QListWidgetItem(game.title)
            item.setData(Qt.ItemDataRole.UserRole, game)
            self.sidebar.addItem(item)

        # Select first game if available
        if games:
            self.sidebar.setCurrentRow(0)
            self.on_game_selected(self.sidebar.item(0))
        else:
            # Show empty state
            self.game_card.title_label.setText("No games found")
            self.game_card.size_label.setText("")
            self.game_card.version_label.setText("")
            self.game_card.update_status_label.setText("")
            self.game_card.play_button.hide()
            self.game_card.update_button.hide()

    def on_scan_complete(self):
        """Handle scan completion."""
        print("Game scan complete")

    def on_game_selected(self, item: QListWidgetItem):
        """Handle game selection from sidebar."""
        game = item.data(Qt.ItemDataRole.UserRole)
        print(f"Game selected: {game.title if game else 'None'}")
        if game:
            self.current_game = game

            # Change theme based on game
            theme = self.theme_manager.set_theme(game.theme)
            self.update_theme_colors(theme)

            # Update game card
            self.game_card.set_game(game, self.loc_manager)
            self.game_card.show()
            self.game_card.play_button.show()
        else:
            print("No game data found")

    def on_language_changed(self, index: int):
        """Handle language change."""
        lang_code = self.lang_combo.itemData(index)
        print(f"Language changed to: {lang_code}")
        self.loc_manager.set_language(lang_code)

        # Update UI text
        self.setWindowTitle(self.loc_manager.get("app_title"))
        if self.current_game:
            self.game_card.set_game(self.current_game, self.loc_manager)

    def launch_game(self):
        """Launch the selected game."""
        if not self.current_game:
            return

        self.launcher_thread = GameLauncherThread(self.current_game)
        self.launcher_thread.launch_started.connect(self.on_launch_started)
        self.launcher_thread.launch_success.connect(self.on_launch_success)
        self.launcher_thread.launch_failed.connect(self.on_launch_failed)
        self.launcher_thread.start()

    def on_launch_started(self, game_title: str):
        """Handle launch start."""
        self.game_card.play_button.setText(self.loc_manager.get("launching"))
        self.game_card.play_button.setEnabled(False)

    def on_launch_success(self, game_title: str):
        """Handle successful launch."""
        self.game_card.play_button.setText(self.loc_manager.get("play"))
        self.game_card.play_button.setEnabled(True)
        print(f"Successfully launched: {game_title}")

    def on_launch_failed(self, game_title: str, error: str):
        """Handle launch failure."""
        self.game_card.play_button.setText(self.loc_manager.get("play"))
        self.game_card.play_button.setEnabled(True)
        print(f"Failed to launch {game_title}: {error}")

    def update_game(self):
        """Handle game update."""
        if self.current_game:
            print(f"Updating {self.current_game.title}...")
            # Implement update logic here

    def open_settings(self):
        """Open settings dialog."""
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle(self.loc_manager.get("settings"))
        settings_dialog.setFixedSize(400, 300)
        settings_dialog.setStyleSheet("""
            QDialog {
                background-color: rgba(45, 45, 45, 230);
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: rgba(0, 122, 255, 200);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(0, 122, 255, 240);
            }
        """)

        layout = QVBoxLayout(settings_dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Settings title
        title = QLabel(self.loc_manager.get("settings"))
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: white;")
        layout.addWidget(title)

        # Placeholder settings options
        info_label = QLabel("Settings will be implemented in future updates.")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        layout.addStretch()

        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(settings_dialog.accept)
        layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignCenter)

        settings_dialog.exec()

    def closeEvent(self, event):
        """Handle window close event."""
        if self.scanner_thread and self.scanner_thread.isRunning():
            self.scanner_thread.stop()
        if self.launcher_thread and self.launcher_thread.isRunning():
            self.launcher_thread.quit()
            self.launcher_thread.wait()
        event.accept()
