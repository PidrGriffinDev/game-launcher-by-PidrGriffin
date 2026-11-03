# PetterGriffinDev Launcher - Setup Guide

## Project Overview

A premium game launcher built with PyQt6 featuring:
- iOS/macOS glassmorphism aesthetic
- Dynamic theme transitions based on game selection
- Smooth animations (60 FPS)
- Multi-language support (English, Russian, Spanish)
- Background processing for smooth UI
- Modern dashboard with game cards

## Installation

### 1. Install Dependencies

```bash
cd Laucher_by_PidrGriffin
pip install -r requirements.txt
```

### 2. Generate Placeholder Icons (Optional)

```bash
python icons/placeholder.py
```

This creates colored placeholder icons for all games. Replace these with actual game icons for production.

### 3. Run the Launcher

```bash
python main.py
```

Or use the batch file:
```bash
run.bat
```

## Project Structure

```
Laucher_by_PidrGriffin/
├── main.py                  # Application entry point
├── main_window.py           # Main window with sidebar and game dashboard
├── localization.py          # Multi-language support (EN, RU, ES)
├── theme_manager.py         # Dynamic theme management with 8 presets
├── game_data.py             # Game data structure and 7 game presets
├── game_scanner.py          # Background threads for scanning/launching
├── requirements.txt         # PyQt6 dependencies
├── styles/
│   └── glassmorphism.qss   # Glassmorphism stylesheet
├── languages/
│   ├── en.json             # English translations
│   ├── ru.json             # Russian translations
│   └── es.json             # Spanish translations
├── icons/
│   ├── placeholder.py      # Icon generator
│   └── *.png               # Game icons (generated)
└── assets/                 # Additional assets
```

## Game Presets & Themes

The launcher includes 7 game presets with custom themes:

1. **WRC 10** - Clean White theme
2. **WRC 9** - Deep Black/Dark Charcoal theme
3. **Forza Horizon 6** - Orange accent theme
4. **Dead Island 2** - Green accent theme
5. **WRC Generations** - Blue accent theme
6. **Teardown** - Yellow accent theme
7. **Assetto Corsa EVO** - Purple accent theme

## Customization

### Adding New Games

Edit `game_data.py`:

```python
"new_game": Game(
    name="new_game",
    title="Game Title",
    executable_path="C:/Path/To/Game.exe",
    icon_path="icons/new_game.png",
    size="50 GB",
    theme="custom_theme",
    update_required=False
)
```

### Adding New Themes

Edit `theme_manager.py` and add to the `themes` dictionary:

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

1. Create `languages/xx.json` with translations
2. Add to `LocalizationManager.available_languages` in `localization.py`:

```python
self.available_languages = {
    "en": "English",
    "ru": "Russian",
    "es": "Spanish",
    "xx": "Language Name"
}
```

## Features

### Glassmorphism UI
- Semi-transparent buttons with blur effects
- Heavily rounded corners (iOS/macOS style)
- Clean, premium typography
- Hover effects with smooth transitions

### Dynamic Themes
- Background and accent colors transition smoothly when selecting games
- Theme colors match game icon aesthetics
- Custom color schemes for each game

### Animations
- Fade-in/fade-out transitions when switching games
- Smooth hover effects on all interactive elements
- 60 FPS performance maintained via background threading

### Multi-language Support
- Language switcher in top-right corner
- JSON-based translation system
- Scalable architecture for adding new languages

### Background Processing
- Game scanning runs in separate thread
- Game launching runs in separate thread
- UI remains responsive during all operations

## Configuration

### Game Executable Paths

Update `executable_path` in `game_data.py` with actual game installation paths:

```python
"wrc10": Game(
    name="wrc10",
    title="WRC 10",
    executable_path="C:/Games/WRC10/WRC10.exe",
    ...
)
```

### Custom Icons

Replace placeholder icons in `icons/` folder with actual game icons (PNG format, recommended 256x256).

## Troubleshooting

### Import Errors
Ensure PyQt6 is installed:
```bash
pip install PyQt6
```

### Missing Icons
Run the icon generator:
```bash
python icons/placeholder.py
```

### Theme Not Applying
Check that `styles/glassmorphism.qss` exists in the project directory.

### Language Not Changing
Verify JSON files in `languages/` folder have correct format and are UTF-8 encoded.

## Notes

- The launcher uses placeholder icons by default
- Game launching is simulated for demo purposes (actual path required)
- All UI operations remain smooth due to background threading
- Themes transition smoothly with animation
- The launcher is fully modular and easy to extend

## Future Enhancements

- Add game installation path detection
- Implement actual update checking
- Add game settings/config management
- Support for custom game profiles
- Cloud save integration
- Achievement tracking
- Screenshot gallery
