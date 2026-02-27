# Backend Endpoint Test Results
**Deployed URL:** https://mor-backend-4i9u.onrender.com

**Test Date:** February 27, 2026

---

## Test Summary

| Endpoint | Method | Status | Result |
|----------|--------|--------|--------|
| `/` | GET | ✅ PASS | Health check working |
| `/detect-disease` | POST | ⚠️ NOT TESTED | Requires image file upload |
| `/chatbot` | POST | ❌ FAIL | 500 Internal Server Error |
| `/gov-schemes` | POST | ❌ FAIL | 500 Internal Server Error |
| `/weather-crop-advisory` | POST | ❌ FAIL | 403 Forbidden |

---

## Detailed Test Results

### 1. Health Check Endpoint
**Endpoint:** `GET /`

**Status:** ✅ PASS

**Response:**
```json
{
  "message": "Crop Disease Detection API is running"
}
```

**Notes:** Server is up and running successfully.

---

### 2. Disease Detection Endpoint
**Endpoint:** `POST /detect-disease`

**Status:** ⚠️ NOT TESTED (Requires multipart/form-data with image file)

**Expected Request Format:**
- Content-Type: `multipart/form-data`
- Field: `file` (image file)

**Test Command (for manual testing):**
```powershell
$filePath = "path/to/crop-image.jpg"
$uri = "https://mor-backend-4i9u.onrender.com/detect-disease"
$form = @{
    file = Get-Item -Path $filePath
}
Invoke-WebRequest -Uri $uri -Method POST -Form $form
```

**Expected Response Schema:**
```json
{
  "disease": "string",
  "cure": "string",
  "confidence": "low|medium|high"
}
```

---

### 3. Chatbot Endpoint
**Endpoint:** `POST /chatbot`

**Status:** ❌ FAIL - 500 Internal Server Error

**Test Request:**
```json
{
  "message": "What are the best practices for rice cultivation?"
}
```

**Error:** Server returned 500 error

**Possible Issues:**
- GEMINI_API_KEY may not be configured on Render
- API key might be invalid or expired
- Network/timeout issues with Gemini API

**Expected Response Schema:**
```json
{
  "reply": "string"
}
```

---

### 4. Government Schemes Endpoint
**Endpoint:** `POST /gov-schemes`

**Status:** ❌ FAIL - 500 Internal Server Error

**Test Request:**
```json
{
  "state": "Maharashtra",
  "type": "Subsidy"
}
```

**Error:** Server returned 500 error

**Possible Issues:**
- GEMINI_API_KEY may not be configured on Render
- Google Search tools may not be available in the API
- API quota/rate limiting issues

**Expected Response Schema:**
```json
{
  "state": "string",
  "type": "string",
  "schemes": [
    {
      "name": "string",
      "state": "string",
      "type": "string",
      "summary": "string",
      "eligibility": "string",
      "benefits": ["string"],
      "how_to_apply": "string",
      "official_links": ["string"]
    }
  ]
}
```

---

### 5. Weather & Crop Advisory Endpoint
**Endpoint:** `POST /weather-crop-advisory`

**Status:** ❌ FAIL - 403 Forbidden

**Test Request:**
```json
{
  "city": "Mumbai",
  "state": "Maharashtra",
  "country": "IN"
}
```

**Error:** 403 Forbidden from Weather API

**Possible Issues:**
- WEATHER_API_KEY may not be configured on Render
- Weather API key might be invalid or expired
- API key might have domain/IP restrictions
- Free tier limitations or quota exceeded

**Expected Response Schema:**
```json
{
  "location": {
    "city": "string",
    "state": "string",
    "country": "string",
    "lat": number,
    "lon": number
  },
  "forecast": [
    {
      "date": "string",
      "temp_min_c": number,
      "temp_max_c": number,
      "humidity_avg": number,
      "rain_mm_total": number,
      "condition": "string"
    }
  ],
  "advisory": {
    "weather_summary": "string",
    "recommended_crops": [
      {
        "crop": "string",
        "reason": "string",
        "suitability": "high|medium|low"
      }
    ],
    "farm_actions": ["string"],
    "risk_alerts": ["string"],
    "other_suggestions": ["string"]
  }
}
```

---

## Issues Found

### Critical Issues:
1. **Environment Variables Not Set:** The API keys (GEMINI_API_KEY, WEATHER_API_KEY) may not be configured in Render's environment variables
2. **Weather API 403 Error:** Weather API key is either invalid, expired, or has restrictions
3. **Gemini API 500 Errors:** Chatbot and gov-schemes endpoints failing, likely due to missing/invalid API key

### Recommendations:

1. **Check Render Environment Variables:**
   - Go to your Render dashboard
   - Navigate to your service settings
   - Add environment variables:
     - `GEMINI_API_KEY`: Your Gemini API key
     - `WEATHER_API_KEY`: Your Weather API key

2. **Verify API Keys:**
   - Test GEMINI_API_KEY: https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=YOUR_KEY
   - Test WEATHER_API_KEY: http://api.weatherapi.com/v1/forecast.json?key=YOUR_KEY&q=Mumbai&days=1

3. **Check API Quotas:**
   - Verify you haven't exceeded free tier limits
   - Check if APIs require billing to be enabled

4. **Add Logging:**
   - Consider adding more detailed error logging to help debug issues
   - Log the actual error messages from external APIs

5. **Test Locally First:**
   - Run the app locally with the same environment variables
   - Verify all endpoints work before deploying

---

## Manual Testing Commands

### Test Health Check:
```powershell
Invoke-WebRequest -Uri "https://mor-backend-4i9u.onrender.com/" -UseBasicParsing
```

### Test Chatbot:
```powershell
$body = @{message='Hello'} | ConvertTo-Json
Invoke-WebRequest -Uri "https://mor-backend-4i9u.onrender.com/chatbot" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
```

### Test Gov Schemes:
```powershell
$body = @{state='Maharashtra'; type='Subsidy'} | ConvertTo-Json
Invoke-WebRequest -Uri "https://mor-backend-4i9u.onrender.com/gov-schemes" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
```

### Test Weather Advisory:
```powershell
$body = @{city='Mumbai'; state='Maharashtra'; country='IN'} | ConvertTo-Json
Invoke-WebRequest -Uri "https://mor-backend-4i9u.onrender.com/weather-crop-advisory" -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
```

---

## Next Steps

1. Configure environment variables in Render
2. Verify API keys are valid and active
3. Re-test all endpoints after configuration
4. Consider adding health check endpoints for external API connectivity
5. Add proper error handling and logging for production debugging
