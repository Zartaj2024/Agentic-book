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
            else:
                print(f"❌ Translation failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                
    except httpx.ConnectError:
        print("❌ Cannot connect to the backend API. Please ensure the backend server is running.")
        print(f"Expected API URL: {api_url}")
    except Exception as e:
        print(f"❌ Error occurred during translation test: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_translation_api())