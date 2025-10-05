@echo off
:: Elevate to admin if not already
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Change to the sync directory
cd /d "C:\Program Files\iclock-sync"

:: Start iClock in a new, minimized CMD that auto-closes when done, activating venv first
start "" /min cmd /c "call .venv\Scripts\activate && iclock --loop 5 --since 7"
