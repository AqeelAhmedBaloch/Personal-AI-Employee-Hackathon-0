@echo off
REM =====================================================
REM    AI Employee Dashboard - Quick Launcher
REM    Starts Flask server and opens browser
REM =====================================================

echo.
echo =====================================================
echo    🤖 AI Employee Dashboard Launcher
echo =====================================================
echo.
echo Yeh script:
echo   1. Flask server start karegi
echo   2. Browser mein dashboard open karegi
echo   3. Server chal raha rahega (Ctrl+C se stop)
echo.
echo =====================================================
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.13+ from python.org
    pause
    exit /b 1
)

echo [1/3] Installing requirements...
pip install -q flask flask-cors python-dotenv watchdog
if errorlevel 1 (
    echo WARNING: Some packages may have failed to install
)

echo.
echo [2/3] Starting Flask Dashboard Server...
echo.
echo Server URL: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Start server in background
start "AI Employee Dashboard Server" cmd /k "cd /d %cd% && python app.py"

echo [3/3] Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul

REM Open dashboard in default browser
start http://localhost:5000

echo.
echo =====================================================
echo    ✅ Dashboard Started Successfully!
echo =====================================================
echo.
echo Server Status:
echo   ✓ Flask server running in new window
echo   ✓ Dashboard opened in browser
echo   ✓ URL: http://localhost:5000
echo.
echo To Stop Server:
echo   1. Close the server window
echo   2. Or press Ctrl+C in server window
echo.
echo =====================================================
echo.

REM Keep this window open for status
echo Dashboard is running. Close this window when done.
pause >nul
