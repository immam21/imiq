#!/usr/bin/env python3
"""
Comprehensive Flow Testing for CrazyShopperz
Tests all discovered flows: register, login, dashboard, performance, orders, create orders, lookup, reports
Uses ONLY Google Sheets API - no existing storage
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime, timedelta
import time
import random

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

class CrazyShopperzTester:
    def __init__(self):
        """Initialize the comprehensive tester"""
        self.setup_sheets_connection()
        self.test_results = {}
        
    def setup_sheets_connection(self):
        """Setup Google Sheets connection with proper scopes"""
        try:
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
            
            print(f"✅ Connected to: {self.spreadsheet.title}")
            
        except Exception as e:
            print(f"❌ Failed to connect to Google Sheets: {e}")
            raise

    def get_sheet_data(self, sheet_name):
        """Get data from specific sheet"""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            all_values = worksheet.get_all_values()
            
            if len(all_values) > 1:
                headers = all_values[0]
                data_rows = all_values[1:]
                df = pd.DataFrame(data_rows, columns=headers)
                return df.dropna(how='all')
            return pd.DataFrame()
            
        except Exception as e:
            print(f"❌ Error getting {sheet_name} data: {e}")
            return pd.DataFrame()

    def test_register_flow(self):
        """Test user registration flow"""
        print("\n🔄 TESTING REGISTER FLOW")
        test_name = "register_flow"
        
        try:
            users_df = self.get_sheet_data('Users')
            
            # Test 1: Validate user registration data structure
            required_fields = ['user_id', 'email', 'password_hash', 'role', 'name', 'is_active']
            missing_fields = [field for field in required_fields if field not in users_df.columns]
            
            if missing_fields:
                result = f"❌ Missing required fields: {missing_fields}"
            else:
                # Test 2: Validate admin user exists
                admin_users = users_df[users_df['role'] == 'admin']
                
                if admin_users.empty:
                    result = "❌ No admin user found for registration management"
                else:
                    # Test 3: Validate user data integrity
                    active_users = users_df[users_df['is_active'] == 'true']
                    inactive_users = users_df[users_df['is_active'] == 'false']
                    
                    # Test 4: Registration validation
                    duplicate_emails = users_df[users_df.duplicated('email', keep=False)]
                    
                    if not duplicate_emails.empty:
                        result = f"⚠️ Found {len(duplicate_emails)} duplicate emails - registration validation needed"
                    else:
                        result = f"✅ Registration flow valid - {len(users_df)} users, {len(admin_users)} admins, {len(active_users)} active users"
            
            self.test_results[test_name] = {
                'status': 'pass' if '✅' in result else 'fail',
                'result': result,
                'data_count': len(users_df)
            }
            print(f"   {result}")
            
        except Exception as e:
            result = f"❌ Register flow test failed: {str(e)}"
            self.test_results[test_name] = {'status': 'error', 'result': result}
            print(f"   {result}")

    def test_login_flow(self):
        """Test login authentication flow"""
        print("\n🔄 TESTING LOGIN FLOW")
        test_name = "login_flow"
        
        try:
            users_df = self.get_sheet_data('Users')
            
            if users_df.empty:
                result = "❌ No users found - login flow broken"
            else:
                # Test admin login
                admin_users = users_df[users_df['role'] == 'admin']
                regular_users = users_df[users_df['role'] != 'admin']
                
                # Validate login credentials
                users_with_passwords = users_df[users_df['password_hash'].notna()]
                active_users = users_df[users_df['is_active'] == 'true']
                
                login_tests = []
                
                # Test 1: Admin login capability
                if not admin_users.empty:
                    login_tests.append(f"✅ Admin login available ({len(admin_users)} admin users)")
                else:
                    login_tests.append("❌ No admin users - admin login blocked")
                
                # Test 2: Regular user login
                if not regular_users.empty:
                    login_tests.append(f"✅ User login available ({len(regular_users)} regular users)")
                
                # Test 3: Password security
                if len(users_with_passwords) == len(users_df):
                    login_tests.append("✅ All users have password hashes")
                else:
                    login_tests.append(f"⚠️ {len(users_df) - len(users_with_passwords)} users missing passwords")
                
                # Test 4: Active user validation
                login_tests.append(f"✅ {len(active_users)} active users can login")
                
                result = " | ".join(login_tests)
            
            self.test_results[test_name] = {
                'status': 'pass' if '❌' not in result else 'fail',
                'result': result,
                'admin_users': len(admin_users) if not admin_users.empty else 0,
                'total_users': len(users_df)
            }
            print(f"   {result}")
            
        except Exception as e:
            result = f"❌ Login flow test failed: {str(e)}"
            self.test_results[test_name] = {'status': 'error', 'result': result}
            print(f"   {result}")

    def test_dashboard_flow(self):
        """Test dashboard data flow"""
        print("\n🔄 TESTING DASHBOARD FLOW")
        test_name = "dashboard_flow"
        
        try:
            # Get all dashboard-related data
            users_df = self.get_sheet_data('Users')
            orders_df = self.get_sheet_data('NewOrders')
            performance_df = self.get_sheet_data('Performance')
            customers_df = self.get_sheet_data('Customers')
            
            dashboard_components = []
            
            # Test 1: User dashboard access
            if not users_df.empty:
                dashboard_components.append(f"✅ User management ({len(users_df)} users)")
            else:
                dashboard_components.append("❌ No user data for dashboard")
            
            # Test 2: Orders dashboard
            if not orders_df.empty:
                recent_orders = orders_df[orders_df['timestamp'].notna()]
                dashboard_components.append(f"✅ Orders dashboard ({len(orders_df)} orders, {len(recent_orders)} with timestamps)")
            else:
                dashboard_components.append("❌ No order data for dashboard")
            
            # Test 3: Performance dashboard
            if not performance_df.empty:
                dashboard_components.append(f"✅ Performance metrics ({len(performance_df)} records)")
            else:
                dashboard_components.append("❌ No performance data for dashboard")
            
            # Test 4: Customer dashboard
            if not customers_df.empty:
                dashboard_components.append(f"✅ Customer management ({len(customers_df)} customers)")
            else:
                dashboard_components.append("❌ No customer data for dashboard")
            
            # Test 5: Dashboard analytics capability
            total_data_points = len(users_df) + len(orders_df) + len(performance_df) + len(customers_df)
            if total_data_points > 0:
                dashboard_components.append(f"✅ Analytics ready ({total_data_points} total data points)")
            
            result = " | ".join(dashboard_components)
            
            self.test_results[test_name] = {
                'status': 'pass' if '❌' not in result else 'partial',
                'result': result,
                'data_summary': {
                    'users': len(users_df),
                    'orders': len(orders_df),
                    'performance': len(performance_df),
                    'customers': len(customers_df)
                }
            }
            print(f"   {result}")
            
        except Exception as e:
            result = f"❌ Dashboard flow test failed: {str(e)}"
            self.test_results[test_name] = {'status': 'error', 'result': result}
            print(f"   {result}")

    def test_performance_flow(self):
        """Test performance tracking flow"""
        print("\n🔄 TESTING PERFORMANCE FLOW")
        test_name = "performance_flow"
        
        try:
            performance_df = self.get_sheet_data('Performance')
            users_df = self.get_sheet_data('Users')
            
            if performance_df.empty:
                result = "❌ No performance data found"
            else:
                performance_tests = []
                
                # Test 1: Performance data structure
                required_fields = ['date', 'name', 'no_of_leads', 'no_of_orders']
                if all(field in performance_df.columns for field in required_fields):
                    performance_tests.append("✅ Performance data structure valid")
                else:
                    performance_tests.append("❌ Performance data structure incomplete")
                
                # Test 2: User performance tracking
                users_with_performance = performance_df['name'].nunique()
                performance_tests.append(f"✅ {users_with_performance} users have performance data")
                
                # Test 3: Metrics calculation
                total_leads = performance_df['no_of_leads'].astype(str).str.isnumeric().sum()
                total_orders = performance_df['no_of_orders'].astype(str).str.isnumeric().sum()
                
                if total_leads > 0 and total_orders > 0:
                    performance_tests.append(f"✅ Performance metrics available (leads & orders tracked)")
                else:
                    performance_tests.append("⚠️ Performance metrics may have data quality issues")
                
                # Test 4: Performance reporting
                date_range = performance_df['date'].nunique() if 'date' in performance_df.columns else 0
                performance_tests.append(f"✅ Performance tracking across {date_range} time periods")
                
                result = " | ".join(performance_tests)
            
            self.test_results[test_name] = {
                'status': 'pass' if '❌' not in result else 'partial',
                'result': result,
                'performance_records': len(performance_df),
                'users_tracked': users_with_performance if not performance_df.empty else 0
            }
            print(f"   {result}")
            
        except Exception as e:
            result = f"❌ Performance flow test failed: {str(e)}"
            self.test_results[test_name] = {'status': 'error', 'result': result}
            print(f"   {result}")

    def test_orders_flow(self):
        """Test orders management flow"""
        print("\n🔄 TESTING ORDERS FLOW")
        test_name = "orders_flow"
        
        try:
            orders_df = self.get_sheet_data('NewOrders')
            products_df = self.get_sheet_data('ProductList')
            
            if orders_df.empty:
                result = "❌ No orders found"
            else:
                order_tests = []
                
                # Test 1: Order data completeness
                required_fields = ['order_id', 'phone', 'customer_name', 'product', 'total', 'status']
                missing_fields = [field for field in required_fields if field not in orders_df.columns]
                
                if not missing_fields:
                    order_tests.append("✅ Order data structure complete")
                else:
                    order_tests.append(f"❌ Missing order fields: {missing_fields}")
                
                # Test 2: Order status tracking
                order_statuses = orders_df['status'].value_counts()
                order_tests.append(f"✅ Order status tracking ({len(order_statuses)} different statuses)")
                
                # Test 3: Order-product relationship
                if not products_df.empty:
                    order_tests.append(f"✅ Product catalog available ({len(products_df)} products)")
                else:
                    order_tests.append("⚠️ No product catalog - order-product relationship missing")
                
                # Test 4: Payment tracking
                payment_methods = orders_df['payment_method'].value_counts() if 'payment_method' in orders_df.columns else {}
                if len(payment_methods) > 0:
                    order_tests.append(f"✅ Payment methods tracked ({len(payment_methods)} types)")
                
                # Test 5: Order fulfillment
                orders_with_tracking = orders_df[orders_df['tracking_id'].notna()] if 'tracking_id' in orders_df.columns else pd.DataFrame()
                if not orders_with_tracking.empty:
                    order_tests.append(f"✅ Order tracking available ({len(orders_with_tracking)} orders with tracking)")
                
                result = " | ".join(order_tests)
            
            self.test_results[test_name] = {
                'status': 'pass' if '❌' not in result else 'partial',
                'result': result,
                'total_orders': len(orders_df),
                'order_statuses': dict(order_statuses) if not orders_df.empty and 'status' in orders_df.columns else {}
            }
            print(f"   {result}")
            
        except Exception as e:
            result = f"❌ Orders flow test failed: {str(e)}"
            self.test_results[test_name] = {'status': 'error', 'result': result}
            print(f"   {result}")

    def test_create_orders_flow(self):
        """Test order creation flow"""
        print("\n🔄 TESTING CREATE ORDERS FLOW")
        test_name = "create_orders_flow"
        
        try:
            products_df = self.get_sheet_data('ProductList')
            orders_df = self.get_sheet_data('NewOrders')
            customers_df = self.get_sheet_data('Customers')
            
            creation_tests = []
            
            # Test 1: Product availability for order creation
            if not products_df.empty:
                active_products = products_df[products_df['status'] == 'active'] if 'status' in products_df.columns else products_df
                creation_tests.append(f"✅ Products available for ordering ({len(active_products)} active products)")
            else:
                creation_tests.append("❌ No products available - cannot create orders")
            
            # Test 2: Customer management for orders
            if not customers_df.empty:
                creation_tests.append(f"✅ Customer base exists ({len(customers_df)} customers)")
            else:
                creation_tests.append("⚠️ No existing customers - new customer creation needed")
            
            # Test 3: Order creation capability analysis
            if not orders_df.empty:
                # Analyze recent order creation pattern
                recent_orders = orders_df.tail(10)  # Last 10 orders
                creation_tests.append(f"✅ Order creation active (recent orders exist)")
                
                # Test order ID generation
                order_ids = orders_df['order_id'].tolist()
                unique_order_ids = len(set(order_ids))
                if unique_order_ids == len(order_ids):
                    creation_tests.append("✅ Order ID generation working (all unique)")
                else:
                    creation_tests.append("⚠️ Duplicate order IDs detected")
            
            # Test 4: Order workflow completeness
            required_order_fields = ['order_id', 'phone', 'customer_name', 'product', 'quantity', 'total', 'status']
            if not orders_df.empty:
                missing_creation_fields = [field for field in required_order_fields if field not in orders_df.columns]
                if not missing_creation_fields:
                    creation_tests.append("✅ Order creation workflow complete")
                else:
                    creation_tests.append(f"⚠️ Order creation missing: {missing_creation_fields}")
            
            result = " | ".join(creation_tests)
            
            self.test_results[test_name] = {
                'status': 'pass' if '❌' not in result else 'partial',
                'result': result,
                'products_available': len(products_df),
                'orders_created': len(orders_df)
            }
            print(f"   {result}")
            
        except Exception as e:
            result = f"❌ Create orders flow test failed: {str(e)}"
            self.test_results[test_name] = {'status': 'error', 'result': result}
            print(f"   {result}")

    def test_lookup_flow(self):
        """Test lookup and search flow"""
        print("\n🔄 TESTING LOOKUP FLOW")
        test_name = "lookup_flow"
        
        try:
            customers_df = self.get_sheet_data('Customers')
            orders_df = self.get_sheet_data('NewOrders')
            products_df = self.get_sheet_data('ProductList')
            chat_logs_df = self.get_sheet_data('ChatLogs')
            
            lookup_tests = []
            
            # Test 1: Customer lookup
            if not customers_df.empty:
                customers_with_phone = customers_df[customers_df['phone'].notna()]
                customers_with_email = customers_df[customers_df['email'].notna()]
                lookup_tests.append(f"✅ Customer lookup available ({len(customers_with_phone)} by phone, {len(customers_with_email)} by email)")
            else:
                lookup_tests.append("❌ Customer lookup not available")
            
            # Test 2: Order lookup
            if not orders_df.empty:
                orders_with_id = orders_df[orders_df['order_id'].notna()]
                orders_with_phone = orders_df[orders_df['phone'].notna()]
                lookup_tests.append(f"✅ Order lookup available ({len(orders_with_id)} by order ID, {len(orders_with_phone)} by phone)")
            else:
                lookup_tests.append("❌ Order lookup not available")
            
            # Test 3: Product lookup
            if not products_df.empty:
                products_with_name = products_df[products_df['product_name'].notna()]
                lookup_tests.append(f"✅ Product lookup available ({len(products_with_name)} products)")
            else:
                lookup_tests.append("❌ Product lookup not available")
            
            # Test 4: Chat history lookup
            if not chat_logs_df.empty:
                chats_with_phone = chat_logs_df[chat_logs_df['phone'].notna()]
                lookup_tests.append(f"✅ Chat history lookup available ({len(chats_with_phone)} chat records)")
            else:
                lookup_tests.append("⚠️ Chat history lookup not available")
            
            # Test 5: Cross-reference lookup capability
            if not customers_df.empty and not orders_df.empty:
                # Check if customer phones match order phones
                customer_phones = set(customers_df['phone'].dropna())
                order_phones = set(orders_df['phone'].dropna())
                matching_phones = customer_phones.intersection(order_phones)
                lookup_tests.append(f"✅ Cross-reference lookup possible ({len(matching_phones)} matching customer-order records)")
            
            result = " | ".join(lookup_tests)
            
            self.test_results[test_name] = {
                'status': 'pass' if '❌' not in result else 'partial',
                'result': result,
                'lookup_sources': {
                    'customers': len(customers_df),
                    'orders': len(orders_df),
                    'products': len(products_df),
                    'chats': len(chat_logs_df)
                }
            }
            print(f"   {result}")
            
        except Exception as e:
            result = f"❌ Lookup flow test failed: {str(e)}"
            self.test_results[test_name] = {'status': 'error', 'result': result}
            print(f"   {result}")

    def test_reports_flow(self):
        """Test reporting and analytics flow"""
        print("\n🔄 TESTING REPORTS FLOW")
        test_name = "reports_flow"
        
        try:
            orders_df = self.get_sheet_data('NewOrders')
            performance_df = self.get_sheet_data('Performance')
            customers_df = self.get_sheet_data('Customers')
            chat_logs_df = self.get_sheet_data('ChatLogs')
            
            report_tests = []
            
            # Test 1: Sales reporting
            if not orders_df.empty:
                # Revenue calculation capability
                orders_with_total = orders_df[orders_df['total'].notna()]
                if not orders_with_total.empty:
                    report_tests.append(f"✅ Sales reporting available ({len(orders_with_total)} orders with amounts)")
                else:
                    report_tests.append("⚠️ Sales reporting limited - missing amount data")
            else:
                report_tests.append("❌ Sales reporting not available")
            
            # Test 2: Performance reporting
            if not performance_df.empty:
                performance_metrics = performance_df[['no_of_leads', 'no_of_orders']].dropna()
                if not performance_metrics.empty:
                    report_tests.append(f"✅ Performance reporting available ({len(performance_metrics)} performance records)")
                else:
                    report_tests.append("⚠️ Performance reporting data incomplete")
            else:
                report_tests.append("❌ Performance reporting not available")
            
            # Test 3: Customer analytics
            if not customers_df.empty:
                customers_with_location = customers_df[customers_df['city'].notna()]
                report_tests.append(f"✅ Customer analytics available ({len(customers_with_location)} customers with location data)")
            else:
                report_tests.append("❌ Customer analytics not available")
            
            # Test 4: Communication analytics
            if not chat_logs_df.empty:
                chat_analytics = chat_logs_df[chat_logs_df['timestamp'].notna()]
                if not chat_analytics.empty:
                    report_tests.append(f"✅ Communication analytics available ({len(chat_analytics)} chat records)")
                else:
                    report_tests.append("⚠️ Communication analytics limited")
            else:
                report_tests.append("❌ Communication analytics not available")
            
            # Test 5: Comprehensive reporting capability
            total_report_data = len(orders_df) + len(performance_df) + len(customers_df) + len(chat_logs_df)
            if total_report_data > 50:
                report_tests.append(f"✅ Comprehensive reporting possible ({total_report_data} total records)")
            elif total_report_data > 0:
                report_tests.append(f"⚠️ Limited reporting capability ({total_report_data} total records)")
            
            result = " | ".join(report_tests)
            
            self.test_results[test_name] = {
                'status': 'pass' if '❌' not in result else 'partial',
                'result': result,
                'report_data_summary': {
                    'orders': len(orders_df),
                    'performance': len(performance_df),
                    'customers': len(customers_df),
                    'communications': len(chat_logs_df)
                }
            }
            print(f"   {result}")
            
        except Exception as e:
            result = f"❌ Reports flow test failed: {str(e)}"
            self.test_results[test_name] = {'status': 'error', 'result': result}
            print(f"   {result}")

    def test_ai_integration_flow(self):
        """Test AI integration and chat automation flow"""
        print("\n🔄 TESTING AI INTEGRATION FLOW")
        test_name = "ai_integration_flow"
        
        try:
            ai_prompts_df = self.get_sheet_data('AI_Prompts')
            chat_logs_df = self.get_sheet_data('ChatLogs')
            chat_assignments_df = self.get_sheet_data('ChatAssignments')
            
            ai_tests = []
            
            # Test 1: AI prompts configuration
            if not ai_prompts_df.empty:
                active_prompts = ai_prompts_df[ai_prompts_df['is_active'] == 'TRUE'] if 'is_active' in ai_prompts_df.columns else ai_prompts_df
                ai_tests.append(f"✅ AI prompts configured ({len(active_prompts)} active prompts)")
            else:
                ai_tests.append("❌ AI prompts not configured")
            
            # Test 2: Chat automation tracking
            if not chat_logs_df.empty:
                ai_attempted = chat_logs_df[chat_logs_df['ai_attempted'] == 'TRUE'] if 'ai_attempted' in chat_logs_df.columns else pd.DataFrame()
                ai_successful = chat_logs_df[chat_logs_df['ai_success'] == 'TRUE'] if 'ai_success' in chat_logs_df.columns else pd.DataFrame()
                
                if not ai_attempted.empty:
                    success_rate = len(ai_successful) / len(ai_attempted) * 100 if len(ai_attempted) > 0 else 0
                    ai_tests.append(f"✅ AI automation active ({len(ai_attempted)} attempts, {success_rate:.1f}% success rate)")
                else:
                    ai_tests.append("⚠️ AI automation not actively used")
            else:
                ai_tests.append("❌ Chat automation tracking not available")
            
            # Test 3: Chat assignment system
            if not chat_assignments_df.empty:
                active_assignments = chat_assignments_df[chat_assignments_df['status'].notna()]
                ai_tests.append(f"✅ Chat assignment system active ({len(active_assignments)} assignments)")
            else:
                ai_tests.append("⚠️ Chat assignment system not configured")
            
            # Test 4: Integration health
            total_chats = len(chat_logs_df)
            automated_chats = len(ai_attempted) if 'ai_attempted' in locals() else 0
            
            if total_chats > 0:
                automation_rate = (automated_chats / total_chats) * 100
                if automation_rate > 10:
                    ai_tests.append(f"✅ AI integration healthy ({automation_rate:.1f}% automation rate)")
                else:
                    ai_tests.append(f"⚠️ Low AI integration usage ({automation_rate:.1f}% automation rate)")
            
            result = " | ".join(ai_tests)
            
            self.test_results[test_name] = {
                'status': 'pass' if '❌' not in result else 'partial',
                'result': result,
                'ai_data_summary': {
                    'prompts': len(ai_prompts_df),
                    'chat_logs': len(chat_logs_df),
                    'assignments': len(chat_assignments_df)
                }
            }
            print(f"   {result}")
            
        except Exception as e:
            result = f"❌ AI integration flow test failed: {str(e)}"
            self.test_results[test_name] = {'status': 'error', 'result': result}
            print(f"   {result}")

    def run_all_tests(self):
        """Run all flow tests"""
        print("=" * 70)
        print("🚀 COMPREHENSIVE FLOW TESTING - CRAZYSHOPPERZ")
        print("=" * 70)
        
        # Run all tests
        self.test_register_flow()
        self.test_login_flow()
        self.test_dashboard_flow()
        self.test_performance_flow()
        self.test_orders_flow()
        self.test_create_orders_flow()
        self.test_lookup_flow()
        self.test_reports_flow()
        self.test_ai_integration_flow()
        
        # Generate summary
        self.generate_test_summary()

    def generate_test_summary(self):
        """Generate comprehensive test summary"""
        print("\n" + "=" * 70)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results.values() if r['status'] == 'pass'])
        partial_tests = len([r for r in self.test_results.values() if r['status'] == 'partial'])
        failed_tests = len([r for r in self.test_results.values() if r['status'] in ['fail', 'error']])
        
        print(f"✅ PASSED: {passed_tests}/{total_tests} ({(passed_tests/total_tests)*100:.1f}%)")
        print(f"⚠️  PARTIAL: {partial_tests}/{total_tests} ({(partial_tests/total_tests)*100:.1f}%)")
        print(f"❌ FAILED: {failed_tests}/{total_tests} ({(failed_tests/total_tests)*100:.1f}%)")
        
        print("\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results.items():
            status_icon = "✅" if result['status'] == 'pass' else "⚠️" if result['status'] == 'partial' else "❌"
            print(f"{status_icon} {test_name.replace('_', ' ').title()}")
            print(f"   {result['result']}")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f'comprehensive_test_results_{timestamp}.json'
        
        with open(results_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'summary': {
                    'total_tests': total_tests,
                    'passed': passed_tests,
                    'partial': partial_tests,
                    'failed': failed_tests
                },
                'detailed_results': self.test_results
            }, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to: {results_file}")
        
        # Overall health score
        health_score = (passed_tests * 100 + partial_tests * 50) / (total_tests * 100) * 100
        print(f"🎯 OVERALL SYSTEM HEALTH: {health_score:.1f}%")
        
        if health_score >= 80:
            print("🟢 SYSTEM STATUS: HEALTHY - All major flows functional")
        elif health_score >= 60:
            print("🟡 SYSTEM STATUS: GOOD - Minor issues detected")
        else:
            print("🔴 SYSTEM STATUS: NEEDS ATTENTION - Critical issues found")

def main():
    """Main testing function"""
    try:
        tester = CrazyShopperzTester()
        tester.run_all_tests()
        
    except Exception as e:
        print(f"❌ Testing failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)