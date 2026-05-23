#!/usr/bin/env python3
"""
Test script to verify OpenAI integration works with the updated chat API
"""
import os
import asyncio
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_openai_integration():
    """
    Test the OpenAI API integration by making a direct call
    """
    # Get API key from environment
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        print("ERROR: LLM_API_KEY environment variable is not set")
        print("Please set your OpenAI API key in the environment variables")
        return False

    # Check if we're configured to use OpenAI
    provider = os.getenv("LLM_PROVIDER", "openai")
    if provider.lower() != "openai":
        print(f"Current provider is: {provider}. Switching to OpenAI for this test.")

    # Prepare the test request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for testing API connections."},
            {"role": "user", "content": "Hello, this is a test to verify the OpenAI API connection."}
        ],
        "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
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
                result = response.json()
                response_text = result["choices"][0]["message"]["content"].strip()
                print("✅ OpenAI API connection successful!")
                print(f"Response: {response_text}")
                return True
            else:
                print(f"❌ OpenAI API error: {response.status_code}")
                print(f"Response: {response.text}")
                return False

    except httpx.RequestError as e:
        print(f"❌ Error connecting to OpenAI API: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

async def test_backend_integration():
    """
    Test the backend integration by simulating the call_llm_api function
    """
    print("\n--- Testing Backend Integration ---")

    # Import the necessary modules to simulate the backend function
    try:
        from backend.routers.chat import call_llm_api

        # Test the function with a simple prompt
        test_prompt = "What is machine learning?"

        try:
            response = await call_llm_api(test_prompt)
            print("✅ Backend integration successful!")
            print(f"Response: {response[:200]}...")  # Truncate for display
            return True
        except Exception as e:
            print(f"❌ Backend integration failed: {str(e)}")
            return False

    except ImportError as e:
        print(f"❌ Could not import backend modules: {str(e)}")
        return False

async def main():
    """
    Main test function
    """
    print("Testing OpenAI Integration")
    print("="*50)

    # Test direct OpenAI API connection
    print("--- Testing Direct OpenAI API Connection ---")
    openai_success = await test_openai_integration()

    # Test backend integration
    backend_success = await test_backend_integration()

    print("\n" + "="*50)
    print("Test Summary:")
    print(f"Direct OpenAI API Connection: {'✅ PASS' if openai_success else '❌ FAIL'}")
    print(f"Backend Integration: {'✅ PASS' if backend_success else '❌ FAIL'}")

    if openai_success and backend_success:
        print("\n🎉 All tests passed! OpenAI integration is working correctly.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check your configuration.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)