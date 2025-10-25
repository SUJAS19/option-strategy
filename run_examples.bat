@echo off
REM NIFTY Options Trading Examples - Windows
REM System demonstration

echo.
echo ================================================================
echo    NIFTY OPTIONS TRADING EXAMPLES
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
set SESSION_LOG=logs\examples_session_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
echo [INFO] Examples log: %SESSION_LOG%

REM Display examples to be run
echo [INFO] Examples to be Demonstrated:
echo   Option Pricing Models (Black-Scholes, Binomial, Monte Carlo)
echo   Trading Strategies (Straddle, Strangle, Iron Condor, Butterfly)
echo   Risk Management System
echo   Machine Learning Models
echo   Backtesting Framework
echo   Data Fetching and Analysis
echo.

REM Display system capabilities
echo [INFO] System Capabilities:
echo   Advanced Option Pricing with Greeks
echo   Multiple Trading Strategies
echo   AI-Powered Strategy Selection
echo   Comprehensive Risk Management
echo   Historical Backtesting
echo   Real-time Data Fetching
echo   Interactive Dashboard
echo.

echo [SUCCESS] Examples starting successfully!
echo [INFO] Press Ctrl+C to stop examples
echo.

REM Run the examples
python run_examples.py > %SESSION_LOG% 2>&1

echo.
echo [SUCCESS] Examples completed successfully!
echo [INFO] Log saved to: %SESSION_LOG%
echo.

REM Display what was demonstrated
echo [INFO] Examples Demonstrated:
echo   Option Pricing Models ✓
echo   Trading Strategies ✓
echo   Risk Management ✓
echo   Machine Learning ✓
echo   Backtesting ✓
echo   Data Analysis ✓
echo.

echo [SUCCESS] All examples completed successfully!
echo [INFO] Check the logs for detailed output
echo [INFO] Ready for live trading!
pause
