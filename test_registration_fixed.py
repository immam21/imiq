#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_registration_with_streamlit_setup():
    """Test registration with the same setup that Streamlit would use"""
    
    print("🧪 Testing Registration with Streamlit Setup")
    print("=" * 50)
    
    # Set up environment like Streamlit would need
    credentials_path = "/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    print(f"✅ Set GOOGLE_APPLICATION_CREDENTIALS: {credentials_path}")
    
    # Import after setting environment
    from imiq.storage import get_storage_instance
    from imiq.settings import SettingsService
    from imiq.auth import AuthService
    
    # Initialize exactly like the app does
    from imiq.storage import ExcelStorage
    base_storage = ExcelStorage('CZ_MasterSheet.xlsx')  
    settings_service = SettingsService(base_storage)
    
    # Get the storage instance (should be Google Sheets now)
    storage = get_storage_instance(settings_service)
    print(f"📊 Storage type: {type(storage).__name__}")
    
    if hasattr(storage, 'sheet_id'):
        print(f"📋 Google Sheet ID: {storage.sheet_id}")
    
    # Initialize auth service
    auth_service = AuthService(storage)
    
    # Test registration
    test_user = {
        'email': 'newuser@test.com',
        'user_id': 'newuser123',
        'password': 'password123',
        'name': 'New Test User'
    }
    
    print(f"\n🔍 Testing registration:")
    print(f"   Email: {test_user['email']}")
    print(f"   User ID: {test_user['user_id']}")
    
    # Check users before
    users_before = storage.read_sheet("Users")
    print(f"Users before registration: {len(users_before)}")
    
    try:
        success = auth_service.create_account(
            email=test_user['email'],
            user_id=test_user['user_id'],
            password=test_user['password'],
            role='user',
            name=test_user['name']
        )
        
        print(f"Registration result: {success}")
        
        if success:
            # Check users after
            users_after = storage.read_sheet("Users")
            print(f"Users after registration: {len(users_after)}")
            
            # Verify user exists
            new_user = users_after[users_after['email'] == test_user['email']]
            if not new_user.empty:
                user_row = new_user.iloc[0]
                print(f"✅ User found in Google Sheets:")
                print(f"   User ID: {user_row['user_id']}")
                print(f"   Email: {user_row['email']}")
                print(f"   Name: {user_row['name']}")
                print(f"   Role: {user_row['role']}")
                print(f"   Active: {user_row['is_active']}")
                return True
            else:
                print("❌ User not found in Google Sheets after registration")
                return False
        else:
            print("❌ Registration returned False")
            return False
            
    except Exception as e:
        print(f"❌ Registration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_registration_with_streamlit_setup()
    if result:
        print("\n🎉 Registration test PASSED!")
    else:
        print("\n💥 Registration test FAILED!")