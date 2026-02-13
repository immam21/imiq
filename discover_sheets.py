#!/usr/bin/env python3
"""
Sheet Discovery and Flow Test
"""

import os
import sys
sys.path.append('.')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService
from imiq.auth import AuthService

def main():
    print("🔍 CrazyShopperz Sheet Discovery & Flow Test")
    print("=" * 55)
    
    try:
        # Initialize
        base_storage = get_storage_instance()
        settings_service = SettingsService(base_storage)
        storage = get_storage_instance(settings_service)
        
        print(f"✅ Storage: {type(storage).__name__}")
        
        # Discover available sheets
        print("\n📋 Available Sheets:")
        sheets_found = {}
        
        # Try common sheet names
        sheet_names = ['Users', 'Orders', 'Inventory', 'Products', 'Customers', 'Settings']
        
        for sheet_name in sheet_names:
            try:
                df = storage.read_sheet(sheet_name)
                sheets_found[sheet_name] = len(df)
                print(f"   ✅ {sheet_name}: {len(df)} records")
            except Exception as e:
                print(f"   ❌ {sheet_name}: Not found ({str(e)[:50]}...)")
        
        # Test authentication if Users sheet exists
        if 'Users' in sheets_found and sheets_found['Users'] > 0:
            print(f"\n🔐 Authentication Test:")
            auth_service = AuthService(storage)
            
            # Test admin login
            admin_result = auth_service.authenticate('imam21', 'Iqrit@2024')
            if admin_result.get('success'):
                admin = admin_result['user']
                print(f"   ✅ Admin: {admin.get('full_name')} ({admin.get('role')})")
            else:
                print(f"   ❌ Admin login failed")
            
            # Test with any available user
            users_df = storage.read_sheet('Users')
            test_user = None
            for _, user in users_df.iterrows():
                if user.get('plain_password') and user.get('user_id'):
                    test_user = user
                    break
            
            if test_user is not None:
                user_result = auth_service.authenticate(
                    test_user['user_id'], 
                    test_user['plain_password']
                )
                if user_result.get('success'):
                    user_data = user_result['user']
                    print(f"   ✅ User: {user_data.get('full_name')} ({user_data.get('role')})")
                else:
                    print(f"   ❌ User login failed")
        
        # Flow Status Summary
        print(f"\n🎯 FLOW STATUS:")
        print(f"   🌐 App URL: http://localhost:8599")
        print(f"   📊 Data Sheets: {len(sheets_found)} found")
        print(f"   🔐 Authentication: {'✅' if 'Users' in sheets_found else '❌'}")
        
        # Test recommendations
        print(f"\n📝 MANUAL TESTING CHECKLIST:")
        print(f"1. 🌐 Open: http://localhost:8599")
        print(f"2. 📝 Register: Create new user account")
        print(f"3. 🔑 Login: Use imam21/Iqrit@2024 (admin)")
        print(f"4. 🏠 Dashboard: Check if data loads properly")
        print(f"5. 📈 Performance: Verify analytics display")
        print(f"6. 📦 Orders: Test order management")
        print(f"7. ➕ Create Order: Add new order")
        print(f"8. 🔍 Lookup: Search functionality")
        print(f"9. 📊 Reports: Generate reports")
        
        # Specific tests based on available sheets
        available_flows = []
        if 'Users' in sheets_found:
            available_flows.append("✅ Registration & Login")
        if 'Orders' in sheets_found or any('order' in name.lower() for name in sheets_found.keys()):
            available_flows.append("✅ Orders Management")
        if 'Inventory' in sheets_found or 'Products' in sheets_found:
            available_flows.append("✅ Inventory/Products")
        
        print(f"\n🎮 AVAILABLE FLOWS:")
        for flow in available_flows:
            print(f"   {flow}")
        
        return len(sheets_found) > 0
        
    except Exception as e:
        print(f"❌ Critical Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'🚀 Ready for comprehensive testing!' if success else '❌ Fix issues before testing'}")