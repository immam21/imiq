#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_registration_flow():
    """Verify that registrations now go to Google Sheets"""
    
    print("✅ Registration Flow Verification")
    print("=" * 50)
    
    # Set up environment like the fixed app
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'
    
    # Clear any problematic environment variables
    if 'GOOGLE_SERVICE_ACCOUNT_JSON' in os.environ:
        del os.environ['GOOGLE_SERVICE_ACCOUNT_JSON']
        print("🧹 Cleared problematic GOOGLE_SERVICE_ACCOUNT_JSON")
    
    from imiq.storage import get_storage_instance, ExcelStorage
    from imiq.settings import SettingsService
    from imiq.auth import AuthService
    
    # Initialize like the app
    base_storage = ExcelStorage('CZ_MasterSheet.xlsx')
    settings_service = SettingsService(base_storage)
    storage = get_storage_instance(settings_service)
    
    print(f"🏪 Active Storage: {type(storage).__name__}")
    
    if hasattr(storage, 'sheet_id'):
        print(f"📋 Google Sheet ID: {storage.sheet_id}")
    
    # Count users before
    from imiq.performance import get_cached_sheet_data
    gs_users_before = get_cached_sheet_data(storage, 'Users')
    excel_users_before = base_storage.read_sheet('Users')
    
    print(f"\\n👥 User Counts Before:")
    print(f"   Google Sheets: {len(gs_users_before)}")
    print(f"   Excel: {len(excel_users_before)}")
    
    # Test registration
    auth_service = AuthService(storage)
    
    import time
    timestamp = int(time.time())
    test_email = f"verification_{timestamp}@example.com"
    test_user_id = f"verify{timestamp}"
    
    print(f"\\n🧪 Testing Registration:")
    print(f"   Email: {test_email}")
    print(f"   User ID: {test_user_id}")
    
    success = auth_service.create_account(
        email=test_email,
        user_id=test_user_id,
        password="verifypass123",
        role="user",
        name="Verification Test User"
    )
    
    if success:
        print("✅ Registration successful!")
        
        # Check both storages after
        gs_users_after = get_cached_sheet_data(storage, 'Users')
        excel_users_after = base_storage.read_sheet('Users')
        
        print(f"\\n👥 User Counts After:")
        print(f"   Google Sheets: {len(gs_users_after)} (+{len(gs_users_after) - len(gs_users_before)})")
        print(f"   Excel: {len(excel_users_after)} (+{len(excel_users_after) - len(excel_users_before)})")
        
        # Verify the user is in the right place
        user_in_gs = gs_users_after[gs_users_after['email'] == test_email]
        user_in_excel = excel_users_after[excel_users_after['email'] == test_email]
        
        print(f"\\n📊 User Location:")
        print(f"   Google Sheets: {'✅ FOUND' if not user_in_gs.empty else '❌ NOT FOUND'}")
        print(f"   Excel: {'⚠️ FOUND (unexpected)' if not user_in_excel.empty else '✅ NOT FOUND (expected)'}")
        
        if not user_in_gs.empty and user_in_excel.empty:
            print(f"\\n🎉 SUCCESS: New registrations are going to Google Sheets!")
            user_row = user_in_gs.iloc[0]
            print(f"   User ID: {user_row['user_id']}")
            print(f"   Email: {user_row['email']}")
            print(f"   Name: {user_row['name']}")
            print(f"   Role: {user_row['role']}")
            print(f"   Created: {user_row['created_at']}")
            return True
        else:
            print(f"\\n⚠️ Issue: User registration didn't go to the expected location")
            return False
    else:
        print("❌ Registration failed")
        return False

if __name__ == "__main__":
    success = verify_registration_flow()
    
    if success:
        print(f"\\n✅ VERIFICATION PASSED: Registrations are now saving to Google Sheets!")
        print(f"\\n📝 Summary:")
        print(f"   • App is using GoogleSheetsStorage")
        print(f"   • New user registrations go to Google Sheets")
        print(f"   • Users can see their data in the shared Google Sheet")
        print(f"\\n🔗 Google Sheet URL: https://docs.google.com/spreadsheets/d/1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4/edit")
    else:
        print(f"\\n❌ VERIFICATION FAILED: Issue with registration flow")