#!/usr/bin/env python3
"""
Direct Google Sheets Access and Structure Reading
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime

# Setup
sys.path.append('.')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

def direct_sheets_access():
    """Direct access to Google Sheets using gspread"""
    if not GSPREAD_AVAILABLE:
        print("❌ gspread not available, trying alternative method")
        return None
    
    try:
        # Use service account credentials
        credentials = Credentials.from_service_account_file(
            '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'
        )
        gc = gspread.authorize(credentials)
        
        # Open the spreadsheet by ID
        sheet_id = '1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4'
        spreadsheet = gc.open_by_key(sheet_id)
        
        print(f"✅ Connected to: {spreadsheet.title}")
        
        # Get all worksheets
        worksheets = spreadsheet.worksheets()
        
        print(f"📋 Found {len(worksheets)} worksheets:")
        
        all_structures = {}
        
        for worksheet in worksheets:
            sheet_name = worksheet.title
            print(f"\n📊 ANALYZING: {sheet_name}")
            
            try:
                # Get all records
                records = worksheet.get_all_records()
                
                if not records:
                    print(f"   ⚠️  Empty sheet")
                    continue
                
                # Convert to DataFrame for analysis
                df = pd.DataFrame(records)
                
                structure = {
                    'name': sheet_name,
                    'rows': len(df),
                    'columns': list(df.columns),
                    'column_count': len(df.columns),
                    'data_types': {},
                    'sample_data': [],
                    'null_counts': {},
                    'unique_counts': {}
                }
                
                # Analyze columns
                print(f"   📏 {len(df)} rows × {len(df.columns)} columns")
                print(f"   📋 Columns: {list(df.columns)}")
                
                # Data type analysis
                for col in df.columns:
                    structure['data_types'][col] = str(df[col].dtype)
                    structure['null_counts'][col] = df[col].isnull().sum()
                    structure['unique_counts'][col] = df[col].nunique()
                
                # Sample data
                sample_count = min(3, len(df))
                structure['sample_data'] = df.head(sample_count).to_dict('records')
                
                print(f"   📊 Sample data ({sample_count} rows):")
                for i, row in enumerate(structure['sample_data']):
                    print(f"      Row {i+1}: {list(row.items())[:3]}")
                
                all_structures[sheet_name] = structure
                
            except Exception as e:
                print(f"   ❌ Error reading {sheet_name}: {e}")
        
        return all_structures
        
    except Exception as e:
        print(f"❌ Direct access failed: {e}")
        return None

def fallback_method():
    """Fallback using the existing storage method"""
    print("\n🔄 Using fallback method...")
    
    from imiq.storage import get_storage_instance
    from imiq.settings import SettingsService
    
    try:
        base_storage = get_storage_instance()
        settings_service = SettingsService(base_storage)
        storage = get_storage_instance(settings_service)
        
        # Try known sheet names from previous analysis
        known_sheets = ['Users', 'Customers', 'Settings']
        
        all_structures = {}
        
        for sheet_name in known_sheets:
            try:
                print(f"\n📊 TESTING: {sheet_name}")
                from imiq.performance import get_cached_sheet_data
                df = get_cached_sheet_data(storage, sheet_name)
                
                if not df.empty:
                    structure = {
                        'name': sheet_name,
                        'rows': len(df),
                        'columns': list(df.columns),
                        'column_count': len(df.columns),
                        'sample_data': df.head(2).to_dict('records')
                    }
                    
                    print(f"   ✅ {len(df)} rows × {len(df.columns)} columns")
                    print(f"   📋 Columns: {list(df.columns)}")
                    
                    all_structures[sheet_name] = structure
                else:
                    print(f"   ⚠️  Empty")
                    
            except Exception as e:
                print(f"   ❌ {sheet_name}: {str(e)[:50]}")
        
        return all_structures
        
    except Exception as e:
        print(f"❌ Fallback method failed: {e}")
        return None

def main():
    """Main structure reading"""
    print("🔍 READING GOOGLE SHEETS STRUCTURE")
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Try direct access first
    structures = direct_sheets_access()
    
    # If direct access fails, try fallback
    if not structures:
        structures = fallback_method()
    
    if not structures:
        print("❌ Could not read sheet structures")
        return
    
    # Save results
    with open('actual_sheet_structures.json', 'w') as f:
        json.dump(structures, f, indent=2, default=str)
    
    print(f"\n📈 STRUCTURE SUMMARY")
    print("=" * 40)
    
    for name, structure in structures.items():
        rows = structure.get('rows', 0)
        cols = structure.get('column_count', 0)
        columns = structure.get('columns', [])
        
        print(f"\n📋 {name}:")
        print(f"   Size: {rows} rows × {cols} columns")
        print(f"   Columns: {columns}")
        
        # Identify purpose
        columns_lower = [col.lower() for col in columns]
        purpose = "Unknown"
        
        if any(col in columns_lower for col in ['user_id', 'email', 'password']):
            purpose = "Users/Authentication"
        elif any(col in columns_lower for col in ['customer_id', 'phone', 'address']):
            purpose = "Customers"
        elif any(col in columns_lower for col in ['product_id', 'price', 'quantity']):
            purpose = "Products/Inventory"
        elif any(col in columns_lower for col in ['order_id', 'transaction_id']):
            purpose = "Orders/Transactions"
        elif any(col in columns_lower for col in ['setting_key', 'setting_value']):
            purpose = "Settings"
        
        print(f"   Purpose: {purpose}")
    
    print(f"\n💾 Detailed structure saved to: actual_sheet_structures.json")
    
    return structures

if __name__ == "__main__":
    result = main()
    
    if result:
        print(f"\n🎉 Successfully read {len(result)} sheet structures!")
        print("   Ready to create targeted test scripts based on actual data!")
    else:
        print("\n❌ Failed to read sheet structures")