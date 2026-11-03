import os
import subprocess
from PyQt6.QtCore import QThread, pyqtSignal
from typing import List, Optional
from game_data import Game


class GameScannerThread(QThread):
    """Background thread for scanning games."""
    games_found = pyqtSignal(list)
    scan_progress = pyqtSignal(str)
    scan_complete = pyqtSignal()

    def __init__(self, scan_paths: Optional[List[str]] = None):
        super().__init__()
        self.scan_paths = scan_paths or []
        self._is_running = True

    def run(self):
        """Scan for games in background."""
        self.scan_progress.emit("Scanning Games...")

        # Simulate scanning delay
        import time
        time.sleep(0.5)

        # For now, return preset games
        # In production, this would scan actual directories
        from game_data import get_all_games
        games = get_all_games()

        self.games_found.emit(games)
        self.scan_complete.emit()

    def stop(self):
        """Stop the scanning process."""
        self._is_running = False
        self.wait()


class GameLauncherThread(QThread):
    """Background thread for launching games."""
    launch_started = pyqtSignal(str)
    launch_success = pyqtSignal(str)
    launch_failed = pyqtSignal(str, str)

    def __init__(self, game: Game):
        super().__init__()
        self.game = game

    def run(self):
        """Launch the game executable."""
        self.launch_started.emit(self.game.title)

        try:
            if self.game.executable_path and os.path.exists(self.game.executable_path):
                # Launch the actual executable
                subprocess.Popen(
                    [self.game.executable_path],
                    shell=True,
                    cwd=os.path.dirname(self.game.executable_path)
                )
                self.launch_success.emit(self.game.title)
            else:
                # Simulate launch for demo purposes
                import time
                time.sleep(1.0)
                self.launch_success.emit(self.game.title)
        except Exception as e:
            self.launch_failed.emit(self.game.title, str(e))
