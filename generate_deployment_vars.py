#!/usr/bin/env python3

import json
import os

def generate_deployment_env_vars():
    """Generate environment variable content for deployment"""
    
    print("🚀 Google Sheets Deployment Helper")
    print("=" * 50)
    
    service_account_path = "/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json"
    
    if not os.path.exists(service_account_path):
        print("❌ service_account.json not found in current directory")
        print("   Make sure your service account file is present")
        return
    
    try:
        # Read and validate JSON
        with open(service_account_path, 'r') as f:
            service_account_data = json.load(f)
        
        project_id = service_account_data.get('project_id', 'unknown')
        client_email = service_account_data.get('client_email', 'unknown')
        
        print(f"📋 Service Account Info:")
        print(f"   Project ID: {project_id}")
        print(f"   Client Email: {client_email}")
        
        # Generate the JSON string (compact format)
        json_string = json.dumps(service_account_data, separators=(',', ':'))
        
        print(f"\\n📝 Environment Variable Content:")
        print(f"\\nFor copy-paste deployment:")
        print(f"```")
        print(f"GOOGLE_SERVICE_ACCOUNT_JSON='{json_string}'")
        print(f"```")
        
        print(f"\\n🔧 Platform-specific instructions:")
        
        print(f"\\n**Heroku:**")
        print(f"```bash")
        print(f"heroku config:set GOOGLE_SERVICE_ACCOUNT_JSON='{json_string}'")
        print(f"```")
        
        print(f"\\n**Docker Compose:**")
        print(f"```yaml")
        print(f"environment:")
        print(f"  - GOOGLE_SERVICE_ACCOUNT_JSON={json_string}")
        print(f"```")
        
        print(f"\\n**Local Testing:**")
        print(f"```bash")
        print(f"export GOOGLE_SERVICE_ACCOUNT_JSON='{json_string}'")
        print(f"python3 -m streamlit run app.py")
        print(f"```")
        
        print(f"\\n⚠️  Security Notes:")
        print(f"   • Never commit credentials to version control")
        print(f"   • Use your platform's secure environment variable system")
        print(f"   • Rotate credentials regularly")
        print(f"   • Limit service account permissions")
        
        # Write to a temp file for easy access
        with open('deployment_env.txt', 'w') as f:
            f.write(f"GOOGLE_SERVICE_ACCOUNT_JSON='{json_string}'\\n")
        
        print(f"\\n📁 Environment variable also saved to: deployment_env.txt")
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in service account file: {e}")
    except Exception as e:
        print(f"❌ Error reading service account file: {e}")

if __name__ == "__main__":
    generate_deployment_env_vars()