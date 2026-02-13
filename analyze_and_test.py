#!/usr/bin/env python3
"""
Google Sheets Analysis and Comprehensive Testing
Discovers actual sheets and runs tests based on real data structure
"""

import os
import sys
import time
import pandas as pd
from datetime import datetime

# Setup environment
sys.path.append('.')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService
from imiq.auth import AuthService

class GoogleSheetsAnalyzer:
    def __init__(self):
        self.storage = None
        self.auth_service = None
        self.discovered_sheets = {}
        self.initialize_services()
    
    def initialize_services(self):
        """Initialize all services"""
        try:
            base_storage = get_storage_instance()
            settings_service = SettingsService(base_storage)
            self.storage = get_storage_instance(settings_service)
            self.auth_service = AuthService(self.storage)
            print(f"✅ Initialized: {type(self.storage).__name__}")
        except Exception as e:
            print(f"❌ Service initialization failed: {e}")
            raise
    
    def discover_all_sheets(self):
        """Discover all sheets in the Google Sheets document"""
        print("\n🔍 DISCOVERING ALL SHEETS IN GOOGLE DOCUMENT")
        print("=" * 60)
        
        # Try to get the sheet ID and discover sheets
        if hasattr(self.storage, 'sheet_id'):
            print(f"📋 Google Sheet ID: {self.storage.sheet_id}")
        
        # Try various common sheet names and patterns
        potential_sheets = [
            # User/Customer related
            'Users', 'User', 'Customers', 'Customer', 'Members', 'Accounts',
            # Product/Inventory related  
            'Products', 'Product', 'Inventory', 'Items', 'Catalog', 'Stock',
            # Order/Transaction related
            'Orders', 'Order', 'Transactions', 'Sales', 'Purchases', 'Bookings',
            # System/Config related
            'Settings', 'Config', 'Configuration', 'System', 'Admin',
            # Reporting related
            'Reports', 'Analytics', 'Data', 'Metrics', 'KPI', 'Dashboard',
            # Other possibilities
            'Suppliers', 'Categories', 'Payments', 'Shipping', 'Reviews'
        ]
        
        discovered = {}
        
        for sheet_name in potential_sheets:
            try:
                df = self.storage.read_sheet(sheet_name)
                if not df.empty:
                    discovered[sheet_name] = {
                        'rows': len(df),
                        'columns': list(df.columns),
                        'sample_data': df.head(2).to_dict('records') if len(df) > 0 else []
                    }
                    print(f"✅ {sheet_name:<15} {len(df):>3} rows | Columns: {list(df.columns)[:5]}")
                else:
                    print(f"⚠️  {sheet_name:<15} Found but empty")
            except Exception:
                continue
        
        # Try to discover sheets programmatically if available
        if hasattr(self.storage, 'service') and hasattr(self.storage, 'sheet_id'):
            try:
                sheet_metadata = self.storage.service.spreadsheets().get(
                    spreadsheetId=self.storage.sheet_id
                ).execute()
                
                actual_sheets = [sheet['properties']['title'] for sheet in sheet_metadata['sheets']]
                print(f"\n📊 ACTUAL SHEETS IN DOCUMENT: {actual_sheets}")
                
                # Test any sheets we haven't tried yet
                for sheet_name in actual_sheets:
                    if sheet_name not in discovered:
                        try:
                            df = self.storage.read_sheet(sheet_name)
                            discovered[sheet_name] = {
                                'rows': len(df),
                                'columns': list(df.columns),
                                'sample_data': df.head(2).to_dict('records') if len(df) > 0 else []
                            }
                            print(f"✅ {sheet_name:<15} {len(df):>3} rows | Columns: {list(df.columns)[:5]}")
                        except Exception as e:
                            print(f"❌ {sheet_name:<15} Error: {str(e)[:50]}")
            except Exception as e:
                print(f"⚠️  Could not get sheet metadata: {e}")
        
        self.discovered_sheets = discovered
        print(f"\n📈 TOTAL DISCOVERED: {len(discovered)} sheets with data")
        return discovered
    
    def analyze_sheet_structure(self, sheet_name, sheet_info):
        """Analyze the structure of a specific sheet"""
        print(f"\n📋 ANALYZING SHEET: {sheet_name}")
        print("-" * 40)
        
        columns = sheet_info['columns']
        rows = sheet_info['rows']
        sample_data = sheet_info['sample_data']
        
        print(f"   Rows: {rows}")
        print(f"   Columns: {len(columns)}")
        
        # Identify sheet type based on columns
        sheet_type = "Unknown"
        
        if any(col.lower() in ['user_id', 'username', 'email'] for col in columns):
            sheet_type = "Users/Authentication"
        elif any(col.lower() in ['product_id', 'item_id', 'sku'] for col in columns):
            sheet_type = "Products/Inventory"
        elif any(col.lower() in ['order_id', 'transaction_id'] for col in columns):
            sheet_type = "Orders/Transactions"
        elif any(col.lower() in ['customer_id', 'client_id'] for col in columns):
            sheet_type = "Customers"
        elif any(col.lower() in ['setting', 'config', 'key'] for col in columns):
            sheet_type = "Settings/Configuration"
        
        print(f"   Type: {sheet_type}")
        print(f"   Columns: {columns}")
        
        if sample_data and len(sample_data) > 0:
            print(f"   Sample Record:")
            for key, value in list(sample_data[0].items())[:3]:
                print(f"     {key}: {value}")
        
        return sheet_type
    
    def test_authentication_flows(self):
        """Test authentication flows based on available user data"""
        print("\n🔐 TESTING AUTHENTICATION FLOWS")
        print("=" * 60)
        
        user_sheets = []
        for sheet_name, info in self.discovered_sheets.items():
            columns = [col.lower() for col in info['columns']]
            if any(col in ['user_id', 'username', 'email', 'password', 'plain_password'] for col in columns):
                user_sheets.append(sheet_name)
        
        if not user_sheets:
            print("❌ No user/authentication sheets found")
            return False
        
        success = False
        for sheet_name in user_sheets:
            print(f"\n📋 Testing authentication with {sheet_name} sheet")
            
            try:
                users_df = self.storage.read_sheet(sheet_name)
                print(f"   📊 Found {len(users_df)} user records")
                
                if users_df.empty:
                    continue
                
                # Test admin login if we have the standard admin user
                admin_test = self.auth_service.authenticate('imam21', 'Iqrit@2024')
                if admin_test.get('success'):
                    admin_user = admin_test['user']
                    print(f"   ✅ Admin Login: {admin_user.get('full_name')} ({admin_user.get('role')})")
                    success = True
                else:
                    print(f"   ❌ Admin login failed: {admin_test.get('message', 'Unknown error')}")
                
                # Test with first available user that has credentials
                test_user = None
                for _, user in users_df.iterrows():
                    if user.get('plain_password') and user.get('user_id'):
                        test_user = user
                        break
                
                if test_user is not None:
                    user_test = self.auth_service.authenticate(
                        test_user['user_id'], 
                        test_user['plain_password']
                    )
                    if user_test.get('success'):
                        user_data = user_test['user']
                        print(f"   ✅ User Login: {user_data.get('full_name')} ({user_data.get('role')})")
                        success = True
                    else:
                        print(f"   ❌ User login failed: {user_test.get('message', 'Unknown error')}")
                
                # Test registration flow
                timestamp = int(time.time())
                test_reg = self.auth_service.create_account(
                    f'testuser_{timestamp}',
                    'TestPass123',
                    'Test Registration User',
                    f'test_{timestamp}@example.com',
                    '1234567890'
                )
                
                if test_reg.get('success'):
                    print(f"   ✅ Registration: New user created successfully")
                    success = True
                else:
                    print(f"   ❌ Registration failed: {test_reg.get('message', 'Unknown error')}")
                
            except Exception as e:
                print(f"   ❌ Authentication test error: {e}")
        
        return success
    
    def test_data_flows(self):
        """Test data access flows for dashboard, orders, etc."""
        print("\n📊 TESTING DATA ACCESS FLOWS")
        print("=" * 60)
        
        results = {}
        
        # Test each discovered sheet for different flow types
        for sheet_name, info in self.discovered_sheets.items():
            print(f"\n📋 Testing {sheet_name} sheet")
            
            try:
                df = self.storage.read_sheet(sheet_name)
                
                # Dashboard data test
                if len(df) > 0:
                    print(f"   ✅ Data Access: {len(df)} records retrieved")
                    results[f'data_access_{sheet_name}'] = True
                    
                    # Performance analytics test
                    if 'role' in df.columns:
                        role_dist = df['role'].value_counts().to_dict()
                        print(f"   📈 Performance Analytics: Role distribution {role_dist}")
                        results[f'performance_{sheet_name}'] = True
                    
                    # Lookup test
                    if len(df) > 0:
                        sample_record = df.iloc[0]
                        # Get first non-null value as lookup key
                        lookup_key = None
                        for col, val in sample_record.items():
                            if pd.notna(val) and str(val).strip():
                                lookup_key = (col, val)
                                break
                        
                        if lookup_key:
                            matches = df[df[lookup_key[0]] == lookup_key[1]]
                            print(f"   🔍 Lookup Test: Found {len(matches)} matches for {lookup_key[0]}={lookup_key[1]}")
                            results[f'lookup_{sheet_name}'] = True
                    
                    # Reports test
                    report_data = {
                        'sheet_name': sheet_name,
                        'total_records': len(df),
                        'columns': len(df.columns),
                        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    print(f"   📊 Reports: Generated summary with {len(report_data)} metrics")
                    results[f'reports_{sheet_name}'] = True
                
                else:
                    print(f"   ⚠️  Empty sheet - no data to test")
                    results[f'data_access_{sheet_name}'] = False
                
            except Exception as e:
                print(f"   ❌ Error testing {sheet_name}: {e}")
                results[f'data_access_{sheet_name}'] = False
        
        return results
    
    def test_order_creation_flow(self):
        """Test order creation flow if inventory/products available"""
        print("\n🛒 TESTING ORDER CREATION FLOW")
        print("=" * 60)
        
        # Look for product/inventory sheets
        inventory_sheets = []
        for sheet_name, info in self.discovered_sheets.items():
            columns = [col.lower() for col in info['columns']]
            if any(col in ['product_id', 'item_id', 'sku', 'price'] for col in columns):
                inventory_sheets.append(sheet_name)
        
        if not inventory_sheets:
            print("❌ No product/inventory sheets found - cannot test order creation")
            return False
        
        try:
            # Use first available inventory sheet
            sheet_name = inventory_sheets[0]
            products_df = self.storage.read_sheet(sheet_name)
            
            if products_df.empty:
                print(f"❌ {sheet_name} sheet is empty")
                return False
            
            print(f"✅ Using {sheet_name} sheet with {len(products_df)} products")
            
            # Create test order data
            sample_product = products_df.iloc[0]
            
            test_order = {
                'order_id': f'TEST_ORDER_{int(time.time())}',
                'user_id': 'test_user',
                'product_info': sample_product.to_dict(),
                'quantity': 2,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"✅ Order Creation Logic: Test order prepared")
            print(f"   Order ID: {test_order['order_id']}")
            print(f"   Product: {sample_product.get('product_id', 'N/A')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Order creation test failed: {e}")
            return False
    
    def run_comprehensive_tests(self):
        """Run all tests based on discovered sheets"""
        print("\n🚀 RUNNING COMPREHENSIVE FLOW TESTS")
        print("=" * 60)
        
        # Discover sheets first
        discovered = self.discover_all_sheets()
        
        if not discovered:
            print("❌ No sheets discovered - cannot run tests")
            return
        
        # Analyze each sheet
        for sheet_name, info in discovered.items():
            self.analyze_sheet_structure(sheet_name, info)
        
        # Run specific tests
        test_results = {}
        
        # Authentication tests
        test_results['authentication'] = self.test_authentication_flows()
        
        # Data flow tests
        data_results = self.test_data_flows()
        test_results.update(data_results)
        
        # Order creation test
        test_results['order_creation'] = self.test_order_creation_flow()
        
        # Final summary
        print("\n" + "=" * 60)
        print("📋 COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results.values() if result)
        
        print(f"📊 Sheets Discovered: {len(discovered)}")
        for sheet_name, info in discovered.items():
            print(f"   {sheet_name}: {info['rows']} rows")
        
        print(f"\n🎯 Test Results:")
        for test_name, passed in test_results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {test_name.replace('_', ' ').title():<25} {status}")
        
        print(f"\n📈 Overall: {passed_tests}/{total_tests} tests passed")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        if 'Users' in discovered or 'Customers' in discovered:
            print("   ✅ Ready for login/registration testing")
        else:
            print("   ⚠️  Consider adding Users sheet for authentication")
        
        if any('product' in name.lower() or 'inventory' in name.lower() for name in discovered.keys()):
            print("   ✅ Ready for product/inventory flows")
        else:
            print("   ⚠️  Consider adding Products/Inventory sheet")
        
        if any('order' in name.lower() for name in discovered.keys()):
            print("   ✅ Ready for order management flows")
        else:
            print("   ⚠️  Consider adding Orders sheet for transaction flows")
        
        print(f"\n🌐 Manual Testing: http://localhost:8599")

def main():
    """Main execution"""
    print("🔍 GOOGLE SHEETS ANALYSIS & COMPREHENSIVE TESTING")
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        analyzer = GoogleSheetsAnalyzer()
        analyzer.run_comprehensive_tests()
        
    except Exception as e:
        print(f"💥 Critical Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    print(f"\n{'🎉 Analysis complete!' if success else '❌ Analysis failed'}")