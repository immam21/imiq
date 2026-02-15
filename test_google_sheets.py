#!/usr/bin/env python3
"""
Google Sheets Connectivity Test Script for IMIQ
"""

import os
import sys

def test_google_sheets_connectivity():
    """Test Google Sheets connection with the provided sheet ID"""
    
    print("🧪 IMIQ Google Sheets Connectivity Test")
    print("=" * 50)
    
    # Check if packages are installed
    try:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        print("✅ Google Sheets packages installed successfully")
    except ImportError as e:
        print(f"❌ Missing packages: {e}")
        return False
    
    # Check credentials
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path:
        print("❌ GOOGLE_APPLICATION_CREDENTIALS not set")
        print("💡 Set it with: export GOOGLE_APPLICATION_CREDENTIALS='path/to/your/credentials.json'")
        return False
    
    if not os.path.exists(credentials_path):
        print(f"❌ Credentials file not found: {credentials_path}")
        return False
    
    print(f"✅ Credentials file found: {credentials_path}")
    
    # Test with your sheet ID
    sheet_id = "1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4"
    print(f"🔍 Testing connection to Sheet ID: {sheet_id}")
    
    try:
        # Set up credentials
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
        client = gspread.authorize(credentials)
        
        # Open the spreadsheet
        spreadsheet = client.open_by_key(sheet_id)
        print(f"✅ Connected to spreadsheet: {spreadsheet.title}")
        
        # List worksheets
        worksheets = spreadsheet.worksheets()
        print(f"📊 Found {len(worksheets)} worksheets:")
        
        for ws in worksheets:
            print(f"   - {ws.title} ({ws.row_count} rows, {ws.col_count} cols)")
        
        # Check required sheets for IMIQ
        required_sheets = ["Users", "NewOrders", "Customers", "ProductList", "ChatLogs", "ChatAssignments"]
        existing_sheets = [ws.title for ws in worksheets]
        
        missing_sheets = [sheet for sheet in required_sheets if sheet not in existing_sheets]
        if missing_sheets:
            print(f"⚠️  Missing required sheets: {missing_sheets}")
            print("💡 These will be created automatically when you enable Google Sheets in IMIQ")
        else:
            print("✅ All required sheets are present")
        
        print("\n🎉 Google Sheets connectivity test SUCCESSFUL!")
        print("✅ You can now enable Google Sheets in IMIQ Settings")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Verify your service account has access to the sheet")
        print("2. Check that the sheet ID is correct")
        print("3. Ensure your credentials JSON is valid")
        print("4. Make sure Google Sheets API is enabled in Google Cloud Console")
        return False

if __name__ == "__main__":
    success = test_google_sheets_connectivity()
    sys.exit(0 if success else 1)