@echo off
REM Daily Briefing Scheduler - Windows Task Scheduler
REM This runs every day at 8:00 AM

cd /d "%~dp0"

echo ============================================
echo    Personal AI Employee Hackathon-0 - Daily Briefing
echo ============================================
echo.

REM Generate daily briefing
python daily_briefing.py .

echo.
echo Briefing complete!
echo Check Briefings folder for today's report.
pause
