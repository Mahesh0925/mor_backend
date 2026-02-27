# 🚀 Render Deployment - Complete Steps

## Issue: Worker Not Starting
Gunicorn is listening but workers aren't booting, causing port detection to fail.

---

## ✅ Solution: 3 Steps

### Step 1: Update Start Command in Render

Go to: **Render Dashboard → Your Service → Settings → Start Command**

Replace with:
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 180 --log-level info --access-logfile - --error-logfile - --preload
```

**What this does:**
- `--log-level info` - Shows detailed logs
- `--access-logfile -` - Logs requests to stdout
- `--error-logfile -` - Logs errors to stdout
- `--preload` - Loads app before forking workers (helps catch import errors)

### Step 2: Verify Environment Variables

Go to: **Render Dashboard → Your Service → Environment**

Make sure these are set:
```
GEMINI_API_KEY=AIzaSyDZuDw08Y1UBeiYvkIU4Z7sdfZFXyN6XeQ
WEATHER_API_KEY=2965ac2eda1e4f82859133314262702
```

**IMPORTANT:** Don't include the `.env` file in your Git repo. Render uses Environment Variables instead.

### Step 3: Push Updated Code

Your `app.py` has been updated to:
- Only load `.env` in development (not on Render)
- Add startup logging to help debug

Commit and push:
```bash
git add app.py
git commit -m "Fix Render deployment - conditional dotenv loading"
git push origin main
```

---

## 🔍 What to Look For in Logs

After redeployment, you should see:

```
Starting app... API keys loaded: Gemini=True, Weather=True
[INFO] Starting gunicorn 25.1.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 57  ← THIS LINE IS CRITICAL
==> Your service is live 🎉
```

If you see "Booting worker", it's working! ✅

---

## 🚨 If Still Failing

### Check 1: Look for Import Errors
If worker doesn't boot, check logs for:
```
ModuleNotFoundError
ImportError
SyntaxError
```

### Check 2: Verify requirements.txt
Make sure all dependencies are listed:
```
flask
flask-cors
python-dotenv
requests
gunicorn
```

### Check 3: Check for Heavy Imports
If you have any heavy model loading at module level, it might timeout.

---

## 📋 Complete Checklist

- [ ] Start Command updated with `--preload` flag
- [ ] Environment Variables set in Render (not .env file)
- [ ] Code pushed to Git
- [ ] Render auto-deployed
- [ ] Logs show "Booting worker with pid: XX"
- [ ] Service shows as "Live"
- [ ] Test endpoint: `curl https://mor-backend-4i9u.onrender.com/`

---

## 🎯 Expected Success Logs

```
==> Building...
==> Installing dependencies
Successfully installed flask-3.0.0 flask-cors-4.0.0 gunicorn-25.1.0 ...
==> Build successful

==> Starting service
Starting app... API keys loaded: Gemini=True, Weather=True
[2026-02-27 23:30:00 +0000] [56] [INFO] Starting gunicorn 25.1.0
[2026-02-27 23:30:00 +0000] [56] [INFO] Listening at: http://0.0.0.0:10000 (56)
[2026-02-27 23:30:00 +0000] [56] [INFO] Using worker: sync
[2026-02-27 23:30:00 +0000] [57] [INFO] Booting worker with pid: 57
==> Your service is live 🎉
```

---

## 🔧 Alternative: Use Waitress (If Gunicorn Fails)

If Gunicorn continues to have issues, try Waitress:

1. Add to `requirements.txt`:
```
waitress
```

2. Update Start Command:
```bash
waitress-serve --host=0.0.0.0 --port=$PORT --call app:app
```

But try Gunicorn with `--preload` first!

---

## 📞 Debug Commands

If you need to debug locally:

```bash
# Test if app imports
python -c "import app; print('Success')"

# Test Gunicorn locally
gunicorn app:app --bind 0.0.0.0:8000 --workers 1 --timeout 180 --log-level debug --preload

# Check for syntax errors
python -m py_compile app.py
```

---

## ✅ Summary

The issue is that Gunicorn workers aren't starting. The fix:

1. Add `--preload` flag to catch import errors early
2. Make sure environment variables are set in Render (not .env)
3. Updated app.py to conditionally load .env
4. Push code and redeploy

Your code is correct - it's just a deployment configuration issue!
