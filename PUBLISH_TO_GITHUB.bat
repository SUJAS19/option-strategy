@echo off
REM NIFTY Options Trading System - GitHub Publishing Script
REM This script helps you publish to GitHub

echo.
echo ================================================================
echo    PUBLISHING TO GITHUB - STEP BY STEP GUIDE
echo ================================================================
echo.

echo [STEP 1] Open your web browser and go to:
echo https://github.com/new
echo.
echo [STEP 2] Fill in the repository details:
echo   Repository name: nifty-options-trading
echo   Description: Advanced Algorithmic Trading System for NIFTY Options with Machine Learning
echo   Visibility: Public (recommended)
echo   DO NOT check "Initialize this repository with a README"
echo.
echo [STEP 3] Click "Create repository"
echo.
echo Press any key when you have created the repository...
pause >nul

echo.
echo [STEP 4] Copy your repository URL from GitHub
echo It should look like: https://github.com/YOUR_USERNAME/nifty-options-trading.git
echo.
set /p REPO_URL="Paste your repository URL here: "

echo.
echo [STEP 5] Connecting to GitHub...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

if %errorlevel% neq 0 (
    echo [ERROR] Failed to add remote. Please check the URL.
    pause
    exit /b 1
)

echo [SUCCESS] Remote added successfully!

echo.
echo [STEP 6] Pushing to GitHub...
git branch -M main
git push -u origin main

if %errorlevel% neq 0 (
    echo [ERROR] Failed to push to GitHub.
    echo.
    echo Common issues:
    echo 1. Check your GitHub credentials
    echo 2. Make sure the repository URL is correct
    echo 3. Ensure you have internet connection
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo    SUCCESS! PUBLISHED TO GITHUB!
echo ================================================================
echo.
echo [SUCCESS] Your NIFTY Options Trading System is now on GitHub!
echo.
echo Your repository: %REPO_URL%
echo.
echo Next steps:
echo 1. Visit your repository on GitHub
echo 2. Set up Issues and Discussions
echo 3. Configure branch protection
echo 4. Add collaborators (if needed)
echo 5. Share with the community!
echo.
echo Available commands:
echo   run_trading.bat      - Start live trading
echo   run_dashboard.bat    - Launch dashboard
echo   run_backtest.bat     - Run backtesting
echo.
echo Happy Trading! 
echo.
pause
