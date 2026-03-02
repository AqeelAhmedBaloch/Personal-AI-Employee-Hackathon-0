@echo off
REM AI Employee - Complete Startup Script
REM Yeh script sab kuch automatically start karegi

echo ============================================
echo    PERSONAL AI EMPLOYEE HACKATHON-0 - COMPLETE STARTUP
echo ============================================
echo.

cd /d "%~dp0"

REM Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.13+
    pause
    exit /b 1
)
echo OK: Python found
echo.

REM Start File Watcher
echo [2/5] Starting File Watcher...
start "AI Employee - File Watcher" python watchers/filesystem_watcher.py . Drop_Folder
timeout /t 2 /nobreak >nul
echo OK: File Watcher started
echo.

REM Start Gmail Watcher
echo [3/5] Starting Gmail Watcher...
start "AI Employee - Gmail Watcher" python gmail_auto_reply_watcher.py 60
timeout /t 2 /nobreak >nul
echo OK: Gmail Watcher started
echo.

REM Start Orchestrator
echo [4/5] Starting Orchestrator...
start "AI Employee - Orchestrator" python orchestrator.py . --dev-mode --interval 30
timeout /t 2 /nobreak >nul
echo OK: Orchestrator started
echo.

REM Open Dashboard
echo [5/5] Opening AI Dashboard...
start "" "%CD%\dashboard\ai-dashboard.html"
echo OK: Dashboard opened in browser
echo.

echo ============================================
echo    ALL SYSTEMS STARTED!
echo ============================================
echo.
echo Running Processes:
echo   - File Watcher (monitoring Drop_Folder)
echo   - Gmail Watcher (checking every 60 seconds)
echo   - Orchestrator (coordinating every 30 seconds)
echo   - Dashboard (open in browser)
echo.
echo Scheduled Tasks:
echo   - LinkedIn Daily Post (12:00 PM daily)
echo.
echo To Stop: Run stop.bat or close terminal windows
echo ============================================
echo.
pause
