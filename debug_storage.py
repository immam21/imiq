#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_app_storage_status():
    """Check what storage the app is actually using"""
    
    print("🔍 Checking App Storage Status")
    print("=" * 50)
    
    # Set credentials like the app does
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'
    
    # Import and initialize exactly like the app does
    from imiq.storage import get_storage_instance, ExcelStorage
    from imiq.settings import SettingsService
    
    # Initialize base services first to get settings (like app.py line 49)
    base_storage = ExcelStorage('CZ_MasterSheet.xlsx')
    settings_service = SettingsService(base_storage)
    
    # Check current settings
    use_gs = settings_service.get_setting('use_google_sheets', False)
    sheet_id = settings_service.get_setting('google_sheet_id', '')
    
    print(f"📋 Settings Configuration:")
    print(f"   use_google_sheets: {use_gs}")
    print(f"   google_sheet_id: {sheet_id}")
    print(f"   GOOGLE_APPLICATION_CREDENTIALS: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'NOT SET')}")
    
    # Get storage instance like the app does (app.py line 55)
    storage = get_storage_instance(settings_service)
    print(f"\\n🏪 Active Storage:")
    print(f"   Type: {type(storage).__name__}")
    
    if hasattr(storage, 'sheet_id'):
        print(f"   Google Sheet ID: {storage.sheet_id}")
    elif hasattr(storage, 'file_path'):
        print(f"   Excel File: {storage.file_path}")
    
    # Count users in both storages
    excel_users = base_storage.read_sheet('Users')
    print(f"\\n👥 User Counts:")
    print(f"   Excel Storage: {len(excel_users)} users")
    
    if isinstance(storage, type(base_storage)):
        print("   ⚠️ App is using Excel storage (same as base)")
    else:
        gs_users = storage.read_sheet('Users')
        print(f"   Google Sheets: {len(gs_users)} users")
        print("   ✅ App is using Google Sheets storage")
    
    # Show recent registrations in Excel
    if not excel_users.empty:
        print(f"\\n📝 Recent Excel registrations:")
        recent = excel_users.tail(3)
        for _, user in recent.iterrows():
            print(f"   - {user['user_id']}: {user['email']} ({user.get('created_at', 'no timestamp')})")
    
    # Test a quick registration to see where it goes
    print(f"\\n🧪 Testing where new registrations go...")
    from imiq.auth import AuthService
    
    # Use the same storage that the app would use
    auth_service = AuthService(storage)
    
    import time
    test_timestamp = int(time.time())
    test_email = f"storage_test_{test_timestamp}@example.com"
    test_user_id = f"storagetest{test_timestamp}"
    
    try:
        success = auth_service.create_account(
            email=test_email,
            user_id=test_user_id,
            password="testpass123",
            role="user",
            name="Storage Test User"
        )
        
        if success:
            print(f"✅ Registration successful!")
            
            # Check where the user ended up
            updated_excel = base_storage.read_sheet('Users')
            test_user_in_excel = updated_excel[updated_excel['email'] == test_email]
            
            print(f"\\n📊 Registration Results:")
            print(f"   Excel: {'FOUND' if not test_user_in_excel.empty else 'NOT FOUND'}")
            
            if hasattr(storage, 'sheet_id') and not isinstance(storage, type(base_storage)):
                updated_gs = storage.read_sheet('Users')
                test_user_in_gs = updated_gs[updated_gs['email'] == test_email]
                print(f"   Google Sheets: {'FOUND' if not test_user_in_gs.empty else 'NOT FOUND'}")
            
        else:
            print("❌ Registration failed")
            
    except Exception as e:
        print(f"❌ Registration error: {e}")

if __name__ == "__main__":
    check_app_storage_status()