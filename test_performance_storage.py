#!/usr/bin/env python3
"""Test script to verify Performance tab is using correct storage"""

import os
# Set Google credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService

def test_performance_storage():
    """Test what storage the Performance tab will use"""
    print("🔍 Testing Performance Tab Storage...")
    
    # Initialize settings service first (like app.py does)
    base_storage = get_storage_instance()  # This will be Excel by default
    settings_service = SettingsService(base_storage)
    
    # Get the storage instance that should be used (with settings)
    proper_storage = get_storage_instance(settings_service)
    print(f"📊 Storage class being used: {proper_storage.__class__.__name__}")
    
    # Read Users data from the storage
    try:
        users_df = proper_storage.read_sheet("Users")
        print(f"👥 Users found in storage: {len(users_df)}")
        if not users_df.empty:
            print(f"   User IDs: {users_df['user_id'].tolist() if 'user_id' in users_df.columns else 'No user_id column'}")
    except Exception as e:
        print(f"❌ Error reading Users: {e}")
    
    return proper_storage

if __name__ == "__main__":
    test_performance_storage()