import requests
import json
import os
from datetime import datetime

# API Configuration
BASE_URL = "http://localhost:8081"
API_VERSION = "/api/v1"

def get_auth_token():
    """
    In a real application, you would implement proper authentication.
    This is a simplified example that assumes a pre-configured token.
    """
    # This would typically involve a login request
    # For testing, we'll use a dummy token
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjE3MTExMjM0NTZ9.your_secret_key_signature"

def test_tts_generation():
    # Get authentication token
    token = get_auth_token()
    
    # Prepare headers with authentication
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Prepare TTS request
    tts_request = {
        "text": "Hello, this is Tim testing the text to speech API. I hope you're having a wonderful day!",
        "voice_profile": "Tim"
    }
    
    # Make request to TTS endpoint
    response = requests.post(
        f"{BASE_URL}{API_VERSION}/tts/synthesize",
        headers=headers,
        json=tts_request
    )
    
    # Check if request was successful
    if response.status_code == 200:
        # Save the audio file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"test_output_{timestamp}.wav"
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        print(f"Successfully generated speech: {output_file}")
        return True
    else:
        print(f"Error generating speech: {response.status_code}")
        print(response.json())
        return False

if __name__ == "__main__":
    # Test health check
    health_response = requests.get(f"{BASE_URL}/health")
    print(f"Health check status: {health_response.json()}")
    
    # Test TTS generation
    test_tts_generation() 