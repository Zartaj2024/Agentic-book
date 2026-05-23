import requests
import os

def test_api_endpoints():
    """
    Test script to verify API endpoints are properly registered
    """
    backend_url = os.getenv("DOCUSAURUS_BACKEND_API_URL", "http://localhost:8000")

    # Test the root endpoint
    try:
        response = requests.get(f"{backend_url}/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error accessing root endpoint: {e}")

    # Test the translate health endpoint
    try:
        response = requests.get(f"{backend_url}/api/v1/health/translate")
        print(f"Translate health endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error accessing translate health endpoint: {e}")

    # Test the chat health endpoint
    try:
        response = requests.get(f"{backend_url}/api/v1/health")
        print(f"Chat health endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error accessing chat health endpoint: {e}")

if __name__ == "__main__":
    test_api_endpoints()