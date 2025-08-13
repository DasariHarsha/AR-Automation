@echo off
cd /d %~dp0..

REM Install required packages
python -m pip install -r Files\requirements.txt

REM Run the main workflow
python gui.py

pause
