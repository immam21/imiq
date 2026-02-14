#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from imiq.auth import AuthService
import bcrypt

def test_bcrypt_hash():
    """Test bcrypt hashing and verification"""
    plain_password = "Iqrit@2024"
    
    # Generate hash manually for comparison
    salt = bcrypt.gensalt()
    manual_hash = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    
    # Test manual verification
    is_valid = bcrypt.checkpw(plain_password.encode('utf-8'), manual_hash)
    
    print("🔐 Manual bcrypt test:")
    print(f"Plain password: {plain_password}")
    print(f"Generated hash: {manual_hash}")
    print(f"Verification result: {is_valid}")
    
    return is_valid

def test_auth_logic():
    """Test authentication logic without Google Sheets dependency"""
    
    print("\n🧪 Testing Authentication Logic")
    print("=" * 50)
    
    # Mock users data
    mock_users = [
        {
            'user_id': 'imam21',
            'email': 'immam2198@gmail.com', 
            'password_hash': '$2b$12$3vAMKJE4Zz1nzAQP3G8eYOFD9K9rV9PXZ5wLX7K8CfV3N1Qm2R3T4',  # This would be the hashed version
            'role': 'admin',
            'name': 'Imam21',
            'is_active': True
        }
    ]
    
    # Hash the actual password for testing
    plain_password = "Iqrit@2024"
    proper_hash = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    mock_users[0]['password_hash'] = proper_hash.decode('utf-8')
    
    print(f"Mock user data created with proper hash")
    
    # Test authentication logic
    login = "imam21"  # Testing user_id login
    password = "Iqrit@2024"
    
    # Find user by email OR user_id
    user = None
    for u in mock_users:
        if u['email'] == login or u.get('user_id') == login:
            user = u
            break
    
    print(f"\n🔍 Looking for user with login: {login}")
    print(f"User found: {user is not None}")
    
    if user:
        print(f"Found user: {user['user_id']} ({user['email']})")
        
        # Verify password
        stored_hash = user['password_hash'].encode('utf-8')
        is_valid = bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        
        print(f"Password verification: {is_valid}")
        
        if is_valid and user.get('is_active', True):
            print("✅ Authentication successful!")
            return {
                'user_id': user['user_id'],
                'email': user['email'],
                'role': user['role'],
                'name': user['name']
            }
        else:
            print("❌ Authentication failed - invalid password or inactive user")
            return None
    else:
        print("❌ Authentication failed - user not found")
        return None

if __name__ == "__main__":
    print("🧪 Simple Authentication Test")
    print("=" * 50)
    
    # Test bcrypt functionality
    bcrypt_works = test_bcrypt_hash()
    
    if bcrypt_works:
        print("\n✅ bcrypt is working correctly")
        
        # Test authentication logic
        result = test_auth_logic()
        
        if result:
            print(f"\n🎉 Final Result: Authentication successful for {result['name']}")
        else:
            print("\n💥 Final Result: Authentication failed")
    else:
        print("\n❌ bcrypt is not working correctly")