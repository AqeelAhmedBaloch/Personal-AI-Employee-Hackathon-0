@echo off
REM Ralph Wiggum Loop - Quick Start
REM Yeh script AI ko autonomous task completion ke liye run karti hai

echo ============================================
echo    RALPH WIGGUM LOOP - Autonomous Mode
echo ============================================
echo.

cd /d "%~dp0"

REM Check if vault path provided
IF "%~1"=="" (
    echo Usage: ralph-loop.bat "Your task prompt" [max_iterations]
    echo.
    echo Example:
    echo   ralph-loop.bat "Process all files in Needs_Action and move to Done" 10
    echo.
    pause
    exit /b 1
)

REM Get prompt from first argument
set PROMPT=%~1

REM Get max iterations (default 10)
IF "%~2"=="" (
    set MAX_ITER=10
) ELSE (
    set MAX_ITER=%~2
)

echo Starting Ralph Wiggum Loop...
echo Prompt: %PROMPT%
echo Max iterations: %MAX_ITER%
echo.

REM Run Ralph Wiggum Loop
python ralph_wiggum_loop.py . --prompt "%PROMPT%" --max-iterations %MAX_ITER%

echo.
echo ============================================
IF %ERRORLEVEL% EQU 0 (
    echo    TASK COMPLETED SUCCESSFULLY!
) ELSE (
    echo    TASK INCOMPLETE - Max iterations reached
)
echo ============================================
echo.
pause
