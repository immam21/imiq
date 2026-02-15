#!/usr/bin/env python3
"""
Google Sheets Direct Discovery
Always uses Google Sheets API - no fallback to existing storage
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime

# Setup
sys.path.append('.')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

# Google Sheets API imports
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False
    print("❌ gspread not available. Install with: pip install gspread")
    sys.exit(1)

try:
    from googleapiclient.discovery import build
    from google.oauth2.service_account import Credentials as ServiceCredentials
    GOOGLEAPIS_AVAILABLE = True
except ImportError:
    GOOGLEAPIS_AVAILABLE = False

def discover_sheets_with_gspread():
    """Discover sheets using gspread with proper scopes"""
    print("🔄 DISCOVERING SHEETS WITH GSPREAD")
    
    try:
        # Define proper scopes for Google Sheets access
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Create credentials with proper scopes
        credentials = Credentials.from_service_account_file(
            '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json',
            scopes=scopes
        )
        
        # Authorize gspread client
        gc = gspread.authorize(credentials)
        
        # Open spreadsheet
        sheet_id = '1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4'
        spreadsheet = gc.open_by_key(sheet_id)
        
        print(f"✅ Connected to spreadsheet: {spreadsheet.title}")
        
        # Get all worksheets
        worksheets = spreadsheet.worksheets()
        print(f"📋 Found {len(worksheets)} worksheets:")
        
        all_sheets = {}
        
        for worksheet in worksheets:
            sheet_name = worksheet.title
            print(f"\n   📊 Analyzing sheet: {sheet_name}")
            
            try:
                # Get all data from the sheet
                all_values = worksheet.get_all_values()
                
                if not all_values:
                    print(f"      ⚠️  Sheet is empty")
                    all_sheets[sheet_name] = {
                        'method': 'gspread',
                        'status': 'empty',
                        'rows': 0,
                        'columns': [],
                        'sample_data': []
                    }
                    continue
                
                # Process data
                if len(all_values) > 1:
                    headers = all_values[0]
                    data_rows = all_values[1:]
                    df = pd.DataFrame(data_rows, columns=headers)
                    
                    # Clean empty rows
                    df = df.dropna(how='all')
                    
                    all_sheets[sheet_name] = {
                        'method': 'gspread',
                        'status': 'success',
                        'rows': len(df),
                        'columns': list(df.columns),
                        'sample_data': df.head(3).to_dict('records') if not df.empty else [],
                        'sheet_info': {
                            'total_cells': worksheet.row_count * worksheet.col_count,
                            'row_count': worksheet.row_count,
                            'col_count': worksheet.col_count
                        }
                    }
                    
                    print(f"      ✅ {len(df)} data rows × {len(df.columns)} columns")
                    print(f"      📋 Columns: {list(df.columns)}")
                    
                    # Show sample data
                    if not df.empty:
                        print(f"      📄 Sample data (first row): {df.iloc[0].to_dict()}")
                else:
                    # Only headers, no data
                    headers = all_values[0] if all_values else []
                    all_sheets[sheet_name] = {
                        'method': 'gspread',
                        'status': 'headers_only',
                        'rows': 0,
                        'columns': headers,
                        'sample_data': []
                    }
                    print(f"      ⚠️  Only headers found: {headers}")
                
            except Exception as e:
                print(f"      ❌ Error reading sheet '{sheet_name}': {str(e)}")
                all_sheets[sheet_name] = {
                    'method': 'gspread',
                    'status': 'error',
                    'error': str(e)
                }
        
        return all_sheets
        
    except Exception as e:
        print(f"❌ gspread discovery failed: {e}")
        return None

def discover_sheets_with_googleapis():
    """Discover sheets using Google APIs directly"""
    print("\n🔄 DISCOVERING SHEETS WITH GOOGLE APIS")
    
    if not GOOGLEAPIS_AVAILABLE:
        print("❌ Google APIs not available. Install with: pip install google-api-python-client")
        return None
    
    try:
        # Define scopes
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        # Create credentials
        credentials = ServiceCredentials.from_service_account_file(
            '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json',
            scopes=scopes
        )
        
        # Build the service
        service = build('sheets', 'v4', credentials=credentials)
        
        # Get spreadsheet metadata
        sheet_id = '1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4'
        spreadsheet = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        
        print(f"✅ Connected to spreadsheet: {spreadsheet['properties']['title']}")
        
        sheets = spreadsheet['sheets']
        print(f"📋 Found {len(sheets)} sheets:")
        
        all_sheets = {}
        
        for sheet in sheets:
            sheet_name = sheet['properties']['title']
            print(f"\n   📊 Analyzing sheet: {sheet_name}")
            
            try:
                # Get sheet data
                range_name = f"'{sheet_name}'"
                result = service.spreadsheets().values().get(
                    spreadsheetId=sheet_id,
                    range=range_name
                ).execute()
                
                values = result.get('values', [])
                
                if not values:
                    print(f"      ⚠️  Sheet is empty")
                    all_sheets[sheet_name] = {
                        'method': 'googleapis',
                        'status': 'empty',
                        'rows': 0,
                        'columns': [],
                        'sample_data': []
                    }
                    continue
                
                if len(values) > 1:
                    headers = values[0]
                    data_rows = values[1:]
                    df = pd.DataFrame(data_rows, columns=headers)
                    
                    # Clean empty rows
                    df = df.dropna(how='all')
                    
                    all_sheets[sheet_name] = {
                        'method': 'googleapis',
                        'status': 'success',
                        'rows': len(df),
                        'columns': list(df.columns),
                        'sample_data': df.head(3).to_dict('records') if not df.empty else []
                    }
                    
                    print(f"      ✅ {len(df)} data rows × {len(df.columns)} columns")
                    print(f"      📋 Columns: {list(df.columns)}")
                else:
                    headers = values[0] if values else []
                    all_sheets[sheet_name] = {
                        'method': 'googleapis',
                        'status': 'headers_only',
                        'rows': 0,
                        'columns': headers,
                        'sample_data': []
                    }
                    print(f"      ⚠️  Only headers found: {headers}")
                
            except Exception as e:
                print(f"      ❌ Error reading sheet '{sheet_name}': {str(e)}")
                all_sheets[sheet_name] = {
                    'method': 'googleapis',
                    'status': 'error',
                    'error': str(e)
                }
        
        return all_sheets
        
    except Exception as e:
        print(f"❌ Google APIs discovery failed: {e}")
        return None

def main():
    """Main discovery function"""
    print("=" * 60)
    print("🔍 GOOGLE SHEETS DISCOVERY (NO EXISTING STORAGE)")
    print("=" * 60)
    
    all_discovered_sheets = {}
    
    # Method 1: Try gspread first
    gspread_result = discover_sheets_with_gspread()
    if gspread_result:
        all_discovered_sheets.update(gspread_result)
        print(f"\n✅ gspread method discovered {len(gspread_result)} sheets")
    else:
        print("\n❌ gspread method failed, trying Google APIs...")
        
        # Method 2: Fallback to Google APIs
        googleapis_result = discover_sheets_with_googleapis()
        if googleapis_result:
            all_discovered_sheets.update(googleapis_result)
            print(f"\n✅ Google APIs method discovered {len(googleapis_result)} sheets")
        else:
            print("\n❌ Both methods failed!")
            return
    
    # Save results
    if all_discovered_sheets:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f'discovered_sheets_{timestamp}.json'
        
        with open(output_file, 'w') as f:
            json.dump(all_discovered_sheets, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 DISCOVERY SUMMARY")
        print("=" * 60)
        
        successful_sheets = [name for name, data in all_discovered_sheets.items() 
                           if data.get('status') == 'success']
        empty_sheets = [name for name, data in all_discovered_sheets.items() 
                       if data.get('status') == 'empty']
        error_sheets = [name for name, data in all_discovered_sheets.items() 
                       if data.get('status') == 'error']
        
        print(f"✅ Successful sheets: {len(successful_sheets)}")
        for sheet in successful_sheets:
            data = all_discovered_sheets[sheet]
            print(f"   📊 {sheet}: {data['rows']} rows, {len(data['columns'])} columns")
        
        if empty_sheets:
            print(f"⚠️  Empty sheets: {len(empty_sheets)}")
            for sheet in empty_sheets:
                print(f"   📄 {sheet}")
        
        if error_sheets:
            print(f"❌ Error sheets: {len(error_sheets)}")
            for sheet in error_sheets:
                print(f"   🚫 {sheet}")
        
        print(f"\n🎯 Total sheets discovered: {len(all_discovered_sheets)}")
    else:
        print("\n❌ No sheets discovered!")

if __name__ == "__main__":
    main()