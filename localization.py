import json
import os
from typing import Dict, Optional
from PyQt6.QtCore import QObject, pyqtSignal


class LocalizationManager(QObject):
    language_changed = pyqtSignal(str)

    def __init__(self, languages_dir: str = "languages"):
        super().__init__()
        self.languages_dir = languages_dir
        self.current_language = "en"
        self.translations: Dict[str, str] = {}
        self.available_languages = {
            "en": "English",
            "ru": "Russian",
            "es": "Spanish"
        }
        self.load_language(self.current_language)

    def load_language(self, language_code: str) -> bool:
        """Load translations for the specified language."""
        lang_file = os.path.join(self.languages_dir, f"{language_code}.json")
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
            self.current_language = language_code
            self.language_changed.emit(language_code)
            return True
        except FileNotFoundError:
            print(f"Language file not found: {lang_file}")
            return False
        except json.JSONDecodeError:
            print(f"Invalid JSON in language file: {lang_file}")
            return False

    def get(self, key: str, default: Optional[str] = None) -> str:
        """Get translation for a key."""
        return self.translations.get(key, default or key)

    def set_language(self, language_code: str) -> bool:
        """Change the current language."""
        if language_code in self.available_languages:
            return self.load_language(language_code)
        return False

    def get_available_languages(self) -> Dict[str, str]:
        """Get available languages as {code: name} dict."""
        return self.available_languages.copy()
