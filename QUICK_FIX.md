# 🚨 QUICK FIX - Render Port Binding Issue

## The Problem
Your app is running but Render can't detect the HTTP port.

## The Solution (2 Minutes)

### 1️⃣ Go to Render Dashboard
Open: https://dashboard.render.com

### 2️⃣ Find Your Service
Click on: `mor-backend-4i9u`

### 3️⃣ Go to Settings
Click: **Settings** tab

### 4️⃣ Update Start Command
Scroll to: **Build & Deploy** section

Find: **Start Command**

Replace with:
```
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 180
```

### 5️⃣ Save
Click: **Save Changes** button at the bottom

### 6️⃣ Wait for Redeploy
Render will automatically redeploy (takes 2-3 minutes)

### 7️⃣ Check Logs
Look for this line in logs:
```
Listening at: http://0.0.0.0:10000
```

### 8️⃣ Test
```bash
curl https://mor-backend-4i9u.onrender.com/
```

Should return:
```json
{"message":"Crop Disease Detection API is running"}
```

---

## ✅ Done!

Your backend will now be accessible at:
```
https://mor-backend-4i9u.onrender.com
```

All 7 endpoints will work! 🎉

---

## 🔍 What Changed?

**Before:**
```
python app.py  ❌ (Development server, wrong port)
```

**After:**
```
gunicorn app:app --bind 0.0.0.0:$PORT  ✅ (Production server, correct port)
```

---

## 📋 Verify Environment Variables

While you're in Settings, check **Environment** section has:

```
GEMINI_API_KEY=AIzaSyDZuDw08Y1UBeiYvkIU4Z7sdfZFXyN6XeQ
WEATHER_API_KEY=2965ac2eda1e4f82859133314262702
```

---

## 🎯 That's It!

Just change the Start Command and you're done.

No code changes needed. Everything else is already correct! ✅
