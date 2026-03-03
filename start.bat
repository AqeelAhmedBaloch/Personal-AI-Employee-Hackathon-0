@echo off
REM Personal AI Employee Hackathon-0 - AI Dashboard Launcher

echo ============================================
echo    AI Employee Dashboard - Starting...
echo ============================================
echo.

cd /d "%~dp0AI_Employee_Vault\dashboard"

echo Opening AI Dashboard in browser...
echo.

REM Open the HTML file directly in default browser
start ai-dashboard.html

echo.
echo Dashboard opened in browser!
echo Note: For full functionality, run: python app.py
echo.

pause
