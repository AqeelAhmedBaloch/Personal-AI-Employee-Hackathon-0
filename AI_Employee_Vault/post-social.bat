@echo off
REM Social Media Auto-Poster - All Platforms
REM Posts to Facebook, Instagram, and Twitter simultaneously

echo ============================================
echo    SOCIAL MEDIA - Multi-Platform Poster
echo ============================================
echo.

cd /d "%~dp0"

REM Check arguments
IF "%~1"=="" (
    echo Usage: post-social.bat "Your content here"
    echo    OR
    echo post-social.bat --daily
    echo.
    pause
    exit /b 1
)

REM Get content
set CONTENT=%~1

echo Posting to all platforms...
echo.

REM Facebook
echo [Facebook] Posting...
python facebook_poster.py "%CONTENT%"
echo.

REM Twitter
echo [Twitter] Posting...
python twitter_poster.py "%CONTENT%"
echo.

REM Instagram (requires photo)
echo [Instagram] Skipping (requires photo)
echo   Use: python instagram_poster.py --photo image.jpg --caption "%CONTENT%"
echo.

echo ============================================
echo    SOCIAL MEDIA POSTING COMPLETE
echo ============================================
pause
