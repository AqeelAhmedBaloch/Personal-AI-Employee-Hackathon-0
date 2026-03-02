@echo off
REM Watchdog Process Monitor - Start
REM Monitors and auto-restarts all AI Employee processes

echo ============================================
echo    WATCHDOG - Process Monitor
echo ============================================
echo.

cd /d "%~dp0"

echo Starting Watchdog Process Monitor...
echo This will monitor and auto-restart:
echo   - Orchestrator
echo   - File Watcher
echo   - Gmail Watcher
echo.
echo Press Ctrl+C to stop monitoring
echo.

REM Start watchdog
python watchdog.py .

echo.
echo ============================================
echo    WATCHDOG STOPPED
echo ============================================
pause
