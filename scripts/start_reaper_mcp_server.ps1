# Start REAPER MCP Server
# This script starts the REAPER MCP server in the appropriate mode

param (
    [string]$mode = "osc",
    [string]$host = "127.0.0.1",
    [int]$sendPort = 8000,
    [int]$receivePort = 9000,
    [string]$transport = "stdio",
    [switch]$debug = $false
)

# Check if REAPER is running
$reaperRunning = Get-Process -Name "reaper" -ErrorAction SilentlyContinue
if (-not $reaperRunning) {
    Write-Host "Starting REAPER..."
    Start-Process "C:\Program Files\REAPER\reaper.exe"
    # Give REAPER time to start up
    Start-Sleep -Seconds 3
}

# Activate the Python virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..."
    & "venv\Scripts\Activate.ps1"
}

# Set debug flag if needed
$debugFlag = ""
if ($debug) {
    $debugFlag = "--debug"
}

# Run the MCP server with the specified options
Write-Host "Starting REAPER MCP Server in $mode mode..."
$arguments = @(
    "-m", "reaper_mcp",
    "--mode=$mode",
    "--host=$host",
    "--send-port=$sendPort",
    "--receive-port=$receivePort",
    "--transport=$transport"
)

if ($debug) {
    $arguments += "--debug"
}

# Start Python with the arguments
& python $arguments

# If there's an error, keep the window open
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error occurred. Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
