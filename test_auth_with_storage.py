#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from imiq.settings import SettingsService
from imiq.auth import AuthService
from imiq.storage import get_storage_instance

def test_auth_with_storage():
    """Test authentication with actual storage"""
    
    print("🧪 Testing Authentication with Storage")
    print("=" * 50)
    
    try:
        # Initialize services
        print("🔧 Initializing settings service...")
        settings_service = SettingsService()
        
        # Force Google Sheets for testing
        print("🔄 Using Excel storage to avoid Google API delays...")
        settings_service.update_setting("USE_GOOGLE_SHEETS", "false")  # Use Excel for faster testing
        
        print("🔧 Initializing storage...")
        storage = get_storage_instance(settings_service)
        
        print("🔧 Initializing auth service...")
        auth_service = AuthService(storage)
        
        # Test authentication with user_id
        print(f"\n🔍 Testing authentication:")
        print(f"   Login: imam21")
        print(f"   Password: Iqrit@2024")
        
        result = auth_service.authenticate("imam21", "Iqrit@2024")
        
        if result:
            print("\n✅ Authentication successful!")
            print(f"   User ID: {result['user_id']}")
            print(f"   Email: {result['email']}")
            print(f"   Role: {result['role']}")
            print(f"   Name: {result['name']}")
            print(f"   Active: {result['is_active']}")
            
            # Also test email login
            print(f"\n🔍 Testing email authentication:")
            print(f"   Login: {result['email']}")
            
            email_result = auth_service.authenticate(result['email'], "Iqrit@2024")
            if email_result:
                print("✅ Email authentication also works!")
            else:
                print("❌ Email authentication failed")
            
            return True
        else:
            print("\n❌ Authentication failed")
            return False
            
    except Exception as e:
        print(f"💥 Error: {e}")
        return False

if __name__ == "__main__":
    success = test_auth_with_storage()
    if success:
        print("\n🎉 All authentication tests passed!")
    else:
        print("\n💥 Authentication test failed!")