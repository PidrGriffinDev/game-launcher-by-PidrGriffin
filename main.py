import sys
import os
import subprocess
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SimpleLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PetterGriffinDev Launcher")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)

        # Load game paths from config
        self.game_paths = self.load_config()

        # Central widget with dark background
        central = QWidget()
        central.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.setCentralWidget(central)

        # Main horizontal layout
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Left sidebar (game list)
        from PyQt6.QtWidgets import QListWidget, QListWidgetItem
        sidebar = QListWidget()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("""
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

        games = ["WRC 10", "WRC 9", "Forza Horizon 6", "Dead Island 2", "WRC Generations", "Teardown", "Assetto Corsa EVO"]
        for game in games:
            sidebar.addItem(game)

        main_layout.addWidget(sidebar)

        # Right area (game card)
        game_area = QWidget()
        game_area.setStyleSheet("background-color: rgba(30, 30, 30, 240);")
        game_layout = QVBoxLayout(game_area)
        game_layout.setContentsMargins(30, 30, 30, 30)
        game_layout.setSpacing(20)

        # Game card frame
        from PyQt6.QtWidgets import QFrame
        game_card = QFrame()
        game_card.setStyleSheet("""
            QFrame {
                background-color: rgba(40, 40, 40, 230);
                border-radius: 24px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """)
        card_layout = QVBoxLayout(game_card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(20)

        # Game title
        title = QLabel("WRC 10")
        title.setStyleSheet("color: white; font-size: 36px; font-weight: 800; background-color: rgba(255,255,255,0.05); padding: 15px 30px; border-radius: 16px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title, 0, Qt.AlignmentFlag.AlignCenter)

        # Size
        size = QLabel("Размер: 45.2 GB")
        size.setStyleSheet("color: white; font-size: 18px; font-weight: 600; background-color: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 12px;")
        size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(size, 0, Qt.AlignmentFlag.AlignCenter)

        # Version
        version = QLabel("Версия: 1.2.5")
        version.setStyleSheet("color: white; font-size: 18px; font-weight: 600; background-color: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 12px;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(version, 0, Qt.AlignmentFlag.AlignCenter)

        # Status
        status = QLabel("Актуально")
        status.setStyleSheet("color: rgba(52,199,89,255); font-size: 16px; font-weight: 700; background-color: rgba(52,199,89,0.2); padding: 8px 24px; border-radius: 12px;")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(status, 0, Qt.AlignmentFlag.AlignCenter)

        card_layout.addSpacing(30)

        # PLAY BUTTON - THE BIG ONE
        play_btn = QPushButton("▶ ИГРАТЬ ▶")
        play_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(52, 199, 89, 240);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 20px 60px;
                font-size: 24px;
                font-weight: 800;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background-color: rgba(52, 199, 89, 255);
            }
        """)
        play_btn.setMinimumHeight(80)
        play_btn.setMinimumWidth(280)
        play_btn.clicked.connect(self.launch_game)
        card_layout.addWidget(play_btn, 0, Qt.AlignmentFlag.AlignCenter)

        card_layout.addStretch()

        game_layout.addWidget(game_card)
        game_layout.addStretch()

        main_layout.addWidget(game_area, 1)

        # Top bar
        from PyQt6.QtWidgets import QFrame, QComboBox
        top_bar = QFrame()
        top_bar.setFixedHeight(70)
        top_bar.setStyleSheet("background-color: rgba(30, 30, 30, 240); border-bottom: 2px solid rgba(255, 255, 255, 0.1);")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)

        title_label = QLabel("PetterGriffinDev Launcher")
        title_label.setStyleSheet("font-size: 22px; font-weight: 800; color: white;")
        top_layout.addWidget(title_label)
        top_layout.addStretch()

        lang_combo = QComboBox()
        lang_combo.setMinimumWidth(150)
        lang_combo.setStyleSheet("""
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
        lang_combo.addItems(["English", "Russian", "Spanish"])
        top_layout.addWidget(lang_combo)

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
        """)
        top_layout.addWidget(settings_btn)

        # Insert top bar at beginning
        main_layout_parent = central.layout()
        main_layout_parent.insertWidget(0, top_bar)

        # Store references
        self.play_btn = play_btn
        self.sidebar = sidebar
        self.title = title
        self.size = size
        self.version = version
        self.status = status

        # Connect sidebar selection
        sidebar.itemClicked.connect(self.on_game_selected)

    def load_config(self):
        """Load game paths from config.json."""
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {game: data['executable'] for game, data in config['games'].items()}
            except Exception as e:
                print(f"Error loading config: {e}")
        return {}

    def save_config(self):
        """Save game paths to config.json."""
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            for game, path in self.game_paths.items():
                if game in config['games']:
                    config['games'][game]['executable'] = path

            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def on_game_selected(self, item):
        """Handle game selection."""
        game_name = item.text()
        self.title.setText(game_name)

        # Update info based on game
        game_info = {
            "WRC 10": {"size": "45.2 GB", "version": "1.2.5", "status": "Актуально"},
            "WRC 9": {"size": "42.8 GB", "version": "1.1.3", "status": "Актуально"},
            "Forza Horizon 6": {"size": "118.5 GB", "version": "2.0.1", "status": "ОБНОВИТЬ"},
            "Dead Island 2": {"size": "67.3 GB", "version": "1.5.0", "status": "Актуально"},
            "WRC Generations": {"size": "48.7 GB", "version": "1.3.2", "status": "Актуально"},
            "Teardown": {"size": "1.2 GB", "version": "1.4.0", "status": "ОБНОВИТЬ"},
            "Assetto Corsa EVO": {"size": "55.4 GB", "version": "0.9.5", "status": "Актуально"}
        }

        if game_name in game_info:
            info = game_info[game_name]
            self.size.setText(f"Размер: {info['size']}")
            self.version.setText(f"Версия: {info['version']}")
            self.status.setText(info['status'])

            # Change status color
            if info['status'] == "Актуально":
                self.status.setStyleSheet("color: rgba(52,199,89,255); font-size: 16px; font-weight: 700; background-color: rgba(52,199,89,0.2); padding: 8px 24px; border-radius: 12px;")
            else:
                self.status.setStyleSheet("color: rgba(255,193,7,255); font-size: 16px; font-weight: 700; background-color: rgba(255,193,7,0.2); padding: 8px 24px; border-radius: 12px;")

    def launch_game(self):
        """Launch the selected game."""
        game_name = self.title.text()
        print(f"Запуск игры: {game_name}")

        # Get executable path from config
        executable_path = self.game_paths.get(game_name, "")

        # Change button text to show launching
        self.play_btn.setText("⏳ ЗАПУСК...")
        self.play_btn.setEnabled(False)

        if executable_path and os.path.exists(executable_path):
            # Launch the actual game
            try:
                subprocess.Popen([executable_path], shell=True)
                self.on_launch_success(game_name)
            except Exception as e:
                self.on_launch_error(game_name, str(e))
        else:
            # Ask user to set the path
            self.ask_for_game_path(game_name)

    def on_launch_success(self, game_name):
        """Handle successful launch."""
        self.play_btn.setText("▶ ИГРАТЬ ▶")
        self.play_btn.setEnabled(True)
        print(f"Игра {game_name} успешно запущена!")

        msg = QMessageBox()
        msg.setWindowTitle("Успешно")
        msg.setText(f"Игра '{game_name}' запущена!")
        msg.setStyleSheet("background-color: rgb(30, 30, 30); color: white;")
        msg.exec()

    def on_launch_error(self, game_name, error):
        """Handle launch error."""
        self.play_btn.setText("▶ ИГРАТЬ ▶")
        self.play_btn.setEnabled(True)
        print(f"Ошибка запуска {game_name}: {error}")

        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText(f"Не удалось запустить игру '{game_name}'\n\nОшибка: {error}")
        msg.setStyleSheet("background-color: rgb(30, 30, 30); color: white;")
        msg.exec()

    def ask_for_game_path(self, game_name):
        """Ask user to select game executable path."""
        self.play_btn.setText("▶ ИГРАТЬ ▶")
        self.play_btn.setEnabled(True)

        msg = QMessageBox()
        msg.setWindowTitle("Путь не настроен")
        msg.setText(f"Путь к игре '{game_name}' не настроен.\n\nХотите выбрать путь к исполняемому файлу игры?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setStyleSheet("background-color: rgb(30, 30, 30); color: white;")

        result = msg.exec()

        if result == QMessageBox.StandardButton.Yes:
            # Open file dialog
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                f"Выберите исполняемый файл для {game_name}",
                "",
                "Executable files (*.exe)"
            )

            if file_path:
                # Save the path
                self.game_paths[game_name] = file_path
                self.save_config()

                # Show success message
                success_msg = QMessageBox()
                success_msg.setWindowTitle("Успешно")
                success_msg.setText(f"Путь к '{game_name}' сохранён:\n{file_path}\n\nТеперь можно запустить игру!")
                success_msg.setStyleSheet("background-color: rgb(30, 30, 30); color: white;")
                success_msg.exec()

                # Try to launch again
                self.launch_game()
            else:
                # User cancelled
                cancel_msg = QMessageBox()
                cancel_msg.setWindowTitle("Отменено")
                cancel_msg.setText("Путь не выбран. Запуск отменён.")
                cancel_msg.setStyleSheet("background-color: rgb(30, 30, 30); color: white;")
                cancel_msg.exec()

app = QApplication(sys.argv)
window = SimpleLauncher()
window.show()
sys.exit(app.exec())
