# Market Prices Endpoint Documentation

## Overview
Get current market prices for vegetables and agricultural commodities using AI-powered search.

---

## Endpoint
```
POST /market-prices
```

---

## Request

**Content-Type:** `application/json`

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `location` | string | Yes | City, state, or region name (e.g., "Mumbai", "Delhi", "Maharashtra") |
| `commodity` | string | No | Specific commodity name (e.g., "Tomato", "Onion", "Rice"). If not provided, returns prices for common vegetables and crops |

### Example Requests

**Specific Commodity:**
```json
{
  "location": "Mumbai",
  "commodity": "Tomato"
}
```

**General Market Prices:**
```json
{
  "location": "Delhi"
}
```

---

## Response

### Success Response
```json
{
  "location": "Mumbai",
  "date": "2023-10-26",
  "prices": [
    {
      "commodity": "Tomato",
      "variety": "Other",
      "unit": "₹/quintal",
      "min_price": 1000,
      "max_price": 2000,
      "modal_price": 1500,
      "market": "APMC Navi Mumbai (Vashi)",
      "trend": "stable"
    },
    {
      "commodity": "Onion",
      "variety": "Red",
      "unit": "₹/quintal",
      "min_price": 800,
      "max_price": 1200,
      "modal_price": 1000,
      "market": "APMC Vashi",
      "trend": "rising"
    }
  ],
  "source": "https://agmarknet.gov.in",
  "last_updated": "2023-10-27"
}
```

### Response Fields

#### Root Level
| Field | Type | Description |
|-------|------|-------------|
| `location` | string | Location for which prices are provided |
| `date` | string | Date of the price data |
| `prices` | array | List of commodity prices |
| `source` | string | Source of the price information |
| `last_updated` | string | When the data was last updated |

#### Price Object
| Field | Type | Description |
|-------|------|-------------|
| `commodity` | string | Name of the commodity (e.g., "Tomato", "Onion") |
| `variety` | string | Variety or grade (e.g., "Red", "Hybrid", "Other") |
| `unit` | string | Unit of measurement (e.g., "₹/quintal", "₹/kg") |
| `min_price` | number | Minimum price in the market |
| `max_price` | number | Maximum price in the market |
| `modal_price` | number | Most common/average price |
| `market` | string | Market or mandi name |
| `trend` | string | Price trend: "rising", "falling", or "stable" |

---

## Usage Examples

### JavaScript/Fetch
```javascript
const getMarketPrices = async (location, commodity = null) => {
  const body = { location };
  if (commodity) {
    body.commodity = commodity;
  }

  const response = await fetch('https://mor-backend-4i9u.onrender.com/market-prices', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });
  
  const data = await response.json();
  return data;
};

// Get specific commodity price
const tomatoPrices = await getMarketPrices('Mumbai', 'Tomato');
console.log('Tomato modal price:', tomatoPrices.prices[0].modal_price);

// Get all market prices
const allPrices = await getMarketPrices('Delhi');
console.log('All commodities:', allPrices.prices);
```

### React Component
```javascript
import React, { useState, useEffect } from 'react';

const MarketPrices = () => {
  const [prices, setPrices] = useState(null);
  const [loading, setLoading] = useState(false);
  const [location, setLocation] = useState('Mumbai');
  const [commodity, setCommodity] = useState('');

  const fetchPrices = async () => {
    setLoading(true);
    try {
      const body = { location };
      if (commodity) body.commodity = commodity;

      const response = await fetch('https://mor-backend-4i9u.onrender.com/market-prices', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      
      const data = await response.json();
      setPrices(data);
    } catch (error) {
      console.error('Error fetching prices:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Market Prices</h2>
      
      <input 
        type="text" 
        placeholder="Location (e.g., Mumbai)" 
        value={location}
        onChange={(e) => setLocation(e.target.value)}
      />
      
      <input 
        type="text" 
        placeholder="Commodity (optional)" 
        value={commodity}
        onChange={(e) => setCommodity(e.target.value)}
      />
      
      <button onClick={fetchPrices} disabled={loading}>
        {loading ? 'Loading...' : 'Get Prices'}
      </button>

      {prices && (
        <div>
          <h3>Prices for {prices.location}</h3>
          <p>Last Updated: {prices.last_updated}</p>
          
          {prices.prices.map((item, index) => (
            <div key={index} className="price-card">
              <h4>{item.commodity} - {item.variety}</h4>
              <p>Market: {item.market}</p>
              <p>
                Price: ₹{item.min_price} - ₹{item.max_price} 
                (Modal: ₹{item.modal_price}) per {item.unit}
              </p>
              <span className={`trend-${item.trend}`}>
                Trend: {item.trend}
              </span>
            </div>
          ))}
          
          <p>Source: <a href={prices.source}>{prices.source}</a></p>
        </div>
      )}
    </div>
  );
};

export default MarketPrices;
```

### cURL
```bash
# Get specific commodity price
curl -X POST https://mor-backend-4i9u.onrender.com/market-prices \
  -H "Content-Type: application/json" \
  -d '{"location": "Mumbai", "commodity": "Tomato"}'

# Get all market prices
curl -X POST https://mor-backend-4i9u.onrender.com/market-prices \
  -H "Content-Type: application/json" \
  -d '{"location": "Delhi"}'
```

### PowerShell
```powershell
# Get specific commodity price
$body = @{location='Mumbai'; commodity='Tomato'} | ConvertTo-Json
Invoke-WebRequest -Uri "https://mor-backend-4i9u.onrender.com/market-prices" `
  -Method POST -Body $body -ContentType "application/json" -UseBasicParsing

# Get all market prices
$body = @{location='Delhi'} | ConvertTo-Json
Invoke-WebRequest -Uri "https://mor-backend-4i9u.onrender.com/market-prices" `
  -Method POST -Body $body -ContentType "application/json" -UseBasicParsing
```

---

## Error Handling

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Errors

**Missing Location:**
```json
{
  "detail": "Field 'location' is required."
}
```

**API Key Not Set:**
```json
{
  "detail": "GEMINI_API_KEY is not set on the server."
}
```

**Rate Limit Exceeded:**
```json
{
  "detail": "Market price request failed: 429 Client Error: Too Many Requests"
}
```

**Parsing Error (with fallback):**
```json
{
  "location": "Mumbai",
  "commodity": "Tomato",
  "prices": [],
  "raw_response": "...",
  "detail": "Could not parse structured JSON. The response may contain useful information in raw_response field."
}
```

### Error Handling Example
```javascript
const fetchPrices = async (location, commodity) => {
  try {
    const response = await fetch('https://mor-backend-4i9u.onrender.com/market-prices', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ location, commodity })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to fetch prices');
    }

    const data = await response.json();
    
    // Check if prices were found
    if (data.prices.length === 0) {
      console.warn('No prices found for this location/commodity');
      // Check raw_response if available
      if (data.raw_response) {
        console.log('Raw response:', data.raw_response);
      }
    }
    
    return data;
  } catch (error) {
    console.error('Error fetching market prices:', error.message);
    // Show user-friendly error message
    alert('Unable to fetch market prices. Please try again later.');
    return null;
  }
};
```

---

## Features

### 1. AI-Powered Search
- Uses Google's Gemini AI with search capabilities
- Fetches real-time data from reliable sources
- Prioritizes government mandi boards and official sources

### 2. Flexible Queries
- Search by specific commodity or get general market overview
- Location-based pricing
- Multiple varieties and markets

### 3. Price Trends
- Indicates if prices are rising, falling, or stable
- Helps farmers make informed selling decisions

### 4. Reliable Sources
- Data from government agricultural market boards
- Official price reporting systems
- Verified market information

---

## Use Cases

### For Farmers
```javascript
// Check best time to sell
const prices = await getMarketPrices('Pune', 'Onion');
const trend = prices.prices[0].trend;

if (trend === 'rising') {
  alert('Prices are rising! Consider waiting to sell.');
} else if (trend === 'falling') {
  alert('Prices are falling. Sell soon to get better rates.');
}
```

### For Buyers
```javascript
// Compare prices across markets
const mumbaiPrices = await getMarketPrices('Mumbai', 'Tomato');
const punePrices = await getMarketPrices('Pune', 'Tomato');

const mumbaiPrice = mumbaiPrices.prices[0].modal_price;
const punePrice = punePrices.prices[0].modal_price;

if (mumbaiPrice < punePrice) {
  console.log('Better to buy from Mumbai');
} else {
  console.log('Better to buy from Pune');
}
```

### For Market Analysis
```javascript
// Track multiple commodities
const location = 'Delhi';
const commodities = ['Tomato', 'Onion', 'Potato', 'Rice', 'Wheat'];

const allPrices = await Promise.all(
  commodities.map(commodity => getMarketPrices(location, commodity))
);

// Display price comparison
allPrices.forEach(data => {
  const item = data.prices[0];
  console.log(`${item.commodity}: ₹${item.modal_price} (${item.trend})`);
});
```

---

## Performance

### Response Time
- **Average:** 60-120 seconds
- **Reason:** Uses AI search to fetch real-time data
- **Recommendation:** Show loading indicator with message

### Loading Message Example
```javascript
setLoadingMessage('Searching for current market prices... This may take up to 2 minutes.');
```

### Caching Recommendation
```javascript
// Cache prices for 1 hour to reduce API calls
const CACHE_DURATION = 60 * 60 * 1000; // 1 hour

const getCachedPrices = (location, commodity) => {
  const cacheKey = `prices_${location}_${commodity || 'all'}`;
  const cached = localStorage.getItem(cacheKey);
  
  if (cached) {
    const { data, timestamp } = JSON.parse(cached);
    if (Date.now() - timestamp < CACHE_DURATION) {
      return data;
    }
  }
  
  return null;
};

const setCachedPrices = (location, commodity, data) => {
  const cacheKey = `prices_${location}_${commodity || 'all'}`;
  localStorage.setItem(cacheKey, JSON.stringify({
    data,
    timestamp: Date.now()
  }));
};
```

---

## Data Sources

The endpoint searches for data from:
- **agmarknet.gov.in** - Government agricultural market portal
- **State Agricultural Marketing Boards**
- **APMC (Agricultural Produce Market Committee) websites**
- **Official government price reporting systems**

---

## Limitations

1. **Search-Based:** Prices depend on available online data
2. **Rate Limits:** Subject to Gemini API rate limits
3. **Data Freshness:** Depends on source update frequency
4. **Coverage:** May not have data for all locations/commodities

---

## Best Practices

### 1. User Experience
```javascript
// Show helpful loading message
setLoading(true);
setMessage('Fetching latest market prices from government sources...');

// Handle no results gracefully
if (data.prices.length === 0) {
  setMessage('No prices found. Try a different location or commodity.');
}
```

### 2. Error Recovery
```javascript
// Retry with broader search if specific commodity fails
try {
  const prices = await getMarketPrices(location, commodity);
  if (prices.prices.length === 0) {
    // Try without commodity filter
    const generalPrices = await getMarketPrices(location);
    return generalPrices;
  }
  return prices;
} catch (error) {
  console.error('Failed to fetch prices:', error);
}
```

### 3. Display Formatting
```javascript
// Format prices for display
const formatPrice = (price) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(price);
};

// Display: ₹1,500
console.log(formatPrice(1500));
```

---

## Integration Checklist

- [ ] Add loading indicator (60-120 second wait)
- [ ] Implement error handling
- [ ] Add location input field
- [ ] Add optional commodity filter
- [ ] Display price trends with visual indicators
- [ ] Show source attribution
- [ ] Implement caching to reduce API calls
- [ ] Add retry logic for failed requests
- [ ] Format prices in Indian Rupees
- [ ] Show last updated timestamp

---

## Support

For issues or questions about the market prices endpoint:
1. Verify location name is correct
2. Check if commodity name is spelled correctly
3. Ensure API key is configured in Render
4. Check rate limits haven't been exceeded
5. Review error messages in response

---

## Changelog

### Version 1.0.0 (Current)
- Initial release
- AI-powered market price search
- Support for specific commodities and general queries
- Price trend indicators
- Multiple market support
