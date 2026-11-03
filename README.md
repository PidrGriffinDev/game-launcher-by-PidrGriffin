# PetterGriffinDev Launcher

A premium game launcher built with PyQt6 featuring iOS/macOS aesthetics, dynamic themes, smooth animations, and multi-language support.

## Features

- **iOS/macOS Aesthetic**: Glassmorphism design with semi-transparent buttons, blur effects, and rounded corners
- **Dynamic Themes**: Background and accent colors smoothly transition based on selected game
- **Smooth Animations**: Fluid fade-in/fade-out transitions and elegant hover effects
- **Multi-language Support**: English, Russian, and Spanish with scalable architecture
- **Background Processing**: Game scanning and launching run in separate threads for smooth 60 FPS UI
- **Modern Dashboard**: Game icons, titles, sizes, update status, and prominent PLAY button

## Game Presets

- WRC 10 (Clean White theme)
- WRC 9 (Deep Black/Dark Charcoal theme)
- Forza Horizon 6 (Orange accent theme)
- Dead Island 2 (Green accent theme)
- WRC Generations (Blue accent theme)
- Teardown (Yellow accent theme)
- Assetto Corsa EVO (Purple accent theme)

## Installation

1. Install Python 3.10 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Generate placeholder icons (optional):
   ```bash
   python icons/placeholder.py
   ```

## Usage

Run the launcher:
```bash
python main.py
```

Or use the batch file:
```bash
run.bat
```

## Customization

### Adding New Games

Edit `game_data.py` to add new games:

```python
"new_game": Game(
    name="new_game",
    title="Game Title",
    executable_path="path/to/game.exe",
    icon_path="icons/new_game.png",
    size="50 GB",
    theme="custom_theme",
    update_required=False
)
```

### Adding New Themes

Edit `theme_manager.py` to add custom themes:

```python
"custom_theme": {
    "background": QColor(r, g, b),
    "sidebar": QColor(r, g, b, alpha),
    "card": QColor(r, g, b, alpha),
    "accent": QColor(r, g, b),
    "text": QColor(r, g, b),
    "text_secondary": QColor(r, g, b),
    "button": QColor(r, g, b, alpha),
    "button_hover": QColor(r, g, b, alpha),
    "play_button": QColor(r, g, b, alpha),
    "play_button_hover": QColor(r, g, b, alpha)
}
```

### Adding New Languages

1. Create a new JSON file in `languages/` (e.g., `fr.json`)
2. Add translations following the format in `en.json`
3. Add the language to `LocalizationManager.available_languages` in `localization.py`

## Project Structure

```
Laucher_by_PidrGriffin/
├── main.py                  # Application entry point
├── main_window.py           # Main window and UI components
├── localization.py          # Multi-language support system
├── theme_manager.py         # Dynamic theme management
├── game_data.py             # Game data structure and presets
├── game_scanner.py          # Background scanning and launching threads
├── requirements.txt         # Python dependencies
├── styles/
│   └── glassmorphism.qss   # Glassmorphism stylesheet
├── languages/
│   ├── en.json             # English translations
│   ├── ru.json             # Russian translations
│   └── es.json             # Spanish translations
├── icons/
│   └── placeholder.py      # Icon generator script
└── assets/                 # Additional assets (images, etc.)
```

## Technical Details

- **Framework**: PyQt6
- **Styling**: QSS (Qt Style Sheets) with glassmorphism effects
- **Threading**: QThread for background operations
- **Animations**: QPropertyAnimation for smooth transitions
- **Localization**: JSON-based translation system

## Notes

- Place actual game icons in the `icons/` folder
- Update `executable_path` in `game_data.py` with actual game paths
- The launcher uses placeholder icons by default
- Theme transitions are smooth and animated
- All UI operations remain responsive during background tasks
