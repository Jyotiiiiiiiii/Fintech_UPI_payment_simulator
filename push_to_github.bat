@echo off
REM GitHub Push Script for UPI Payment System
REM Run this file to push your project to GitHub

cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         GitHub Push Setup - UPI Payment System            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo This script will help you push your code to GitHub.
echo.

REM Check if git is installed
git --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com
    pause
    exit /b 1
)

REM Get GitHub username
set /p GITHUB_USER="Enter your GitHub username: "

if "%GITHUB_USER%"=="" (
    echo.
    echo You need a GitHub account first:
    echo   1. Go to https://github.com
    echo   2. Click 'Sign up'
    echo   3. Complete the registration
    echo   4. Run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo GitHub username: %GITHUB_USER%
echo.

REM Get name and email
set /p NAME="Enter your name (for commits): "
set /p EMAIL="Enter your email (for commits): "

echo.
echo Configuring Git...
git config --global user.name "%NAME%"
git config --global user.email "%EMAIL%"
echo Git configured successfully.
echo.

echo Staging files...
git add .
echo Files staged.
echo.

echo Creating commit...
git commit -m "Initial commit: UPI Payment System with frontend and backend"
echo Commit created.
echo.

echo Renaming branch to main...
git branch -M main
echo Branch renamed.
echo.

echo Adding remote repository...
set REPO_URL=https://github.com/%GITHUB_USER%/upi-payment-system.git
git remote add origin %REPO_URL%
echo Remote added: %REPO_URL%
echo.

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                   IMPORTANT - READ BELOW                  ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Next step: Create the repository on GitHub
echo.
echo 1. Go to: https://github.com/new
echo.
echo 2. Fill in:
echo    Repository name: upi-payment-system
echo    Description: UPI Payment Simulation System
echo    Public: [X]
echo.
echo 3. Do NOT check:
echo    [ ] Add a README file
echo    [ ] Add .gitignore
echo    [ ] Choose a license
echo.
echo 4. Click 'Create repository'
echo.
echo After creating the repository, press ENTER to continue...
pause

echo.
echo Pushing code to GitHub...
echo (You may be asked to authenticate)
echo.

git push -u origin main

if "%ERRORLEVEL%"=="0" (
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║                    SUCCESS! ✓                             ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo Your code is now on GitHub!
    echo.
    echo Repository URL:
    echo %REPO_URL%
    echo.
    echo View on GitHub:
    echo https://github.com/%GITHUB_USER%/upi-payment-system
    echo.
    echo Next steps:
    echo  1. Deploy to Render using DEPLOYMENT_GUIDE.md
    echo  2. Or deploy to Vercel using DEPLOYMENT_GUIDE.md
    echo.
) else (
    echo.
    echo Push failed. Check the error above.
    echo.
    echo Troubleshooting:
    echo  - Make sure repository exists on GitHub
    echo  - Check your authentication
    echo  - Verify GitHub username is correct: %GITHUB_USER%
    echo.
)

pause
