# Deployment Guide - Streamlit Cloud

## Quick Start: Deploy to Streamlit Cloud

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in (create account if needed)
2. Click the **+** icon in the top-right → **New repository**
3. Name it: `Employee-Dashboard`
4. Make it **Public** (required for Streamlit Cloud free tier)
5. **Don't** initialize with README/gitignore (we have them locally)
6. Click **Create repository**

### Step 2: Push Code to GitHub

Copy and run these commands in your terminal:

```bash
cd /Users/bhupesh.goyal/Employee-Dashboard

git remote add origin https://github.com/YOUR_USERNAME/Employee-Dashboard.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 3: Deploy to Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Click **Sign up** or **Sign in** with GitHub
3. Click **New app**
4. Select:
   - **Repository**: `YOUR_USERNAME/Employee-Dashboard`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **Deploy**

Your app will be live in minutes! 🚀

### Step 4: Share Your App

Once deployed, Streamlit Cloud provides a public URL:
```
https://employee-dashboard-YOUR_USERNAME.streamlit.app/
```

---

## Features Ready for Cloud

✅ All code is production-ready  
✅ No database required (uses session state)  
✅ No secrets/API keys needed  
✅ Requirements.txt configured  
✅ Fully functional prototype  

---

## Post-Deployment Notes

The app uses mocked data and session state, so:
- Data resets on each session
- No database persistence
- Perfect for demos and prototypes

To add a real database later:
- Connect to PostgreSQL, MongoDB, or Firebase
- Use Streamlit secrets for credentials
- Replace mock data functions with API calls

---

## Troubleshooting

**App doesn't load?**
- Check `requirements.txt` is in root
- Verify `app.py` is the main file
- Check Streamlit Cloud logs

**Want to update code?**
```bash
cd /Users/bhupesh.goyal/Employee-Dashboard
git add .
git commit -m "Your message"
git push
```
Streamlit Cloud auto-deploys on push!

---

Need help? Check the [Streamlit Cloud docs](https://docs.streamlit.io/deploy)
