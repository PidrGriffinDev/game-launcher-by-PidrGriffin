"""
Placeholder icon generator.
Run this script to generate unique placeholder icons for games.
"""

from PyQt6.QtGui import QPainter, QColor, QFont, QIcon, QPixmap, QBrush, QLinearGradient, QPen
from PyQt6.QtCore import Qt, QSize, QPointF
import os


def create_placeholder_icon(text: str, color: QColor, size: QSize = QSize(256, 256)) -> QIcon:
    """Create a placeholder icon with text and gradient background."""
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Create gradient background
    gradient = QLinearGradient(QPointF(0, 0), QPointF(size.width(), size.height()))
    gradient.setColorAt(0, color)
    gradient.setColorAt(1, color.lighter(120))
    painter.setBrush(QBrush(gradient))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(0, 0, size.width(), size.height(), 32, 32)

    # Draw border
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(QPen(QColor(255, 255, 255, 50), 3))
    painter.drawRoundedRect(2, 2, size.width()-4, size.height()-4, 30, 30)

    # Draw text
    painter.setPen(QColor(255, 255, 255))
    font = QFont("Arial Black", 52, QFont.Weight.Black)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, text[:3].upper())

    painter.end()
    return QIcon(pixmap)


def generate_all_icons():
    """Generate unique placeholder icons for all games."""
    icons_dir = "icons"
    os.makedirs(icons_dir, exist_ok=True)

    game_icons = {
        "wrc10": ("WRC", QColor(0, 120, 212)),
        "wrc9": ("WR9", QColor(255, 107, 107)),
        "forza": ("FOR", QColor(255, 140, 0)),
        "dead_island": ("DII", QColor(76, 175, 80)),
        "wrc_generations": ("WRG", QColor(33, 150, 243)),
        "teardown": ("TED", QColor(255, 193, 7)),
        "assetto_corsa": ("ACE", QColor(156, 39, 176)),
        "assetto_corsa_comp": ("ACC", QColor(200, 50, 50)),
        "project_cars3": ("PC3", QColor(0, 180, 200)),
        "nfs_heat": ("NFS", QColor(255, 80, 0)),
        "tlou_remastered": ("TLO", QColor(180, 100, 80)),
        "watch_dogs2": ("WD2", QColor(50, 150, 180)),
        "bodycam": ("BCM", QColor(100, 100, 120))
    }

    for game_name, (text, color) in game_icons.items():
        icon = create_placeholder_icon(text, color)
        pixmap = icon.pixmap(256, 256, QIcon.Mode.Normal, QIcon.State.Off)
        pixmap.save(os.path.join(icons_dir, f"{game_name}.png"))
        print(f"Generated icon: {game_name}.png with text '{text}'")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    generate_all_icons()
    print("All unique placeholder icons generated successfully!")
