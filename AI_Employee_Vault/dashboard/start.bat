@echo off
REM AI Employee Dashboard - Quick Start

echo ============================================
echo    AI Employee Dashboard - Quick Start
echo ============================================
echo.

cd /d "%~dp0"

echo Installing requirements...
pip install -r requirements.txt

echo.
echo Starting Dashboard...
echo.

python app.py

pause
