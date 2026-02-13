#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from imiq.storage import ExcelStorage, get_storage_instance
from imiq.settings import SettingsService

def configure_google_sheets():
    """Configure Google Sheets settings properly"""
    
    print("🔧 Configuring Google Sheets Settings")
    print("=" * 50)
    
    # Initialize with Excel storage first
    excel_storage = ExcelStorage('CZ_MasterSheet.xlsx')
    settings_service = SettingsService(excel_storage)
    
    # Check current settings
    current_use_gs = settings_service.get_setting('use_google_sheets', False)
    current_sheet_id = settings_service.get_setting('google_sheet_id', '')
    
    print(f"Current use_google_sheets: {current_use_gs}")
    print(f"Current google_sheet_id: {current_sheet_id}")
    
    # Configure proper settings
    sheet_id = "1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4"
    
    print(f"\n🔄 Setting use_google_sheets to True")
    settings_service.update_setting('use_google_sheets', True)
    
    print(f"🔄 Setting google_sheet_id to: {sheet_id}")
    settings_service.update_setting('google_sheet_id', sheet_id)
    
    # Verify settings were saved
    updated_use_gs = settings_service.get_setting('use_google_sheets', False)
    updated_sheet_id = settings_service.get_setting('google_sheet_id', '')
    
    print(f"\n✅ Updated use_google_sheets: {updated_use_gs}")
    print(f"✅ Updated google_sheet_id: {updated_sheet_id}")
    
    # Check environment variables
    google_creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    print(f"📁 Google credentials path: {google_creds}")
    
    if google_creds and os.path.exists(google_creds):
        print("✅ Google credentials file exists")
    else:
        print("❌ Google credentials file not found")
    
    # Test storage initialization
    print(f"\n🧪 Testing storage initialization:")
    try:
        storage = get_storage_instance(settings_service)
        print(f"Storage type: {type(storage).__name__}")
        
        if hasattr(storage, 'sheet_id'):
            print(f"Google Sheet ID: {storage.sheet_id}")
        
        # Test reading Users sheet
        users_df = storage.read_sheet("Users")
        print(f"Users sheet has {len(users_df)} rows")
        
        print("✅ Google Sheets storage working correctly!")
        
    except Exception as e:
        print(f"❌ Storage initialization failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    configure_google_sheets()