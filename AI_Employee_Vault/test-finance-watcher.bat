@echo off
REM Test Finance Watcher

cd /d "%~dp0"

echo ============================================
echo    Testing Finance Watcher
echo ============================================
echo.

python watchers\finance_watcher.py . 10

pause
