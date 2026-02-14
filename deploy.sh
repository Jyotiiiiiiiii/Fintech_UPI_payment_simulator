#!/bin/bash
# GitHub & Render Deployment Script for UPI Payment System

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  UPI PAYMENT SYSTEM - DEPLOYMENT SETUP SCRIPT          ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "[ERROR] Git is not installed. Please install Git first."
    echo "Download from: https://git-scm.com/download/linux"
    exit 1
fi

echo "[✓] Git is installed"
echo ""

# Initialize Git if not already done
if [ ! -d .git ]; then
    echo "[*] Initializing Git repository..."
    git init
    git config user.email "your-email@example.com"
    git config user.name "Your Name"
    echo "[✓] Git repository initialized"
else
    echo "[✓] Git repository already initialized"
fi

echo ""
echo "[*] Staging all files..."
git add .
echo "[✓] Files staged"

echo ""
echo "[*] Creating initial commit..."
git commit -m "Initial commit: UPI Payment System with Frontend and Backend"
echo "[✓] Commit created"

echo ""
echo "===================================================="
echo " NEXT STEPS - GITHUB SETUP"
echo "===================================================="
echo ""
echo "1. Go to https://github.com/new"
echo "2. Create a repository:"
echo "   - Name: upi-payment-system"
echo "   - Public or Private: Your choice"
echo "   - Do NOT initialize with README"
echo ""
echo "3. Copy the HTTPS URL shown"
echo "4. Run the following command:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/upi-payment-system.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "5. Replace YOUR_USERNAME with your actual GitHub username"
echo ""

read -p "Enter your GitHub repository URL (press Enter for example): " github_url
if [ -z "$github_url" ]; then
    github_url="https://github.com/YOUR_USERNAME/upi-payment-system.git"
    echo "Using example URL: $github_url"
    echo "Replace YOUR_USERNAME with your actual GitHub username"
fi

echo ""
echo "[*] Adding remote repository..."
git remote remove origin 2>/dev/null
git remote add origin "$github_url"
echo "[✓] Remote repository added"

echo ""
echo "[*] Renaming branch to main..."
git branch -M main
echo "[✓] Branch renamed to main"

echo ""
echo "[*] Pushing to GitHub..."
git push -u origin main
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to push to GitHub"
    echo "Please check your GitHub URL and credentials"
    exit 1
fi
echo "[✓] Successfully pushed to GitHub!"

echo ""
echo "===================================================="
echo " GITHUB DEPLOYMENT COMPLETE!"
echo "===================================================="
echo ""
echo "Your repository is now on GitHub at:"
echo "$github_url"
echo ""
echo "===================================================="
echo " NEXT STEPS - RENDER DEPLOYMENT"
echo "===================================================="
echo ""
echo "1. Go to https://render.com"
echo "2. Sign up or Log in (you can use GitHub account)"
echo "3. Click \"New +\" then \"Web Service\""
echo "4. Click \"Connect Repository\""
echo "5. Select your upi-payment-system repository"
echo ""
echo "Configuration:"
echo "  - Name: upi-payment-system"
echo "  - Environment: Python 3"
echo "  - Build Command: pip install -r requirements.txt"
echo "  - Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
echo "  - Runtime: Python 3.12 (or latest)"
echo ""
echo "6. Click \"Create Web Service\""
echo "7. Wait for deployment (5-10 minutes)"
echo "8. Your app will be available at: https://your-app.onrender.com"
echo ""
echo "===================================================="
echo " DEPLOYMENT GUIDE"
echo "===================================================="
echo ""
echo "See DEPLOYMENT_GUIDE.md for detailed instructions"
echo "for:"
echo "  - GitHub setup and pushing code"
echo "  - Render deployment"
echo "  - Vercel deployment"
echo "  - Environment configuration"
echo "  - Troubleshooting"
echo ""
