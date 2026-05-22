import asyncio
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_translation_api():
    """
    Test script to verify the translation API functionality
    """
    # Get backend URL from environment or use default
    backend_url = os.getenv("DOCUSAURUS_BACKEND_API_URL", "http://localhost:8000")
    api_url = f"{backend_url}/api/v1/translate"

    # Sample text to translate
    sample_text = "Physical AI refers to the integration of artificial intelligence with physical systems, particularly robots and other embodied agents."

    # Translation payload
    payload = {
        "text": sample_text,
        "target_language": "ur",
        "source_language": "en"
    }

    print(f"Testing translation API at: {api_url}")
    print(f"Sample text: {sample_text}")
    print("-" * 50)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )

            if response.status_code == 200:
                result = response.json()
                print("✅ Translation successful!")
                print(f"Original text: {result['original_text']}")
                print(f"Translated text: {result['translated_text']}")
                print(f"Target language: {result['target_language']}")
                print(f"Source language: {result['source_language']}")
                return True
            elif response.status_code == 501:
                print(f"❌ Translation provider not implemented: {response.text}")
                return False
            elif response.status_code == 400:
                print(f"❌ Bad request: {response.text}")
                return False
            else:
                print(f"❌ Translation failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                return False

    except httpx.ConnectError:
        print("❌ Cannot connect to the backend API. Please ensure the backend server is running.")
        print(f"Expected API URL: {api_url}")
        return False
    except Exception as e:
        print(f"❌ Error occurred during translation test: {str(e)}")
        return False

async def test_endpoints():
    """
    Test all API endpoints to ensure they're properly registered
    """
    backend_url = os.getenv("DOCUSAURUS_BACKEND_API_URL", "http://localhost:8000")

    endpoints_to_test = [
        ("/", "Root"),
        ("/api/v1/health", "Chat Health"),
        ("/api/v1/health/translate", "Translate Health"),
        ("/api/v1/translate", "Translate (POST)"),
    ]

    print("\nTesting API endpoints:")
    print("-" * 30)

    async with httpx.AsyncClient() as client:
        for endpoint, name in endpoints_to_test:
            try:
                if endpoint == "/api/v1/translate":
                    # This is a POST endpoint, so we'll test with a minimal request
                    response = await client.post(
                        f"{backend_url}{endpoint}",
                        json={"text": "test", "target_language": "ur"},
                        headers={"Content-Type": "application/json"},
                        timeout=10.0
                    )
                else:
                    response = await client.get(
                        f"{backend_url}{endpoint}",
                        timeout=10.0
                    )

                status = "✅" if response.status_code in [200, 400, 422] else "❌"
                print(f"{status} {name} endpoint ({endpoint}): {response.status_code}")
            except httpx.ConnectError:
                print(f"❌ {name} endpoint ({endpoint}): Cannot connect")
            except Exception as e:
                print(f"❌ {name} endpoint ({endpoint}): Error - {str(e)}")

async def main():
    """
    Main test function
    """
    print("Testing Translation API Implementation")
    print("=" * 50)

    # Test endpoints first
    await test_endpoints()

    # Then test translation functionality if possible
    print("\nTesting Translation Functionality:")
    print("-" * 35)
    success = await test_translation_api()

    if success:
        print("\n🎉 All tests passed! Translation API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. This is expected if the backend is not running or API keys are not configured.")

if __name__ == "__main__":
    asyncio.run(main())