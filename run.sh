#!/bin/bash

# Quick Start - Run IMIQ Application
# This script starts the Streamlit application

echo "🚀 Starting IMIQ Application..."
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found."
    echo ""
    echo "Please run setup first:"
    echo "   bash setup.sh"
    echo ""
    exit 1
fi

echo "📱 Starting Streamlit server..."
echo "🌐 Access the app at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
