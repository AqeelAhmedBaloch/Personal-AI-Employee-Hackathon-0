@echo off
REM LinkedIn Daily AI Post - 02-03-2026
REM Scheduled for 12:00 PM

cd /d "%~dp0"

echo ============================================
echo    LinkedIn Daily AI Post
echo    Date: 02-03-2026 at 12:00 PM
echo ============================================
echo.
echo Current Time: %TIME%
echo.

python linkedin_daily_post_browser.py

echo.
echo ============================================
echo    Post Complete!
echo ============================================
