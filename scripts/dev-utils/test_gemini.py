import os
import requests
import json
import sys

def test_gemini(api_key, model="gemini-2.0-flash"):
    print(f"Testing Gemini model: {model}")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [{"text": "Hello, are you active?"}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("✅ Success! Gemini is working.")
            print(f"Response: {response.json()['candidates'][0]['content']['parts'][0]['text']}")
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Request error: {str(e)}")

if __name__ == "__main__":
    # key = input("Paste your Gemini API Key: ").strip()
    key = os.getenv("LLM_API_KEY")
    if not key:
        print("No key provided in env LLM_API_KEY.")
        sys.exit(1)
    test_gemini(key)
