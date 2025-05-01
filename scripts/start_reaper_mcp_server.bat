@echo off
REM Start REAPER MCP Server
REM This script starts the REAPER MCP server in the appropriate mode

REM Default settings
set MODE=osc
set HOST=127.0.0.1
set SEND_PORT=8000
set RECEIVE_PORT=9000
set TRANSPORT=stdio
set DEBUG=false

REM Parse command line arguments
:parse_args
if "%~1"=="" goto end_parse_args
set arg=%~1
if "%arg:~0,7%"=="--mode=" (
    set MODE=%arg:~7%
) else if "%arg:~0,7%"=="--host=" (
    set HOST=%arg:~7%
) else if "%arg:~0,12%"=="--send-port=" (
    set SEND_PORT=%arg:~12%
) else if "%arg:~0,15%"=="--receive-port=" (
    set RECEIVE_PORT=%arg:~15%
) else if "%arg:~0,12%"=="--transport=" (
    set TRANSPORT=%arg:~12%
) else if "%arg%"=="--debug" (
    set DEBUG=true
) else (
    echo Unknown option: %arg%
    exit /b 1
)
shift
goto parse_args
:end_parse_args

REM Check if REAPER is running
tasklist /FI "IMAGENAME eq reaper.exe" 2>NUL | find /I /N "reaper.exe">NUL
if "%ERRORLEVEL%"=="1" (
    echo Starting REAPER...
    start "" "C:\Program Files\REAPER\reaper.exe"
    REM Give REAPER time to start up
    timeout /t 3 /nobreak > nul
)

REM Activate the Python virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Set debug flag if needed
set DEBUG_FLAG=
if "%DEBUG%"=="true" (
    set DEBUG_FLAG=--debug
)

REM Run the MCP server with the specified options
echo Starting REAPER MCP Server in %MODE% mode...
python -m reaper_mcp --mode=%MODE% --host=%HOST% --send-port=%SEND_PORT% --receive-port=%RECEIVE_PORT% --transport=%TRANSPORT% %DEBUG_FLAG%

REM Keep the window open if there's an error
if %ERRORLEVEL% neq 0 (
    echo Error occurred. Press any key to exit...
    pause > nul
)
