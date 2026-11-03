from dataclasses import dataclass
from typing import Optional
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize


@dataclass
class Game:
    """Game data structure."""
    name: str
    title: str
    executable_path: str
    icon_path: Optional[str] = None
    size: str = "Unknown"
    version: str = "1.0.0"
    theme: str = "default"
    update_required: bool = False
    installed: bool = True

    def get_icon(self) -> QIcon:
        """Get game icon or default."""
        if self.icon_path:
            return QIcon(self.icon_path)
        return QIcon()

    def get_display_size(self) -> str:
        """Return formatted size string."""
        return self.size

    def get_display_version(self) -> str:
        """Return formatted version string."""
        return self.version


# Game presets with themes
GAME_PRESETS = {
    "wrc10": Game(
        name="wrc10",
        title="WRC 10",
        executable_path="",
        icon_path="icons/wrc10.png",
        size="45.2 GB",
        version="1.2.5",
        theme="wrc10",
        update_required=False
    ),
    "wrc9": Game(
        name="wrc9",
        title="WRC 9",
        executable_path="",
        icon_path="icons/wrc9.png",
        size="42.8 GB",
        version="1.1.3",
        theme="wrc9",
        update_required=False
    ),
    "forza": Game(
        name="forza",
        title="Forza Horizon 6",
        executable_path="",
        icon_path="icons/forza.png",
        size="118.5 GB",
        version="2.0.1",
        theme="forza",
        update_required=True
    ),
    "dead_island": Game(
        name="dead_island",
        title="Dead Island 2",
        executable_path="",
        icon_path="icons/dead_island.png",
        size="67.3 GB",
        version="1.5.0",
        theme="dead_island",
        update_required=False
    ),
    "wrc_generations": Game(
        name="wrc_generations",
        title="WRC Generations",
        executable_path="",
        icon_path="icons/wrc_generations.png",
        size="48.7 GB",
        version="1.3.2",
        theme="wrc_generations",
        update_required=False
    ),
    "teardown": Game(
        name="teardown",
        title="Teardown",
        executable_path="",
        icon_path="icons/teardown.png",
        size="1.2 GB",
        version="1.4.0",
        theme="teardown",
        update_required=True
    ),
    "assetto_corsa": Game(
        name="assetto_corsa",
        title="Assetto Corsa EVO",
        executable_path="",
        icon_path="icons/assetto_corsa.png",
        size="55.4 GB",
        version="0.9.5",
        theme="assetto_corsa",
        update_required=False
    )
}


def get_all_games() -> list[Game]:
    """Get all available games."""
    return list(GAME_PRESETS.values())


def get_game_by_name(name: str) -> Optional[Game]:
    """Get game by name."""
    return GAME_PRESETS.get(name)
