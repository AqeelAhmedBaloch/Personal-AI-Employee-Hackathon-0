@echo off
REM =====================================================
REM    Personal AI Employee - Quick Start
REM    Email Auto-Reply + Dashboard
REM =====================================================

echo.
echo =====================================================
echo    PERSONAL AI EMPLOYEE - QUICK START
echo =====================================================
echo.
echo Yeh script 2 cheezein start karegi:
echo   1. Gmail Auto-Reply Watcher (emails monitor karega)
echo   2. Dashboard (http://localhost:5000)
echo.
echo =====================================================
echo.

cd /d "%~dp0"

REM Check if credentials are configured
echo [1/3] Checking Gmail credentials...
if exist "mcp_servers\email_mcp\.env" (
     echo ✓ Gmail credentials found
 ) else (
     echo ✗ .env file not found!
     echo Please create: mcp_servers\email_mcp\.env
     pause
     exit /b 1
 )

echo.
echo [2/3] Starting Gmail Auto-Reply Watcher...
echo.
start "Gmail Watcher" cmd /k "cd /d %cd% && python gmail_auto_reply_watcher.py"
timeout /t 3 /nobreak >nul

echo.
echo [3/3] Starting Dashboard...
echo.
start "AI Employee Dashboard" cmd /k "cd /d %cd%\dashboard && python app.py"

echo.
echo =====================================================
echo    SYSTEM STARTED SUCCESSFULLY!
echo =====================================================
echo.
echo ✓ Gmail Watcher: Running in separate window
echo ✓ Dashboard: http://localhost:5000
echo.
echo Ab aap:
echo   1. Browser mein http://localhost:5000 kholain
echo   2. Dashboard se Gmail Watcher control kar sakte hain
echo   3. Test email bhej kar auto-reply verify karein
echo.
echo Windows close karne ke liye:
echo   - Gmail Watcher window: Ctrl+C press karein
echo   - Dashboard window: Ctrl+C press karein
echo.
echo =====================================================
echo.

REM Open dashboard in browser automatically
timeout /t 5 /nobreak >nul
start http://localhost:5000

echo Dashboard browser mein open ho gaya hoga!
echo.
pause
