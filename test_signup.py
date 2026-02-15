#!/usr/bin/env python3
"""
Test signup functionality for IMIQ system
"""
import sys
import os
sys.path.append('.')

from imiq.storage import get_storage_instance
from imiq.auth import AuthService
import pandas as pd

def test_signup():
    """Test the signup functionality"""
    try:
        print("🔧 Testing signup functionality...")
        
        storage = get_storage_instance()
        auth_service = AuthService(storage)
        
        # Check current users
        users_df = storage.read_sheet('Users')
        print(f"Current users in database: {len(users_df) if not users_df.empty else 0}")
        
        if not users_df.empty:
            print("Existing users:")
            for idx, row in users_df.iterrows():
                print(f"  - {row['email']} (ID: {row['user_id']}, Role: {row['role']})")
        
        # Test creating a new user
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        test_email = f"newuser_{unique_id}@example.com"
        test_user_id = f"newuser_{unique_id}"
        
        print(f"\n🧪 Testing account creation for: {test_email}")
        
        try:
            success = auth_service.create_account(
                email=test_email,
                user_id=test_user_id,
                password="testpass123",
                role="user",
                name="Test Signup User"
            )
            
            if success:
                print("✅ Account creation returned success")
                
                # Verify the user was actually saved
                updated_users_df = storage.read_sheet('Users')
                if test_email in updated_users_df['email'].values:
                    print("✅ User successfully found in database")
                    test_user = updated_users_df[updated_users_df['email'] == test_email].iloc[0]
                    print(f"   - Email: {test_user['email']}")
                    print(f"   - User ID: {test_user['user_id']}")
                    print(f"   - Name: {test_user['name']}")
                    print(f"   - Role: {test_user['role']}")
                    print(f"   - Has password hash: {bool(test_user.get('password_hash'))}")
                else:
                    print("❌ User NOT found in database after creation!")
                    
                # Test authentication
                print(f"\n🔐 Testing authentication for new user...")
                auth_result = auth_service.authenticate(test_email, "testpass123")
                if auth_result:
                    print("✅ Authentication successful")
                    print(f"   Authenticated user: {auth_result['name']} ({auth_result['role']})")
                else:
                    print("❌ Authentication failed")
                    
            else:
                print("❌ Account creation returned failure")
                
        except Exception as create_error:
            print(f"❌ Exception during account creation: {create_error}")
            import traceback
            traceback.print_exc()
            
        # Check final state
        final_users_df = storage.read_sheet('Users')
        print(f"\n📊 Final user count: {len(final_users_df) if not final_users_df.empty else 0}")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_signup()