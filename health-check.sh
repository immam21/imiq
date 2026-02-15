#!/bin/bash

# CrazyShopperz Deployment Health Check Script

set -e

echo "🏥 CrazyShopperz Health Check Starting..."

# Check Python version
echo "🐍 Checking Python version..."
python3 --version

# Check if required packages are installed
echo "📦 Checking required packages..."
python3 -c "
import streamlit, pandas, plotly, openpyxl
import google.auth, gspread, filelock
print('✅ All required packages are installed')
"

# Check if the application can be imported
echo "🔍 Checking application imports..."
python3 -c "
import sys
sys.path.append('.')
from app import main
from imiq.storage import get_storage_instance
from imiq.business_analytics import get_business_analytics_instance
print('✅ Application imports successfully')
"

# Check Google Sheets credentials
echo "🔐 Checking Google Sheets credentials..."
python3 -c "
import os
if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
    print('✅ GOOGLE_APPLICATION_CREDENTIALS environment variable set')
elif os.path.exists('service_account.json'):
    print('✅ Local service account file found')
else:
    print('⚠️  No Google Sheets credentials found - using Excel fallback')
"

# Check port availability
PORT=${PORT:-8501}
echo "🌐 Checking port $PORT availability..."

if command -v lsof >/dev/null 2>&1; then
    if lsof -i:$PORT >/dev/null 2>&1; then
        echo "⚠️  Port $PORT is already in use"
    else
        echo "✅ Port $PORT is available"
    fi
else
    echo "ℹ️  lsof not available, skipping port check"
fi

echo "🎉 Health check completed successfully!"
echo "🚀 Ready for deployment!"

# Optional: Start the application
if [ "$1" = "--start" ]; then
    echo "🏃 Starting CrazyShopperz application..."
    exec streamlit run app.py --server.port $PORT --server.address 0.0.0.0
fi