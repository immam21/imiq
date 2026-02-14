#!/usr/bin/env python3
"""
Debug authentication result
"""

import os

# Set up environment
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService
from imiq.auth import AuthService

def debug_authentication():
    """Debug the authentication process"""
    
    print("🔍 Debug Authentication Process")
    print("=" * 50)
    
    try:
        # Initialize services
        base_storage = get_storage_instance()
        settings_service = SettingsService(base_storage)
        
        # Enable Google Sheets
        settings_service.update_setting('use_google_sheets', True)
        settings_service.update_setting('google_sheet_id', '1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4')
        
        storage = get_storage_instance(settings_service)
        auth_service = AuthService(storage)
        
        print(f"📊 Storage type: {type(storage).__name__}")
        
        # Check users in sheet
        users_df = storage.read_sheet("Users")
        print(f"👥 Users in sheet: {len(users_df)}")
        
        if not users_df.empty:
            print("📋 User columns:", list(users_df.columns))
            for idx, user in users_df.iterrows():
                print(f"   User {idx}: {user.get('email', 'no_email')} ({user.get('role', 'no_role')})")
        
        # Test authentication
        email = "immam2198@gmail.com"
        password = "Iqrit@2024"
        
        print(f"\n🔐 Testing authentication for: {email}")
        result = auth_service.authenticate(email, password)
        
        print(f"🔍 Authentication result type: {type(result)}")
        print(f"🔍 Authentication result: {result}")
        
        if result is None:
            print("❌ Authentication returned None")
        elif isinstance(result, dict):
            print("✅ Result is a dictionary")
            for key, value in result.items():
                print(f"   {key}: {value}")
        else:
            print(f"⚠️  Unexpected result type: {type(result)}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_authentication()