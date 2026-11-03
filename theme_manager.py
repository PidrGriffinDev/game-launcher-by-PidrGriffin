from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import QObject, pyqtSignal, QPropertyAnimation, QEasingCurve
from typing import Dict, Tuple


class ThemeManager(QObject):
    theme_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.current_theme = "default"
        self.themes = {
            "default": {
                "background": QColor(30, 30, 30),
                "sidebar": QColor(45, 45, 45, 200),
                "card": QColor(60, 60, 60, 150),
                "accent": QColor(0, 122, 255),
                "text": QColor(255, 255, 255),
                "text_secondary": QColor(180, 180, 180),
                "button": QColor(0, 122, 255, 200),
                "button_hover": QColor(0, 122, 255, 240),
                "play_button": QColor(52, 199, 89, 220),
                "play_button_hover": QColor(52, 199, 89, 255)
            },
            "wrc10": {
                "background": QColor(250, 250, 250),
                "sidebar": QColor(255, 255, 255, 230),
                "card": QColor(240, 240, 240, 180),
                "accent": QColor(0, 120, 212),
                "text": QColor(30, 30, 30),
                "text_secondary": QColor(100, 100, 100),
                "button": QColor(0, 120, 212, 200),
                "button_hover": QColor(0, 120, 212, 240),
                "play_button": QColor(52, 199, 89, 220),
                "play_button_hover": QColor(52, 199, 89, 255)
            },
            "wrc9": {
                "background": QColor(20, 20, 20),
                "sidebar": QColor(35, 35, 35, 210),
                "card": QColor(50, 50, 50, 160),
                "accent": QColor(255, 107, 107),
                "text": QColor(255, 255, 255),
                "text_secondary": QColor(180, 180, 180),
                "button": QColor(255, 107, 107, 200),
                "button_hover": QColor(255, 107, 107, 240),
                "play_button": QColor(52, 199, 89, 220),
                "play_button_hover": QColor(52, 199, 89, 255)
            },
            "forza": {
                "background": QColor(45, 25, 15),
                "sidebar": QColor(60, 40, 30, 200),
                "card": QColor(75, 50, 40, 150),
                "accent": QColor(255, 140, 0),
                "text": QColor(255, 255, 255),
                "text_secondary": QColor(200, 180, 160),
                "button": QColor(255, 140, 0, 200),
                "button_hover": QColor(255, 140, 0, 240),
                "play_button": QColor(52, 199, 89, 220),
                "play_button_hover": QColor(52, 199, 89, 255)
            },
            "dead_island": {
                "background": QColor(25, 35, 25),
                "sidebar": QColor(40, 50, 40, 200),
                "card": QColor(55, 65, 55, 150),
                "accent": QColor(76, 175, 80),
                "text": QColor(255, 255, 255),
                "text_secondary": QColor(180, 200, 180),
                "button": QColor(76, 175, 80, 200),
                "button_hover": QColor(76, 175, 80, 240),
                "play_button": QColor(255, 87, 34, 220),
                "play_button_hover": QColor(255, 87, 34, 255)
            },
            "wrc_generations": {
                "background": QColor(15, 25, 40),
                "sidebar": QColor(30, 40, 55, 200),
                "card": QColor(45, 55, 70, 150),
                "accent": QColor(33, 150, 243),
                "text": QColor(255, 255, 255),
                "text_secondary": QColor(180, 190, 210),
                "button": QColor(33, 150, 243, 200),
                "button_hover": QColor(33, 150, 243, 240),
                "play_button": QColor(52, 199, 89, 220),
                "play_button_hover": QColor(52, 199, 89, 255)
            },
            "teardown": {
                "background": QColor(40, 35, 30),
                "sidebar": QColor(55, 50, 45, 200),
                "card": QColor(70, 65, 60, 150),
                "accent": QColor(255, 193, 7),
                "text": QColor(255, 255, 255),
                "text_secondary": QColor(200, 195, 190),
                "button": QColor(255, 193, 7, 200),
                "button_hover": QColor(255, 193, 7, 240),
                "play_button": QColor(233, 30, 99, 220),
                "play_button_hover": QColor(233, 30, 99, 255)
            },
            "assetto_corsa": {
                "background": QColor(20, 30, 45),
                "sidebar": QColor(35, 45, 60, 200),
                "card": QColor(50, 60, 75, 150),
                "accent": QColor(156, 39, 176),
                "text": QColor(255, 255, 255),
                "text_secondary": QColor(190, 200, 215),
                "button": QColor(156, 39, 176, 200),
                "button_hover": QColor(156, 39, 176, 240),
                "play_button": QColor(52, 199, 89, 220),
                "play_button_hover": QColor(52, 199, 89, 255)
            }
        }

    def get_theme(self, theme_name: str) -> Dict[str, QColor]:
        """Get theme colors by name."""
        return self.themes.get(theme_name, self.themes["default"])

    def set_theme(self, theme_name: str) -> Dict[str, QColor]:
        """Set current theme and emit signal."""
        self.current_theme = theme_name
        theme = self.get_theme(theme_name)
        self.theme_changed.emit(theme)
        return theme

    def get_current_theme(self) -> Dict[str, QColor]:
        """Get current theme colors."""
        return self.get_theme(self.current_theme)

    @staticmethod
    def interpolate_color(color1: QColor, color2: QColor, t: float) -> QColor:
        """Interpolate between two colors."""
        r = int(color1.red() + (color2.red() - color1.red()) * t)
        g = int(color1.green() + (color2.green() - color1.green()) * t)
        b = int(color1.blue() + (color2.blue() - color1.blue()) * t)
        a = int(color1.alpha() + (color2.alpha() - color1.alpha()) * t)
        return QColor(r, g, b, a)
