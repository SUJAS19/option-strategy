@echo off
REM NIFTY Options Trading Dashboard - Windows
REM Professional web dashboard

echo.
echo ================================================================
echo    NIFTY OPTIONS TRADING DASHBOARD
echo ================================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found. Please run deploy.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo [ERROR] .env file not found. Please copy env_example.txt to .env and configure it.
    pause
    exit /b 1
)

REM Create session log
set SESSION_LOG=logs\dashboard_session_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
echo [INFO] Dashboard log: %SESSION_LOG%

REM Display system information
echo [INFO] Dashboard Information:
echo   Python Version: 
python --version
echo   Working Directory: %CD%
echo   Virtual Environment: %CD%\venv
echo   Dashboard Port: 8050
echo.

REM Check if port 8050 is available
netstat -an | find "8050" >nul 2>&1
if %errorlevel% equ 0 (
    echo [WARNING] Port 8050 is already in use. Trying port 8051...
    set DASHBOARD_PORT=8051
) else (
    set DASHBOARD_PORT=8050
)

REM Display dashboard features
echo [INFO] Dashboard Features:
echo   Real-time NIFTY spot price and volatility
echo   Live portfolio performance and P&L
echo   Interactive trading controls
echo   Risk metrics and alerts
echo   Strategy performance charts
echo   Options chain data
echo   Market indicators and analysis
echo.

REM Start the dashboard
echo [DASHBOARD] Starting NIFTY Options Trading Dashboard...
echo [DASHBOARD] Dashboard URL: http://localhost:%DASHBOARD_PORT%
echo [DASHBOARD] Auto-refresh: Every 30 seconds
echo [DASHBOARD] Mobile-friendly interface
echo.

echo [SUCCESS] Dashboard starting successfully!
echo [INFO] Press Ctrl+C to stop dashboard
echo.

REM Run the dashboard
python dashboard.py > %SESSION_LOG% 2>&1

echo.
echo [INFO] Dashboard session ended.
echo [INFO] Dashboard log saved to: %SESSION_LOG%
echo [INFO] Thank you for using NIFTY Options Trading Dashboard!
pause
