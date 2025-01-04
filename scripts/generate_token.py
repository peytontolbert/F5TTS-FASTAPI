import jwt
from datetime import datetime, timedelta
import os

def generate_test_token():
    """Generate a test JWT token"""
    # Use the same secret key as in settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM = "HS256"
    
    # Token data
    payload = {
        "sub": "test_user",  # subject (user identifier)
        "exp": datetime.utcnow() + timedelta(days=1),  # expiration time
        "iat": datetime.utcnow(),  # issued at
        "scope": "tts"  # scope of access
    }
    
    # Generate token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

if __name__ == "__main__":
    token = generate_test_token()
    print("\nGenerated test token:")
    print(token)
    print("\nUse this token in the Authorization header as:")
    print(f"Bearer {token}") 