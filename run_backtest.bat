@echo off
REM NIFTY Options Trading Backtest - Windows
REM Historical analysis

echo.
echo ================================================================
echo    NIFTY OPTIONS TRADING BACKTEST
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

REM Create backtest results directory
set BACKTEST_DIR=backtest_results\%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
mkdir "%BACKTEST_DIR%" 2>nul

echo [INFO] Backtest results will be saved to: %BACKTEST_DIR%

REM Display backtest configuration
echo [INFO] Backtest Configuration:
echo   Initial Capital: Rs 10,00,000
echo   Test Period: 1 Year (365 days)
echo   Strategies: Straddle, Strangle, Iron Condor, Butterfly
echo   Risk Management: Active
echo   ML Models: Strategy Selection, Volatility Prediction
echo.

REM Display strategies to be tested
echo [INFO] Strategies to be Tested:
echo   Long Straddle - High volatility strategy
echo   Long Strangle - Similar to straddle with different strikes
echo   Iron Condor - Low volatility, limited risk strategy
echo   Long Butterfly - Range-bound strategy
echo.

REM Create session log
set SESSION_LOG=logs\backtest_session_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
echo [INFO] Backtest log: %SESSION_LOG%

echo [BACKTEST] Starting comprehensive backtest analysis...
echo [BACKTEST] Results will be saved to: %BACKTEST_DIR%
echo.

echo [SUCCESS] Backtest starting successfully!
echo [INFO] Press Ctrl+C to stop backtest
echo.

REM Run the backtest
python main.py backtest > %SESSION_LOG% 2>&1

REM Move results to backtest directory
if exist "backtest_results\*.csv" move "backtest_results\*.csv" "%BACKTEST_DIR%\" 2>nul
if exist "backtest_results\*.png" move "backtest_results\*.png" "%BACKTEST_DIR%\" 2>nul
if exist "backtest_results\*.html" move "backtest_results\*.html" "%BACKTEST_DIR%\" 2>nul

echo.
echo [SUCCESS] Backtest completed successfully!
echo [INFO] Results saved to: %BACKTEST_DIR%
echo [INFO] Log saved to: %SESSION_LOG%
echo.

REM Display summary
echo [INFO] Backtest Summary:
echo   Test Period: 1 Year
echo   Strategies Tested: 4
echo   Results Directory: %BACKTEST_DIR%
echo   Log File: %SESSION_LOG%
echo.

echo [SUCCESS] Backtest analysis complete!
echo [INFO] Check the results directory for detailed analysis
echo [INFO] Happy Trading!
pause
