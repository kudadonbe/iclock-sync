@echo off
:: Check for admin rights
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Now we're running as admin
cd /d "C:\Program Files\iclock-sync"
iclock --loop 5
pause
