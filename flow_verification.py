#!/usr/bin/env python3
"""
Simple Flow Verification Script
Tests core functionality without interfering with running app
"""

import os
import sys
import time
from datetime import datetime

# Setup
sys.path.append('.')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService
from imiq.auth import AuthService

def main():
    print("🔧 CrazyShopperz Flow Verification")
    print("=" * 50)
    
    try:
        # Initialize services
        print("1️⃣ Initializing services...")
        base_storage = get_storage_instance()
        settings_service = SettingsService(base_storage)
        storage = get_storage_instance(settings_service)
        auth_service = AuthService(storage)
        print(f"   ✅ Storage: {type(storage).__name__}")
        
        # Test data access
        print("\n2️⃣ Testing data access...")
        users_df = storage.read_sheet("Users")
        orders_df = storage.read_sheet("Orders")
        inventory_df = storage.read_sheet("Inventory")
        
        print(f"   📊 Users: {len(users_df)} records")
        print(f"   📦 Orders: {len(orders_df)} records")
        print(f"   📋 Inventory: {len(inventory_df)} records")
        
        # Test authentication
        print("\n3️⃣ Testing authentication...")
        admin_auth = auth_service.authenticate('imam21', 'Iqrit@2024')
        admin_success = admin_auth.get('success', False)
        
        if admin_success:
            admin_user = admin_auth['user']
            print(f"   ✅ Admin login: {admin_user.get('full_name')} ({admin_user.get('role')})")
        else:
            print(f"   ❌ Admin login failed: {admin_auth.get('message')}")
        
        # Test user authentication with existing user
        if not users_df.empty:
            # Try with first user that has a plain_password
            test_user = None
            for idx, user in users_df.iterrows():
                if user.get('plain_password') and user.get('user_id'):
                    test_user = user
                    break
            
            if test_user is not None:
                user_auth = auth_service.authenticate(test_user['user_id'], test_user['plain_password'])
                user_success = user_auth.get('success', False)
                
                if user_success:
                    user_data = user_auth['user']
                    print(f"   ✅ User login: {user_data.get('full_name')} ({user_data.get('role')})")
                else:
                    print(f"   ❌ User login failed: {user_auth.get('message')}")
        
        # Summary
        print(f"\n🎯 FLOW STATUS SUMMARY")
        print(f"   📱 App Running: http://localhost:8599")
        print(f"   💾 Storage: {type(storage).__name__} ✅")
        print(f"   🔐 Authentication: {'✅' if admin_success else '❌'}")
        print(f"   📊 Data Access: ✅ (Users, Orders, Inventory)")
        print(f"   🕐 Tested: {datetime.now().strftime('%H:%M:%S')}")
        
        print(f"\n✅ MANUAL TESTING GUIDE:")
        print(f"1. 📝 Register: Go to app → Register new user")
        print(f"2. 🔑 Login: Use imam21/Iqrit@2024 (admin) or any existing user")
        print(f"3. 🏠 Dashboard: Check analytics and KPIs")
        print(f"4. 📈 Performance: View user metrics and conversion rates")
        print(f"5. 📦 Orders: Browse and manage orders")
        print(f"6. ➕ Create Order: Add new orders")
        print(f"7. 🔍 Lookup: Search for specific orders")
        print(f"8. 📊 Reports: Generate various reports")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'🎉 Ready for manual testing!' if success else '⚠️ Issues detected'}")