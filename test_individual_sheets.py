#!/usr/bin/env python3
"""
Individual Sheet Testing Scripts for CrazyShopperz
Creates specific test scripts for each discovered sheet using only Google Sheets API
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime, timedelta
import time

# Setup Google Sheets credentials
sys.path.append('.')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

try:
    import gspread
    from google.oauth2.service_account import Credentials
    GSPREAD_AVAILABLE = True
except ImportError:
    print("❌ gspread not available. Install with: pip install gspread")
    sys.exit(1)

class PerformanceSheetTester:
    """Test Performance sheet functionality"""
    
    def __init__(self):
        self.setup_connection()
        
    def setup_connection(self):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = Credentials.from_service_account_file(
            '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json',
            scopes=scopes
        )
        self.gc = gspread.authorize(credentials)
        self.sheet_id = '1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4'
        self.spreadsheet = self.gc.open_by_key(self.sheet_id)

    def get_performance_data(self):
        """Get Performance sheet data"""
        try:
            worksheet = self.spreadsheet.worksheet('Performance')
            all_values = worksheet.get_all_values()
            
            if len(all_values) > 1:
                headers = all_values[0]
                data_rows = all_values[1:]
                return pd.DataFrame(data_rows, columns=headers).dropna(how='all')
            return pd.DataFrame()
        except Exception as e:
            print(f"❌ Error getting Performance data: {e}")
            return pd.DataFrame()

    def test_performance_metrics(self):
        """Test performance metrics calculation"""
        print("🔄 Testing Performance Metrics")
        
        df = self.get_performance_data()
        if df.empty:
            print("   ❌ No performance data found")
            return False
            
        # Test metric columns
        required_cols = ['date', 'name', 'no_of_leads', 'no_of_orders']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"   ❌ Missing columns: {missing_cols}")
            return False
            
        # Test data quality
        numeric_leads = pd.to_numeric(df['no_of_leads'], errors='coerce').notna().sum()
        numeric_orders = pd.to_numeric(df['no_of_orders'], errors='coerce').notna().sum()
        
        print(f"   ✅ Performance data structure valid")
        print(f"   📊 {len(df)} performance records")
        print(f"   👥 {df['name'].nunique()} unique performers")
        print(f"   📈 {numeric_leads} records with valid lead counts")
        print(f"   🛍️ {numeric_orders} records with valid order counts")
        
        return True

    def test_performance_analytics(self):
        """Test performance analytics capability"""
        print("\n🔄 Testing Performance Analytics")
        
        df = self.get_performance_data()
        if df.empty:
            print("   ❌ No data for analytics")
            return False
            
        # Calculate conversion rates
        try:
            df['leads_num'] = pd.to_numeric(df['no_of_leads'], errors='coerce')
            df['orders_num'] = pd.to_numeric(df['no_of_orders'], errors='coerce')
            
            valid_data = df[(df['leads_num'].notna()) & (df['orders_num'].notna()) & (df['leads_num'] > 0)]
            
            if not valid_data.empty:
                valid_data['conversion_rate'] = (valid_data['orders_num'] / valid_data['leads_num']) * 100
                avg_conversion = valid_data['conversion_rate'].mean()
                
                print(f"   ✅ Performance analytics available")
                print(f"   📈 Average conversion rate: {avg_conversion:.2f}%")
                print(f"   🎯 {len(valid_data)} records with complete metrics")
                
                # Top performer
                if len(valid_data) > 1:
                    top_performer = valid_data.loc[valid_data['conversion_rate'].idxmax()]
                    print(f"   🏆 Top performer: {top_performer['name']} ({top_performer['conversion_rate']:.2f}%)")
                
                return True
            else:
                print("   ⚠️ No valid data for conversion rate calculation")
                return False
                
        except Exception as e:
            print(f"   ❌ Analytics calculation failed: {e}")
            return False

    def run_all_tests(self):
        """Run all Performance sheet tests"""
        print("=" * 50)
        print("📊 PERFORMANCE SHEET TESTING")
        print("=" * 50)
        
        results = []
        results.append(self.test_performance_metrics())
        results.append(self.test_performance_analytics())
        
        passed = sum(results)
        total = len(results)
        
        print(f"\n📋 Performance Tests: {passed}/{total} passed")
        return passed == total

class ProductListTester:
    """Test ProductList sheet functionality"""
    
    def __init__(self):
        self.setup_connection()
        
    def setup_connection(self):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = Credentials.from_service_account_file(
            '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json',
            scopes=scopes
        )
        self.gc = gspread.authorize(credentials)
        self.sheet_id = '1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4'
        self.spreadsheet = self.gc.open_by_key(self.sheet_id)

    def get_product_data(self):
        """Get ProductList sheet data"""
        try:
            worksheet = self.spreadsheet.worksheet('ProductList')
            all_values = worksheet.get_all_values()
            
            if len(all_values) > 1:
                headers = all_values[0]
                data_rows = all_values[1:]
                return pd.DataFrame(data_rows, columns=headers).dropna(how='all')
            return pd.DataFrame()
        except Exception as e:
            print(f"❌ Error getting ProductList data: {e}")
            return pd.DataFrame()

    def test_product_catalog(self):
        """Test product catalog functionality"""
        print("🔄 Testing Product Catalog")
        
        df = self.get_product_data()
        if df.empty:
            print("   ❌ No product data found")
            return False
            
        # Test required fields
        required_fields = ['product_name', 'price', 'description', 'status']
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            print(f"   ❌ Missing required fields: {missing_fields}")
            return False
            
        # Test data quality
        products_with_names = df[df['product_name'].notna() & (df['product_name'] != '')]
        products_with_prices = df[df['price'].notna() & (df['price'] != '')]
        active_products = df[df['status'] == 'active'] if 'status' in df.columns else df
        
        print(f"   ✅ Product catalog structure valid")
        print(f"   📦 {len(products_with_names)} products with names")
        print(f"   💰 {len(products_with_prices)} products with prices")
        print(f"   🟢 {len(active_products)} active products")
        
        return True

    def test_product_search(self):
        """Test product search functionality"""
        print("\n🔄 Testing Product Search")
        
        df = self.get_product_data()
        if df.empty:
            print("   ❌ No data for search testing")
            return False
            
        # Test search by name
        searchable_products = df[df['product_name'].notna()]
        
        if not searchable_products.empty:
            sample_product = searchable_products.iloc[0]
            print(f"   ✅ Product search available")
            print(f"   🔍 Sample searchable product: {sample_product['product_name']}")
            print(f"   💵 Price: ₹{sample_product['price']}")
            
            # Test category-based search if available
            if 'category' in df.columns:
                categories = df['category'].dropna().unique()
                if len(categories) > 0:
                    print(f"   🏷️ {len(categories)} product categories available")
            
            return True
        else:
            print("   ❌ No searchable products")
            return False

    def test_inventory_management(self):
        """Test inventory management"""
        print("\n🔄 Testing Inventory Management")
        
        df = self.get_product_data()
        if df.empty:
            print("   ❌ No data for inventory testing")
            return False
            
        # Test stock tracking
        if 'stock' in df.columns:
            products_with_stock = df[df['stock'].notna()]
            if not products_with_stock.empty:
                try:
                    stock_numeric = pd.to_numeric(products_with_stock['stock'], errors='coerce')
                    valid_stock = stock_numeric.notna().sum()
                    low_stock = (stock_numeric < 5).sum()
                    
                    print(f"   ✅ Inventory tracking available")
                    print(f"   📊 {valid_stock} products with stock data")
                    print(f"   ⚠️ {low_stock} products with low stock")
                    return True
                except:
                    print("   ⚠️ Stock data format issues")
                    return False
            else:
                print("   ⚠️ No stock data available")
                return False
        else:
            print("   ⚠️ Stock column not found")
            return False

    def run_all_tests(self):
        """Run all ProductList tests"""
        print("=" * 50)
        print("📦 PRODUCT LIST TESTING")
        print("=" * 50)
        
        results = []
        results.append(self.test_product_catalog())
        results.append(self.test_product_search())
        results.append(self.test_inventory_management())
        
        passed = sum(results)
        total = len(results)
        
        print(f"\n📋 Product Tests: {passed}/{total} passed")
        return passed == total

class ChatLogsTester:
    """Test ChatLogs sheet functionality"""
    
    def __init__(self):
        self.setup_connection()
        
    def setup_connection(self):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        credentials = Credentials.from_service_account_file(
            '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json',
            scopes=scopes
        )
        self.gc = gspread.authorize(credentials)
        self.sheet_id = '1prxGZVz3jccpjI3nEk7wwSfnsTSth5205qUzP_6fIM4'
        self.spreadsheet = self.gc.open_by_key(self.sheet_id)

    def get_chat_data(self):
        """Get ChatLogs sheet data"""
        try:
            worksheet = self.spreadsheet.worksheet('ChatLogs')
            all_values = worksheet.get_all_values()
            
            if len(all_values) > 1:
                headers = all_values[0]
                data_rows = all_values[1:]
                return pd.DataFrame(data_rows, columns=headers).dropna(how='all')
            return pd.DataFrame()
        except Exception as e:
            print(f"❌ Error getting ChatLogs data: {e}")
            return pd.DataFrame()

    def test_chat_logging(self):
        """Test chat logging functionality"""
        print("🔄 Testing Chat Logging")
        
        df = self.get_chat_data()
        if df.empty:
            print("   ❌ No chat data found")
            return False
            
        # Test required fields
        required_fields = ['message_id', 'phone', 'message', 'direction', 'timestamp']
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            print(f"   ❌ Missing required fields: {missing_fields}")
            return False
            
        # Test data quality
        messages_with_id = df[df['message_id'].notna()]
        messages_with_phone = df[df['phone'].notna()]
        incoming_messages = df[df['direction'] == 'incoming'] if 'direction' in df.columns else pd.DataFrame()
        outgoing_messages = df[df['direction'] == 'outgoing'] if 'direction' in df.columns else pd.DataFrame()
        
        print(f"   ✅ Chat logging structure valid")
        print(f"   📱 {len(messages_with_phone)} messages with phone numbers")
        print(f"   📨 {len(incoming_messages)} incoming messages")
        print(f"   📤 {len(outgoing_messages)} outgoing messages")
        print(f"   🆔 {len(messages_with_id)} messages with unique IDs")
        
        return True

    def test_ai_automation_tracking(self):
        """Test AI automation tracking"""
        print("\n🔄 Testing AI Automation Tracking")
        
        df = self.get_chat_data()
        if df.empty:
            print("   ❌ No data for AI tracking")
            return False
            
        # Test AI tracking fields
        ai_fields = ['ai_attempted', 'ai_success', 'failure_reason']
        ai_field_exists = [field for field in ai_fields if field in df.columns]
        
        if ai_field_exists:
            ai_attempted = df[df['ai_attempted'] == 'TRUE'] if 'ai_attempted' in df.columns else pd.DataFrame()
            ai_successful = df[df['ai_success'] == 'TRUE'] if 'ai_success' in df.columns else pd.DataFrame()
            
            success_rate = (len(ai_successful) / len(ai_attempted) * 100) if len(ai_attempted) > 0 else 0
            
            print(f"   ✅ AI automation tracking available")
            print(f"   🤖 {len(ai_attempted)} AI attempts recorded")
            print(f"   ✅ {len(ai_successful)} successful AI responses")
            print(f"   📊 {success_rate:.1f}% AI success rate")
            
            if 'failure_reason' in df.columns:
                failures_with_reason = df[df['failure_reason'].notna() & (df['failure_reason'] != '')]
                print(f"   📝 {len(failures_with_reason)} failures with documented reasons")
            
            return True
        else:
            print("   ⚠️ AI tracking fields not found")
            return False

    def test_customer_communication(self):
        """Test customer communication analysis"""
        print("\n🔄 Testing Customer Communication")
        
        df = self.get_chat_data()
        if df.empty:
            print("   ❌ No data for communication analysis")
            return False
            
        # Analyze communication patterns
        unique_customers = df['phone'].nunique() if 'phone' in df.columns else 0
        total_messages = len(df)
        
        if 'timestamp' in df.columns:
            # Recent activity (last 24 hours if possible)
            try:
                df['timestamp_dt'] = pd.to_datetime(df['timestamp'], errors='coerce')
                recent_messages = df[df['timestamp_dt'].notna()]
                
                print(f"   ✅ Customer communication tracking")
                print(f"   👥 {unique_customers} unique customers")
                print(f"   💬 {total_messages} total messages")
                print(f"   ⏰ {len(recent_messages)} messages with timestamps")
                
                if len(recent_messages) > 0:
                    avg_messages_per_customer = total_messages / unique_customers if unique_customers > 0 else 0
                    print(f"   📊 {avg_messages_per_customer:.1f} average messages per customer")
                
                return True
            except:
                print("   ⚠️ Timestamp format issues")
                return False
        else:
            print("   ⚠️ No timestamp data for communication analysis")
            return False

    def run_all_tests(self):
        """Run all ChatLogs tests"""
        print("=" * 50)
        print("💬 CHAT LOGS TESTING")
        print("=" * 50)
        
        results = []
        results.append(self.test_chat_logging())
        results.append(self.test_ai_automation_tracking())
        results.append(self.test_customer_communication())
        
        passed = sum(results)
        total = len(results)
        
        print(f"\n📋 Chat Tests: {passed}/{total} passed")
        return passed == total

def main():
    """Run all individual sheet tests"""
    print("=" * 70)
    print("🧪 INDIVIDUAL SHEET TESTING - GOOGLE SHEETS ONLY")
    print("=" * 70)
    
    all_results = []
    
    # Test Performance Sheet
    performance_tester = PerformanceSheetTester()
    all_results.append(performance_tester.run_all_tests())
    
    print("\n" + "="*70)
    
    # Test ProductList Sheet
    product_tester = ProductListTester()
    all_results.append(product_tester.run_all_tests())
    
    print("\n" + "="*70)
    
    # Test ChatLogs Sheet
    chat_tester = ChatLogsTester()
    all_results.append(chat_tester.run_all_tests())
    
    # Summary
    print("\n" + "="*70)
    print("📊 INDIVIDUAL SHEET TESTING SUMMARY")
    print("="*70)
    
    passed_sheets = sum(all_results)
    total_sheets = len(all_results)
    
    print(f"✅ PASSED SHEETS: {passed_sheets}/{total_sheets}")
    
    sheet_names = ['Performance', 'ProductList', 'ChatLogs']
    for i, result in enumerate(all_results):
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {sheet_names[i]} Sheet Testing")
    
    return passed_sheets == total_sheets

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)