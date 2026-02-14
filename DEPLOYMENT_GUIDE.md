# Deployment Guide for UPI Payment System

## 📋 Prerequisites

- GitHub account
- Render account (recommended) or Vercel account
- Git installed on your computer

## 🚀 Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface (Easiest)

1. Go to https://github.com/new
2. Fill in repository details:
   - **Repository name**: `upi-payment-system` (or any name)
   - **Description**: "UPI Payment Simulation System - Full Stack"
   - **Public** or **Private**: Choose your preference
   - **Initialize repo**: Leave unchecked (we have files already)
3. Click "Create repository"
4. Copy the repository URL (HTTPS or SSH)

### Option B: Using Git CLI

```bash
cd c:\Users\jyoti\OneDrive\Desktop\Fin_UPI
git init
git add .
git commit -m "Initial commit: UPI Payment System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/upi-payment-system.git
git push -u origin main
```

---

## 🔧 Step 2: Configure and Push to GitHub

### 1. Initialize Local Git Repository

```bash
cd c:\Users\jyoti\OneDrive\Desktop\Fin_UPI
git init
```

### 2. Add All Files

```bash
git add .
```

### 3. Create Initial Commit

```bash
git commit -m "Initial commit: Complete UPI Payment System with frontend"
```

### 4. Add Remote Repository

Replace `YOUR_USERNAME` and `REPO_NAME` with your GitHub username and repository name:

```bash
git remote add origin https://github.com/YOUR_USERNAME/upi-payment-system.git
git branch -M main
git push -u origin main
```

### 5. Verify on GitHub

Go to `https://github.com/YOUR_USERNAME/upi-payment-system` to see your repository.

---

## 🎯 Step 3: Deploy to Render (Recommended for Full-Stack)

Render is better for full-stack apps as it can host both frontend and backend.

### 1. Create Render Account

- Go to https://render.com
- Sign up (you can use GitHub account)

### 2. Create Web Service

1. Click "New +" → "Web Service"
2. Click "Connect Repository"
3. Select your GitHub repository
4. Fill in details:
   - **Name**: `upi-payment-system` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"

### 3. Configure Environment Variables

1. In Render dashboard, go to "Environment"
2. Add variables:
   ```
   DATABASE_URL = sqlite:///./upi_system.db
   PYTHON_VERSION = 3.12
   ```

### 4. Deploy

Render will automatically build and deploy when you push to GitHub.

### Access Your App

Your app will be available at: `https://upi-payment-system.onrender.com`

---

## 🌐 Step 4: Deploy to Vercel (Alternative - Frontend Only)

Vercel is best for frontend. You can deploy the backend to Render and frontend to Vercel.

### Option A: Deploy Full Stack to Render (Recommended)

Follow the Render instructions above.

### Option B: Separate Frontend to Vercel and Backend to Render

#### 1. Deploy Frontend to Vercel

1. Create `vercel.json` in root (already created)
2. Go to https://vercel.com
3. Sign up / Log in
4. Click "Add New" → "Project"
5. Import your GitHub repository
6. Configure:
   - **Framework**: None
   - **Build Command**: Leave empty (static files only)
   - **Output Directory**: `static`
7. Add Environment Variable:
   - **API_URL**: Your Render backend URL
8. Deploy

#### 2. Update API URL in Frontend

Edit `static/script.js`:

```javascript
// Change this line
const API_BASE_URL = 'http://localhost:8000/api';

// To this (replace with your Render URL)
const API_BASE_URL = 'https://your-render-app.onrender.com/api';
```

---

## 📊 Deployment Comparison

| Feature | Render | Vercel |
|---------|--------|--------|
| **Full Stack Support** | ✅ Yes | ❌ No (Frontend only) |
| **Backend Support** | ✅ Yes | ⚠️ Limited |
| **Database Support** | ✅ SQLite/PostgreSQL | ⚠️ Limited |
| **Cost** | 💰 Free tier available | 💰 More generous free tier |
| **Setup Complexity** | ⭐⭐ Easy | ⭐⭐ Easy |
| **Recommended For** | Full-stack apps | Frontend only |

**Recommendation: Use Render for this full-stack application**

---

## ✅ Testing Your Deployment

### 1. Check Server Status

```bash
curl https://your-app.onrender.com/health
```

### 2. Test API

```bash
curl https://your-app.onrender.com/api/users/
```

### 3. Test Frontend

Open in browser:
```
https://your-app.onrender.com
```

### 4. Register Test User

Use the frontend to register a user and verify it works.

---

## 🔄 Continuous Deployment

Once you connect to GitHub:
- Every push to `main` branch triggers automatic deployment
- No manual deployment needed
- Check deployment status in Render/Vercel dashboard

---

## 📝 Making Updates

After deployment, to make changes:

1. Edit files locally
2. Commit changes:
   ```bash
   git add .
   git commit -m "Your message"
   ```
3. Push to GitHub:
   ```bash
   git push origin main
   ```
4. Render/Vercel automatically deploys the new version

---

## 🐛 Troubleshooting

### Issue: "Cannot find module" error

**Solution**: Make sure `requirements.txt` is up to date:
```bash
pip freeze > requirements.txt
```

### Issue: "Database is locked"

**Solution**: Render uses ephemeral storage. Use PostgreSQL instead:
1. Add PostgreSQL add-on in Render
2. Update connection string in code

### Issue: CORS errors

**Solution**: Already configured in `app/main.py`
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    ...
)
```

### Issue: 404 on frontend routes

**Solution**: Already handled in `app/main.py` with catch-all route

---

## 💾 Database Migration for Production

For production (optional), use PostgreSQL instead of SQLite:

1. Go to Render → "Database"
2. Create "PostgreSQL" instance
3. Copy connection string
4. Update in environment variables
5. Update `app/database/config.py`:

```python
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://...")
```

---

## 📊 Monitoring Your App

### Render Dashboard
- View logs
- Check resource usage
- Monitor uptime
- Restart service if needed

### Vercel Dashboard
- View deployments
- Check analytics
- Monitor performance
- View error logs

---

## 🎉 Final Checklist

- [ ] GitHub repository created and synced
- [ ] Render account created
- [ ] Web service connected to GitHub
- [ ] Environment variables configured
- [ ] Initial deployment successful
- [ ] Frontend accessible at deployment URL
- [ ] API responding to requests
- [ ] Test user registration working
- [ ] Test payment working
- [ ] Transaction history working

---

## 📞 Support Links

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **GitHub Help**: https://docs.github.com

---

## 🚀 You're All Set!

Your UPI Payment System is now deployed to the cloud!

Share your deployment URL:
```
https://your-app.onrender.com
```

Enjoy! 💳✨
