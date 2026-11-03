@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Starting launcher...
python main.py

pause
