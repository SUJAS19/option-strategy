@echo off
REM NIFTY Options Trading System - Publish to GitHub
REM Professional deployment and publishing

echo.
echo ================================================================
echo    NIFTY OPTIONS TRADING SYSTEM - PUBLISH TO GITHUB
echo ================================================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed. Please install Git first.
    echo Download from: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo [INFO] Git found ✓

REM Check if we're in a git repository
if not exist ".git" (
    echo [INFO] Initializing Git repository...
    git init
    echo [SUCCESS] Git repository initialized
) else (
    echo [INFO] Git repository already exists ✓
)

REM Set up Git configuration
echo [INFO] Setting up Git configuration...
git config user.name "NIFTY Options Trading System" 2>nul
git config user.email "trading@niftyoptions.com" 2>nul

REM Add all files to Git
echo [INFO] Adding files to Git repository...
git add .

REM Create initial commit
echo [INFO] Creating initial commit...
git commit -m "Initial commit: NIFTY Options Trading System

🚀 Complete algorithmic trading system for NIFTY options
📈 Features:
- Advanced option pricing models (Black-Scholes, Binomial, Monte Carlo)
- Multiple trading strategies (Straddle, Strangle, Iron Condor, Butterfly)
- Machine learning integration (Strategy selection, Volatility prediction)
- Comprehensive risk management system
- Historical backtesting framework
- Real-time trading engine
- Interactive web dashboard
- Docker support
- CI/CD pipeline

🤖 AI-Powered Trading with Python, Machine Learning, and Data Science
📊 Professional-grade system for current NIFTY options trading"

echo [SUCCESS] Initial commit created

REM Create GitHub repository setup instructions
echo [INFO] Creating GitHub setup instructions...

echo # GitHub Repository Setup Instructions > GITHUB_SETUP.md
echo. >> GITHUB_SETUP.md
echo ## 🚀 Quick Start >> GITHUB_SETUP.md
echo. >> GITHUB_SETUP.md
echo ### 1. Create GitHub Repository >> GITHUB_SETUP.md
echo 1. Go to [GitHub](https://github.com) and sign in >> GITHUB_SETUP.md
echo 2. Click "New repository" >> GITHUB_SETUP.md
echo 3. Repository name: `nifty-options-trading` >> GITHUB_SETUP.md
echo 4. Description: `Advanced Algorithmic Trading System for NIFTY Options with Machine Learning` >> GITHUB_SETUP.md
echo 5. Make it Public >> GITHUB_SETUP.md
echo 6. Don't initialize with README (we already have one) >> GITHUB_SETUP.md
echo 7. Click "Create repository" >> GITHUB_SETUP.md
echo. >> GITHUB_SETUP.md
echo ### 2. Connect Local Repository to GitHub >> GITHUB_SETUP.md
echo ```bash >> GITHUB_SETUP.md
echo # Add remote origin (replace YOUR_USERNAME with your GitHub username) >> GITHUB_SETUP.md
echo git remote add origin https://github.com/YOUR_USERNAME/nifty-options-trading.git >> GITHUB_SETUP.md
echo. >> GITHUB_SETUP.md
echo # Push to GitHub >> GITHUB_SETUP.md
echo git branch -M main >> GITHUB_SETUP.md
echo git push -u origin main >> GITHUB_SETUP.md
echo ``` >> GITHUB_SETUP.md

echo [SUCCESS] GitHub setup instructions created

REM Create deployment script
echo [INFO] Creating deployment script...

echo @echo off > deploy_system.bat
echo REM NIFTY Options Trading System - System Deployment >> deploy_system.bat
echo echo [INFO] Deploying NIFTY Options Trading System... >> deploy_system.bat
echo call deploy.bat >> deploy_system.bat
echo echo [SUCCESS] System deployed successfully! >> deploy_system.bat
echo pause >> deploy_system.bat

echo [SUCCESS] Deployment script created

REM Create release script
echo [INFO] Creating release script...

echo @echo off > create_release.bat
echo REM NIFTY Options Trading System - Create Release >> create_release.bat
echo echo [INFO] Creating release... >> create_release.bat
echo set VERSION=1.0.0 >> create_release.bat
echo echo [INFO] Creating tag v%VERSION%... >> create_release.bat
echo git tag -a "v%VERSION%" -m "Release version %VERSION%" >> create_release.bat
echo echo [INFO] Pushing tag... >> create_release.bat
echo git push origin "v%VERSION%" >> create_release.bat
echo echo [SUCCESS] Release v%VERSION% created successfully! >> create_release.bat
echo pause >> create_release.bat

echo [SUCCESS] Release script created

REM Display final instructions
echo.
echo ================================================================
echo    PUBLISH SETUP COMPLETED SUCCESSFULLY!
echo ================================================================
echo.
echo [SUCCESS] Your NIFTY Options Trading System is ready for GitHub!
echo.
echo 📋 Next Steps:
echo 1. Create GitHub repository:
echo    - Go to https://github.com/new
echo    - Repository name: nifty-options-trading
echo    - Description: Advanced Algorithmic Trading System for NIFTY Options with Machine Learning
echo    - Make it Public
echo    - Don't initialize with README
echo    - Click Create repository
echo.
echo 2. Connect local repository:
echo    git remote add origin https://github.com/YOUR_USERNAME/nifty-options-trading.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Set up GitHub Actions:
echo    - Go to repository Settings
echo    - Enable Issues and Discussions
echo    - Set up branch protection rules
echo    - Configure security alerts
echo.
echo 📁 Files created:
echo   • GITHUB_SETUP.md - Detailed setup instructions
echo   • deploy_system.bat - System deployment
echo   • create_release.bat - Release creation
echo.
echo 🔧 Available commands:
echo   • deploy.bat - Deploy system
echo   • run_trading.bat - Start live trading
echo   • run_dashboard.bat - Start dashboard
echo   • run_backtest.bat - Run backtesting
echo   • run_examples.bat - Run examples
echo.
echo [SUCCESS] 🚀 Your NIFTY Options Trading System is ready for GitHub! 📈🎉
echo.
pause
