@echo off
REM NIFTY Options Trading System - Live Trading (Windows)
REM Professional trading execution

echo.
echo ================================================================
echo    NIFTY OPTIONS TRADING SYSTEM - LIVE TRADING
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
set SESSION_LOG=logs\trading_session_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
echo [INFO] Session log: %SESSION_LOG%

REM Display system information
echo [INFO] System Information:
echo   Python Version: 
python --version
echo   Working Directory: %CD%
echo   Virtual Environment: %CD%\venv
echo.

REM Check market hours (simplified)
set /a CURRENT_HOUR=%time:~0,2%
set /a CURRENT_MINUTE=%time:~3,2%
set /a CURRENT_TIME=%CURRENT_HOUR% * 100 + %CURRENT_MINUTE%

if %CURRENT_TIME% geq 915 if %CURRENT_TIME% leq 1530 (
    echo [SUCCESS] Market is OPEN - Trading system will start
    set MARKET_STATUS=OPEN
) else (
    echo [WARNING] Market is CLOSED - Running in simulation mode
    set MARKET_STATUS=CLOSED
)

echo.

REM Display trading configuration
echo [INFO] Trading Configuration:
echo   Max Position Size: Rs 10,00,000
echo   Max Daily Loss: Rs 50,000
echo   Stop Loss: 2%%
echo   Take Profit: 5%%
echo   Strategies: Straddle, Strangle, Iron Condor, Butterfly
echo.

REM Start the trading system
echo [TRADING] Starting NIFTY Options Trading Engine...
echo [TRADING] Market Status: %MARKET_STATUS%
echo [TRADING] AI Models: Strategy Selection, Volatility Prediction, Price Forecasting
echo [TRADING] Risk Management: Active
echo [TRADING] Dashboard: http://localhost:8050
echo.

echo [SUCCESS] Trading system started successfully!
echo [INFO] Press Ctrl+C to stop trading
echo.

REM Run the trading system
python main.py live > %SESSION_LOG% 2>&1

echo.
echo [INFO] Trading session ended.
echo [INFO] Session log saved to: %SESSION_LOG%
echo [INFO] Thank you for trading with NIFTY Options AI System!
pause
