import requests
import json
from generate_token import generate_test_token
import os
import time

BASE_URL = "http://localhost:8081/api/v1"

def test_api():
    # Ensure the server is running
    max_retries = 3
    retry_delay = 2
    
    # Generate token
    token = generate_test_token()
    print(f"\nUsing token: {token}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Test health endpoint
    try:
        for i in range(max_retries):
            try:
                health_response = requests.get(f"http://localhost:8081/health")
                print("\nHealth check:", health_response.json())
                break
            except requests.exceptions.ConnectionError:
                if i < max_retries - 1:
                    print(f"Connection failed, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    raise
    except Exception as e:
        print(f"Health check failed: {str(e)}")
        return

    # List available voices
    voices_response = None
    try:
        voices_response = requests.get(
            f"{BASE_URL}/voices/list",
            headers=headers
        )
        print("\nAvailable voices:", voices_response.json())
    except Exception as e:
        print(f"Failed to list voices: {str(e)}")
        if voices_response and hasattr(voices_response, 'text'):
            print(f"Response: {voices_response.text}")
        return

    # Synthesize speech
    tts_request = {
        "text": "Hello, this is a test of the F5 TTS system.",
        "voice_profile": "bane"  # Use one of the available voices from the list
    }

    try:
        tts_response = requests.post(
            f"{BASE_URL}/tts/synthesize",
            headers=headers,
            json=tts_request
        )

        if tts_response.status_code == 200:
            # Save the audio file
            with open("test_output.wav", "wb") as f:
                f.write(tts_response.content)
            print("\nSpeech generated successfully! Saved as test_output.wav")
        else:
            print(f"\nError generating speech: {tts_response.status_code}")
            print(f"Response: {tts_response.text}")
    except Exception as e:
        print(f"\nFailed to generate speech: {str(e)}")

if __name__ == "__main__":
    test_api() 