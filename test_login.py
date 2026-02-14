#!/usr/bin/env python3
"""
Test login after signup for IMIQ system
"""
import sys
import os
sys.path.append('.')

from imiq.storage import get_storage_instance
from imiq.auth import AuthService
import pandas as pd

def test_login_after_signup():
    """Test login functionality with existing users"""
    try:
        print("🔐 Testing login after signup...")
        
        storage = get_storage_instance()
        auth_service = AuthService(storage)
        
        # Get all users from database
        users_df = storage.read_sheet('Users')
        print(f"Total users in database: {len(users_df)}")
        
        if users_df.empty:
            print("❌ No users found in database")
            return
        
        # Test with the most recently created user (assuming it's a test user)
        print("\n🧪 Testing authentication with existing users:")
        
        # Let's test with a few users
        test_users = [
            ("test_signup@example.com", "testpass123"),
            ("immam2198@gmail.com", "password"),
            ("admin@test.com", "admin123")
        ]
        
        for email, password in test_users:
            print(f"\n🔍 Testing: {email}")
            
            # Check if user exists in database
            user_exists = email in users_df['email'].values
            print(f"   User exists in DB: {'Yes' if user_exists else 'No'}")
            
            if user_exists:
                user_row = users_df[users_df['email'] == email].iloc[0]
                print(f"   User ID: {user_row['user_id']}")
                print(f"   Role: {user_row['role']}")
                print(f"   Has password hash: {'Yes' if user_row.get('password_hash') else 'No'}")
                
                # Try authentication
                try:
                    auth_result = auth_service.authenticate(email, password)
                    if auth_result:
                        print("   ✅ Authentication: SUCCESS")
                        print(f"   Logged in as: {auth_result['name']} ({auth_result['role']})")
                    else:
                        print("   ❌ Authentication: FAILED")
                        
                        # Try with different passwords if this is a known user
                        if email == "immam2198@gmail.com":
                            alt_passwords = ["123456", "admin", "immam2198"]
                            for alt_pass in alt_passwords:
                                alt_result = auth_service.authenticate(email, alt_pass)
                                if alt_result:
                                    print(f"   ✅ Authentication with '{alt_pass}': SUCCESS")
                                    break
                                    
                except Exception as auth_error:
                    print(f"   ❌ Authentication error: {auth_error}")
                    
        print(f"\n📊 Summary:")
        print(f"   Total users: {len(users_df)}")
        print(f"   Admin users: {len(users_df[users_df['role'] == 'admin'])}")
        print(f"   Regular users: {len(users_df[users_df['role'] == 'user'])}")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_login_after_signup()