:: iClock-Sync Launcher Script (Debug Mode)
:: - Ensures script runs as admin
:: - Manages logs and verifies access to cache directory
:: - Runs iclock in a loop with progressive backoff (waits longer if no new logs found)

:: === Admin Rights Check ===
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Relaunching with administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: === Begin Admin Logic ===
setlocal EnableDelayedExpansion

:: Change to iClock-Sync installation directory
cd /d "C:\Program Files\iclock-sync"
if %errorlevel% NEQ 0 (
    echo ERROR: Failed to change directory. Exiting.
    exit /b 1
)

:: === Log Initialization ===
:: Create timestamp for log file naming
for /f "tokens=2 delims==." %%I in ('"wmic os get LocalDateTime /value"') do set ts=%%I
set "ts=%ts:~0,4%-%ts:~4,2%-%ts:~6,2%_%ts:~8,2%%ts:~10,2%%ts:~12,2%"
set "LOGFILE=logs\bat_runlog_%ts%.log"

:: Create logs folder if not exists
if not exist logs (
    mkdir logs
    if %errorlevel% NEQ 0 (
        echo ERROR: Could not create logs directory. Exiting.
        exit /b 1
    )
)

:: Start log file
echo === iClock-Sync Batch Started at %DATE% %TIME% === > "%LOGFILE%"
echo Working Directory: %CD% >> "%LOGFILE%"

:: === Clean Up Old Logs ===
:: Deletes .log files older than 30 days
forfiles /p "logs" /s /m *.log /d -30 /c "cmd /c echo Deleting: @path >> \"%LOGFILE%\" & del /q @path"
echo Log cleanup complete. >> "%LOGFILE%"

:: === Cache Directory Access Check ===
:: Verifies read/write access to `cache` directory before starting sync
set "CACHE_DIR=cache"
set "CACHE_FILE=%CACHE_DIR%\uploaded_ids_cache.json"
set "TEMP_TEST_FILE=%CACHE_DIR%\temp_access_test_%RANDOM%.tmp"
set RETRIES=5
set WAIT=5
set FOUND=0

:: Create cache directory if missing
if not exist "%CACHE_DIR%" (
    mkdir "%CACHE_DIR%"
    if %errorlevel% NEQ 0 (
        echo ERROR: Failed to create cache directory. >> "%LOGFILE%"
        exit /b 1
    )
    echo Created cache directory. >> "%LOGFILE%"
)

:: Try multiple times to verify both read and write access to the cache
for /L %%R in (1,1,%RETRIES%) do (
    echo Attempt %%R of %RETRIES% to verify access... >> "%LOGFILE%"

    :: Test write
    echo Test data > "%TEMP_TEST_FILE%"
    if !errorlevel! NEQ 0 (
        echo Write failed. >> "%LOGFILE%"
        set WRITE_ACCESS_OK=0
    ) else (
        echo Write succeeded. >> "%LOGFILE%"
        del /q "%TEMP_TEST_FILE%" >nul
        set WRITE_ACCESS_OK=1
    )

    :: Test read
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

    :: If both succeeded, break loop early
    if "!WRITE_ACCESS_OK!"=="1" if "!READ_ACCESS_OK!"=="1" (
        set FOUND=1
        goto :end_retry_loop
    )

    :: Wait before next attempt if not last try
    if %%R lss %RETRIES% (
        echo Waiting %WAIT% seconds before retry... >> "%LOGFILE%"
        timeout /t %WAIT% /nobreak >nul
    )
)

:end_retry_loop

:: === Launch iClock with Progressive Backoff Loop ===
if "!FOUND!"=="1" (
    echo All checks passed. Starting iClock progressive loop... >> "%LOGFILE%"

    :: Start with 5 seconds delay, increase it up to 86400 (24 hours)
    set wait=5
    set maxWait=86400

    :loop
    echo Running iClock at %TIME%... >> "%LOGFILE%"
    iclock > "%TEMP%\iclock_out.txt"

    :: Check if iclock output says "No new logs to save."
    findstr /C:"No new logs to save." "%TEMP%\iclock_out.txt" >nul
    if !errorlevel! == 0 (
        :: No new logs — wait and increase delay
        echo No new logs. Waiting !wait! seconds... >> "%LOGFILE%"
        timeout /t !wait! /nobreak >nul

        :: Double wait time up to maxWait
        set /a wait=wait*2
        if !wait! GTR %maxWait% set wait=%maxWait%
    ) else (
        :: Logs found — reset wait to minimum
        echo New logs found. Resetting wait. >> "%LOGFILE%"
        set wait=5
        timeout /t 5 /nobreak >nul
    )

    goto loop

) else (
    echo ERROR: Access checks failed. >> "%LOGFILE%"
)

:: === Script End Logging ===
echo === iClock-Sync Batch Ended at %DATE% %TIME% === >> "%LOGFILE%"
pause
endlocal
