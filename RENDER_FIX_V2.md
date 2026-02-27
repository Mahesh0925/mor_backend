# 🔧 Render Fix V2 - Worker Exiting Issue

## Problem
Worker starts (pid: 58) but immediately exits. Render then kills the process.

## Root Cause
The worker is likely timing out during health checks or there's a silent crash.

---

## ✅ Solution: Try These Start Commands

### Option 1: Remove --preload (Recommended)
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 180 --log-level debug
```

The `--preload` flag might be causing issues. Remove it and let workers load the app individually.

### Option 2: Increase Worker Timeout
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --graceful-timeout 300 --log-level debug
```

### Option 3: Use Gevent Worker (Async)
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --worker-class gevent --timeout 180 --log-level debug
```

**Note:** For Option 3, add `gevent` to requirements.txt:
```
flask
flask-cors
python-dotenv
requests
gunicorn
gevent
```

---

## 🔍 What to Check

### 1. Environment Variables
Make sure these are set in Render Environment tab:
```
GEMINI_API_KEY=AIzaSyDZuDw08Y1UBeiYvkIU4Z7sdfZFXyN6XeQ
WEATHER_API_KEY=2965ac2eda1e4f82859133314262702
```

### 2. Check for Startup Print
Look for this in logs:
```
Starting app... API keys loaded: Gemini=True, Weather=True
```

If you see `Gemini=False`, the environment variable isn't set correctly.

### 3. Look for Python Errors
Check logs for:
```
Traceback
Error
Exception
ModuleNotFoundError
```

---

## 🎯 Step-by-Step Fix

### 1. Update Start Command
Go to Render Settings → Start Command

Try **Option 1** first (without --preload):
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 180 --log-level debug
```

### 2. Save and Redeploy
Click "Save Changes" - Render will redeploy automatically

### 3. Watch Logs Carefully
Look for:
```
Starting app... API keys loaded: Gemini=True, Weather=True
[INFO] Starting gunicorn 25.1.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Booting worker with pid: 58
```

**Key:** Worker should stay alive, not exit immediately.

### 4. If Worker Still Exits
Try **Option 2** with longer timeout:
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --graceful-timeout 300 --log-level debug
```

---

## 🚨 Alternative: Use Waitress Instead

If Gunicorn keeps failing, try Waitress (simpler, more reliable):

### 1. Update requirements.txt
Add:
```
waitress
```

### 2. Update Start Command
```bash
waitress-serve --host=0.0.0.0 --port=$PORT --threads=4 --call app:app
```

### 3. Push and Deploy
```bash
git add requirements.txt
git commit -m "Switch to Waitress"
git push origin main
```

---

## 🔍 Debug: Check If App Loads

To verify your app can load without errors:

```bash
# Locally test
python -c "from app import app; print('App loaded successfully')"

# Test with Gunicorn locally
gunicorn app:app --bind 0.0.0.0:8000 --workers 1 --timeout 180 --log-level debug
```

If this works locally but fails on Render, it's an environment issue.

---

## 📊 Expected Success Logs

```
Starting app... API keys loaded: Gemini=True, Weather=True
[2026-02-27 23:40:00 +0000] [56] [INFO] Starting gunicorn 25.1.0
[2026-02-27 23:40:00 +0000] [56] [INFO] Listening at: http://0.0.0.0:10000 (56)
[2026-02-27 23:40:00 +0000] [56] [INFO] Using worker: sync
[2026-02-27 23:40:00 +0000] [58] [INFO] Booting worker with pid: 58
[2026-02-27 23:40:05 +0000] [58] [INFO] Worker started  ← Should stay running
==> Your service is live 🎉
```

Worker should NOT exit after starting.

---

## ✅ Quick Checklist

- [ ] Remove `--preload` from Start Command
- [ ] Verify environment variables in Render
- [ ] Check logs for "Starting app... API keys loaded: Gemini=True"
- [ ] Worker boots and stays alive (doesn't exit)
- [ ] Service shows as "Live"
- [ ] Test: `curl https://mor-backend-4i9u.onrender.com/`

---

## 🎯 Recommended Action

**Try this Start Command NOW:**
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 180 --log-level debug
```

This is the simplest, most reliable configuration. The `--preload` flag was likely causing the issue.

If this doesn't work, switch to Waitress (see Alternative section above).
