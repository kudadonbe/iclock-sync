:: iClock-Sync Launcher Script (Debug Mode)
:: Admin elevation, log management, access check, direct execution for debugging

:: === Admin Rights Check ===
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Relaunching with administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: === Begin Admin Logic ===
setlocal EnableDelayedExpansion

:: Change to the working directory
cd /d "C:\Program Files\iclock-sync"
if %errorlevel% NEQ 0 (
    echo ERROR: Failed to change directory. Exiting.
    exit /b 1
)

:: Generate timestamp for log file
for /f "tokens=2 delims==." %%I in ('"wmic os get LocalDateTime /value"') do set ts=%%I
set "ts=%ts:~0,4%-%ts:~4,2%-%ts:~6,2%_%ts:~8,2%%ts:~10,2%%ts:~12,2%"
set "LOGFILE=logs\bat_runlog_%ts%.log"

if not exist logs (
    mkdir logs
    if %errorlevel% NEQ 0 (
        echo ERROR: Could not create logs directory. Exiting.
        exit /b 1
    )
)

echo === iClock-Sync Batch Started at %DATE% %TIME% === > "%LOGFILE%"
echo Working Directory: %CD% >> "%LOGFILE%"

:: Clean old logs
forfiles /p "logs" /s /m *.log /d -30 /c "cmd /c echo Deleting: @path >> \"%LOGFILE%\" & del /q @path"
echo Log cleanup complete. >> "%LOGFILE%"

:: Cache access check
set "CACHE_DIR=cache"
set "CACHE_FILE=%CACHE_DIR%\uploaded_ids_cache.json"
set "TEMP_TEST_FILE=%CACHE_DIR%\temp_access_test_%RANDOM%.tmp"
set RETRIES=5
set WAIT=5
set FOUND=0

if not exist "%CACHE_DIR%" (
    mkdir "%CACHE_DIR%"
    if %errorlevel% NEQ 0 (
        echo ERROR: Failed to create cache directory. >> "%LOGFILE%"
        exit /b 1
    )
    echo Created cache directory. >> "%LOGFILE%"
)

for /L %%R in (1,1,%RETRIES%) do (
    echo Attempt %%R of %RETRIES% to verify access... >> "%LOGFILE%"

    echo Test data > "%TEMP_TEST_FILE%"
    if !errorlevel! NEQ 0 (
        echo Write failed. >> "%LOGFILE%"
        set WRITE_ACCESS_OK=0
    ) else (
        echo Write succeeded. >> "%LOGFILE%"
        del /q "%TEMP_TEST_FILE%" >nul
        set WRITE_ACCESS_OK=1
    )

    set READ_ACCESS_OK=0
    if exist "%CACHE_FILE%" (
        >nul type "%CACHE_FILE%"
        if !errorlevel! NEQ 0 (
            echo Read failed. >> "%LOGFILE%"
        ) else (
            echo Read succeeded. >> "%LOGFILE%"
            set READ_ACCESS_OK=1
        )
    ) else (
        echo Cache file not found; read OK assumed. >> "%LOGFILE%"
        set READ_ACCESS_OK=1
    )

    if "!WRITE_ACCESS_OK!"=="1" if "!READ_ACCESS_OK!"=="1" (
        set FOUND=1
        goto :end_retry_loop
    )

    if %%R lss %RETRIES% (
        echo Waiting %WAIT% seconds before retry... >> "%LOGFILE%"
        timeout /t %WAIT% /nobreak >nul
    )
)

:end_retry_loop

:: Final check and launch
if "!FOUND!"=="1" (
    echo All checks passed. Starting: iclock --loop 5 >> "%LOGFILE%"
    echo Running command: iclock --loop 5
    iclock --loop 5
    echo Sync process finished or running in loop. >> "%LOGFILE%"
) else (
    echo ERROR: Access checks failed. >> "%LOGFILE%"
)

echo === iClock-Sync Batch Ended at %DATE% %TIME% === >> "%LOGFILE%"
pause
endlocal
