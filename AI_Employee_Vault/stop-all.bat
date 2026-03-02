@echo off
REM AI Employee - Stop All Script
REM Yeh script sab processes ko stop karegi

echo ============================================
echo    AI EMPLOYEE - STOPPING ALL PROCESSES
echo ============================================
echo.

echo Stopping Python processes...
taskkill /F /FI "WINDOWTITLE eq AI Employee*" 2>nul
echo.

echo Stopping all Python processes (careful)...
taskkill /F /IM python.exe 2>nul
if errorlevel 1 (
    echo No Python processes found or already stopped
) else (
    echo OK: Python processes stopped
)
echo.

echo ============================================
echo    ALL PROCESSES STOPPED
echo ============================================
echo.
echo You can now safely close this window.
echo.
pause
