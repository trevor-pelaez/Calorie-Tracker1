@echo off
setlocal
cd /d "%~dp0"

echo This will delete the local SQLite database file.
echo The app will recreate it with starter data next time it runs.
echo.
choice /C YN /M "Delete calorietracker.db"
if errorlevel 2 exit /b 0

if exist "calorietracker.db" (
    del /f /q "calorietracker.db"
    echo Database deleted.
) else (
    echo No database file was found.
)

pause
