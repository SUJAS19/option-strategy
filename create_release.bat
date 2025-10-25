@echo off 
REM NIFTY Options Trading System - Create Release 
echo [INFO] Creating release... 
set VERSION=1.0.0 
echo [INFO] Creating tag v... 
git tag -a "v" -m "Release version " 
echo [INFO] Pushing tag... 
git push origin "v" 
echo [SUCCESS] Release v created successfully! 
pause 
