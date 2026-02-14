#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_userid_only_auth():
    """Test the new user_id only authentication system"""
    
    print("🧪 Testing User ID Only Authentication")
    print("=" * 50)
    
    # Set up environment
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'
    
    from imiq.storage import get_storage_instance, ExcelStorage
    from imiq.settings import SettingsService
    from imiq.auth import AuthService
    
    # Initialize services
    base_storage = ExcelStorage('CZ_MasterSheet.xlsx')
    settings_service = SettingsService(base_storage)
    storage = get_storage_instance(settings_service)
    auth_service = AuthService(storage)
    
    print(f"🏪 Using storage: {type(storage).__name__}")
    
    # Test creating account without email
    import time
    timestamp = int(time.time())
    test_user_id = f"testuser{timestamp}"
    test_password = "testpass123"
    test_name = "Test User"
    
    print(f"\\n🆕 Testing Account Creation:")
    print(f"   User ID: {test_user_id}")
    print(f"   Password: {test_password}")
    print(f"   Name: {test_name}")
    print(f"   Email: Not provided")
    
    try:
        success = auth_service.create_account(
            user_id=test_user_id,
            password=test_password,
            role="user",
            name=test_name
        )
        
        if success:
            print("✅ Account created successfully!")
            
            # Test authentication with user_id
            print(f"\\n🔐 Testing Authentication:")
            user = auth_service.authenticate(test_user_id, test_password)
            
            if user:
                print("✅ Authentication successful!")
                print(f"   User ID: {user['user_id']}")
                print(f"   Name: {user['name']}")
                print(f"   Role: {user['role']}")
                print(f"   Email: '{user.get('email', 'Not provided')}'")
                print(f"   Active: {user['is_active']}")
                
                # Test login method
                print(f"\\n🔑 Testing Login Method:")
                login_success = auth_service.login(test_user_id, test_password)
                print(f"Login result: {'✅ Success' if login_success else '❌ Failed'}")
                
                return True
            else:
                print("❌ Authentication failed")
                return False
        else:
            print("❌ Account creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_existing_users():
    """Test authentication with existing users"""
    
    print(f"\\n👥 Testing Existing Users:")
    print("=" * 30)
    
    # Set up environment
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'
    
    from imiq.storage import get_storage_instance, ExcelStorage
    from imiq.settings import SettingsService
    from imiq.auth import AuthService
    
    # Initialize services
    base_storage = ExcelStorage('CZ_MasterSheet.xlsx')
    settings_service = SettingsService(base_storage)
    storage = get_storage_instance(settings_service)
    auth_service = AuthService(storage)
    
    # Test with admin user
    admin_user_id = "imam21"
    admin_password = "Iqrit@2024"
    
    print(f"🔐 Testing Admin Authentication:")
    print(f"   User ID: {admin_user_id}")
    
    try:
        user = auth_service.authenticate(admin_user_id, admin_password)
        
        if user:
            print("✅ Admin authentication successful!")
            print(f"   User ID: {user['user_id']}")
            print(f"   Name: {user['name']}")
            print(f"   Role: {user['role']}")
            print(f"   Email: '{user.get('email', 'Not provided')}'")
            return True
        else:
            print("❌ Admin authentication failed")
            return False
    except Exception as e:
        print(f"❌ Admin auth error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 User ID Only Authentication Testing")
    print("=" * 60)
    
    # Test new account creation
    new_user_test = test_userid_only_auth()
    
    # Test existing users
    existing_user_test = test_existing_users()
    
    print(f"\\n📊 Test Results:")
    print(f"   New User Creation & Auth: {'✅ PASS' if new_user_test else '❌ FAIL'}")
    print(f"   Existing User Auth: {'✅ PASS' if existing_user_test else '❌ FAIL'}")
    
    if new_user_test and existing_user_test:
        print(f"\\n🎉 All tests passed! User ID only authentication is working!")
        print(f"\\n📝 Summary:")
        print(f"   • Email field is now optional")
        print(f"   • Users can register with just User ID and Password") 
        print(f"   • Authentication works with User ID only")
        print(f"   • Existing users continue to work")
    else:
        print(f"\\n💥 Some tests failed. Check the errors above.")