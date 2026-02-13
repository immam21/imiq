#!/usr/bin/env python3
"""
CrazyShopperz Application Entry Point
Optimized for production deployment
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def setup_environment():
    """Setup environment variables and configurations for deployment"""
    
    # Set default port for deployment
    os.environ.setdefault('PORT', '8501')
    
    # Configure Google Sheets credentials
    # For deployment, credentials should be set via environment variables
    if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS') and not os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'):
        # Check for local service account file
        local_service_account = project_root / 'service_account.json'
        if local_service_account.exists():
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(local_service_account)
            logging.info("Using local service account file for Google Sheets access")
        else:
            logging.warning("No Google Sheets credentials found. Excel storage will be used as fallback.")
    
    # Set Streamlit configuration
    os.environ.setdefault('STREAMLIT_SERVER_HEADLESS', 'true')
    os.environ.setdefault('STREAMLIT_SERVER_ENABLE_CORS', 'false')
    os.environ.setdefault('STREAMLIT_BROWSER_GATHER_USAGE_STATS', 'false')

def main():
    """Main application entry point"""
    setup_environment()
    
    try:
        # Import and run the main application
        from app import main as app_main
        logging.info("Starting CrazyShopperz application...")
        app_main()
    except Exception as e:
        logging.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()