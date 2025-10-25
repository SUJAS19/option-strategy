@echo off
REM NIFTY Options Trading System - Windows Deployment Script
REM Professional deployment for Windows systems

echo.
echo ================================================================
echo    NIFTY OPTIONS TRADING SYSTEM - DEPLOYMENT
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [INFO] Python found ✓

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not available. Please install pip.
    pause
    exit /b 1
)

echo [INFO] pip found ✓

REM Create virtual environment
echo [INFO] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)

echo [INFO] Virtual environment created ✓

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [INFO] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo [INFO] Dependencies installed ✓

REM Create necessary directories
echo [INFO] Creating project directories...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "backtest_results" mkdir backtest_results
if not exist "trades" mkdir trades
if not exist "positions" mkdir positions
if not exist "screenshots" mkdir screenshots
if not exist "reports" mkdir reports
if not exist "models" mkdir models

echo [INFO] Directories created ✓

REM Create environment file if it doesn't exist
if not exist ".env" (
    echo [INFO] Creating environment file...
    copy env_example.txt .env
    echo [WARNING] Please edit .env file with your API credentials
)

REM Test installation
echo [INFO] Testing installation...
python -c "import numpy, pandas, sklearn, xgboost, lightgbm; print('All dependencies imported successfully')"
if %errorlevel% neq 0 (
    echo [ERROR] Installation test failed.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo    DEPLOYMENT COMPLETED SUCCESSFULLY!
echo ================================================================
echo.
echo [SUCCESS] NIFTY Options Trading System is ready!
echo.
echo Available Commands:
echo   run_examples.bat     - Run system examples
echo   run_trading.bat      - Start live trading
echo   run_dashboard.bat    - Start web dashboard
echo   run_backtest.bat     - Run backtesting
echo.
echo Dashboard will be available at: http://localhost:8050
echo.
pause
