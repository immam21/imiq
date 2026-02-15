#!/usr/bin/env python3
"""
Test admin login credentials
"""

import os
import sys

# Set up environment
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService
from imiq.auth import AuthService

def test_admin_login():
    """Test admin login with provided credentials"""
    
    print("🧪 Testing Admin Login Credentials")
    print("=" * 50)
    
    # Admin credentials - can use either email or user_id
    admin_login = "imam21"  # Using user_id instead of email
    admin_password = "Iqrit@2024"
    
    print(f"📧 Login: {admin_login}")
    print(f"🔑 Password: {admin_password}")
    print()
    
    try:
        # Initialize services
        print("🔧 Initializing services...")
        base_storage = get_storage_instance()
        settings_service = SettingsService(base_storage)
        
        # Enable Google Sheets for testing
        print("🔄 Enabling Google Sheets...")
        settings_service.update_setting('use_google_sheets', True)
        settings_service.update_setting('google_sheet_id', '1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4')
        
        # Get storage with Google Sheets
        storage = get_storage_instance(settings_service)
        auth_service = AuthService(storage)
        
        print(f"📊 Using storage type: {type(storage).__name__}")
        print()
        
        # Test authentication
        print("🔐 Testing authentication...")
        result = auth_service.authenticate(admin_login, admin_password)
        
        if result is not None and isinstance(result, dict) and 'email' in result:
            user_data = result
            print("✅ Authentication SUCCESSFUL!")
            print()
            print("👤 User Details:")
            print(f"   - User ID: {user_data['user_id']}")
            print(f"   - Email: {user_data['email']}")
            print(f"   - Role: {user_data['role']}")
            print(f"   - Name: {user_data['name']}")
            print(f"   - Created: {user_data['created_at']}")
            print(f"   - Active: {user_data['is_active']}")
            print()
            
            if user_data['role'].lower() == 'admin':
                print("🔑 ✅ ADMIN ACCESS CONFIRMED!")
                print("🎯 You can login to IMIQ with these credentials:")
                print(f"   Login: {admin_login} (user_id)")
                print(f"   Or: {user_data['email']} (email)")
                print(f"   Password: {admin_password}")
            else:
                print(f"⚠️  User role is '{user_data['role']}', not admin")
                
            return True
            
        else:
            print("❌ Authentication FAILED!")
            print(f"Result: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_admin_login()
    if success:
        print("\n🎉 Admin user login test SUCCESSFUL!")
        print("✅ You can login with either:")
        print("   - User ID: imam21")
        print("   - Email: immam2198@gmail.com")
        print("   - Password: Iqrit@2024")
    sys.exit(0 if success else 1)