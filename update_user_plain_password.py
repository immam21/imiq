"""
Update user to use plain password authentication
"""
import streamlit as st
from imiq.storage import get_storage_instance
from imiq.auth import AuthService

def update_user_password():
    """Update Sowmiya01 to use plain password"""
    
    # Initialize storage and auth
    storage = get_storage_instance()
    auth_service = AuthService(storage)
    
    user_id = "Sowmiya01"
    new_password = input(f"Enter new plain password for user '{user_id}': ")
    
    if not new_password:
        print("❌ Password cannot be empty")
        return
    
    # Update user
    success = auth_service.update_user_to_plain_password(user_id, new_password)
    
    if success:
        print(f"✅ Successfully updated user '{user_id}' to use plain password")
        print(f"   New password: {new_password}")
        
        # Test authentication
        user_data = auth_service.authenticate(user_id, new_password)
        if user_data:
            print("✅ Authentication test successful!")
            print(f"   User: {user_data}")
        else:
            print("❌ Authentication test failed")
    else:
        print(f"❌ Failed to update user '{user_id}'")

if __name__ == "__main__":
    update_user_password()