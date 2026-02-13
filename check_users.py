#!/usr/bin/env python3
"""
Check actual user credentials in IMIQ system
"""
import sys
import os
sys.path.append('.')

from imiq.storage import get_storage_instance
from imiq.auth import AuthService
import pandas as pd

def check_user_credentials():
    """Check actual user data and test authentication"""
    try:
        storage = get_storage_instance()
        users_df = storage.read_sheet('Users')
        
        print('=== EXISTING USERS ===')
        if not users_df.empty:
            print(f'Total users: {len(users_df)}')
            print('\nUser details:')
            
            for idx, row in users_df.iterrows():
                email = row.get('email', 'N/A')
                user_id = row.get('user_id', 'N/A')
                role = row.get('role', 'N/A')
                name = row.get('name', 'N/A')
                plain_password = row.get('plain_password', '')
                has_hash = bool(row.get('password_hash', ''))
                
                print(f'\n{idx+1}. Email: {email}')
                print(f'   User ID: {user_id}')
                print(f'   Role: {role}')
                print(f'   Name: {name}')
                if plain_password:
                    print(f'   Plain Password: {plain_password}')
                print(f'   Has Password Hash: {has_hash}')
                print('---')
        else:
            print('No users found!')
            
        # Test authentication with known users
        print('\n=== TESTING AUTHENTICATION ===')
        auth_service = AuthService(storage)
        
        # Test credentials that might exist
        test_credentials = [
            ('admin@imiq.com', 'admin123'),
            ('admin@test.com', 'admin123'),
            ('crazyshopperz.in@gmail.com', 'password'),
            ('crazyshopperz.in@gmail.com', '123456'),
            ('immam2198@gmail.com', 'password'),
            ('immam2198@gmail.com', '123456'),
        ]
        
        for email, password in test_credentials:
            try:
                user = auth_service.authenticate(email, password)
                if user:
                    print(f'✅ SUCCESS: {email} / {password}')
                    print(f'   User: {user["name"]} ({user["role"]})')
                    break
                else:
                    print(f'❌ FAILED: {email} / {password}')
            except Exception as e:
                print(f'❌ ERROR: {email} / {password} - {e}')
                
        # If plain passwords exist, try those
        if not users_df.empty:
            for idx, row in users_df.iterrows():
                email = row.get('email', '')
                plain_password = row.get('plain_password', '')
                if email and plain_password:
                    try:
                        user = auth_service.authenticate(email, plain_password)
                        if user:
                            print(f'✅ SUCCESS (from plain): {email} / {plain_password}')
                            print(f'   User: {user["name"]} ({user["role"]})')
                        else:
                            print(f'❌ FAILED (from plain): {email} / {plain_password}')
                    except Exception as e:
                        print(f'❌ ERROR (from plain): {email} / {plain_password} - {e}')
        
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_user_credentials()