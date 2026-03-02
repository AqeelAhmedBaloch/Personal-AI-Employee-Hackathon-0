@echo off
REM CEO Briefing Generator - Quick Start
REM Generates weekly Monday Morning CEO Briefing

echo ============================================
echo    CEO BRIEFING GENERATOR
echo ============================================
echo.

cd /d "%~dp0"

echo Generating Monday Morning CEO Briefing...
echo.

REM Generate briefing
python ceo_briefing.py .

echo.
echo ============================================
echo    BRIEFING COMPLETE!
echo ============================================
echo.
echo Check the /Briefings folder for the report.
echo.
pause
