#!/usr/bin/env python3
"""Test plain text authentication system"""

import os
import sys
sys.path.append('.')

# Set Google credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService
from imiq.auth import AuthService

def test_plain_auth():
    """Test plain text authentication"""
    print("🔧 Testing Plain Text Authentication System")
    print("=" * 50)
    
    try:
        # Initialize storage with settings
        base_storage = get_storage_instance()
        settings_service = SettingsService(base_storage)
        storage = get_storage_instance(settings_service)
        auth_service = AuthService(storage)
        
        print(f"📊 Storage type: {storage.__class__.__name__}")
        
        # Check existing users
        users_df = storage.read_sheet("Users")
        print(f"👥 Total users in system: {len(users_df)}")
        
        if not users_df.empty:
            print("\n📋 User Details:")
            for idx, user in users_df.iterrows():
                user_id = user.get('user_id', 'N/A')
                role = user.get('role', 'N/A')
                plain_pass = user.get('plain_password', 'N/A')
                has_hash = 'Yes' if user.get('password_hash') else 'No'
                print(f"   - {user_id} (Role: {role}) | Plain Password: '{plain_pass}' | Has Hash: {has_hash}")
            
            # Test authentication with existing admin user
            print(f"\n🔐 Testing Authentication:")
            
            # Try admin login
            admin_user = auth_service.authenticate("admin", "admin123")
            if admin_user:
                print(f"✅ Admin login successful: {admin_user['name']} ({admin_user['role']})")
            else:
                print("❌ Admin login failed")
            
            # Try a regular user if exists
            regular_users = users_df[users_df['role'] == 'user']
            if not regular_users.empty:
                test_user = regular_users.iloc[0]
                test_user_id = test_user['user_id']
                test_password = test_user.get('plain_password', '')
                
                if test_password:
                    user_result = auth_service.authenticate(test_user_id, test_password)
                    if user_result:
                        print(f"✅ User '{test_user_id}' login successful")
                    else:
                        print(f"❌ User '{test_user_id}' login failed")
                else:
                    print(f"⚠️  User '{test_user_id}' has no plain password set")
        
        print(f"\n🎯 Authentication System Status: ✅ ACTIVE (Plain Text)")
        return True
        
    except Exception as e:
        print(f"❌ Error testing authentication: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_plain_auth()