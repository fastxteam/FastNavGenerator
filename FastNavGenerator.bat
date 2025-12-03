@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ============================================
:: 强制切换到脚本所在目录（管理员模式兼容）
:: ============================================
set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: 检查当前目录是否与脚本目录相同
cd
set "CURRENT_DIR=%CD%"
if /i not "%CURRENT_DIR%"=="%SCRIPT_DIR%" (
    echo [INFO] 切换到脚本目录: %SCRIPT_DIR%
    cd /d "%SCRIPT_DIR%" 2>nul
    if %errorlevel% neq 0 (
        echo [ERROR] 无法切换到脚本目录
        echo [INFO] 请手动切换到目录: %SCRIPT_DIR%
        pause
        exit /b 1
    )
)

echo [INFO] 工作目录: %CD%
echo.

:: ============================================
:: Configuration Section - No external .ini files
:: ============================================
set "CONFIG_FILE=FastNavGenerator.json"
set "OUTPUT_FILE=index.html"
set "SERVER_PORT=8080"
set "AUTO_OPEN=true"
set "ENABLE_NETWORKING=true"
set "START_ON_BOOT=true"
set "SERVICE_NAME=FastNavWebService"
set "SERVICE_DISPLAY_NAME=FastNav Web Service"
set "SERVICE_DESCRIPTION=Auto-generate and serve navigation website"
set "TITLE=Embedded Development Center"
set "DEFAULT_LAYOUT=list"
:: ============================================

title FastNav Generator - v3.7
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
echo.
echo ========================================
echo.
echo 1. Generate HTML Website
echo 2. Start Local Server
echo 3. Install as System Service (Daemon)
echo 4. Uninstall System Service
echo 5. Check for Updates
echo 6. Config Management
echo 7. Start and Open in Browser
echo 8. Open Generated File
echo 9. Exit
echo.
set /p choice="Select operation (1-9): "

if "%choice%"=="1" call :GENERATE_WEBSITE && goto MENU_MAIN
if "%choice%"=="2" call :START_SERVER && goto MENU_MAIN
if "%choice%"=="3" call :INSTALL_SERVICE && goto MENU_MAIN
if "%choice%"=="4" call :UNINSTALL_SERVICE && goto MENU_MAIN
if "%choice%"=="5" call :CHECK_UPDATE && goto MENU_MAIN
if "%choice%"=="6" call :MANAGE_CONFIG && goto MENU_MAIN
if "%choice%"=="7" call :START_AND_OPEN && goto MENU_MAIN
if "%choice%"=="8" call :OPEN_FILE && goto MENU_MAIN
if "%choice%"=="9" exit /b 0

echo [ERROR] Invalid selection
timeout /t 2 >nul
goto MENU_MAIN
:: ============================================

:INITIALIZE
:: Check Python environment
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found, please install Python 3.6+
    echo [INFO] Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check required files
if not exist "FastNavGenerator.py" (
    echo [ERROR] Main program file not found: FastNavGenerator.py
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
python -c "import json; f = open('!CONFIG_FILE!', 'r', encoding='utf-8'); data = json.load(f); f.close(); print('[OK] Config file syntax is valid')"
if %errorlevel% neq 0 (
    echo [ERROR] Config file has syntax errors
    pause
    exit /b 1
)

:: Generate website
python FastNavGenerator.py --config "!CONFIG_FILE!" --output "!OUTPUT_FILE!"

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Website generated: !OUTPUT_FILE!
    echo [INFO] File location: %CD%\!OUTPUT_FILE!
) else (
    echo.
    echo [ERROR] Website generation failed!
)

echo.
pause
exit /b 0

:START_SERVER
cls
echo.
echo [SERVER] Starting local server...
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

:: Start server
start cmd /k "title FastNav Server - Port:!SERVER_PORT! && echo [INFO] Server running... && echo [URL] http://localhost:!SERVER_PORT! && echo [INFO] Press Ctrl+C to stop && python -m http.server !SERVER_PORT!"

if "!AUTO_OPEN!"=="true" (
    timeout /t 1 >nul
    start "" "http://localhost:!SERVER_PORT!"
)

echo.
echo [INFO] Server started in new window
echo [INFO] Return to main menu...
timeout /t 3 >nul
exit /b 0

:GENERATE_WEBSITE_SILENT
python FastNavGenerator.py --config "!CONFIG_FILE!" --output "!OUTPUT_FILE!" >nul 2>&1
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

:INSTALL_SERVICE
cls
echo.
echo [INSTALL] Installing as system service...
echo.

:: Check admin rights
call :CHECK_ADMIN
if !IS_ADMIN! neq 1 (
    echo [ERROR] Administrator rights required
    echo [INFO] Right-click and "Run as administrator"
    pause
    exit /b 0
)

:: First check for FastNavService.exe (compiled version)
if exist "FastNavService.exe" (
    echo [INFO] Found compiled service executable
    set "SERVICE_CMD=FastNavService.exe"
) else if exist "FastNavService.py" (
    echo [INFO] Using Python script (compiled version not found)
    set "SERVICE_CMD=python FastNavService.py"
) else (
    echo [ERROR] Service file not found
    echo [INFO] Neither FastNavService.exe nor FastNavService.py exists
    pause
    exit /b 1
)

:: Stop existing service (if exists)
echo [INFO] Stopping existing service...
sc stop "%SERVICE_NAME%" >nul 2>&1
timeout /t 2 >nul

:: Install service
echo [INFO] Installing service using: %SERVICE_CMD%
%SERVICE_CMD% install

if %errorlevel% equ 0 (
    echo [SUCCESS] Service installed successfully

    if "!START_ON_BOOT!"=="true" (
        echo [INFO] Starting service...
        net start "%SERVICE_NAME%"
        timeout /t 2 >nul
        sc query "%SERVICE_NAME%" | findstr /c:"RUNNING" >nul
        if %errorlevel% equ 0 (
            echo [SUCCESS] Service started and running
        ) else (
            echo [WARNING] Service installed but failed to start
            echo [INFO] Start manually: net start %SERVICE_NAME%
        )
    )

    echo.
    echo [INFO] Service management commands:
    echo   Start: net start %SERVICE_NAME%
    echo   Stop: net stop %SERVICE_NAME%
    echo   Restart: net stop %SERVICE_NAME% && net start %SERVICE_NAME%
    echo   Remove: sc delete %SERVICE_NAME%

) else (
    echo [ERROR] Service installation failed
    echo [INFO] Possible issues:
    echo   1. Missing pywin32 dependency (if using Python script)
    echo   2. Administrator rights required
    echo   3. Service already exists
)

echo.
pause
call :CHECK_SERVICE_STATUS
exit /b 0

:UNINSTALL_SERVICE
cls
echo.
echo [UNINSTALL] Removing system service...
echo.

:: Check admin rights
call :CHECK_ADMIN
if !IS_ADMIN! neq 1 (
    echo [ERROR] Administrator rights required
    pause
    exit /b 0
)

:: First check for FastNavService.exe (compiled version)
if exist "FastNavService.exe" (
    echo [INFO] Found compiled service executable
    set "SERVICE_CMD=FastNavService.exe"
) else if exist "FastNavService.py" (
    echo [INFO] Using Python script (compiled version not found)
    set "SERVICE_CMD=python FastNavService.py"
) else (
    echo [WARNING] Service file not found, using system commands
    set "SERVICE_CMD="
)

:: Stop and remove service
echo [INFO] Stopping service...
sc stop "%SERVICE_NAME%" >nul 2>&1
timeout /t 2 >nul

echo [INFO] Removing service...
if defined SERVICE_CMD (
    %SERVICE_CMD% remove
) else (
    sc delete "%SERVICE_NAME%"
)

if %errorlevel% equ 0 (
    echo [SUCCESS] Service removed successfully
) else (
    echo [WARNING] Service may not exist or already removed
)

echo.
pause
call :CHECK_SERVICE_STATUS
exit /b 0

:CHECK_ADMIN
set "IS_ADMIN=0"
net session >nul 2>&1
if %errorlevel% equ 0 set "IS_ADMIN=1"
exit /b 0

:CREATE_SERVICE_SCRIPT
(
echo import win32serviceutil
echo import win32service
echo import win32event
echo import servicemanager
echo import socket
echo import time
echo import os
echo import sys
echo import threading
echo from http.server import HTTPServer, SimpleHTTPRequestHandler
echo.
echo class FastNavService(win32serviceutil.ServiceFramework):
echo     _svc_name_ = "FastNavWebService"
echo     _svc_display_name_ = "FastNav Web Service"
echo     _svc_description_ = "Auto-generate and serve navigation website"
echo.
echo     def __init__(self, args):
echo         win32serviceutil.ServiceFramework.__init__(self, args)
echo         self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
echo         self.is_running = True
echo.
echo     def SvcStop(self):
echo         self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
echo         win32event.SetEvent(self.hWaitStop)
echo         self.is_running = False
echo.
echo     def SvcDoRun(self):
echo         servicemanager.LogMsg(
echo             servicemanager.EVENTLOG_INFORMATION_TYPE,
echo             servicemanager.PYSERVICE_SERVICE_STARTED,
echo             (self._svc_name_, '')
echo         )
echo         self.main()
echo.
echo     def main(self):
echo         port = 8080
echo         os.chdir(os.path.dirname(os.path.abspath(__file__)))
echo.
echo         class Handler(SimpleHTTPRequestHandler):
echo             def __init__(self, *args, **kwargs):
echo                 super().__init__(*args, directory=os.getcwd(), **kwargs)
echo.
echo         server = HTTPServer(('', port), Handler)
echo         server_thread = threading.Thread(target=server.serve_forever, daemon=True)
echo         server_thread.start()
echo.
echo         while self.is_running:
echo             time.sleep(1)
echo         server.shutdown()
echo.
echo if __name__ == '__main__':
echo     if len(sys.argv) == 1:
echo         servicemanager.Initialize()
echo         servicemanager.PrepareToHostSingle(FastNavService)
echo         servicemanager.StartServiceCtrlDispatcher()
echo     elif sys.argv[1] == 'install':
echo         win32serviceutil.InstallService(
echo             None,
echo             "FastNavWebService",
echo             "FastNav Web Service",
echo             description="Auto-generate and serve navigation website",
echo             startType=win32service.SERVICE_AUTO_START
echo         )
echo         print('[SUCCESS] Service installed')
echo     elif sys.argv[1] == 'remove':
echo         win32serviceutil.RemoveService("FastNavWebService")
echo         print('[SUCCESS] Service removed')
) > FastNavService.py

echo [INFO] Service script created: FastNavService.py
exit /b 0

:CHECK_UPDATE
cls
echo.
echo [UPDATE] Checking for updates...
echo.
echo [INFO] Current Version: v3.7
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
echo 5. Return to Main Menu
echo.
set /p choice="Select: "

if "%choice%"=="1" goto EDIT_CONFIG
if "%choice%"=="2" goto CREATE_EXAMPLE
if "%choice%"=="3" goto CHANGE_PORT
if "%choice%"=="4" goto TOGGLE_AUTOOPEN
if "%choice%"=="5" exit /b 0

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
    echo [SUCCESS] Port changed to: %SERVER_PORT%
) else (
    echo [WARNING] No change made
)
pause
goto MENU_CONFIG

:TOGGLE_AUTOOPEN
if "%AUTO_OPEN%"=="true" (
    set "AUTO_OPEN=false"
    echo [INFO] Auto-open browser disabled
) else (
    set "AUTO_OPEN=true"
    echo [INFO] Auto-open browser enabled
)
pause
goto MENU_CONFIG

:CREATE_DEFAULT_CONFIG
(
echo {
echo     "site": {
echo         "title": "%TITLE%",
echo         "default_layout": "%DEFAULT_LAYOUT%"
echo     },
echo     "categories": [
echo         {
echo             "name": "Development Tools",
echo             "icon": "🛠️",
echo             "type": "normal"
echo         },
echo         {
echo             "name": "Release Notes",
echo             "icon": "📋",
echo             "type": "ReleaseNotes"
echo         },
echo         {
echo             "name": "Interface Map",
echo             "icon": "📊",
echo             "type": "InterfaceMap"
echo         },
echo         {
echo             "name": "Configuration Docs",
echo             "icon": "📖",
echo             "type": "ConfigDocs"
echo         },
echo         {
echo             "name": "Icons Reference",
echo             "icon": "🎨",
echo             "type": "IconsReference"
echo         }
echo     ],
echo     "normal": {
echo         "Development Tools": {
echo             "links": [
echo                 {
echo                     "name": "Visual Studio Code",
echo                     "url": "https://code.visualstudio.com/",
echo                     "description": "Lightweight powerful code editor",
echo                     "type": "Editor",
echo                     "tag": "IDE"
echo                 },
echo                 {
echo                     "name": "Python Official",
echo                     "url": "https://www.python.org/",
echo                     "description": "Python programming language official site",
echo                     "type": "Programming",
echo                     "tag": "Python"
echo                 }
echo             ]
echo         }
echo     }
echo }
) > "%CONFIG_FILE%"
exit /b 0