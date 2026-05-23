import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

async def test_openai_integration():
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        print("ERROR: LLM_API_KEY environment variable is not set")
        return False

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for testing API connections."},
            {"role": "user", "content": "Hello, this is a test."}
        ],
        "model": "gpt-3.5-turbo",
        "temperature": 0.3,
        "max_tokens": 100
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers
            )

            if response.status_code == 200:
                print("✅ OpenAI API connection successful!")
                return True
            else:
                print(f"❌ OpenAI API error: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_openai_integration())
