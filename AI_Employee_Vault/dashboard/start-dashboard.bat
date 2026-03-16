@echo off
REM AI Employee Dashboard - Complete Startup with Backend
REM Yeh script backend server ke sath dashboard start karegi

echo ============================================
echo    AI Employee Dashboard - Complete Startup
echo ============================================
echo.

cd /d "%~dp0"

REM Install dependencies if needed
echo [1/3] Checking dependencies...
pip install flask flask-cors python-dotenv -q
echo OK: Dependencies installed
echo.

REM Start Backend Server
echo [2/3] Starting Backend Server...
start "AI Employee Dashboard Backend" python app.py
timeout /t 3 /nobreak >nul
echo OK: Backend server started on http://localhost:5000
echo.

REM Open Dashboard in Browser
echo [3/3] Opening Dashboard in browser...
start "" "http://localhost:5000"
echo OK: Dashboard opened in browser
echo.

echo ============================================
echo    ALL SYSTEMS STARTED!
echo ============================================
echo.
echo Backend Server: http://localhost:5000
echo Dashboard: Opening in default browser
echo.
echo Features:
echo   - Auto-start Gmail Watcher
echo   - Auto-start File Watcher  
echo   - Auto-start Orchestrator
echo   - Real-time email activity
echo   - Live auto-reply tracking
echo.
echo To Stop: Close the backend terminal window
echo ============================================
echo.
pause
