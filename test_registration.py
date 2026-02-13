#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from imiq.storage import ExcelStorage, GoogleSheetsStorage, get_storage_instance
from imiq.settings import SettingsService
from imiq.auth import AuthService

def test_registration():
    """Test user registration with both storage types"""
    
    print("🧪 Testing User Registration")
    print("=" * 50)
    
    # First test with Excel storage (baseline)
    print("\n📊 Testing with Excel Storage:")
    excel_storage = ExcelStorage('CZ_MasterSheet.xlsx')
    settings_service = SettingsService(excel_storage)
    
    # Ensure Excel is being used
    settings_service.update_setting("USE_GOOGLE_SHEETS", "false")
    
    excel_auth = AuthService(excel_storage)
    
    test_email = "test@example.com"
    test_user_id = "testuser123"
    test_password = "testpass123"
    
    # Check current users first
    users_before = excel_storage.read_sheet("Users")
    print(f"Users before registration: {len(users_before)}")
    
    # Try registration with Excel
    try:
        success = excel_auth.create_account(
            email=test_email,
            user_id=test_user_id,
            password=test_password,
            role="user",
            name="Test User"
        )
        
        print(f"Excel registration result: {success}")
        
        if success:
            users_after = excel_storage.read_sheet("Users")
            print(f"Users after registration: {len(users_after)}")
            
            # Check if user exists
            new_user = users_after[users_after['email'] == test_email]
            if not new_user.empty:
                print("✅ User successfully saved in Excel")
            else:
                print("❌ User not found in Excel after registration")
        
    except Exception as e:
        print(f"❌ Excel registration error: {e}")
    
    # Now test with Google Sheets
    print(f"\n🔗 Testing with Google Sheets Storage:")
    
    # Check if Google credentials are available
    google_creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    print(f"Google credentials path: {google_creds}")
    
    if google_creds and os.path.exists(google_creds):
        try:
            # Enable Google Sheets
            settings_service.update_setting("USE_GOOGLE_SHEETS", "true")
            
            # Get Google Sheets storage
            gs_storage = get_storage_instance(settings_service)
            print(f"Storage type: {type(gs_storage).__name__}")
            
            if isinstance(gs_storage, GoogleSheetsStorage):
                gs_auth = AuthService(gs_storage)
                
                # Check current users in Google Sheets
                users_before_gs = gs_storage.read_sheet("Users")
                print(f"Users in Google Sheets before registration: {len(users_before_gs)}")
                
                # Try registration with Google Sheets
                test_email_gs = "testgs@example.com"
                test_user_id_gs = "testgs123"
                
                try:
                    success_gs = gs_auth.create_account(
                        email=test_email_gs,
                        user_id=test_user_id_gs,
                        password=test_password,
                        role="user",
                        name="Test GS User"
                    )
                    
                    print(f"Google Sheets registration result: {success_gs}")
                    
                    if success_gs:
                        users_after_gs = gs_storage.read_sheet("Users")
                        print(f"Users in Google Sheets after registration: {len(users_after_gs)}")
                        
                        # Check if user exists
                        new_user_gs = users_after_gs[users_after_gs['email'] == test_email_gs]
                        if not new_user_gs.empty:
                            print("✅ User successfully saved in Google Sheets")
                        else:
                            print("❌ User not found in Google Sheets after registration")
                    
                except Exception as e:
                    print(f"❌ Google Sheets registration error: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("❌ Google Sheets storage not initialized properly")
                
        except Exception as e:
            print(f"❌ Google Sheets setup error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ Google credentials not found or path doesn't exist")
        print("   Please set GOOGLE_APPLICATION_CREDENTIALS environment variable")

if __name__ == "__main__":
    test_registration()