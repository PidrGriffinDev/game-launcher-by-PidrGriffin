@echo off
cd /d "%~dp0"
echo Starting PetterGriffinDev Launcher...
python main.py
if errorlevel 1 (
    echo Error occurred. Press any key to exit...
    pause
)
