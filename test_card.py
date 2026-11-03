import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Game Card")
        self.resize(1200, 800)

        central = QWidget()
        central.setStyleSheet("background-color: rgb(30, 30, 30);")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(50, 50, 50, 50)

        # Title
        title = QLabel("WRC 10")
        title.setStyleSheet("color: white; font-size: 36px; font-weight: 800; background-color: rgba(255,255,255,0.05); padding: 15px 30px; border-radius: 16px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title, 0, Qt.AlignmentFlag.AlignCenter)

        # Size
        size = QLabel("Размер: 45.2 GB")
        size.setStyleSheet("color: white; font-size: 18px; font-weight: 600; background-color: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 12px;")
        size.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(size, 0, Qt.AlignmentFlag.AlignCenter)

        # Version
        version = QLabel("Версия: 1.2.5")
        version.setStyleSheet("color: white; font-size: 18px; font-weight: 600; background-color: rgba(255,255,255,0.1); padding: 10px 20px; border-radius: 12px;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version, 0, Qt.AlignmentFlag.AlignCenter)

        # Status
        status = QLabel("Актуально")
        status.setStyleSheet("color: rgba(52,199,89,255); font-size: 16px; font-weight: 700; background-color: rgba(52,199,89,0.2); padding: 8px 24px; border-radius: 12px;")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(status, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addSpacing(30)

        # PLAY BUTTON
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
        layout.addWidget(play_btn, 0, Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

app = QApplication(sys.argv)
window = TestWindow()
window.show()
sys.exit(app.exec())
