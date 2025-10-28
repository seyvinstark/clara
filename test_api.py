"""
API Testing Script for NMT API
Tests all endpoints and logs results to api_mapping.json
"""

import requests
import json
from datetime import datetime
import sys
import io

# Fix Windows console encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "https://nmt-api.umuganda.digital/api/v1/translate/"

def test_get_languages():
    """Test GET request to retrieve supported languages and models"""
    print("Testing GET /api/v1/translate/...")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        data = response.json()
        print("[OK] GET successful")
        print(f"  Response: {json.dumps(data, indent=2)}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"[FAIL] GET failed: {e}")
        return None

def test_translate(src, tgt, text):
    """Test POST request to translate text"""
    print(f"\nTesting POST /api/v1/translate/ ({src} → {tgt})...")
    print(f"  Text: '{text}'")
    
    try:
        response = requests.post(
            BASE_URL,
            json={
                "src": src,
                "tgt": tgt,
                "text": text
            }
        )
        response.raise_for_status()
        data = response.json()
        translation = data.get("translation", "")
        print("  [OK] Translation successful")
        print(f"  Translation: '{translation}'")
        return data
    except requests.exceptions.RequestException as e:
        print(f"  [FAIL] Translation failed: {e}")
        if hasattr(e.response, 'json'):
            try:
                error_detail = e.response.json()
                print(f"  Error details: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"  Error: {e.response.text}")
        return None

def main():
    """Run all API tests and generate mapping file"""
    print("=" * 60)
    print("NMT API Testing Script")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "base_url": BASE_URL,
        "get_request": {},
        "post_requests": []
    }
    
    # Test 1: GET languages
    get_data = test_get_languages()
    results["get_request"] = get_data
    
    if get_data:
        # Extract language codes from the response
        languages = get_data.get("languages", {})
        print(f"\nSupported languages: {json.dumps(languages, indent=2)}")
    
    # Test 2: POST translations - Test various language pairs
    test_cases = [
        ("en", "rw", "Hello, how are you?"),
        ("en", "rw", "Good morning"),
        ("en", "rw", "How can I help you today?"),
        ("rw", "en", "Muraho"),
        ("rw", "en", "Muraho, mumeze mute?"),
        ("fr", "rw", "Bonjour"),
        ("fr", "en", "Bonjour, comment allez-vous?")
    ]
    
    for src, tgt, text in test_cases:
        result = test_translate(src, tgt, text)
        results["post_requests"].append({
            "request": {"src": src, "tgt": tgt, "text": text},
            "response": result,
            "success": result is not None
        })
    
    # Save results to JSON file
    output_file = "api_mapping.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print(f"[OK] Test results saved to {output_file}")
    print("=" * 60)
    
    # Print summary
    print("\nSummary:")
    print(f"- GET request: {'Success' if get_data else 'Failed'}")
    
    successful_translations = sum(1 for r in results["post_requests"] if r["success"])
    print(f"- POST requests: {successful_translations}/{len(test_cases)} successful")
    
    # Determine supported language pairs
    print("\nSupported language pairs:")
    for req in results["post_requests"]:
        if req["success"]:
            src = req["request"]["src"]
            tgt = req["request"]["tgt"]
            print(f"  [OK] {src} → {tgt}")
        else:
            src = req["request"]["src"]
            tgt = req["request"]["tgt"]
            print(f"  [FAIL] {src} → {tgt} (not supported)")

if __name__ == "__main__":
    main()


