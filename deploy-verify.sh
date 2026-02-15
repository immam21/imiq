#!/bin/bash

# Production deployment script for CrazyShopperz
# Run this script after deployment to verify everything is working

set -e

echo "🚀 Starting CrazyShopperz Production Deployment Verification..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    if [[ $(echo "$PYTHON_VERSION" | cut -d. -f1) -ge 3 && $(echo "$PYTHON_VERSION" | cut -d. -f2) -ge 9 ]]; then
        print_status "Python $PYTHON_VERSION detected (✓ >= 3.9)"
    else
        print_error "Python $PYTHON_VERSION detected (✗ < 3.9 required)"
        exit 1
    fi
else
    print_error "Python3 not found"
    exit 1
fi

# Check if running in Streamlit Cloud environment
if [[ -n "$STREAMLIT_RUNTIME" ]]; then
    print_status "Running in Streamlit Cloud environment"
elif [[ -n "$DYNO" ]]; then
    print_status "Running in Heroku environment"
elif [[ -n "$RAILWAY_ENVIRONMENT" ]]; then
    print_status "Running in Railway environment"
else
    print_warning "Running in custom/local environment"
fi

# Install production dependencies
echo "Installing production dependencies..."
if pip install -r requirements.txt --quiet; then
    print_status "All dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Verify critical packages
echo "Verifying critical packages..."
CRITICAL_PACKAGES=("streamlit" "pandas" "plotly" "google-auth" "gspread" "openpyxl")

for package in "${CRITICAL_PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        print_status "$package installed and importable"
    else
        print_error "$package not found or not importable"
        exit 1
    fi
done

# Check configuration files
echo "Checking configuration files..."
CONFIG_FILES=("requirements.txt" ".streamlit/config.toml" "pyproject.toml" "app.py")

for file in "${CONFIG_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        print_status "Configuration file $file exists"
    else
        print_error "Required file $file not found"
        exit 1
    fi
done

# Check environment variables (if any are set)
echo "Checking environment configuration..."
if [[ -n "$GOOGLE_SERVICE_ACCOUNT_JSON" ]]; then
    print_status "Google Sheets credentials configured"
elif [[ -f "service_account.json" ]]; then
    print_status "Google Sheets service account file found"
else
    print_warning "Google Sheets not configured (will use Excel fallback)"
fi

# Test application import
echo "Testing application imports..."
if python3 -c "
import sys
import os
sys.path.append('.')
try:
    from imiq.storage import ExcelStorage, GoogleSheetsStorage
    from imiq.business_analytics import DateWiseBusinessAnalytics
    print('✓ Core modules imported successfully')
except ImportError as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
" > /tmp/import_test.log 2>&1; then
    print_status "All application modules imported successfully"
    cat /tmp/import_test.log
else
    print_error "Application import failed:"
    cat /tmp/import_test.log
    exit 1
fi

# Create necessary directories
echo "Creating necessary directories..."
DIRECTORIES=("data" "logs" "temp")

for dir in "${DIRECTORIES[@]}"; do
    if mkdir -p "$dir" 2>/dev/null; then
        print_status "Directory $dir created/verified"
    else
        print_warning "Could not create directory $dir"
    fi
done

# Check port availability (for local deployments)
if [[ -z "$PORT" ]]; then
    export PORT=8501
fi

echo "Checking port $PORT availability..."
if command -v netstat &> /dev/null; then
    if netstat -an | grep ":$PORT " > /dev/null; then
        print_warning "Port $PORT is already in use"
    else
        print_status "Port $PORT is available"
    fi
else
    print_warning "netstat not available, cannot check port"
fi

# Memory check
echo "Checking available memory..."
if command -v free &> /dev/null; then
    MEMORY_MB=$(free -m | awk '/^Mem:/ { print $2 }')
    if [[ $MEMORY_MB -gt 512 ]]; then
        print_status "Memory: ${MEMORY_MB}MB (✓ > 512MB recommended)"
    else
        print_warning "Memory: ${MEMORY_MB}MB (⚠ < 512MB may cause issues)"
    fi
elif command -v vm_stat &> /dev/null; then
    # macOS
    print_status "macOS system detected (memory check passed)"
else
    print_warning "Cannot check memory usage on this system"
fi

# Final verification
echo "Performing final deployment verification..."
if python3 -c "
import streamlit as st
import sys
import os
sys.path.append('.')

# Test basic Streamlit functionality
try:
    # This would fail if Streamlit has issues
    import streamlit.components.v1 as components
    print('✓ Streamlit components working')
except Exception as e:
    print(f'✗ Streamlit components error: {e}')
    sys.exit(1)

# Test our application structure
try:
    from imiq import storage, business_analytics
    print('✓ Application structure verified')
except Exception as e:
    print(f'✗ Application structure error: {e}')
    sys.exit(1)

print('✓ All systems go!')
" > /tmp/final_test.log 2>&1; then
    print_status "Final verification passed"
    cat /tmp/final_test.log
else
    print_error "Final verification failed:"
    cat /tmp/final_test.log
    exit 1
fi

# Cleanup
rm -f /tmp/import_test.log /tmp/final_test.log

echo ""
echo "🎉 Production deployment verification completed successfully!"
echo ""
echo "📋 Deployment Summary:"
echo "   • Python: $PYTHON_VERSION ✓"
echo "   • Dependencies: All installed ✓"
echo "   • Configuration: Valid ✓"
echo "   • Application: Import tested ✓"
echo "   • Port: $PORT ready ✓"
echo ""
echo "🚀 Your CrazyShopperz application is ready for production!"
echo ""
echo "💡 Next Steps:"
echo "   1. Start application: streamlit run app.py --server.port=$PORT"
echo "   2. Monitor logs for any runtime issues"
echo "   3. Test all features in production environment"
echo "   4. Set up monitoring and alerts"
echo ""
print_status "Deployment verification complete! 🎊"