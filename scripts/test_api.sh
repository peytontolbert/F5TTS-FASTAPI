#!/bin/bash

# Generate token (you'll need to replace this with an actual token)
TOKEN="your_generated_token_here"

# List available voices
curl -X GET "http://localhost:8081/api/v1/voices/list" \
     -H "Authorization: Bearer $TOKEN"

# Synthesize speech
curl -X POST "http://localhost:8081/api/v1/tts/synthesize" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
         "text": "Hello, this is a test of the F5 TTS system.",
         "voice_profile": "Tim"
     }' \
     --output test_output.wav 