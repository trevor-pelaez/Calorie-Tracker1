@echo off
setlocal EnableExtensions

cd /d "%~dp0"

echo.
echo Starting Calorie Tracker...
echo.

set "PYTHON_CMD="

where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=py"
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set "PYTHON_CMD=python"
    )
)

if "%PYTHON_CMD%"=="" (
    echo Python was not found on this computer.
    echo.
    echo Install Python first:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check: Add python.exe to PATH
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv .venv
)

echo Installing required packages...
".venv\Scripts\python.exe" -m pip install -r requirements.txt

echo Starting app...
start "" "http://127.0.0.1:5000"
".venv\Scripts\python.exe" app.py

pause