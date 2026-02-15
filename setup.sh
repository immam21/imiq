#!/bin/bash

# IMIQ Local Development Setup Script
# This script sets up everything needed to run IMIQ locally

set -e  # Exit on error

echo "🚀 IMIQ Local Setup"
echo "===================="
echo ""

# Check Python version
echo "📌 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Install requirements
echo "📦 Installing dependencies..."
echo "   (This may take a few minutes)"
echo ""

pip3 install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "🎉 Setup Successful!"
echo ""
echo "To start the application, run:"
echo ""
echo "   streamlit run app.py"
echo ""
echo "The app will be available at: http://localhost:8501"
echo ""
echo "Test Credentials:"
echo "   Admin: admin@test.com / admin123"
echo "   User: Create via signup form"
echo ""
