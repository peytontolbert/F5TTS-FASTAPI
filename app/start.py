import logging
import uvicorn
from app.core.config import settings
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Check Python version
    if sys.version_info < (3, 11):
        logger.error("Python 3.11 or higher is required")
        sys.exit(1)
        
    logger.info(f"Starting FastAPI application on port {settings.PORT}")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 