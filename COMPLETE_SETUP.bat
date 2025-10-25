@echo off
REM NIFTY Options Trading System - Complete Setup and Publishing
REM This script completes everything in one go

echo.
echo ================================================================
echo    NIFTY OPTIONS TRADING SYSTEM - COMPLETE SETUP
echo ================================================================
echo.

REM Step 1: Deploy the system
echo [STEP 1/5] Deploying the system...
call deploy.bat
if %errorlevel% neq 0 (
    echo [ERROR] Deployment failed!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] System deployed successfully!
echo.

REM Step 2: Run examples to verify
echo [STEP 2/5] Running examples to verify system...
call run_examples.bat
if %errorlevel% neq 0 (
    echo [ERROR] Examples failed!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Examples completed successfully!
echo.

REM Step 3: Git setup
echo [STEP 3/5] Setting up Git repository...
git status >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Initializing Git repository...
    git init
    git add .
    git commit -m "Complete NIFTY Options Trading System"
)

echo [SUCCESS] Git repository ready!
echo.

REM Step 4: Display GitHub instructions
echo [STEP 4/5] GitHub Publishing Instructions
echo ================================================================
echo.
echo To publish to GitHub, follow these steps:
echo.
echo 1. Create GitHub Repository:
echo    - Go to: https://github.com/new
echo    - Repository name: nifty-options-trading
echo    - Description: Advanced Algorithmic Trading System for NIFTY Options with Machine Learning
echo    - Make it Public
echo    - Click "Create repository"
echo.
echo 2. Connect and Push:
echo    git remote add origin https://github.com/YOUR_USERNAME/nifty-options-trading.git
echo    git push -u origin main
echo.
echo ================================================================
echo.

REM Step 5: Create quick reference
echo [STEP 5/5] Creating quick reference guide...

echo # NIFTY Options Trading System - Quick Reference > QUICK_START.md
echo. >> QUICK_START.md
echo ## Quick Commands: >> QUICK_START.md
echo. >> QUICK_START.md
echo ### Deploy System: >> QUICK_START.md
echo ```cmd >> QUICK_START.md
echo deploy.bat >> QUICK_START.md
echo ``` >> QUICK_START.md
echo. >> QUICK_START.md
echo ### Run Examples: >> QUICK_START.md
echo ```cmd >> QUICK_START.md
echo run_examples.bat >> QUICK_START.md
echo ``` >> QUICK_START.md
echo. >> QUICK_START.md
echo ### Start Trading: >> QUICK_START.md
echo ```cmd >> QUICK_START.md
echo run_trading.bat >> QUICK_START.md
echo ``` >> QUICK_START.md
echo. >> QUICK_START.md
echo ### Launch Dashboard: >> QUICK_START.md
echo ```cmd >> QUICK_START.md
echo run_dashboard.bat >> QUICK_START.md
echo ``` >> QUICK_START.md
echo. >> QUICK_START.md
echo ### Run Backtest: >> QUICK_START.md
echo ```cmd >> QUICK_START.md
echo run_backtest.bat >> QUICK_START.md
echo ``` >> QUICK_START.md
echo. >> QUICK_START.md
echo ## System Features: >> QUICK_START.md
echo - Advanced Option Pricing Models >> QUICK_START.md
echo - Multiple Trading Strategies >> QUICK_START.md
echo - Machine Learning Integration >> QUICK_START.md
echo - Comprehensive Risk Management >> QUICK_START.md
echo - Real-time Trading Engine >> QUICK_START.md
echo - Interactive Web Dashboard >> QUICK_START.md

echo [SUCCESS] Quick reference created!
echo.

REM Final summary
echo ================================================================
echo    COMPLETE SETUP FINISHED SUCCESSFULLY!
echo ================================================================
echo.
echo [SUCCESS] Your NIFTY Options Trading System is ready!
echo.
echo Available Commands:
echo   run_trading.bat      - Start live trading
echo   run_dashboard.bat    - Start web dashboard
echo   run_backtest.bat     - Run backtesting
echo   run_examples.bat     - Run examples
echo.
echo Documentation:
echo   README.md                    - Complete documentation
echo   DEPLOYMENT_GUIDE.md          - Deployment guide
echo   GITHUB_PUBLISHING_GUIDE.md   - GitHub setup
echo   NEXT_STEPS.md                - Next steps
echo   QUICK_START.md               - Quick reference
echo.
echo Dashboard: http://localhost:8050
echo.
echo [INFO] To publish to GitHub, follow the instructions above
echo.
pause
