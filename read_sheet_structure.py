#!/usr/bin/env python3
"""
Google Sheets Structure Reader
Reads and analyzes the structure of all sheets in the Google document
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime

# Setup
sys.path.append('.')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService

def get_all_sheet_names(storage):
    """Get all sheet names from the Google Sheets document"""
    sheet_names = []
    
    if hasattr(storage, 'service') and hasattr(storage, 'sheet_id'):
        try:
            sheet_metadata = storage.service.spreadsheets().get(
                spreadsheetId=storage.sheet_id
            ).execute()
            
            sheet_names = [sheet['properties']['title'] for sheet in sheet_metadata['sheets']]
            print(f"📋 Found {len(sheet_names)} sheets in document:")
            for name in sheet_names:
                print(f"   - {name}")
            
        except Exception as e:
            print(f"❌ Could not get sheet names: {e}")
    
    return sheet_names

def analyze_sheet_structure(storage, sheet_name):
    """Analyze the detailed structure of a specific sheet"""
    print(f"\n📊 ANALYZING SHEET: {sheet_name}")
    print("=" * 50)
    
    try:
        df = storage.read_sheet(sheet_name)
        
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
        
        if not df.empty:
            # Analyze data types
            for col in df.columns:
                structure['data_types'][col] = str(df[col].dtype)
                structure['null_counts'][col] = df[col].isnull().sum()
                structure['unique_counts'][col] = df[col].nunique()
            
            # Get sample data (first 3 rows)
            sample_count = min(3, len(df))
            structure['sample_data'] = df.head(sample_count).to_dict('records')
            
            # Print detailed analysis
            print(f"✅ Sheet Status: Active with data")
            print(f"📏 Dimensions: {len(df)} rows × {len(df.columns)} columns")
            print(f"📋 Columns: {list(df.columns)}")
            
            print(f"\n📊 Column Analysis:")
            for col in df.columns:
                dtype = structure['data_types'][col]
                nulls = structure['null_counts'][col]
                unique = structure['unique_counts'][col]
                print(f"   {col:<20} | Type: {dtype:<10} | Nulls: {nulls:<3} | Unique: {unique}")
            
            print(f"\n📝 Sample Data ({sample_count} rows):")
            for i, row in enumerate(structure['sample_data']):
                print(f"   Row {i+1}:")
                for key, value in list(row.items())[:5]:  # Show first 5 columns
                    print(f"     {key}: {value}")
                if len(row) > 5:
                    print(f"     ... and {len(row)-5} more columns")
        else:
            print(f"⚠️  Sheet Status: Empty (no data)")
            
        return structure
        
    except Exception as e:
        print(f"❌ Error analyzing {sheet_name}: {e}")
        return None

def identify_sheet_purpose(structure):
    """Identify the likely purpose of a sheet based on its structure"""
    if not structure or structure['rows'] == 0:
        return "Empty"
    
    columns = [col.lower() for col in structure['columns']]
    
    # User/Authentication sheets
    if any(col in columns for col in ['user_id', 'username', 'email', 'password']):
        return "Users/Authentication"
    
    # Customer sheets
    elif any(col in columns for col in ['customer_id', 'client_id', 'phone', 'address']):
        return "Customers/Clients"
    
    # Product/Inventory sheets
    elif any(col in columns for col in ['product_id', 'item_id', 'sku', 'price', 'quantity']):
        return "Products/Inventory"
    
    # Order/Transaction sheets
    elif any(col in columns for col in ['order_id', 'transaction_id', 'purchase_id']):
        return "Orders/Transactions"
    
    # Settings/Configuration
    elif any(col in columns for col in ['setting_key', 'config_key', 'parameter']):
        return "Settings/Configuration"
    
    # Reports/Analytics
    elif any(col in columns for col in ['metric', 'report_date', 'analytics']):
        return "Reports/Analytics"
    
    else:
        return "General Data"

def main():
    """Main structure analysis"""
    print("🔍 GOOGLE SHEETS STRUCTURE ANALYSIS")
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Initialize storage
        base_storage = get_storage_instance()
        settings_service = SettingsService(base_storage)
        storage = get_storage_instance(settings_service)
        
        print(f"✅ Storage initialized: {type(storage).__name__}")
        
        if hasattr(storage, 'sheet_id'):
            print(f"📋 Google Sheet ID: {storage.sheet_id}")
        
        # Get all sheet names
        sheet_names = get_all_sheet_names(storage)
        
        if not sheet_names:
            print("❌ No sheets found or could not access sheets")
            return
        
        # Analyze each sheet
        all_structures = {}
        
        for sheet_name in sheet_names:
            structure = analyze_sheet_structure(storage, sheet_name)
            if structure:
                purpose = identify_sheet_purpose(structure)
                structure['purpose'] = purpose
                all_structures[sheet_name] = structure
                print(f"🎯 Purpose: {purpose}")
        
        # Save structure analysis to file
        output_file = 'sheet_structures.json'
        with open(output_file, 'w') as f:
            json.dump(all_structures, f, indent=2, default=str)
        
        print(f"\n💾 Structure analysis saved to: {output_file}")
        
        # Summary report
        print(f"\n📈 SUMMARY REPORT")
        print("=" * 60)
        
        purposes = {}
        total_rows = 0
        total_columns = 0
        
        for name, structure in all_structures.items():
            purpose = structure.get('purpose', 'Unknown')
            if purpose not in purposes:
                purposes[purpose] = []
            purposes[purpose].append(name)
            total_rows += structure.get('rows', 0)
            total_columns += structure.get('column_count', 0)
        
        print(f"📊 Total Sheets: {len(all_structures)}")
        print(f"📏 Total Data: {total_rows} rows across all sheets")
        print(f"📋 Total Columns: {total_columns} columns across all sheets")
        
        print(f"\n🎯 Sheet Categories:")
        for purpose, sheets in purposes.items():
            print(f"   {purpose}: {len(sheets)} sheet(s) - {', '.join(sheets)}")
        
        # Recommendations for testing
        print(f"\n💡 TESTING RECOMMENDATIONS:")
        
        if 'Users/Authentication' in purposes:
            print("   ✅ Can test: Registration, Login, Authentication flows")
        
        if 'Products/Inventory' in purposes:
            print("   ✅ Can test: Product catalog, Inventory management")
        
        if 'Orders/Transactions' in purposes:
            print("   ✅ Can test: Order creation, Order management, Transaction flows")
        
        if 'Customers/Clients' in purposes:
            print("   ✅ Can test: Customer management, CRM flows")
        
        if 'Settings/Configuration' in purposes:
            print("   ✅ Can test: System configuration, Settings management")
        
        missing_categories = []
        if 'Users/Authentication' not in purposes:
            missing_categories.append("Users/Authentication")
        if 'Products/Inventory' not in purposes:
            missing_categories.append("Products/Inventory")
        if 'Orders/Transactions' not in purposes:
            missing_categories.append("Orders/Transactions")
        
        if missing_categories:
            print(f"\n⚠️  MISSING FOR COMPLETE E-COMMERCE TESTING:")
            for category in missing_categories:
                print(f"   - {category} sheet")
        
        return all_structures
        
    except Exception as e:
        print(f"💥 Error: {e}")
        return None

if __name__ == "__main__":
    structures = main()
    
    if structures:
        print(f"\n🎉 Structure analysis complete!")
        print(f"   Check 'sheet_structures.json' for detailed analysis")
        print(f"   Ready to create targeted test scripts!")
    else:
        print(f"\n❌ Analysis failed")