#!/usr/bin/env python3
"""
Complete Google Sheets Discovery
Discovers ALL sheets in the Google Sheets document and analyzes their structure
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime

# Setup
sys.path.append('.')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

# Try multiple methods to access Google Sheets
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False

try:
    from googleapiclient.discovery import build
    from google.oauth2.service_account import Credentials as ServiceCredentials
    GOOGLEAPIS_AVAILABLE = True
except ImportError:
    GOOGLEAPIS_AVAILABLE = False

def method_1_gspread():
    """Method 1: Use gspread library"""
    print("🔄 TRYING METHOD 1: gspread library")
    
    if not GSPREAD_AVAILABLE:
        print("❌ gspread not available")
        return None
    
    try:
        credentials = Credentials.from_service_account_file(
            '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'
        )
        gc = gspread.authorize(credentials)
        
        sheet_id = '1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4'
        spreadsheet = gc.open_by_key(sheet_id)
        
        print(f"✅ Connected to spreadsheet: {spreadsheet.title}")
        
        worksheets = spreadsheet.worksheets()
        print(f"📋 Found {len(worksheets)} worksheets:")
        
        all_sheets = {}
        
        for worksheet in worksheets:
            sheet_name = worksheet.title
            print(f"\n   📊 {sheet_name}")
            
            try:
                # Get all data
                all_values = worksheet.get_all_values()
                if not all_values:
                    print(f"      ⚠️  Empty sheet")
                    continue
                
                # Convert to DataFrame
                if len(all_values) > 1:
                    headers = all_values[0]
                    data = all_values[1:]
                    df = pd.DataFrame(data, columns=headers)
                else:
                    df = pd.DataFrame()
                
                all_sheets[sheet_name] = {
                    'method': 'gspread',
                    'rows': len(df),
                    'columns': list(df.columns) if not df.empty else [],
                    'sample_data': df.head(2).to_dict('records') if not df.empty else []
                }
                
                print(f"      ✅ {len(df)} rows × {len(df.columns)} columns")
                print(f"      📋 Columns: {list(df.columns)}")
                
            except Exception as e:
                print(f"      ❌ Error reading sheet: {str(e)[:100]}")
                all_sheets[sheet_name] = {'method': 'gspread', 'error': str(e)}
        
        return all_sheets
        
    except Exception as e:
        print(f"❌ gspread method failed: {e}")
        return None

def method_2_googleapis():
    """Method 2: Use Google APIs directly"""
    print("\n🔄 TRYING METHOD 2: Google APIs")
    
    if not GOOGLEAPIS_AVAILABLE:
        print("❌ Google APIs not available")
        return None
    
    try:
        credentials = ServiceCredentials.from_service_account_file(
            '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        
        service = build('sheets', 'v4', credentials=credentials)
        sheet_id = '1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4'
        
        # Get spreadsheet metadata
        sheet_metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        
        print(f"✅ Connected to: {sheet_metadata['properties']['title']}")
        
        sheets = sheet_metadata['sheets']
        print(f"📋 Found {len(sheets)} sheets:")
        
        all_sheets = {}
        
        for sheet in sheets:
            sheet_name = sheet['properties']['title']
            print(f"\n   📊 {sheet_name}")
            
            try:
                # Get data from this sheet
                range_name = f"'{sheet_name}'!A:Z"  # Get first 26 columns
                result = service.spreadsheets().values().get(
                    spreadsheetId=sheet_id,
                    range=range_name
                ).execute()
                
                values = result.get('values', [])
                
                if not values:
                    print(f"      ⚠️  Empty sheet")
                    all_sheets[sheet_name] = {
                        'method': 'googleapis', 
                        'rows': 0, 
                        'columns': [], 
                        'sample_data': []
                    }
                    continue
                
                # Convert to DataFrame
                if len(values) > 1:
                    headers = values[0]
                    data = values[1:]
                    # Pad rows to match header length
                    padded_data = []
                    for row in data:
                        padded_row = row + [''] * (len(headers) - len(row))
                        padded_data.append(padded_row)
                    
                    df = pd.DataFrame(padded_data, columns=headers)
                else:
                    df = pd.DataFrame()
                
                all_sheets[sheet_name] = {
                    'method': 'googleapis',
                    'rows': len(df),
                    'columns': list(df.columns) if not df.empty else [],
                    'sample_data': df.head(2).to_dict('records') if not df.empty else []
                }
                
                print(f"      ✅ {len(df)} rows × {len(df.columns)} columns")
                print(f"      📋 Columns: {list(df.columns)}")
                
            except Exception as e:
                print(f"      ❌ Error reading sheet: {str(e)[:100]}")
                all_sheets[sheet_name] = {'method': 'googleapis', 'error': str(e)}
        
        return all_sheets
        
    except Exception as e:
        print(f"❌ Google APIs method failed: {e}")
        return None

def method_3_existing_storage():
    """Method 3: Use existing storage system but try more sheet names"""
    print("\n🔄 TRYING METHOD 3: Existing storage with expanded sheet search")
    
    try:
        from imiq.storage import get_storage_instance
        from imiq.settings import SettingsService
        
        base_storage = get_storage_instance()
        settings_service = SettingsService(base_storage)
        storage = get_storage_instance(settings_service)
        
        # Extended list of possible sheet names based on common patterns
        possible_sheets = [
            # Original sheets
            'Users', 'Customers', 'Settings',
            # Product variations
            'Products', 'Product', 'Items', 'Inventory', 'Stock', 'Catalog',
            # Order variations
            'Orders', 'Order', 'Transactions', 'Sales', 'Purchases', 'Bookings',
            # Customer variations
            'Customer', 'Clients', 'Client', 'Members', 'Member',
            # User variations
            'User', 'Accounts', 'Account', 'Profiles', 'Profile',
            # System variations
            'Config', 'Configuration', 'Admin', 'System',
            # Business specific
            'Suppliers', 'Vendor', 'Vendors', 'Categories', 'Category',
            'Payments', 'Payment', 'Billing', 'Invoices', 'Invoice',
            'Shipping', 'Delivery', 'Returns', 'Reviews', 'Feedback',
            # Analytics
            'Reports', 'Analytics', 'Metrics', 'KPI', 'Dashboard',
            # Generic sheet names
            'Sheet1', 'Sheet2', 'Sheet3', 'Data', 'Main', 'Master',
            # Date-based or numbered
            'Jan2026', 'Feb2026', '2026', 'Q1', 'Q2', 'Monthly', 'Daily'
        ]
        
        all_sheets = {}
        
        print(f"🔍 Searching through {len(possible_sheets)} possible sheet names...")
        
        for sheet_name in possible_sheets:
            try:
                df = storage.read_sheet(sheet_name)
                
                if not df.empty:
                    all_sheets[sheet_name] = {
                        'method': 'storage',
                        'rows': len(df),
                        'columns': list(df.columns),
                        'sample_data': df.head(2).to_dict('records')
                    }
                    
                    print(f"   ✅ {sheet_name}: {len(df)} rows × {len(df.columns)} columns")
                    print(f"      📋 Columns: {list(df.columns)}")
                else:
                    print(f"   ⚠️  {sheet_name}: Found but empty")
                    
            except Exception as e:
                # Only print errors for sheets that seem likely to exist
                if any(keyword in sheet_name.lower() for keyword in ['user', 'customer', 'order', 'product', 'setting']):
                    print(f"   ❌ {sheet_name}: {str(e)[:50]}...")
        
        return all_sheets if all_sheets else None
        
    except Exception as e:
        print(f"❌ Storage method failed: {e}")
        return None

def main():
    """Main discovery process"""
    print("🔍 COMPLETE GOOGLE SHEETS DISCOVERY")
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📋 Sheet ID: 1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4")
    print("=" * 70)
    
    # Try all methods
    all_sheets = None
    
    # Method 1: gspread
    if not all_sheets:
        all_sheets = method_1_gspread()
    
    # Method 2: Google APIs
    if not all_sheets:
        all_sheets = method_2_googleapis()
    
    # Method 3: Existing storage
    if not all_sheets:
        all_sheets = method_3_existing_storage()
    
    if not all_sheets:
        print("\n❌ FAILED: Could not discover any sheets using any method")
        return None
    
    # Save results
    output_file = 'complete_sheet_discovery.json'
    with open(output_file, 'w') as f:
        json.dump(all_sheets, f, indent=2, default=str)
    
    # Display results
    print(f"\n" + "=" * 70)
    print("📋 DISCOVERED SHEETS SUMMARY")
    print("=" * 70)
    
    total_sheets = len(all_sheets)
    total_rows = sum(sheet.get('rows', 0) for sheet in all_sheets.values())
    
    print(f"📊 Total sheets found: {total_sheets}")
    print(f"📏 Total data rows: {total_rows}")
    
    # Categorize sheets
    categories = {
        'Users/Authentication': [],
        'Products/Inventory': [],
        'Orders/Transactions': [],
        'Customers/CRM': [],
        'Settings/Config': [],
        'Reports/Analytics': [],
        'Other': []
    }
    
    for sheet_name, info in all_sheets.items():
        if 'error' in info:
            continue
            
        columns = [col.lower() for col in info.get('columns', [])]
        
        # Categorize based on column names
        if any(col in columns for col in ['user_id', 'username', 'email', 'password']):
            categories['Users/Authentication'].append(sheet_name)
        elif any(col in columns for col in ['product_id', 'item_id', 'sku', 'price']):
            categories['Products/Inventory'].append(sheet_name)
        elif any(col in columns for col in ['order_id', 'transaction_id', 'purchase_id']):
            categories['Orders/Transactions'].append(sheet_name)
        elif any(col in columns for col in ['customer_id', 'client_id', 'phone', 'address']):
            categories['Customers/CRM'].append(sheet_name)
        elif any(col in columns for col in ['setting_key', 'config_key', 'parameter']):
            categories['Settings/Config'].append(sheet_name)
        elif any(col in columns for col in ['report_date', 'metric', 'analytics']):
            categories['Reports/Analytics'].append(sheet_name)
        else:
            categories['Other'].append(sheet_name)
    
    print(f"\n🎯 SHEET CATEGORIES:")
    for category, sheets in categories.items():
        if sheets:
            print(f"   {category}: {sheets}")
    
    print(f"\n📋 DETAILED SHEET INFORMATION:")
    for sheet_name, info in all_sheets.items():
        if 'error' in info:
            print(f"   ❌ {sheet_name}: {info['error'][:50]}...")
        else:
            rows = info.get('rows', 0)
            cols = len(info.get('columns', []))
            print(f"   ✅ {sheet_name}: {rows} rows × {cols} columns")
            
            # Show sample data structure
            if info.get('sample_data'):
                sample = info['sample_data'][0]
                sample_keys = list(sample.keys())[:5]  # First 5 columns
                print(f"      Sample fields: {sample_keys}")
    
    print(f"\n💾 Complete discovery saved to: {output_file}")
    print(f"🎯 Ready to create targeted test scripts for {total_sheets} sheets!")
    
    return all_sheets

if __name__ == "__main__":
    result = main()
    
    if result:
        print(f"\n🎉 Successfully discovered {len(result)} sheets!")
        print("   Use this data to create proper test scripts for each sheet")
    else:
        print("\n❌ Discovery failed - check Google Sheets access")