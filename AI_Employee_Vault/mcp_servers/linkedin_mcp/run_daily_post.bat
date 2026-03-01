@echo off
REM LinkedIn Daily Auto-Post
REM Run this via Task Scheduler daily at 9 AM

cd /d "%~dp0"

echo ============================================
echo    LinkedIn Daily AI Auto-Post
echo ============================================
echo.
echo Date: %DATE%
echo Time: %TIME%
echo.

python linkedin_daily_auto_post.py

echo.
echo ============================================
echo    Post Complete!
echo ============================================
