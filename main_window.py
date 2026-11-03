import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QLabel, QPushButton,
    QFrame, QComboBox, QDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QIcon, QFont
from typing import Optional
from localization import LocalizationManager
from theme_manager import ThemeManager
from game_data import Game, get_all_games
from game_scanner import GameScannerThread, GameLauncherThread


class GameCard(QFrame):
    """Game display card."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.game: Optional[Game] = None
        self.setup_ui()

    def setup_ui(self):
        """Setup card UI."""
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(40, 40, 40, 230);
                border-radius: 24px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)
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

        # Game title
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: 800;
                color: white;
                background-color: rgba(255, 255, 255, 0.05);
                padding: 15px 30px;
                border-radius: 16px;
            }
        """)
        layout.addWidget(self.title_label, 0, Qt.AlignmentFlag.AlignCenter)

        # Game info
        info_layout = QHBoxLayout()
        info_layout.setSpacing(30)

        self.size_label = QLabel()
        self.size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.size_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: rgba(255, 255, 255, 200);
                background-color: rgba(255, 255, 255, 0.1);
                padding: 10px 20px;
                border-radius: 12px;
            }
        """)
        info_layout.addWidget(self.size_label, 1)

        self.version_label = QLabel()
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version_label.setStyleSheet("""
            QLabel {
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

        # Update status
        self.update_status_label = QLabel()
        self.update_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 700;
                color: rgba(52, 199, 89, 255);
                background-color: rgba(52, 199, 89, 0.2);
                padding: 8px 24px;
                border-radius: 12px;
            }
        """)
        layout.addWidget(self.update_status_label, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(25)

        # Play button
        self.play_button = QPushButton()
        self.play_button.setMinimumHeight(80)
        self.play_button.setMinimumWidth(280)
        self.play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.play_button.setStyleSheet("""
            QPushButton {
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
            QPushButton:hover {
                background-color: rgba(52, 199, 89, 255);
            }
            QPushButton:pressed {
                background-color: rgba(52, 199, 89, 220);
            }
        """)
        layout.addWidget(self.play_button, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(15)

        # Update button
        self.update_button = QPushButton()
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

        # Play button
        play_text = loc_manager.get("play")
        self.play_button.setText(f"▶ {play_text} ▶")


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

        self.setup_ui()
        self.scan_games()

    def setup_ui(self):
        """Setup main window UI."""
        self.setWindowTitle(self.loc_manager.get("app_title"))
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # Central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.setCentralWidget(central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Top bar
        top_bar = QFrame()
        top_bar.setFixedHeight(70)
        top_bar.setStyleSheet("background-color: rgba(30, 30, 30, 240); border-bottom: 2px solid rgba(255, 255, 255, 0.1);")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)

        title = QLabel(self.loc_manager.get("app_title"))
        title.setStyleSheet("font-size: 22px; font-weight: 800; color: white;")
        top_layout.addWidget(title)
        top_layout.addStretch()

        lang_label = QLabel(f"{self.loc_manager.get('language')}:")
        lang_label.setStyleSheet("color: white; font-size: 15px; font-weight: 600;")
        top_layout.addWidget(lang_label)

        self.lang_combo = QComboBox()
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
        """)
        for code, name in self.loc_manager.get_available_languages().items():
            self.lang_combo.addItem(name, code)
        self.lang_combo.setCurrentIndex(
            list(self.loc_manager.get_available_languages().keys()).index(self.loc_manager.current_language)
        )
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        top_layout.addWidget(self.lang_combo)

        settings_btn = QPushButton("⚙ Настройки")
        settings_btn.setFixedSize(120, 40)
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 122, 255, 200);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: rgba(0, 122, 255, 240);
            }
        """)
        settings_btn.clicked.connect(self.open_settings)
        top_layout.addWidget(settings_btn)

        main_layout.addWidget(top_bar)

        # Content area (horizontal)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(content_layout, 1)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(300)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: rgba(20, 20, 20, 250);
                border: none;
                border-right: 2px solid rgba(255, 255, 255, 0.1);
                padding: 15px;
            }
            QListWidget::item {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                padding: 15px 20px;
                margin: 8px 0px;
                color: white;
                font-size: 16px;
                font-weight: 600;
            }
            QListWidget::item:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
            QListWidget::item:selected {
                background-color: rgba(0, 122, 255, 0.4);
                border: 2px solid rgba(0, 122, 255, 0.6);
            }
        """)
        self.sidebar.itemClicked.connect(self.on_game_selected)
        content_layout.addWidget(self.sidebar)

        # Game card area
        game_area = QWidget()
        game_area.setStyleSheet("background-color: rgba(30, 30, 30, 240);")
        game_layout = QVBoxLayout(game_area)
        game_layout.setContentsMargins(30, 30, 30, 30)
        game_layout.setSpacing(20)

        self.game_card = GameCard()
        self.game_card.setMinimumSize(500, 600)
        self.game_card.play_button.clicked.connect(self.launch_game)
        self.game_card.update_button.clicked.connect(self.update_game)

        game_layout.addWidget(self.game_card)
        game_layout.addStretch()

        content_layout.addWidget(game_area, 1)

    def scan_games(self):
        """Start game scanning."""
        self.scanner_thread = GameScannerThread()
        self.scanner_thread.games_found.connect(self.on_games_found)
        self.scanner_thread.scan_complete.connect(self.on_scan_complete)
        self.scanner_thread.start()

    def on_games_found(self, games: list[Game]):
        """Handle games found."""
        self.games = games
        self.sidebar.clear()

        for game in games:
            item = QListWidgetItem(game.title)
            item.setData(Qt.ItemDataRole.UserRole, game)
            self.sidebar.addItem(item)

        if games:
            self.sidebar.setCurrentRow(0)
            self.on_game_selected(self.sidebar.item(0))

    def on_scan_complete(self):
        print("Game scan complete")

    def on_game_selected(self, item: QListWidgetItem):
        """Handle game selection."""
        game = item.data(Qt.ItemDataRole.UserRole)
        if game:
            self.current_game = game
            self.game_card.set_game(game, self.loc_manager)

    def on_language_changed(self, index: int):
        """Handle language change."""
        lang_code = self.lang_combo.itemData(index)
        self.loc_manager.set_language(lang_code)
        self.setWindowTitle(self.loc_manager.get("app_title"))
        if self.current_game:
            self.game_card.set_game(self.current_game, self.loc_manager)

    def launch_game(self):
        """Launch game."""
        if not self.current_game:
            return
        print(f"Launching {self.current_game.title}...")

    def update_game(self):
        """Update game."""
        if self.current_game:
            print(f"Updating {self.current_game.title}...")

    def open_settings(self):
        """Open settings."""
        dialog = QDialog(self)
        dialog.setWindowTitle(self.loc_manager.get("settings"))
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet("""
            QDialog {
                background-color: rgba(45, 45, 45, 230);
                border-radius: 16px;
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
            }
        """)
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel(self.loc_manager.get("settings"))
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: white;")
        layout.addWidget(title)

        info = QLabel("Settings will be implemented in future updates.")
        info.setWordWrap(True)
        layout.addWidget(info)

        layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignCenter)

        dialog.exec()

    def closeEvent(self, event):
        if self.scanner_thread and self.scanner_thread.isRunning():
            self.scanner_thread.stop()
        event.accept()
