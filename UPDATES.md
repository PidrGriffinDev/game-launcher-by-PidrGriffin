# Launcher Updates - Fixes and Improvements

## Issues Fixed

### 1. CSS Transform Errors
**Problem**: PyQt6 QSS doesn't support CSS `transform` property
**Error**: `Unknown property transform`
**Solution**: Removed all `transform: scale()` from QSS stylesheet
**File**: `styles/glassmorphism.qss` (lines 69-77)

### 2. Icon pixmap() API Error
**Problem**: PyQt6 requires explicit Mode and State parameters
**Error**: TypeError for pixmap() calls
**Solution**: Added `QIcon.Mode.Normal, QIcon.State.Off` to all pixmap() calls
**Files**:
- `icons/placeholder.py` (line 51)
- `main_window.py` (line 135)

### 3. Window Transparency & macOS/iOS Look
**Problem**: Window had solid background, no transparency
**Solution**:
- Added `WA_TranslucentBackground` attribute
- Added `FramelessWindowHint` window flag
- Added glassmorphism containers with semi-transparent backgrounds
- Added window dragging support (mouse events)
**File**: `main_window.py`

### 4. Background Color Display
**Problem**: Background color wasn't showing properly
**Solution**:
- Implemented smooth color transition animation (60 FPS timer)
- Added dynamic background color interpolation
- Colors transition smoothly when switching games
**File**: `main_window.py` (animate_background method)

### 5. Glassmorphism Effect
**Problem**: No real glass/blur effect
**Solution**:
- Added glassmorphism container with semi-transparent backgrounds
- Applied `rgba(60, 60, 60, 120)` for glass effect
- Added subtle borders `rgba(255, 255, 255, 0.15)`
- Updated dynamically based on theme
**File**: `main_window.py`

### 6. UI Elements Missing
**Problem**: Game card elements not displaying correctly
**Solution**:
- Added proper spacing between elements
- Set minimum widths for buttons (200px)
- Added glass container wrapper
- Improved layout structure
**File**: `main_window.py` (GameCard class)

### 7. Window Controls
**Problem**: No way to close/minimize frameless window
**Solution**:
- Added minimize button (orange)
- Added close button (red)
- Added window dragging via mouse events
**File**: `main_window.py` (setup_top_bar, mousePressEvent, mouseMoveEvent)

## New Features Added

### 1. Smooth Color Transitions
- Background color animates smoothly when selecting games
- 60 FPS animation timer (16ms interval)
- Linear interpolation for smooth transitions
- Colors match game theme presets

### 2. Window Dragging
- Click and drag anywhere on window to move it
- Frameless window support
- Proper mouse event handling

### 3. Window Controls
- Minimize button (top-right, orange)
- Close button (top-right, red)
- macOS-style window management

### 4. Enhanced Glassmorphism
- Semi-transparent card backgrounds
- Subtle borders
- Dynamic theme-based colors
- Multiple glass layers for depth

### 5. Theme-Accented Elements
- Sidebar selection color matches theme accent
- Play button color matches theme
- Text colors adapt to theme (light/dark)
- Glass container color matches theme

## Current Features

✅ iOS/macOS aesthetic with glassmorphism
✅ Semi-transparent buttons and cards
✅ Smooth background color transitions (60 FPS)
✅ Dynamic theme switching (8 themes)
✅ Window transparency
✅ Window dragging support
✅ Minimize/Close buttons
✅ 7 game presets with unique themes
✅ Multi-language support (EN, RU, ES)
✅ Language switcher in top bar
✅ Background threading for smooth UI
✅ Game icon display
✅ Game title, size, update status
✅ Play button (green, prominent)
✅ Update button (when needed)
✅ Settings button (placeholder)
✅ Fade-in animations on game switch

## How to Run

### Option 1: Python
```bash
cd Laucher_by_PidrGriffin
python main.py
```

### Option 2: Batch File
```bash
cd Laucher_by_PidrGriffin
start_launcher.bat
```

## Window Management

- **Drag**: Click and drag anywhere on the window to move it
- **Minimize**: Click the orange "−" button (top-right)
- **Close**: Click the red "✕" button (top-right)
- **Language**: Use dropdown in top-right to switch languages
- **Games**: Click games in sidebar to switch themes

## Theme Colors

Each game has a unique theme:
- WRC 10: White (#fafafa)
- WRC 9: Dark red/grey (#ff6b6b)
- Forza Horizon 6: Orange (#ff8c00)
- Dead Island 2: Green (#4caf50)
- WRC Generations: Blue (#2196f3)
- Teardown: Yellow (#ffc107)
- Assetto Corsa EVO: Purple (#9c27b0)

## Technical Details

- **Framework**: PyQt6
- **Animation**: QPropertyAnimation + QTimer (60 FPS)
- **Styling**: QSS (Qt Style Sheets)
- **Glassmorphism**: RGBA colors with alpha channels
- **Transparency**: WA_TranslucentBackground attribute
- **Window**: FramelessWindowHint flag
- **Threading**: QThread for background operations

## Notes

- Window is frameless for macOS/iOS look
- Can be dragged by clicking anywhere
- Minimize and close buttons in top-right
- Background color transitions smoothly (60 FPS)
- All UI elements adapt to selected game theme
- Glassmorphism effect with semi-transparent layers
