# GitHub Push Script for UPI Payment System
# This script guides you through pushing your code to GitHub

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         GitHub Push Setup - UPI Payment System            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check if GitHub account exists
$github_user = Read-Host "Enter your GitHub username (or press Enter to skip this step)"

if ([string]::IsNullOrWhiteSpace($github_user)) {
    Write-Host ""
    Write-Host "⚠️  You need a GitHub account first:" -ForegroundColor Yellow
    Write-Host "   1. Go to https://github.com"
    Write-Host "   2. Click 'Sign up'"
    Write-Host "   3. Complete the registration"
    Write-Host "   4. Run this script again"
    Write-Host ""
    pause
    exit
}

Write-Host ""
Write-Host "✓ GitHub username: $github_user" -ForegroundColor Green
Write-Host ""

# Ask for email
$email = Read-Host "Enter your email (used for commits)"

# Ask for name
$name = Read-Host "Enter your name (for commits)"

Write-Host ""
Write-Host "Configuring Git..." -ForegroundColor Cyan

# Configure Git globally
git config --global user.name "$name"
git config --global user.email "$email"

Write-Host "✓ Git configured with:" -ForegroundColor Green
Write-Host "  Name: $name"
Write-Host "  Email: $email"
Write-Host ""

# Stage files
Write-Host "Staging files..." -ForegroundColor Cyan
git add .
Write-Host "✓ Files staged" -ForegroundColor Green
Write-Host ""

# Create commit
Write-Host "Creating commit..." -ForegroundColor Cyan
git commit -m "Initial commit: UPI Payment System with frontend and backend"
Write-Host "✓ Commit created" -ForegroundColor Green
Write-Host ""

# Rename branch
Write-Host "Renaming branch to main..." -ForegroundColor Cyan
git branch -M main
Write-Host "✓ Branch renamed" -ForegroundColor Green
Write-Host ""

# Add remote
Write-Host "Adding remote repository..." -ForegroundColor Cyan
$repo_url = "https://github.com/$github_user/upi-payment-system.git"
git remote add origin $repo_url
Write-Host "✓ Remote added: $repo_url" -ForegroundColor Green
Write-Host ""

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║                   IMPORTANT - READ BELOW                  ║" -ForegroundColor Yellow
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next step: Create the repository on GitHub" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
Write-Host ""
Write-Host "2. Fill in:" -ForegroundColor White
Write-Host "   Repository name: upi-payment-system" -ForegroundColor Gray
Write-Host "   Description: UPI Payment Simulation System" -ForegroundColor Gray
Write-Host "   Public: ✓ (checked)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Do NOT check:" -ForegroundColor White
Write-Host "   ☐ Add a README file" -ForegroundColor Gray
Write-Host "   ☐ Add .gitignore" -ForegroundColor Gray
Write-Host "   ☐ Choose a license" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Click 'Create repository'" -ForegroundColor White
Write-Host ""
Write-Host "Waiting for you to create the repository..." -ForegroundColor Yellow
Read-Host "Press ENTER when you've created the repository on GitHub"
Write-Host ""

# Push to GitHub
Write-Host "Pushing code to GitHub..." -ForegroundColor Cyan
Write-Host "(You may be asked to authenticate)" -ForegroundColor Gray
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                    SUCCESS! 🎉                            ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your code is now on GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repository URL:" -ForegroundColor Cyan
    Write-Host "$repo_url" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "View on GitHub:" -ForegroundColor Cyan
    Write-Host "https://github.com/$github_user/upi-payment-system" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Deploy to Render (see DEPLOYMENT_GUIDE.md)" -ForegroundColor White
    Write-Host "2. Or deploy to Vercel (see DEPLOYMENT_GUIDE.md)" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Push failed. Check the error above." -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "- Make sure repository exists on GitHub" -ForegroundColor Gray
    Write-Host "- Check your authentication token" -ForegroundColor Gray
    Write-Host "- Verify GitHub username is correct: $github_user" -ForegroundColor Gray
    Write-Host ""
}

pause
