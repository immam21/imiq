#!/usr/bin/env python3
"""
Fix admin user password hash in Google Sheets
"""

import os
import bcrypt

# Set up environment
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService
from imiq.utils import get_ist_now

def fix_admin_user():
    """Fix admin user password hash"""
    
    print("🔧 Fixing Admin User Password Hash")
    print("=" * 50)
    
    try:
        # Initialize services with Google Sheets
        base_storage = get_storage_instance()
        settings_service = SettingsService(base_storage)
        
        # Enable Google Sheets
        settings_service.update_setting('use_google_sheets', True)
        settings_service.update_setting('google_sheet_id', '1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4')
        
        storage = get_storage_instance(settings_service)
        
        # Read current users
        print("📊 Reading current users from Google Sheets...")
        from imiq.performance import get_cached_sheet_data
        users_df = get_cached_sheet_data(storage, "Users")
        print(f"Found {len(users_df)} users")
        
        # Find admin user
        admin_email = "immam2198@gmail.com"
        admin_users = users_df[users_df['email'] == admin_email]
        
        if len(admin_users) == 0:
            print(f"❌ Admin user not found: {admin_email}")
            return False
        
        admin_user = admin_users.iloc[0]
        print(f"✅ Found admin user: {admin_user['name']} ({admin_user['email']})")
        
        # Hash the password
        plain_password = "Iqrit@2024"
        print(f"🔑 Hashing password: {plain_password}")
        
        # Generate bcrypt hash
        password_bytes = plain_password.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
        
        print(f"🔐 Generated hash: {password_hash[:50]}...")
        
        # Update the user record
        print("💾 Updating user record...")
        
        def update_admin_user(row):
            if row['email'] == admin_email:
                row['password_hash'] = password_hash
                row['plain_password'] = plain_password  # Keep for reference
                row['updated_at'] = get_ist_now().isoformat()
            return row
        
        def filter_admin_user(row):
            return row['email'] == admin_email
        
        updated_count = storage.update_rows("Users", filter_admin_user, update_admin_user)
        
        if updated_count > 0:
            print(f"✅ Successfully updated {updated_count} user record")
            
            # Verify the update
            print("🔍 Verifying update...")
            updated_users_df = get_cached_sheet_data(storage, "Users")
            updated_admin = updated_users_df[updated_users_df['email'] == admin_email].iloc[0]
            
            print(f"📧 Email: {updated_admin['email']}")
            print(f"👤 Name: {updated_admin['name']}")
            print(f"🔑 Role: {updated_admin['role']}")
            print(f"🔐 Password Hash: {updated_admin['password_hash'][:50]}...")
            print(f"🔓 Plain Password: {updated_admin['plain_password']}")
            
            return True
        else:
            print("❌ Failed to update user record")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fix_admin_user()
    if success:
        print("\n🎉 Admin user password hash fixed!")
        print("✅ You can now login with: immam2198@gmail.com / Iqrit@2024")
    else:
        print("\n❌ Failed to fix admin user")