#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from imiq.auth import AuthService
from imiq.storage import ExcelStorage

def test_auth_direct():
    """Test authentication directly with Excel storage"""
    
    print("🧪 Testing Authentication with Excel Storage")
    print("=" * 50)
    
    try:
        # Use Excel directly
        excel_file = "/Users/i0s04a6/Documents/GitHub/CrazyShopperz/CZ_MasterSheet.xlsx"
        print(f"📊 Using Excel file: {excel_file}")
        
        if not os.path.exists(excel_file):
            print("❌ Excel file not found!")
            return False
        
        # Initialize storage and auth
        print("🔧 Initializing storage...")
        storage = ExcelStorage(excel_file)
        
        print("🔧 Initializing auth service...")
        auth_service = AuthService(storage)
        
        # Test authentication with user_id
        print(f"\n🔍 Testing user_id authentication:")
        print(f"   Login: imam21")
        print(f"   Password: Iqrit@2024")
        
        result = auth_service.authenticate("imam21", "Iqrit@2024")
        
        if result:
            print("\n✅ User ID authentication successful!")
            print(f"   User ID: {result['user_id']}")
            print(f"   Email: {result['email']}")
            print(f"   Role: {result['role']}")
            print(f"   Name: {result['name']}")
            print(f"   Active: {result['is_active']}")
            
            # Also test email login
            print(f"\n🔍 Testing email authentication:")
            print(f"   Login: {result['email']}")
            
            email_result = auth_service.authenticate(result['email'], "Iqrit@2024")
            if email_result:
                print("✅ Email authentication also works!")
            else:
                print("❌ Email authentication failed")
            
            return True
        else:
            print("\n❌ Authentication failed")
            print("Let me check what users exist in the sheet...")
            
            # Check users in sheet
            users_df = storage.read_sheet("Users")
            print(f"Users in sheet: {len(users_df)}")
            if not users_df.empty:
                print("Available users:")
                for idx, row in users_df.head(3).iterrows():
                    print(f"  - ID: {row['user_id']}, Email: {row['email']}, Active: {row.get('is_active', 'N/A')}")
            
            return False
            
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_auth_direct()
    if success:
        print("\n🎉 All authentication tests passed!")
    else:
        print("\n💥 Authentication test failed!")