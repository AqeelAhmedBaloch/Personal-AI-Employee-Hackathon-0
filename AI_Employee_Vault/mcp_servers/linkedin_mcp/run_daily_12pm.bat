@echo off
REM LinkedIn Daily Post - 12:00 PM
REM Runs every day automatically

cd /d "%~dp0"

echo ============================================
echo    LinkedIn Daily AI Post
echo    Time: 12:00 PM Daily
echo ============================================
echo.
echo Date: %DATE%
echo Time: %TIME%
echo.

python linkedin_daily_post_browser.py

echo.
echo ============================================
echo    Done!
echo ============================================

REM Log the run
echo %DATE% %TIME% - Post attempted >> linkedin_post_log.txt
