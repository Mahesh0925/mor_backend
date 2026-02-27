#!/usr/bin/env python3
"""Test if app can be imported successfully"""

import sys
import traceback

print("=" * 50)
print("Testing app import...")
print("=" * 50)

try:
    print("Step 1: Importing app module...")
    import app
    print("✅ App module imported successfully")
    
    print("\nStep 2: Checking Flask app...")
    print(f"Flask app: {app.app}")
    print(f"Flask app name: {app.app.name}")
    
    print("\nStep 3: Checking API keys...")
    print(f"Gemini API key loaded: {bool(app.api_key)}")
    print(f"Weather API key loaded: {bool(app.weather_api_key)}")
    
    print("\nStep 4: Checking routes...")
    routes = [str(rule) for rule in app.app.url_map.iter_rules()]
    print(f"Number of routes: {len(routes)}")
    for route in routes:
        print(f"  - {route}")
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED - App can be imported!")
    print("=" * 50)
    sys.exit(0)
    
except Exception as e:
    print("\n" + "=" * 50)
    print("❌ ERROR - App import failed!")
    print("=" * 50)
    print(f"\nError: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
