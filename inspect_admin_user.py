#!/usr/bin/env python3
"""
Inspect Google Sheet structure and create admin user
"""

import os
import bcrypt

# Set up environment
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService
from imiq.utils import get_ist_now, generate_id

def inspect_and_create_admin():
    """Inspect sheet structure and create admin user"""
    
    print("🔍 Inspecting Google Sheets Structure")
    print("=" * 50)
    
    try:
        # Initialize services with Google Sheets
        base_storage = get_storage_instance()
        settings_service = SettingsService(base_storage)
        
        # Enable Google Sheets
        settings_service.update_setting('use_google_sheets', True)
        settings_service.update_setting('google_sheet_id', '1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4')
        
        storage = get_storage_instance(settings_service)
        
        # Read Users sheet
        print("📊 Reading Users sheet structure...")
        users_df = storage.read_sheet("Users")
        
        print(f"📋 Users sheet info:")
        print(f"   - Rows: {len(users_df)}")
        print(f"   - Columns: {list(users_df.columns)}")
        
        if not users_df.empty:
            print(f"📄 First few rows:")
            print(users_df.head(3))
        
        # Create admin user with proper structure
        print("\n👤 Creating admin user...")
        
        admin_data = {
            'user_id': 'imam21',
            'email': 'immam2198@gmail.com',
            'password_hash': '',  # Will be filled below
            'plain_password': 'Iqrit@2024',
            'role': 'admin',
            'name': 'Imam21',
            'created_at': '2026-02-05T07:57:40.451Z',
            'is_active': 'TRUE'
        }
        
        # Hash the password
        plain_password = admin_data['plain_password']
        password_bytes = plain_password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        admin_data['password_hash'] = password_hash
        
        print(f"🔐 Generated password hash: {password_hash[:50]}...")
        
        # Add admin user to sheet
        print("💾 Adding admin user to Google Sheets...")
        storage.append_row("Users", admin_data)
        
        # Verify the addition
        print("🔍 Verifying user creation...")
        updated_users_df = storage.read_sheet("Users")
        admin_users = updated_users_df[updated_users_df['email'] == 'immam2198@gmail.com'] if 'email' in updated_users_df.columns else updated_users_df
        
        if len(admin_users) > 0:
            print("✅ Admin user created successfully!")
            admin_user = admin_users.iloc[-1]  # Get the last matching user
            print(f"📧 Email: {admin_user.get('email', 'N/A')}")
            print(f"👤 Name: {admin_user.get('name', 'N/A')}")  
            print(f"🔑 Role: {admin_user.get('role', 'N/A')}")
            print(f"🔐 Has password hash: {'Yes' if admin_user.get('password_hash', '') else 'No'}")
            return True
        else:
            print("❌ Failed to verify admin user creation")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = inspect_and_create_admin()
    if success:
        print("\n🎉 Admin user setup complete!")
        print("✅ Login credentials: immam2198@gmail.com / Iqrit@2024")
    else:
        print("\n❌ Failed to setup admin user")