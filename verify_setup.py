#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set credentials like the app does
credentials_path = os.path.join(os.path.dirname(__file__), 'service_account.json')
if os.path.exists(credentials_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    print(f"✅ Set GOOGLE_APPLICATION_CREDENTIALS: {credentials_path}")

from imiq.storage import get_storage_instance, ExcelStorage
from imiq.settings import SettingsService

def verify_current_setup():
    """Verify the current app setup matches what we expect"""
    
    print("🔍 Verifying Current App Setup")
    print("=" * 50)
    
    # Initialize like the app does
    base_storage = ExcelStorage('CZ_MasterSheet.xlsx')  # App line 49
    settings_service = SettingsService(base_storage)    # App base_services
    
    # Check settings
    use_gs = settings_service.get_setting('use_google_sheets', False)
    sheet_id = settings_service.get_setting('google_sheet_id', '')
    
    print(f"📋 use_google_sheets: {use_gs}")
    print(f"📋 google_sheet_id: {sheet_id}")
    print(f"📁 GOOGLE_APPLICATION_CREDENTIALS: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'NOT SET')}")
    
    # Get storage instance like the app does
    storage = get_storage_instance(settings_service)    # App line 55
    print(f"📊 Storage type: {type(storage).__name__}")
    
    if hasattr(storage, 'sheet_id'):
        print(f"📋 Active Sheet ID: {storage.sheet_id}")
    
    # Test reading Users sheet
    try:
        users_df = storage.read_sheet("Users")
        print(f"👥 Users in storage: {len(users_df)} rows")
        
        if not users_df.empty:
            print("Latest users:")
            for _, user in users_df.tail(3).iterrows():
                print(f"  - {user['user_id']}: {user['email']} ({user['role']})")
        
        print("✅ Storage is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Storage error: {e}")
        return False

if __name__ == "__main__":
    verify_current_setup()