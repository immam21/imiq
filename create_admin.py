#!/usr/bin/env python3
"""
Create admin user for IMIQ system
"""
import sys
import os
sys.path.append('.')

from imiq.storage import get_storage_instance
from imiq.utils import get_ist_now
from imiq.auth import AuthService

def create_admin_user():
    """Create admin user with proper authentication"""
    try:
        storage = get_storage_instance()
        auth_service = AuthService(storage)
        
        # Check existing users
        from imiq.performance import get_cached_sheet_data
        users_df = get_cached_sheet_data(storage, 'Users')
        print(f'Current users: {len(users_df) if not users_df.empty else 0}')
        
        if not users_df.empty:
            print('Existing emails:', users_df['email'].tolist())
            if 'admin@imiq.com' in users_df['email'].values:
                print('Admin user already exists!')
                return test_authentication(auth_service)
        
        # Create admin user using the proper auth service
        print('Creating admin user...')
        success = auth_service.create_account(
            email='admin@imiq.com',
            user_id='admin', 
            password='admin123',
            role='admin',
            name='Admin User'
        )
        
        if success:
            print('✅ Admin user created successfully!')
            print('Email: admin@imiq.com')
            print('Password: admin123')
            return test_authentication(auth_service)
        else:
            print('❌ Failed to create admin user')
            return False
            
    except Exception as e:
        print(f'Error creating admin user: {e}')
        import traceback
        traceback.print_exc()
        return False

def test_authentication(auth_service):
    """Test the authentication system"""
    print('\nTesting authentication...')
    
    try:
        # Test authentication
        user = auth_service.authenticate('admin@imiq.com', 'admin123')
        if user:
            print('✅ Authentication successful!')
            print(f'User: {user["name"]} ({user["role"]})')
            return True
        else:
            print('❌ Authentication failed')
            return False
    except Exception as e:
        print(f'Authentication error: {e}')
        return False

if __name__ == '__main__':
    create_admin_user()