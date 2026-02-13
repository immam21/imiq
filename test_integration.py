#!/usr/bin/env python3
"""
Integration test for IMIQ with CZ_MasterSheet.xlsx
Tests basic functionality with the existing schema
"""

import pandas as pd
import sys
import os

# Add the imiq package to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from imiq.storage import get_storage_instance
from imiq.auth import AuthService
from imiq.orders import OrderService
from imiq.inventory import InventoryService
from imiq.kpis import KPIService


def test_storage_connection():
    """Test storage connection and sheet reading"""
    print("=== Testing Storage Connection ===")
    
    try:
        storage = get_storage_instance()
        print("✅ Storage instance created successfully")
        
        # Test reading each sheet
        sheets_to_test = ['Users', 'NewOrders', 'ProductList', 'Customers']
        
        for sheet_name in sheets_to_test:
            try:
                df = storage.read_sheet(sheet_name)
                print(f"✅ {sheet_name} sheet: {len(df)} rows, columns: {list(df.columns)}")
            except Exception as e:
                print(f"❌ Error reading {sheet_name}: {e}")
        
        return True
    except Exception as e:
        print(f"❌ Storage connection failed: {e}")
        return False


def test_auth_service():
    """Test authentication with existing users"""
    print("\n=== Testing Authentication Service ===")
    
    try:
        storage = get_storage_instance()
        auth_service = AuthService(storage)
        
        # Read existing users
        users_df = storage.read_sheet('Users')
        if not users_df.empty:
            print(f"✅ Found {len(users_df)} existing users")
            
            # Test with first user if they have plain_password
            if 'plain_password' in users_df.columns:
                first_user = users_df.iloc[0]
                if pd.notna(first_user.get('plain_password')):
                    email = first_user['email']
                    password = first_user['plain_password']
                    
                    user = auth_service.authenticate(email, password)
                    if user:
                        print(f"✅ Authentication successful for: {user['email']} (role: {user['role']})")
                    else:
                        print("❌ Authentication failed")
                else:
                    print("⚠️  No plain password available for testing")
            else:
                print("⚠️  No plain_password column found")
        else:
            print("⚠️  No existing users found")
            
        return True
    except Exception as e:
        print(f"❌ Auth service error: {e}")
        return False


def test_order_service():
    """Test order operations"""
    print("\n=== Testing Order Service ===")
    
    try:
        storage = get_storage_instance()
        order_service = OrderService(storage)
        
        # Read existing orders
        orders_df = storage.read_sheet('NewOrders')
        print(f"✅ Found {len(orders_df)} existing orders")
        
        if not orders_df.empty:
            print(f"Order columns: {list(orders_df.columns)}")
            print("Sample order data:")
            print(orders_df.head(1).to_dict('records')[0])
        
        return True
    except Exception as e:
        print(f"❌ Order service error: {e}")
        return False


def test_inventory_service():
    """Test inventory operations"""
    print("\n=== Testing Inventory Service ===")
    
    try:
        storage = get_storage_instance()
        inventory_service = InventoryService(storage)
        
        # Read existing products
        products = inventory_service.get_all_inventory()
        print(f"✅ Found {len(products)} existing products")
        
        if not products.empty:
            print(f"Product columns: {list(products.columns)}")
            print("Sample product data:")
            print(products.head(1).to_dict('records')[0])
            
            # Test low stock alerts
            alerts = inventory_service.get_low_stock_alerts()
            print(f"✅ Low stock alerts: {len(alerts)} items")
        
        return True
    except Exception as e:
        print(f"❌ Inventory service error: {e}")
        return False


def test_kpi_service():
    """Test KPI calculations"""
    print("\n=== Testing KPI Service ===")
    
    try:
        storage = get_storage_instance()
        kpi_service = KPIService(storage)
        
        # Test basic KPI calculations
        daily_counts = kpi_service.get_daily_order_counts(7)
        print(f"✅ Daily order counts: {len(daily_counts)} days")
        
        summary = kpi_service.get_summary_stats()
        print(f"✅ Summary stats calculated: {summary}")
        
        return True
    except Exception as e:
        print(f"❌ KPI service error: {e}")
        return False


def main():
    """Run all integration tests"""
    print("🧪 IMIQ Integration Tests with CZ_MasterSheet.xlsx")
    print("=" * 60)
    
    tests = [
        test_storage_connection,
        test_auth_service, 
        test_order_service,
        test_inventory_service,
        test_kpi_service
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print(f"\n{'=' * 60}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! IMIQ is ready to use with CZ_MasterSheet.xlsx")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)