#!/usr/bin/env python3

"""
Script to check available user IDs in Google Sheets
"""

import sys
import os

# Add the imiq directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from imiq.storage import get_storage_instance

def check_available_userids():
    """Check what user IDs are currently available in Google Sheets"""
    print("🔍 Checking available User IDs in Google Sheets...")
    print("=" * 50)
    
    try:
        # Get storage instance
        storage = get_storage_instance()
        
        # Read Users sheet
        print("📊 Reading Users sheet...")
        users_df = storage.read_sheet("Users")
        
        if users_df.empty:
            print("❌ No users found in the Users sheet")
            return
        
        print(f"✅ Found {len(users_df)} users in the sheet")
        print("\n📋 Available User IDs:")
        print("-" * 30)
        
        # Check different possible user ID columns
        possible_id_columns = ['user_id', 'userid', 'email', 'name']
        
        for col in possible_id_columns:
            if col in users_df.columns:
                print(f"\n{col.upper()} Column:")
                unique_values = users_df[col].dropna().unique()
                for i, value in enumerate(unique_values, 1):
                    print(f"  {i}. {value}")
        
        # Show full user data structure
        print(f"\n📊 Full User Data Structure:")
        print(f"Columns: {list(users_df.columns)}")
        
        print(f"\n📝 Sample User Records:")
        for i, (idx, row) in enumerate(users_df.head().iterrows()):
            print(f"\nUser {i+1}:")
            for col in users_df.columns:
                if pd.notna(row[col]):
                    print(f"  {col}: {row[col]}")
        
        # Check what's being used for created_by in orders
        print(f"\n🛍️ Checking Orders sheet for comparison...")
        try:
            orders_df = storage.read_sheet("NewOrders")
            if not orders_df.empty and 'created_by' in orders_df.columns:
                unique_creators = orders_df['created_by'].dropna().unique()
                print(f"Unique 'created_by' values in orders:")
                for creator in unique_creators[:10]:  # Show first 10
                    print(f"  - {creator}")
                if len(unique_creators) > 10:
                    print(f"  ... and {len(unique_creators) - 10} more")
            else:
                print("No orders found or no 'created_by' column")
        except Exception as e:
            print(f"Could not read orders sheet: {e}")
        
        # Check performance sheet
        print(f"\n📈 Checking Performance sheet...")
        try:
            performance_df = storage.read_sheet("Performance")
            if not performance_df.empty:
                print(f"Performance sheet columns: {list(performance_df.columns)}")
                
                # Check user identification columns in performance
                for col in ['user_id', 'userid', 'name', 'created_by']:
                    if col in performance_df.columns:
                        unique_values = performance_df[col].dropna().unique()
                        print(f"Unique {col} in Performance: {list(unique_values[:5])}")
                        if len(unique_values) > 5:
                            print(f"  ... and {len(unique_values) - 5} more")
            else:
                print("No performance data found")
        except Exception as e:
            print(f"Could not read performance sheet: {e}")
            
    except Exception as e:
        print(f"❌ Error reading Google Sheets: {e}")
        return
    
    print(f"\n" + "=" * 50)
    print("✅ User ID check completed!")

if __name__ == "__main__":
    import pandas as pd
    check_available_userids()