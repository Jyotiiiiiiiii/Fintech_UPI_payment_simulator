# Git Push Quick Reference - UPI Payment System

## What These Scripts Do

The automated scripts (`push_to_github.ps1` or `push_to_github.bat`) will:

1. **Configure Git** - Set your name and email for commits
2. **Stage Changes** - Add all files to be committed
3. **Create Commit** - Package changes with a message
4. **Setup Remote** - Connect to GitHub repository
5. **Push Code** - Upload everything to GitHub

---

## How to Use

### Option 1: Run PowerShell Script (Recommended)
```powershell
# Open terminal in project directory
.\push_to_github.ps1
```

### Option 2: Run Batch Script
```cmd
# Open Command Prompt in project directory
push_to_github.bat
```

### Option 3: Manual Commands
```powershell
# Configure Git (one-time setup)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Stage all files
git add .

# Create commit
git commit -m "Initial commit: UPI Payment System with frontend and backend"

# Rename branch to main
git branch -M main

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/upi-payment-system.git

# Create repository at https://github.com/new first!

# Push to GitHub
git push -u origin main
```

---

## Prerequisites

### 1. GitHub Account
- Sign up at https://github.com
- Free account is fine
- Verify your email

### 2. Git Installed
- Windows: Download from https://git-scm.com
- During installation: Use default settings
- Check "Git from the command line and also from 3rd-party software"

### 3. Repository Created on GitHub
- Go to https://github.com/new
- Repository name: `upi-payment-system`
- Description: `UPI Payment Simulation System`
- Public repository
- Do NOT add README or .gitignore (we have them)

---

## Step-by-Step Instructions

### Step 1: Create GitHub Repository
1. Open https://github.com/new
2. Repository name: `upi-payment-system`
3. Description: `UPI Payment Simulation System` (optional)
4. Choose Public
5. **Uncheck**: "Add a README file"
6. **Uncheck**: "Add .gitignore"
7. Click "Create repository"

### Step 2: Run Push Script
**Windows PowerShell:**
```powershell
cd c:\Users\jyoti\OneDrive\Desktop\Fin_UPI
.\push_to_github.ps1
```

**Windows Command Prompt:**
```cmd
cd c:\Users\jyoti\OneDrive\Desktop\Fin_UPI
push_to_github.bat
```

### Step 3: When Prompted
- Enter your GitHub username
- Enter your name (can be real name or username)
- Enter your email (same as GitHub account)
- When asked about creating repository: confirm you've done Step 1
- Press ENTER to continue

### Step 4: Authenticate
When asked for password/token:
- **If using username/password**: Your GitHub password
- **Recommended**: Personal Access Token (safer)

#### Creating Personal Access Token:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Token name: `git-from-pc`
4. Expiration: 90 days
5. Scopes: Select `repo` (all sub-options auto-selected)
6. Click "Generate token"
7. Copy the token immediately (won't show again)
8. Paste as password when prompted

### Step 5: Verify Success
After script completes, you should see:
```
✓ SUCCESS!
Your code is now on GitHub!
Repository URL: https://github.com/YOUR_USERNAME/upi-payment-system
```

Visit that URL in browser to verify your code is there.

---

## What Gets Pushed

### Backend API
```
app/
├── main.py           - FastAPI server
├── routes/
│   ├── users.py      - User endpoints
│   └── transactions.py - Payment endpoints
├── models/
│   └── schemas.py    - Data validation
└── database/
    ├── config.py     - Database setup
    └── models.py     - SQL models
```

### Frontend
```
static/
├── index.html   - Complete web interface
├── style.css    - Responsive styling
└── script.js    - Client-side logic
```

### Configuration & Docs
```
requirements.txt         - Python dependencies
.env                     - Configuration
.gitignore              - What to exclude from git
Procfile                - Render deployment
vercel.json             - Vercel deployment
.github/workflows/      - GitHub Actions CI/CD
README.md               - Documentation
```

### Tests & Utilities
```
test_api.py             - API tests
test_api_advanced.py    - Advanced tests
deploy.bat/deploy.sh    - Deployment scripts
```

---

## Troubleshooting

### Error: "Git is not installed"
**Solution**: Download Git from https://git-scm.com and install

### Error: "fatal: not a git repository"
**Solution**: Make sure you're in the project directory:
```powershell
cd c:\Users\jyoti\OneDrive\Desktop\Fin_UPI
```

### Error: "remote origin already exists"
**Solution**: Run this first:
```powershell
git remote remove origin
```
Then run the push script again.

### Error: "fatal: 'origin' does not appear to be a 'git' repository"
**Solution**: Verify GitHub username is correct in the script. Check:
```powershell
git remote -v
```
Should show your GitHub URL.

### Authentication Failed
**Solutions**:
1. Double-check GitHub username
2. Make sure repository exists on GitHub
3. Use Personal Access Token instead of password
4. Token must have `repo` scope

### Error: "Branch 'main' set up to track remote"
This is SUCCESS! Your code is pushing to GitHub.

### Nothing happens after `git push`
Wait 30 seconds - uploading may be slow on first push.

---

## What Happens After Push

### Once Code is on GitHub:

1. **View your repository**
   - Go to https://github.com/YOUR_USERNAME/upi-payment-system

2. **Deploy to Render** (Production Python Hosting)
   - See DEPLOYMENT_GUIDE.md for step-by-step

3. **Deploy to Vercel** (Optional Frontend Only)
   - See DEPLOYMENT_GUIDE.md for step-by-step

4. **Add Collaborators**
   - Settings → Collaborators → Add people

5. **Enable GitHub Actions**
   - Actions tab → Enable workflows
   - Auto-runs tests on each push

---

## Git Commands Explained

```bash
git config --global user.name "Name"     # Your identity for commits
git config --global user.email "email"   # Your email for commits
git add .                                 # Stage all changes
git commit -m "message"                  # Create snapshot of changes
git branch -M main                        # Rename branch
git remote add origin URL                 # Connect to GitHub repo
git push -u origin main                  # Upload to GitHub
```

---

## Next Steps

1. ✅ Push to GitHub (this script)
2. 📦 Deploy to Render (DEPLOYMENT_GUIDE.md)
3. 🌐 Optional: Deploy frontend to Vercel (DEPLOYMENT_GUIDE.md)
4. 🎉 Access your live system!

---

## Support

If you encounter issues:
1. Check error message carefully
2. Review this troubleshooting section
3. Verify each prerequisite is complete
4. Check GITHUB_SETUP.txt for detailed information
5. Verify project files exist:
   - `app/` directory with Python files
   - `static/` directory with HTML/CSS/JS
   - `requirements.txt`
   - `.env`

---

## Files Included

- **push_to_github.ps1** - PowerShell version (recommended for Windows)
- **push_to_github.bat** - Batch version (for Command Prompt)
- **GITHUB_SETUP.txt** - Detailed step-by-step guide
- **This file** - Quick reference
