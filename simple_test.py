import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SimpleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Window")
        self.resize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        label = QLabel("TEST LABEL")
        label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        layout.addWidget(label)

        button = QPushButton("PLAY BUTTON")
        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(52, 199, 89, 240);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 20px 60px;
                font-size: 24px;
                font-weight: 800;
            }
        """)
        button.setMinimumHeight(80)
        button.setMinimumWidth(280)
        layout.addWidget(button, 0, Qt.AlignmentFlag.AlignCenter)

        # Dark background
        central.setStyleSheet("background-color: rgb(30, 30, 30);")

app = QApplication(sys.argv)
window = SimpleWindow()
window.show()
sys.exit(app.exec())
