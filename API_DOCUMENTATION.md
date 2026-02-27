# Crop Disease Detection API Documentation

**Base URL (Production):** `https://mor-backend-4i9u.onrender.com`

**Base URL (Local):** `http://127.0.0.1:8000`

---

## Table of Contents
1. [Health Check](#1-health-check)
2. [Test API Keys](#2-test-api-keys)
3. [Detect Disease](#3-detect-disease)
4. [Chatbot](#4-chatbot)
5. [Government Schemes](#5-government-schemes)
6. [Weather & Crop Advisory](#6-weather--crop-advisory)
7. [Error Handling](#error-handling)
8. [Rate Limits](#rate-limits)

---

## 1. Health Check

Check if the API server is running.

### Endpoint
```
GET /
```

### Request
No parameters required.

### Response
```json
{
  "message": "Crop Disease Detection API is running"
}
```

### Example (JavaScript/Fetch)
```javascript
fetch('https://mor-backend-4i9u.onrender.com/')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Example (cURL)
```bash
curl https://mor-backend-4i9u.onrender.com/
```

---

## 2. Test API Keys

Verify that API keys are properly configured and working.

### Endpoint
```
GET /test-api-keys
```

### Request
No parameters required.

### Response
```json
{
  "gemini_api_key_loaded": true,
  "gemini_api_key_preview": "AIzaSyA6mh6OlIiz6wow...",
  "gemini_api_status": "✅ Working",
  "weather_api_key_loaded": true,
  "weather_api_key_preview": "2965ac2eda...",
  "weather_api_status": "✅ Working"
}
```

### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| `gemini_api_key_loaded` | boolean | Whether Gemini API key is set |
| `gemini_api_key_preview` | string | First 20 characters of the key |
| `gemini_api_status` | string | Status of Gemini API connection |
| `weather_api_key_loaded` | boolean | Whether Weather API key is set |
| `weather_api_key_preview` | string | First 10 characters of the key |
| `weather_api_status` | string | Status of Weather API connection |

### Example (JavaScript/Fetch)
```javascript
fetch('https://mor-backend-4i9u.onrender.com/test-api-keys')
  .then(response => response.json())
  .then(data => {
    if (data.gemini_api_status.includes('✅')) {
      console.log('APIs are working!');
    }
  });
```

---

## 3. Detect Disease

Analyze crop images to detect diseases and get treatment recommendations.

### Endpoint
```
POST /detect-disease
```

### Request
**Content-Type:** `multipart/form-data`

**Body Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File | Yes | Image file of the crop (JPEG, PNG, etc.) |

### Response (Success)
```json
{
  "disease": "Leaf Blight",
  "cure": "1. Remove infected leaves immediately. 2. Apply copper-based fungicide. 3. Ensure proper spacing between plants for air circulation. 4. Avoid overhead watering.",
  "confidence": "high"
}
```

### Response (Healthy Crop)
```json
{
  "disease": "No disease detected",
  "cure": "Your crop appears healthy! Continue with regular care: 1. Water consistently. 2. Monitor for pests. 3. Apply balanced fertilizer.",
  "confidence": "high"
}
```

### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| `disease` | string | Name of detected disease or "No disease detected" |
| `cure` | string | Treatment recommendations or preventive care |
| `confidence` | string | Confidence level: "low", "medium", or "high" |

### Example (JavaScript/Fetch)
```javascript
const formData = new FormData();
formData.append('file', imageFile); // imageFile is a File object

fetch('https://mor-backend-4i9u.onrender.com/detect-disease', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => {
    console.log('Disease:', data.disease);
    console.log('Cure:', data.cure);
    console.log('Confidence:', data.confidence);
  });
```

### Example (React with File Input)
```javascript
const handleImageUpload = async (event) => {
  const file = event.target.files[0];
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('https://mor-backend-4i9u.onrender.com/detect-disease', {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    setDisease(data.disease);
    setCure(data.cure);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

### Example (cURL)
```bash
curl -X POST https://mor-backend-4i9u.onrender.com/detect-disease \
  -F "file=@/path/to/crop-image.jpg"
```

---

## 4. Chatbot

Get farming advice and answers to agriculture-related questions.

### Endpoint
```
POST /chatbot
```

### Request
**Content-Type:** `application/json`

**Body Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | Yes | User's question or message |
| `history` | array | No | Conversation history for context |

### History Format
```json
[
  {
    "role": "user",
    "content": "What is the best time to plant rice?"
  },
  {
    "role": "assistant",
    "content": "The best time to plant rice is during the monsoon season..."
  }
]
```

### Response
```json
{
  "reply": "Great question! Here are key steps for successful rice cultivation:\n\n1. **Prepare Your Land:** Plow and level your field until it's smooth. This helps water spread evenly.\n2. **Choose Good Seeds:** Use healthy, certified seeds..."
}
```

### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| `reply` | string | AI-generated response with farming advice |

### Example (JavaScript/Fetch)
```javascript
const chatWithBot = async (message, history = []) => {
  const response = await fetch('https://mor-backend-4i9u.onrender.com/chatbot', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      message: message,
      history: history
    })
  });
  
  const data = await response.json();
  return data.reply;
};

// Usage
const reply = await chatWithBot('What are the best practices for rice cultivation?');
console.log(reply);
```

### Example with History (React)
```javascript
const [messages, setMessages] = useState([]);

const sendMessage = async (userMessage) => {
  const history = messages.map(msg => ({
    role: msg.sender === 'user' ? 'user' : 'assistant',
    content: msg.text
  }));

  const response = await fetch('https://mor-backend-4i9u.onrender.com/chatbot', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: userMessage,
      history: history
    })
  });

  const data = await response.json();
  
  setMessages([
    ...messages,
    { sender: 'user', text: userMessage },
    { sender: 'bot', text: data.reply }
  ]);
};
```

### Example (cURL)
```bash
curl -X POST https://mor-backend-4i9u.onrender.com/chatbot \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the best practices for rice cultivation?"}'
```

---

## 5. Government Schemes

Get information about government schemes for farmers.

### Endpoint
```
POST /gov-schemes
```

### Request
**Content-Type:** `application/json`

**Body Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `state` | string | No | State name (default: "All States") |
| `type` | string | No | Scheme type (default: "All Types") |

### Scheme Types
- Income Support
- Crop Insurance
- Credit/Loan
- Irrigation/Water Management
- Market Access/Trade
- Infrastructure/Credit
- Soil Management/Advisory
- Mechanization/Subsidy
- Production Enhancement/Subsidy
- All Types (default)

### Response
```json
{
  "state": "Maharashtra",
  "type": "Subsidy",
  "schemes": [
    {
      "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
      "state": "All States",
      "type": "Income Support",
      "summary": "Provides income support to all landholding farmer families...",
      "eligibility": "All landholding farmer families...",
      "benefits": [
        "Financial benefit of Rs. 6,000 per year in three equal installments...",
        "Supplements financial needs for agricultural inputs..."
      ],
      "how_to_apply": "Farmers can register through CSCs, SNOs, or Farmers Corner...",
      "official_links": [
        "https://pmkisan.gov.in/"
      ]
    }
  ]
}
```

### Response Fields
| Field | Type | Description |
|-------|------|-------------|
| `state` | string | Requested state filter |
| `type` | string | Requested scheme type filter |
| `schemes` | array | List of matching schemes |
| `schemes[].name` | string | Scheme name |
| `schemes[].state` | string | Applicable state(s) |
| `schemes[].type` | string | Scheme category |
| `schemes[].summary` | string | Brief description |
| `schemes[].eligibility` | string | Who can apply |
| `schemes[].benefits` | array | List of benefits |
| `schemes[].how_to_apply` | string | Application process |
| `schemes[].official_links` | array | Official website URLs |

### Example (JavaScript/Fetch)
```javascript
const getSchemes = async (state = 'All States', type = 'All Types') => {
  const response = await fetch('https://mor-backend-4i9u.onrender.com/gov-schemes', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      state: state,
      type: type
    })
  });
  
  const data = await response.json();
  return data.schemes;
};

// Usage
const schemes = await getSchemes('Maharashtra', 'Subsidy');
schemes.forEach(scheme => {
  console.log(scheme.name);
  console.log(scheme.benefits);
});
```

### Example (React Component)
```javascript
const GovernmentSchemes = () => {
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchSchemes = async (state, type) => {
    setLoading(true);
    try {
      const response = await fetch('https://mor-backend-4i9u.onrender.com/gov-schemes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ state, type })
      });
      const data = await response.json();
      setSchemes(data.schemes);
    } catch (error) {
      console.error('Error fetching schemes:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {loading ? <p>Loading schemes...</p> : (
        schemes.map(scheme => (
          <div key={scheme.name}>
            <h3>{scheme.name}</h3>
            <p>{scheme.summary}</p>
            <a href={scheme.official_links[0]}>Apply Now</a>
          </div>
        ))
      )}
    </div>
  );
};
```

### Example (cURL)
```bash
curl -X POST https://mor-backend-4i9u.onrender.com/gov-schemes \
  -H "Content-Type: application/json" \
  -d '{"state": "Maharashtra", "type": "Subsidy"}'
```

### Note
⚠️ This endpoint may take 60-120 seconds to respond as it searches for current information.

---

## 6. Weather & Crop Advisory

Get weather forecast and crop recommendations for a specific location.

### Endpoint
```
POST /weather-crop-advisory
```

### Request
**Content-Type:** `application/json`

**Body Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `city` | string | Yes | City name |
| `state` | string | No | State name |
| `country` | string | No | Country code (default: "IN") |

### Response
```json
{
  "location": {
    "city": "Mumbai",
    "state": "Maharashtra",
    "country": "India",
    "lat": 18.975,
    "lon": 72.8258
  },
  "forecast": [
    {
      "date": "2026-02-27",
      "temp_min_c": 23.5,
      "temp_max_c": 25.7,
      "humidity_avg": 60,
      "rain_mm_total": 0.0,
      "condition": "Sunny"
    }
  ],
  "advisory": {
    "weather_summary": "The forecast predicts consistently sunny and dry weather...",
    "recommended_crops": [
      {
        "crop": "Okra (Bhindi)",
        "reason": "Thrives in warm, sunny conditions...",
        "suitability": "high"
      }
    ],
    "farm_actions": [
      "Ensure regular and adequate irrigation...",
      "Prepare land for new plantings..."
    ],
    "risk_alerts": [
      "Increased risk of water stress...",
      "Watch out for common pests..."
    ],
    "other_suggestions": [
      "Implement water-saving irrigation methods...",
      "Regularly check soil moisture levels..."
    ]
  }
}
```

### Response Fields

#### Location Object
| Field | Type | Description |
|-------|------|-------------|
| `city` | string | City name |
| `state` | string | State/region name |
| `country` | string | Country name |
| `lat` | number | Latitude |
| `lon` | number | Longitude |

#### Forecast Array (5 days)
| Field | Type | Description |
|-------|------|-------------|
| `date` | string | Date (YYYY-MM-DD) |
| `temp_min_c` | number | Minimum temperature (°C) |
| `temp_max_c` | number | Maximum temperature (°C) |
| `humidity_avg` | number | Average humidity (%) |
| `rain_mm_total` | number | Total rainfall (mm) |
| `condition` | string | Weather condition |

#### Advisory Object
| Field | Type | Description |
|-------|------|-------------|
| `weather_summary` | string | Summary of weather conditions |
| `recommended_crops` | array | Crops suitable for current weather |
| `recommended_crops[].crop` | string | Crop name |
| `recommended_crops[].reason` | string | Why it's suitable |
| `recommended_crops[].suitability` | string | "high", "medium", or "low" |
| `farm_actions` | array | Recommended farming activities |
| `risk_alerts` | array | Weather-related risks |
| `other_suggestions` | array | Additional tips |

### Example (JavaScript/Fetch)
```javascript
const getWeatherAdvisory = async (city, state = '', country = 'IN') => {
  const response = await fetch('https://mor-backend-4i9u.onrender.com/weather-crop-advisory', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      city: city,
      state: state,
      country: country
    })
  });
  
  const data = await response.json();
  return data;
};

// Usage
const advisory = await getWeatherAdvisory('Mumbai', 'Maharashtra', 'IN');
console.log('Weather:', advisory.forecast);
console.log('Recommended Crops:', advisory.advisory.recommended_crops);
```

### Example (React Component)
```javascript
const WeatherAdvisory = () => {
  const [advisory, setAdvisory] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchAdvisory = async (city) => {
    setLoading(true);
    try {
      const response = await fetch('https://mor-backend-4i9u.onrender.com/weather-crop-advisory', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ city })
      });
      const data = await response.json();
      setAdvisory(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {advisory && (
        <>
          <h2>Weather for {advisory.location.city}</h2>
          <div className="forecast">
            {advisory.forecast.map(day => (
              <div key={day.date}>
                <p>{day.date}: {day.condition}</p>
                <p>{day.temp_min_c}°C - {day.temp_max_c}°C</p>
              </div>
            ))}
          </div>
          <h3>Recommended Crops</h3>
          {advisory.advisory.recommended_crops.map(crop => (
            <div key={crop.crop}>
              <h4>{crop.crop}</h4>
              <p>{crop.reason}</p>
              <span>Suitability: {crop.suitability}</span>
            </div>
          ))}
        </>
      )}
    </div>
  );
};
```

### Example (cURL)
```bash
curl -X POST https://mor-backend-4i9u.onrender.com/weather-crop-advisory \
  -H "Content-Type: application/json" \
  -d '{"city": "Mumbai", "state": "Maharashtra", "country": "IN"}'
```

---

## Error Handling

All endpoints return appropriate HTTP status codes and error messages.

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes
| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid request parameters |
| 500 | Internal Server Error | Server-side error (API key issues, external API failures) |
| 502 | Bad Gateway | External API returned invalid response |

### Example Error Responses

#### Missing Required Field
```json
{
  "detail": "Field 'message' is required."
}
```

#### Invalid Image File
```json
{
  "detail": "Please upload a valid image file."
}
```

#### API Key Not Set
```json
{
  "detail": "GEMINI_API_KEY is not set on the server."
}
```

#### External API Failure
```json
{
  "detail": "Gemini request failed: 403 Client Error: Forbidden"
}
```

### Error Handling Example (JavaScript)
```javascript
const handleApiCall = async () => {
  try {
    const response = await fetch('https://mor-backend-4i9u.onrender.com/chatbot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'Hello' })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Request failed');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('API Error:', error.message);
    // Show user-friendly error message
    alert('Something went wrong. Please try again.');
  }
};
```

---

## Rate Limits

Currently, there are no enforced rate limits on the API. However, please be mindful of:

1. **Gemini API Quotas:** The backend uses Google's Gemini API which has usage limits
2. **Weather API Quotas:** Weather API has daily request limits
3. **Server Resources:** Avoid making excessive concurrent requests

### Best Practices
- Implement client-side caching for repeated requests
- Add debouncing for user input (chatbot, search)
- Show loading states during long-running requests
- Handle timeouts gracefully (especially for /gov-schemes)

---

## Complete Integration Example (React)

```javascript
import React, { useState } from 'react';

const API_BASE_URL = 'https://mor-backend-4i9u.onrender.com';

const FarmingApp = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Disease Detection
  const detectDisease = async (imageFile) => {
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('file', imageFile);

      const response = await fetch(`${API_BASE_URL}/detect-disease`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) throw new Error('Detection failed');
      
      const data = await response.json();
      return data;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Chatbot
  const askChatbot = async (message, history = []) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/chatbot`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, history })
      });

      if (!response.ok) throw new Error('Chat failed');
      
      const data = await response.json();
      return data.reply;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Weather Advisory
  const getWeatherAdvisory = async (city, state = '', country = 'IN') => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/weather-crop-advisory`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ city, state, country })
      });

      if (!response.ok) throw new Error('Weather fetch failed');
      
      const data = await response.json();
      return data;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Government Schemes
  const getSchemes = async (state = 'All States', type = 'All Types') => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/gov-schemes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ state, type })
      });

      if (!response.ok) throw new Error('Schemes fetch failed');
      
      const data = await response.json();
      return data.schemes;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      {loading && <div>Loading...</div>}
      {error && <div>Error: {error}</div>}
      {/* Your UI components here */}
    </div>
  );
};

export default FarmingApp;
```

---

## Testing the API

### Quick Test Script (JavaScript)
```javascript
const testAPI = async () => {
  const baseURL = 'https://mor-backend-4i9u.onrender.com';
  
  // Test 1: Health Check
  console.log('Testing health check...');
  const health = await fetch(`${baseURL}/`).then(r => r.json());
  console.log('✅ Health:', health);
  
  // Test 2: API Keys
  console.log('Testing API keys...');
  const keys = await fetch(`${baseURL}/test-api-keys`).then(r => r.json());
  console.log('✅ API Keys:', keys);
  
  // Test 3: Chatbot
  console.log('Testing chatbot...');
  const chat = await fetch(`${baseURL}/chatbot`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'Hello' })
  }).then(r => r.json());
  console.log('✅ Chatbot:', chat);
  
  console.log('All tests completed!');
};

testAPI();
```

---

## Support

For issues or questions:
1. Check the `/test-api-keys` endpoint to verify configuration
2. Review error messages in the response
3. Ensure all required parameters are provided
4. Check network connectivity and CORS settings

---

## Changelog

### Version 1.0.0 (Current)
- Initial release
- 6 endpoints: health check, API test, disease detection, chatbot, government schemes, weather advisory
- Gemini AI integration for intelligent responses
- Weather API integration for forecasts
- Image analysis for crop disease detection
