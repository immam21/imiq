#!/usr/bin/env python3

import os
import json
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_environment_variable_deployment():
    """Test deployment using GOOGLE_SERVICE_ACCOUNT_JSON environment variable"""
    
    print("🧪 Testing Environment Variable Deployment Method")
    print("=" * 60)
    
    # Clear any existing file-based credentials
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        del os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        print("🧹 Cleared GOOGLE_APPLICATION_CREDENTIALS")
    
    # Read the service account JSON file and set as environment variable
    service_account_path = "/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json"
    
    if not os.path.exists(service_account_path):
        print("❌ service_account.json not found. Cannot run test.")
        return False
    
    try:
        # Read JSON content
        with open(service_account_path, 'r') as f:
            service_account_json = f.read()
        
        # Validate JSON
        service_account_data = json.loads(service_account_json)
        print(f"✅ Read service account JSON for project: {service_account_data.get('project_id', 'unknown')}")
        
        # Set environment variable
        os.environ['GOOGLE_SERVICE_ACCOUNT_JSON'] = service_account_json
        print("✅ Set GOOGLE_SERVICE_ACCOUNT_JSON environment variable")
        
        # Test the deployment setup
        print(f"\\n🔧 Testing storage initialization...")
        
        # Import after setting environment variable
        from imiq.storage import get_storage_instance, ExcelStorage
        from imiq.settings import SettingsService
        
        # Initialize like production would
        base_storage = ExcelStorage('CZ_MasterSheet.xlsx')
        settings_service = SettingsService(base_storage)
        
        # Get storage instance (should use environment variable JSON)
        storage = get_storage_instance(settings_service)
        print(f"📊 Storage type: {type(storage).__name__}")
        
        if hasattr(storage, 'sheet_id'):
            print(f"📋 Google Sheet ID: {storage.sheet_id}")
        
        # Test reading data
        from imiq.performance import get_cached_sheet_data
        users_df = get_cached_sheet_data(storage, "Users")
        print(f"👥 Users in storage: {len(users_df)} rows")
        
        # Test creating a user (deployment simulation)
        print(f"\\n🧪 Testing user creation in deployment mode...")
        
        from imiq.auth import AuthService
        auth_service = AuthService(storage)
        
        import time
        timestamp = int(time.time())
        test_email = f"deploy_test_{timestamp}@example.com"
        test_user_id = f"deploytest{timestamp}"
        
        try:
            success = auth_service.create_account(
                email=test_email,
                user_id=test_user_id,
                password="deploypass123",
                role="user",
                name="Deploy Test User"
            )
            
            if success:
                print("✅ User creation successful in deployment mode!")
                
                # Verify user exists
                updated_users = get_cached_sheet_data(storage, "Users")
                new_user = updated_users[updated_users['email'] == test_email]
                
                if not new_user.empty:
                    print(f"✅ User verified in Google Sheets:")
                    print(f"   Email: {new_user.iloc[0]['email']}")
                    print(f"   User ID: {new_user.iloc[0]['user_id']}")
                    print(f"   Role: {new_user.iloc[0]['role']}")
                    return True
                else:
                    print("❌ User not found after creation")
                    return False
            else:
                print("❌ User creation failed")
                return False
                
        except Exception as e:
            print(f"❌ Error during user creation test: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_deployment_examples():
    """Show deployment examples"""
    
    print(f"\\n📚 Deployment Examples")
    print("=" * 60)
    
    print(f"\\n🚀 **Heroku Deployment:**")
    print(f"```")
    print(f"heroku config:set GOOGLE_SERVICE_ACCOUNT_JSON='$(cat service_account.json)'")
    print(f"```")
    
    print(f"\\n🐳 **Docker Deployment:**")
    print(f"```yaml")
    print(f"version: '3'")
    print(f"services:")
    print(f"  app:")
    print(f"    image: your-app:latest")
    print(f"    environment:")
    print(f"      - GOOGLE_SERVICE_ACCOUNT_JSON=${{GOOGLE_SERVICE_ACCOUNT_JSON}}")
    print(f"```")
    
    print(f"\\n☁️ **General Cloud Deployment:**")
    print(f"```bash")
    print(f"export GOOGLE_SERVICE_ACCOUNT_JSON='$(cat service_account.json)'")
    print(f"python3 -m streamlit run app.py")
    print(f"```")

if __name__ == "__main__":
    success = test_environment_variable_deployment()
    
    if success:
        print(f"\\n🎉 Environment Variable Deployment Test: PASSED!")
        show_deployment_examples()
    else:
        print(f"\\n💥 Environment Variable Deployment Test: FAILED!")
    
    print(f"\\n📖 See GOOGLE_SHEETS_DEPLOYMENT.md for complete deployment guide")