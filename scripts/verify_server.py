import requests
import time
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_server(url, max_retries=5, delay=2):
    """Wait for server to become available"""
    for i in range(max_retries):
        try:
            logger.info(f"Attempting to connect to server (attempt {i+1}/{max_retries})")
            response = requests.get(url)
            if response.status_code == 200:
                logger.info("Server is up and running!")
                return True
        except requests.ConnectionError:
            logger.warning(f"Server not available, retrying in {delay} seconds...")
            time.sleep(delay)
    
    logger.error("Failed to connect to server after maximum retries")
    return False

if __name__ == "__main__":
    server_url = "http://localhost:8081/health"
    if not wait_for_server(server_url):
        sys.exit(1) 