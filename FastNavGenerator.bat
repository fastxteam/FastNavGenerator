@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ============================================
:: Force switch to batch file directory
:: ============================================
cd /d "%~dp0"

:: Verify switch
echo [INFO] Current working directory: %CD%
echo [INFO] Batch file location: %~dp0
echo.

:: ============================================
:: Configuration Section
:: ============================================
set "CONFIG_FILE=FastNavGenerator.json"
set "OUTPUT_FILE=index.html"
set "SERVER_PORT=8002"
set "AUTO_OPEN=true"
set "ENABLE_NETWORKING=true"
set "START_ON_BOOT=true"
set "SERVICE_NAME=FastNavWebService"
set "SERVICE_DISPLAY_NAME=FastNav Web Service"
set "SERVICE_DESCRIPTION=Auto-generate and serve navigation website"
set "TITLE=Embedded Development Center"
set "DEFAULT_LAYOUT=list"
set "HTTP_SERVER=webhttp\nhttp.exe"
set "NSSM_EXE=nssm\win64\nssm.exe"

:: ============================================

title FastNav Generator - v4.0 (NSSM Edition)
color 0A

:: Initialize
call :INITIALIZE

:: Main Menu
:MENU_MAIN
cls
echo.
echo ========================================
echo   FastNav Generator - Main Menu
echo ========================================
echo.
echo   Current Config:
echo   - Config File: %CONFIG_FILE%
echo   - Output File: %OUTPUT_FILE%
echo   - Server Port: %SERVER_PORT%
echo   - Service Status: %SERVICE_STATUS%
echo   - HTTP Server: %HTTP_SERVER%
echo.
echo ========================================
echo.
echo 1. Generate HTML Website
echo 2. Start Local Server (Temporary)
echo 3. Install as Windows Service (NSSM)
echo 4. Uninstall Windows Service
echo 5. Start Service
echo 6. Stop Service
echo 7. Restart Service
echo 8. Check Service Status
echo 9. View Service Logs
echo 10. Config Management
echo 11. Start and Open in Browser
echo 12. Open Generated File
echo 13. Test Service Access
echo 14. System Diagnostics
echo 15. Exit
echo.
set /p choice="Select operation (1-15): "

if "%choice%"=="1" call :GENERATE_WEBSITE && goto MENU_MAIN
if "%choice%"=="2" call :START_SERVER_TEMP && goto MENU_MAIN
if "%choice%"=="3" call :INSTALL_SERVICE && goto MENU_MAIN
if "%choice%"=="4" call :UNINSTALL_SERVICE && goto MENU_MAIN
if "%choice%"=="5" call :START_SERVICE && goto MENU_MAIN
if "%choice%"=="6" call :STOP_SERVICE && goto MENU_MAIN
if "%choice%"=="7" call :RESTART_SERVICE && goto MENU_MAIN
if "%choice%"=="8" call :STATUS_SERVICE && goto MENU_MAIN
if "%choice%"=="9" call :VIEW_SERVICE_LOGS && goto MENU_MAIN
if "%choice%"=="10" call :MANAGE_CONFIG && goto MENU_MAIN
if "%choice%"=="11" call :START_AND_OPEN && goto MENU_MAIN
if "%choice%"=="12" call :OPEN_FILE && goto MENU_MAIN
if "%choice%"=="13" call :TEST_SERVICE_ACCESS && goto MENU_MAIN
if "%choice%"=="14" call :SYSTEM_DIAGNOSE && goto MENU_MAIN
if "%choice%"=="15" exit /b 0

echo [ERROR] Invalid selection
timeout /t 2 >nul
goto MENU_MAIN

:: ============================================
:: Functions
:: ============================================

:INITIALIZE
:: Check required files
set "HAS_EXE=0"
set "HAS_PY=0"

if exist "FastNavGenerator.exe" (
    set "HAS_EXE=1"
)

if exist "FastNavGenerator.py" (
    set "HAS_PY=1"
)

if !HAS_EXE! equ 0 if !HAS_PY! equ 0 (
    echo [ERROR] No generator found!
    echo [INFO] Need either:
    echo   - FastNavGenerator.exe (compiled)
    echo   - FastNavGenerator.py (Python script)
    pause
    exit /b 1
)

:: Check config file
if not exist "%CONFIG_FILE%" (
    echo [WARNING] Config file not found, creating example...
    call :CREATE_DEFAULT_CONFIG
)

:: Check service status
call :CHECK_SERVICE_STATUS
exit /b 0

:CHECK_SERVICE_STATUS
sc query "%SERVICE_NAME%" >nul 2>nul
if %errorlevel% equ 0 (
    sc query "%SERVICE_NAME%" | findstr /c:"RUNNING" >nul
    if %errorlevel% equ 0 (
        set "SERVICE_STATUS=[RUNNING]"
    ) else (
        set "SERVICE_STATUS=[STOPPED]"
    )
) else (
    set "SERVICE_STATUS=[NOT INSTALLED]"
)
exit /b 0

:GENERATE_WEBSITE
cls
echo.
echo [START] Generating website...
echo [FILE] Config File: %CONFIG_FILE%
echo [FILE] Output File: %OUTPUT_FILE%
echo.

:: Check if config file exists
if not exist "%CONFIG_FILE%" (
    echo [ERROR] Config file not found: %CONFIG_FILE%
    pause
    exit /b 1
)

:: Simple JSON syntax check
echo [INFO] Checking config file syntax...
python -c "import json; f = open('!CONFIG_FILE!', 'r', encoding='utf-8'); data = json.load(f); f.close(); print('[OK] Config file syntax is valid')" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Config file check skipped or Python not available
    echo [INFO] Continuing anyway...
    timeout /t 1 >nul
)

:: Determine which generator to use
set "GENERATOR_CMD="

:: Priority 1: Use EXE if available and works
if exist "FastNavGenerator.exe" (
    echo [INFO] Testing compiled executable...
    FastNavGenerator.exe --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "GENERATOR_CMD=FastNavGenerator.exe"
        echo [INFO] Using: FastNavGenerator.exe
    ) else (
        echo [WARNING] EXE may be corrupted
    )
)

:: Priority 2: Use Python script if EXE not available or not working
if not defined GENERATOR_CMD (
    if exist "FastNavGenerator.py" (
        where python >nul 2>&1
        if %errorlevel% equ 0 (
            set "GENERATOR_CMD=python FastNavGenerator.py"
            echo [INFO] Using: python FastNavGenerator.py
        ) else (
            echo [ERROR] Python not found for script execution
            pause
            exit /b 1
        )
    )
)

if not defined GENERATOR_CMD (
    echo [ERROR] No working generator found!
    pause
    exit /b 1
)

:: Generate website
echo [INFO] Running: !GENERATOR_CMD! --config "!CONFIG_FILE!" --output "!OUTPUT_FILE!"
!GENERATOR_CMD! --config "!CONFIG_FILE!" --output "!OUTPUT_FILE!"

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Website generated: !OUTPUT_FILE!
    echo [INFO] File location: %CD%\!OUTPUT_FILE!

    :: Show file info
    if exist "!OUTPUT_FILE!" (
        for %%F in ("!OUTPUT_FILE!") do (
            echo [INFO] File size: %%~zF bytes
        )
    )
) else (
    echo.
    echo [ERROR] Website generation failed with error code: %errorlevel%
)

echo.
pause
exit /b 0

:START_SERVER_TEMP
cls
echo.
echo [SERVER] Starting temporary local server...
echo [INFO] This is a temporary server (closes when batch ends)
echo.

:: Ensure website exists
if not exist "!OUTPUT_FILE!" (
    echo [WARNING] Website file not found, generating...
    call :GENERATE_WEBSITE_SILENT
)

:: Get network info
set "IP=localhost"
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /c:"IPv4" 2^>nul') do (
    set "IP=%%i"
    set "IP=!IP: =!"
    goto :IP_FOUND
)

:IP_FOUND

echo [INFO] Server Information:
echo    Local Access: http://localhost:!SERVER_PORT!
echo    Network Access: http://!IP!:!SERVER_PORT!
echo    Directory: %CD%
echo.
echo [INFO] Press Ctrl+C to stop server
echo.

:: Start temporary server using Python HTTP server
echo [INFO] Starting Python HTTP server...
start cmd /k "title FastNav Temporary Server - Port:!SERVER_PORT! && echo [INFO] Server running... && echo [URL] http://localhost:!SERVER_PORT! && echo [INFO] Press Ctrl+C to stop && python -m http.server !SERVER_PORT!"

if "!AUTO_OPEN!"=="true" (
    timeout /t 1 >nul
    start "" "http://localhost:!SERVER_PORT!"
)

echo.
echo [INFO] Temporary server started in new window
echo [INFO] Return to main menu...
timeout /t 3 >nul
exit /b 0

:GENERATE_WEBSITE_SILENT
:: Silent website generation
set "GENERATOR_CMD="

if exist "FastNavGenerator.exe" (
    FastNavGenerator.exe --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "GENERATOR_CMD=FastNavGenerator.exe"
    )
)

if not defined GENERATOR_CMD (
    if exist "FastNavGenerator.py" (
        where python >nul 2>&1
        if %errorlevel% equ 0 (
            set "GENERATOR_CMD=python FastNavGenerator.py"
        )
    )
)

if defined GENERATOR_CMD (
    !GENERATOR_CMD! --config "!CONFIG_FILE!" --output "!OUTPUT_FILE!" >nul 2>&1
)
exit /b 0

:START_AND_OPEN
call :GENERATE_WEBSITE_SILENT
start "" "http://localhost:!SERVER_PORT!"
echo [INFO] Browser opened with website
pause
exit /b 0

:OPEN_FILE
if exist "!OUTPUT_FILE!" (
    start "" "!OUTPUT_FILE!"
    echo [INFO] File opened in default browser
) else (
    echo [ERROR] File not found: !OUTPUT_FILE!
)
pause
exit /b 0

:: ============================================
:: NSSM Service Management Functions
:: ============================================

:INSTALL_SERVICE
cls
echo.
echo [INSTALL] Installing as Windows Service (NSSM)...
echo.

:: Ensure we're in correct directory
cd /d "%~dp0"
echo [INFO] Current directory: %CD%

:: Check administrator rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Administrator rights required!
    echo [INFO] Please run this script as administrator
    echo.
    echo Instructions:
    echo 1. Close this window
    echo 2. Right-click on FastNavGenerator.bat
    echo 3. Select "Run as administrator"
    echo 4. Select option 3 again
    echo.
    pause
    exit /b 1
)

echo [INFO] Administrator privileges confirmed

:: Check required files
echo [INFO] Checking required files...

:: 1. Check HTTP server executable
if not exist "%HTTP_SERVER%" (
    echo [ERROR] HTTP server not found: %HTTP_SERVER%
    echo [INFO] Please ensure webhttp folder exists with nhttp.exe
    pause
    exit /b 1
)
echo [OK] HTTP server: %HTTP_SERVER%

:: 2. Check NSSM
if not defined NSSM_EXE (
    echo [ERROR] NSSM not found!
    echo [INFO] Please ensure nssm folder exists with nssm.exe
    pause
    exit /b 1
)
echo [OK] NSSM: %NSSM_EXE%

:: 3. Ensure website exists
if not exist "!OUTPUT_FILE!" (
    echo [WARNING] Website file not found, generating...
    call :GENERATE_WEBSITE_SILENT

    if not exist "!OUTPUT_FILE!" (
        echo [ERROR] Failed to generate website!
        pause
        exit /b 1
    )
)
echo [OK] Website: !OUTPUT_FILE!

:: Step 1: Clean up existing service
echo [STEP 1] Cleaning up existing service...
call :CLEANUP_SERVICE_COMPLETELY

:: Step 2: Install service using NSSM
echo [STEP 2] Installing service with NSSM...
echo [CMD] "%NSSM_EXE%" install "%SERVICE_NAME%" "%CD%\%HTTP_SERVER%" -host 0.0.0.0 -port !SERVER_PORT! -path="%CD%"

"%NSSM_EXE%" install "%SERVICE_NAME%" "%CD%\%HTTP_SERVER%" -host 0.0.0.0 -port !SERVER_PORT! -path="%CD%"

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install service!
    pause
    exit /b 1
)

:: Step 3: Configure service
echo [STEP 3] Configuring service parameters...

"%NSSM_EXE%" set "%SERVICE_NAME%" DisplayName "%SERVICE_DISPLAY_NAME%"
"%NSSM_EXE%" set "%SERVICE_NAME%" Description "%SERVICE_DESCRIPTION%"
"%NSSM_EXE%" set "%SERVICE_NAME%" Start SERVICE_AUTO_START
"%NSSM_EXE%" set "%SERVICE_NAME%" AppDirectory "%CD%"
"%NSSM_EXE%" set "%SERVICE_NAME%" AppStdout "%CD%\service.log"
"%NSSM_EXE%" set "%SERVICE_NAME%" AppStderr "%CD%\service_error.log"
"%NSSM_EXE%" set "%SERVICE_NAME%" AppRotateFiles 1
"%NSSM_EXE%" set "%SERVICE_NAME%" AppRotateOnline 1
"%NSSM_EXE%" set "%SERVICE_NAME%" AppRotateSeconds 86400
"%NSSM_EXE%" set "%SERVICE_NAME%" AppRotateBytes 10485760

:: Set recovery options
"%NSSM_EXE%" set "%SERVICE_NAME%" AppExit Default Restart
"%NSSM_EXE%" set "%SERVICE_NAME%" AppRestartDelay 5000

:: Step 4: Start the service
echo [STEP 4] Starting service...
call :START_SERVICE_WITH_RETRY

echo.
echo [INFO] Service management commands:
echo   Start: "%NSSM_EXE%" start "%SERVICE_NAME%"
echo   Stop: "%NSSM_EXE%" stop "%SERVICE_NAME%"
echo   Restart: "%NSSM_EXE%" restart "%SERVICE_NAME%"
echo   Status: "%NSSM_EXE%" status "%SERVICE_NAME%"
echo   Delete: "%NSSM_EXE%" remove "%SERVICE_NAME%" confirm
echo.
echo [INFO] Website: http://0.0.0.0:%SERVER_PORT%
echo.

pause
call :CHECK_SERVICE_STATUS
exit /b 0

:UNINSTALL_SERVICE
cls
echo.
echo [UNINSTALL] Removing Windows service...
echo.

:: Check administrator rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Administrator rights required!
    pause
    exit /b 0
)

:: Check NSSM
if not defined NSSM_EXE (
    echo [ERROR] NSSM not found!
    pause
    exit /b 0
)

echo [INFO] Using NSSM to remove service...

:: Stop service
echo [STEP 1] Stopping service...
"%NSSM_EXE%" stop "%SERVICE_NAME%" confirm >nul 2>&1
timeout /t 2 >nul

:: Delete service
echo [STEP 2] Deleting service...
"%NSSM_EXE%" remove "%SERVICE_NAME%" confirm

if %errorlevel% equ 0 (
    echo [SUCCESS] Service removed from system
) else (
    echo [INFO] Service may already be removed
)

:: Clean up service files
if exist "service.log" del "service.log"
if exist "service_error.log" del "service_error.log"

echo.
pause
call :CHECK_SERVICE_STATUS
exit /b 0

:START_SERVICE
cls
if not defined NSSM_EXE (
    echo [ERROR] NSSM not found!
    pause
    exit /b 0
)

echo [INFO] Starting service...
"%NSSM_EXE%" start "%SERVICE_NAME%"

if %errorlevel% equ 0 (
    echo [SUCCESS] Service started
) else (
    echo [ERROR] Failed to start service
)

timeout /t 2 >nul
call :CHECK_SERVICE_STATUS
echo.
pause
exit /b 0

:STOP_SERVICE
cls
if not defined NSSM_EXE (
    echo [ERROR] NSSM not found!
    pause
    exit /b 0
)

echo [INFO] Stopping service...
"%NSSM_EXE%" stop "%SERVICE_NAME%"

if %errorlevel% equ 0 (
    echo [SUCCESS] Service stopped
) else (
    echo [ERROR] Failed to stop service
)

timeout /t 2 >nul
call :CHECK_SERVICE_STATUS
echo.
pause
exit /b 0

:RESTART_SERVICE
cls
if not defined NSSM_EXE (
    echo [ERROR] NSSM not found!
    pause
    exit /b 0
)

echo [INFO] Restarting service...
"%NSSM_EXE%" restart "%SERVICE_NAME%"

if %errorlevel% equ 0 (
    echo [SUCCESS] Service restarted
) else (
    echo [ERROR] Failed to restart service
)

timeout /t 3 >nul
call :CHECK_SERVICE_STATUS
echo.
pause
exit /b 0

:STATUS_SERVICE
cls
echo.
echo [STATUS] Service Information
echo ========================================
echo.

:: Check via NSSM
if defined NSSM_EXE (
    echo [NSSM Status]
    "%NSSM_EXE%" status "%SERVICE_NAME%"
    echo.
)

:: Check via SC
echo [System Service Status]
sc query "%SERVICE_NAME%"
echo.

:: Check process
echo [Process Information]
tasklist /fi "imagename eq nhttp.exe" /fo table
echo.

:: Check port
echo [Port Listening Status]
netstat -ano | findstr ":%SERVER_PORT%"
echo.

pause
exit /b 0

:VIEW_SERVICE_LOGS
cls
echo.
echo [LOGS] Service Logs
echo ========================================
echo.

if exist "service.log" (
    echo === service.log (last 30 lines) ===
    powershell "Get-Content 'service.log' | Select-Object -Last 30"
) else (
    echo service.log not found
)

echo.
if exist "service_error.log" (
    echo === service_error.log (last 30 lines) ===
    powershell "Get-Content 'service_error.log' | Select-Object -Last 30"
) else (
    echo service_error.log not found
)

echo.
echo [INFO] Log files location: %CD%
pause
exit /b 0

:TEST_SERVICE_ACCESS
cls
echo.
echo [TEST] Testing service access...
echo.
echo Testing http://localhost:%SERVER_PORT% ...

:: Use PowerShell for testing
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:%SERVER_PORT%' -TimeoutSec 3; Write-Host '[SUCCESS] Service is accessible!' -ForegroundColor Green; Write-Host 'Status code:' $response.StatusCode; Write-Host 'Response time:' $response.TimeMS 'ms' } catch { Write-Host '[ERROR] Service is not accessible!' -ForegroundColor Red; Write-Host 'Error:' $_.Exception.Message }"

echo.
echo [INFO] Checking port status:
netstat -an | findstr ":%SERVER_PORT%"
echo.
pause
exit /b 0

:SYSTEM_DIAGNOSE
cls
echo.
echo [DIAGNOSE] System Diagnostics
echo ========================================
echo.

:: 1. System information
echo [1/8] System Information:
ver
echo.

:: 2. Service Status
echo [2/8] Service Status:
sc query "%SERVICE_NAME%" 2>&1
echo.

:: 3. Port Availability
echo [3/8] Port %SERVER_PORT% Status:
netstat -ano | findstr ":%SERVER_PORT%"
echo.

:: 4. Required Files
echo [4/8] Required Files Check:
if exist "%HTTP_SERVER%" (echo "HTTP Server: EXISTS (%HTTP_SERVER%)") else (echo "HTTP Server: NOT FOUND")
if defined NSSM_EXE (
    if exist "%NSSM_EXE%" (echo "NSSM: EXISTS (%NSSM_EXE%)") else (echo "NSSM: NOT FOUND")
) else (
    echo "NSSM: NOT FOUND"
)
if exist "%CONFIG_FILE%" (echo "Config File: EXISTS") else (echo "Config File: NOT FOUND")
if exist "%OUTPUT_FILE%" (echo "Website: EXISTS") else (echo "Website: NOT FOUND")
echo.

:: 5. Directory Structure
echo [5/8] Directory Structure:
dir /b "nssm" 2>nul
echo.
dir /b "webhttp" 2>nul
echo.

:: 6. Log Files
echo [6/8] Log Files:
if exist "service.log" (
    echo "service.log: EXISTS (size: "
    for %%F in ("service.log") do echo %%~zF bytes")
) else (
    echo "service.log: NOT FOUND"
)
if exist "service_error.log" (
    echo "service_error.log: EXISTS (size: "
    for %%F in ("service_error.log") do echo %%~zF bytes")
) else (
    echo "service_error.log: NOT FOUND"
)
echo.

:: 7. Process Check
echo [7/8] Process Check:
tasklist /fi "imagename eq nhttp.exe"
echo.

:: 8. Network Information
echo [8/8] Network Information:
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /c:"IPv4" 2^>nul') do (
    set "IP=%%i"
    set "IP=!IP: =!"
    echo "Local IP: !IP!"
)

echo.
echo [INFO] Access URLs:
echo   Local: http://localhost:%SERVER_PORT%
if defined IP echo   Network: http://!IP!:%SERVER_PORT%

echo.
pause
exit /b 0

:: ============================================
:: Helper Functions
:: ============================================

:CLEANUP_SERVICE_COMPLETELY
:: Completely clean up existing service
if not defined NSSM_EXE exit /b 0

echo [INFO] Stopping existing service...
"%NSSM_EXE%" stop "%SERVICE_NAME%" confirm >nul 2>&1
timeout /t 2 >nul

echo [INFO] Deleting service...
"%NSSM_EXE%" remove "%SERVICE_NAME%" confirm >nul 2>&1
timeout /t 2 >nul

:: Clean registry entries
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\%SERVICE_NAME%" /f >nul 2>&1
echo [INFO] Cleanup completed
exit /b 0

:START_SERVICE_WITH_RETRY
:: Start service with retry mechanism
set "MAX_RETRIES=3"
set "RETRY_COUNT=0"

:START_LOOP
set /a RETRY_COUNT+=1
echo [INFO] Starting service (attempt !RETRY_COUNT! of !MAX_RETRIES!)...

"%NSSM_EXE%" start "%SERVICE_NAME%"

if %errorlevel% equ 0 (
    echo [SUCCESS] Service started successfully
    set "SERVICE_STATUS=[RUNNING]"

    :: Verify service is actually running
    timeout /t 3 >nul
    sc query "%SERVICE_NAME%" | findstr /c:"RUNNING" >nul
    if %errorlevel% equ 0 (
        echo [INFO] Service confirmed running

        :: Test if website is accessible
        echo [INFO] Testing web server...
        timeout /t 2 >nul

        powershell -Command "try { $null = Invoke-WebRequest -Uri 'http://localhost:%SERVER_PORT%' -TimeoutSec 5; Write-Host '[SUCCESS] Website accessible' -ForegroundColor Green } catch { Write-Host '[INFO] Website may need more time to start' -ForegroundColor Yellow }"

        :: Open browser if auto-open is enabled
        if "!AUTO_OPEN!"=="true" (
            echo [INFO] Opening browser...
            start "" "http://localhost:%SERVER_PORT%"
        )
    ) else (
        echo [WARNING] Service may not be responding properly
    )
    exit /b 0
)

if !RETRY_COUNT! geq !MAX_RETRIES! (
    echo [ERROR] Failed to start service after !MAX_RETRIES! attempts
    echo.
    echo [TROUBLESHOOTING]
    echo 1. Check Event Viewer: eventvwr.msc
    echo 2. Check service_error.log in current directory
    echo 3. Verify port %SERVER_PORT% is available
    echo 4. Try running %HTTP_SERVER% manually
    set "SERVICE_STATUS=[STOPPED]"
    exit /b 1
)

echo [INFO] Waiting 2 seconds before retry...
timeout /t 2 >nul
goto START_LOOP

:CHECK_UPDATE
cls
echo.
echo [UPDATE] Checking for updates...
echo.
echo [INFO] Current Version: v4.0 (NSSM Edition)
echo [INFO] Last Updated: February 2025
echo.
echo [INFO] Update check feature in development
echo   Visit project page for latest version
echo.
pause
exit /b 0

:MANAGE_CONFIG
cls
:MENU_CONFIG
echo.
echo [CONFIG] Configuration Management
echo ========================================
echo.
echo 1. Edit Config File (%CONFIG_FILE%)
echo 2. Create Example Config
echo 3. Change Server Port (Current: %SERVER_PORT%)
echo 4. Toggle Auto-Open Browser (Current: %AUTO_OPEN%)
echo 5. Change HTTP Server (Current: %HTTP_SERVER%)
echo 6. Return to Main Menu
echo.
set /p choice="Select: "

if "%choice%"=="1" goto EDIT_CONFIG
if "%choice%"=="2" goto CREATE_EXAMPLE
if "%choice%"=="3" goto CHANGE_PORT
if "%choice%"=="4" goto TOGGLE_AUTOOPEN
if "%choice%"=="5" goto CHANGE_HTTP_SERVER
if "%choice%"=="6" exit /b 0

echo [ERROR] Invalid selection
timeout /t 2 >nul
goto MENU_CONFIG

:EDIT_CONFIG
if exist "%CONFIG_FILE%" (
    notepad "%CONFIG_FILE%"
) else (
    call :CREATE_DEFAULT_CONFIG
    notepad "%CONFIG_FILE%"
)
goto MENU_CONFIG

:CREATE_EXAMPLE
call :CREATE_DEFAULT_CONFIG
echo [SUCCESS] Example config created
pause
goto MENU_CONFIG

:CHANGE_PORT
echo.
set /p NEW_PORT="Enter new port (Current: %SERVER_PORT%): "
if defined NEW_PORT (
    set "SERVER_PORT=%NEW_PORT%"

    :: Update config file
    if exist "%CONFIG_FILE%" (
        python -c "
import json
try:
    with open('!CONFIG_FILE!', 'r', encoding='utf-8') as f:
        config = json.load(f)

    if 'server' not in config:
        config['server'] = {}
    config['server']['port'] = !SERVER_PORT!

    if 'site' not in config:
        config['site'] = {}
    config['site']['port'] = !SERVER_PORT!

    with open('!CONFIG_FILE!', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print('[SUCCESS] Port updated in config file')
except Exception as e:
    print(f'[ERROR] Could not update config: {e}')
" 2>nul
    )

    echo [SUCCESS] Port changed to: %SERVER