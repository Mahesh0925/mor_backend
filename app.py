import base64
import json
import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY", "")
weather_api_key = os.getenv("WEATHER_API_KEY", "")
MODEL_NAME = "gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"
WEATHER_FORECAST_URL = "http://api.weatherapi.com/v1/forecast.json"


@app.get("/")
def health_check():
    return jsonify({"message": "Crop Disease Detection API is running"})


@app.post("/detect-disease")
def detect_disease():
    if not api_key:
        return jsonify({"detail": "GEMINI_API_KEY is not set on the server."}), 500

    if "file" not in request.files:
        return jsonify({"detail": "Image file field 'file' is required."}), 400

    image_file = request.files["file"]

    if not image_file.mimetype or not image_file.mimetype.startswith("image/"):
        return jsonify({"detail": "Please upload a valid image file."}), 400

    image_bytes = image_file.read()
    if not image_bytes:
        return jsonify({"detail": "Uploaded image is empty."}), 400

    prompt = (
        "You are an agriculture expert. Analyze this crop image and detect disease if present. "
        "Return strictly valid JSON with this schema: "
        "{\"disease\":\"...\",\"cure\":\"...\",\"confidence\":\"low|medium|high\"}. "
        "If healthy, set disease to 'No disease detected' and give preventive care in cure."
    )

    try:
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": image_file.mimetype,
                                "data": image_b64,
                            }
                        },
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json",
            },
        }

        response = requests.post(
            GEMINI_URL,
            params={"key": api_key},
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=90,
        )
        response.raise_for_status()

        response_json = response.json()
        raw_text = (
            response_json.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )

        cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()

        try:
            result = json.loads(cleaned_text)
            if "disease" not in result or "cure" not in result:
                raise ValueError("Missing required keys")
            return jsonify(result)
        except Exception:
            return (
                jsonify(
                    {
                        "disease": "Unknown",
                        "cure": "Could not parse structured output. Please retry with a clearer crop image.",
                        "raw_response": raw_text,
                    }
                ),
                200,
            )

    except Exception as exc:
        return jsonify({"detail": f"Gemini request failed: {exc}"}), 500


@app.post("/chatbot")
def chatbot():
    if not api_key:
        return jsonify({"detail": "GEMINI_API_KEY is not set on the server."}), 500

    body = request.get_json(silent=True) or {}
    message = (body.get("message") or "").strip()
    history = body.get("history") or []

    if not message:
        return jsonify({"detail": "Field 'message' is required."}), 400

    if not isinstance(history, list):
        return jsonify({"detail": "Field 'history' must be a list if provided."}), 400

    conversation_lines = []
    for item in history:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or "user").strip().lower()
        content = str(item.get("content") or "").strip()
        if content:
            speaker = "Farmer" if role == "user" else "Assistant"
            conversation_lines.append(f"{speaker}: {content}")

    conversation_lines.append(f"Farmer: {message}")
    conversation_text = "\n".join(conversation_lines)

    system_prompt = (
        "You are a helpful agriculture assistant for farmers using our app. "
        "Our app supports crop disease detection, land measurement, and other farm utilities. "
        "Give practical, safe, low-cost, step-by-step advice in simple language. "
        "If location-specific or uncertain, ask a short follow-up question before assuming. "
        "Keep replies concise and action-oriented."
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": system_prompt},
                    {"text": conversation_text},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
        },
    }

    try:
        response = requests.post(
            GEMINI_URL,
            params={"key": api_key},
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=90,
        )
        response.raise_for_status()

        response_json = response.json()
        raw_text = (
            response_json.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )

        if not raw_text:
            return jsonify({"detail": "Empty response from model."}), 502

        return jsonify({"reply": raw_text})

    except Exception as exc:
        return jsonify({"detail": f"Gemini request failed: {exc}"}), 500


@app.post("/gov-schemes")
def gov_schemes():
    if not api_key:
        return jsonify({"detail": "GEMINI_API_KEY is not set on the server."}), 500

    body = request.get_json(silent=True) or {}
    state = str(body.get("state") or "All States").strip()
    scheme_type = str(body.get("type") or "All Types").strip()

    prompt = (
        "Find Indian government schemes only for farmers from official or reliable public sources. "
        "Use internet search results to provide up-to-date information. "
        f"Filter preference: state='{state}', type='{scheme_type}'. "
        "Return STRICTLY valid JSON with this schema: "
        "{"
        "\"state\":\"...\","
        "\"type\":\"...\","
        "\"schemes\":["
        "{"
        "\"name\":\"...\","
        "\"state\":\"...\","
        "\"type\":\"...\","
        "\"summary\":\"...\","
        "\"eligibility\":\"...\","
        "\"benefits\":[\"...\"],"
        "\"how_to_apply\":\"...\","
        "\"official_links\":[\"https://...\"]"
        "}"
        "]"
        "}. "
        "Rules: include only schemes for farmers, exclude non-farmer schemes, and include official links whenever possible."
    )

    base_payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
        },
    }

    payload_variants = [
        {**base_payload, "tools": [{"google_search": {}}]},
        {**base_payload, "tools": [{"google_search_retrieval": {}}]},
        base_payload,
    ]

    try:
        response = None
        last_error = None

        for payload in payload_variants:
            try:
                candidate_response = requests.post(
                    GEMINI_URL,
                    params={"key": api_key},
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=120,
                )
                candidate_response.raise_for_status()
                response = candidate_response
                break
            except requests.HTTPError as http_exc:
                last_error = http_exc
                status_code = getattr(http_exc.response, "status_code", None)
                if status_code != 400:
                    raise

        if response is None:
            raise last_error if last_error else RuntimeError("No successful Gemini response")

        response_json = response.json()
        raw_text = (
            response_json.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )

        cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()

        try:
            result = json.loads(cleaned_text)
            if "schemes" not in result or not isinstance(result["schemes"], list):
                raise ValueError("Missing or invalid 'schemes' field")
            return jsonify(result)
        except Exception:
            return (
                jsonify(
                    {
                        "state": state,
                        "type": scheme_type,
                        "schemes": [],
                        "raw_response": raw_text,
                        "detail": "Could not parse structured JSON."
                    }
                ),
                200,
            )

    except Exception as exc:
        return jsonify({"detail": f"Gemini request failed: {exc}"}), 500


@app.post("/weather-crop-advisory")
def weather_crop_advisory():
    if not weather_api_key:
        return jsonify({"detail": "WEATHER_API_KEY is not set on the server."}), 500
    if not api_key:
        return jsonify({"detail": "GEMINI_API_KEY is not set on the server."}), 500

    body = request.get_json(silent=True) or {}
    city = str(body.get("city") or "").strip()
    state = str(body.get("state") or "").strip()
    country = str(body.get("country") or "IN").strip()

    if not city:
        return jsonify({"detail": "Field 'city' is required."}), 400

    query = ",".join(part for part in [city, state, country] if part)

    try:
        forecast_response = requests.get(
            WEATHER_FORECAST_URL,
            params={
                "key": weather_api_key,
                "q": query,
                "days": 5,
                "aqi": "no",
                "alerts": "yes",
            },
            timeout=30,
        )
        forecast_response.raise_for_status()
        forecast_json = forecast_response.json()

        location = forecast_json.get("location", {})
        forecast_days = forecast_json.get("forecast", {}).get("forecastday", [])

        if not forecast_days:
            return jsonify({"detail": "Weather forecast data not available for this location."}), 502

        lat = location.get("lat")
        lon = location.get("lon")
        resolved_name = location.get("name", city)
        resolved_state = location.get("region", state)
        resolved_country = location.get("country", country)

        daily_forecast = []
        for forecast_day in forecast_days[:5]:
            day_info = forecast_day.get("day", {})
            date_key = forecast_day.get("date", "")
            daily_forecast.append(
                {
                    "date": date_key,
                    "temp_min_c": round(day_info.get("mintemp_c", 0), 1),
                    "temp_max_c": round(day_info.get("maxtemp_c", 0), 1),
                    "humidity_avg": round(day_info.get("avghumidity", 0), 1),
                    "rain_mm_total": round(day_info.get("totalprecip_mm", 0), 1),
                    "condition": day_info.get("condition", {}).get("text", "unknown"),
                }
            )

        advisory_prompt = (
            "You are an agriculture advisory expert. Based on the weather forecast, suggest crops to cultivate "
            "and practical farm actions for farmers. Keep language simple and actionable. "
            "Return STRICTLY valid JSON with this schema: "
            "{"
            "\"weather_summary\":\"...\","
            "\"recommended_crops\":[{\"crop\":\"...\",\"reason\":\"...\",\"suitability\":\"high|medium|low\"}],"
            "\"farm_actions\":[\"...\"],"
            "\"risk_alerts\":[\"...\"],"
            "\"other_suggestions\":[\"...\"]"
            "}. "
            f"Location: {resolved_name}, {resolved_state}, {resolved_country}. "
            f"Forecast data: {json.dumps(daily_forecast)}"
        )

        gemini_payload = {
            "contents": [
                {
                    "parts": [
                        {"text": advisory_prompt},
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "responseMimeType": "application/json",
            },
        }

        gemini_response = requests.post(
            GEMINI_URL,
            params={"key": api_key},
            headers={"Content-Type": "application/json"},
            json=gemini_payload,
            timeout=90,
        )
        gemini_response.raise_for_status()

        gemini_json = gemini_response.json()
        raw_text = (
            gemini_json.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )
        cleaned_text = raw_text.replace("```json", "").replace("```", "").strip()

        try:
            advisory = json.loads(cleaned_text)
        except Exception:
            advisory = {
                "weather_summary": "Could not parse structured advisory.",
                "recommended_crops": [],
                "farm_actions": [],
                "risk_alerts": [],
                "other_suggestions": [],
                "raw_response": raw_text,
            }

        return jsonify(
            {
                "location": {
                    "city": resolved_name,
                    "state": resolved_state,
                    "country": resolved_country,
                    "lat": lat,
                    "lon": lon,
                },
                "forecast": daily_forecast,
                "advisory": advisory,
            }
        )

    except requests.HTTPError as http_exc:
        status_code = getattr(http_exc.response, "status_code", 500)
        error_text = getattr(http_exc.response, "text", str(http_exc))
        return jsonify({"detail": f"Weather/Gemini request failed: {error_text}"}), status_code
    except Exception as exc:
        return jsonify({"detail": f"Weather advisory failed: {exc}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")), debug=True)