@echo off
REM Quick Deploy to Railway

echo.
echo ============================================
echo    Push to GitHub for Railway Deploy
echo ============================================
echo.

cd /d "%~dp0"

REM Check git status
git status

echo.
echo Adding new files for Railway...
git add requirements.txt
git add Procfile
git add railway.json

echo.
git commit -m "Add Railway deployment files"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ============================================
echo    ✅ Pushed to GitHub!
echo ============================================
echo.
echo Railway will auto-deploy.
echo Check: https://railway.app/dashboard
echo.

pause
