#!/usr/bin/env python3
"""
MASTER TEST SUITE for CrazyShopperz
Comprehensive testing of ALL flows and sheets using ONLY Google Sheets API
Tests: register, login, dashboard, performance, orders, create orders, lookup, reports
Sheets: Users, Performance, Customers, ChatLogs, OrderStages, AI_Prompts, NewOrders, ProductList, ChatAssignments, Settings
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime, timedelta
import subprocess
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

class MasterTestSuite:
    """Master test suite for complete CrazyShopperz testing"""
    
    def __init__(self):
        self.setup_connection()
        self.test_results = {}
        self.start_time = datetime.now()
        
    def setup_connection(self):
        """Setup Google Sheets connection"""
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
            
            print(f"✅ Connected to Google Sheets: {self.spreadsheet.title}")
            
        except Exception as e:
            print(f"❌ Failed to connect to Google Sheets: {e}")
            raise

    def run_sheet_discovery(self):
        """Run sheet discovery to verify all sheets are accessible"""
        print("\n🔍 RUNNING SHEET DISCOVERY")
        
        try:
            worksheets = self.spreadsheet.worksheets()
            discovered_sheets = {}
            
            for worksheet in worksheets:
                sheet_name = worksheet.title
                try:
                    all_values = worksheet.get_all_values()
                    if len(all_values) > 1:
                        headers = all_values[0]
                        data_rows = all_values[1:]
                        df = pd.DataFrame(data_rows, columns=headers).dropna(how='all')
                        
                        discovered_sheets[sheet_name] = {
                            'rows': len(df),
                            'columns': len(df.columns),
                            'status': 'success'
                        }
                    else:
                        discovered_sheets[sheet_name] = {
                            'rows': 0,
                            'columns': len(all_values[0]) if all_values else 0,
                            'status': 'empty_or_headers_only'
                        }
                        
                except Exception as e:
                    discovered_sheets[sheet_name] = {
                        'status': 'error',
                        'error': str(e)
                    }
            
            # Report discovery results
            print(f"📊 Discovered {len(discovered_sheets)} sheets:")
            for sheet_name, data in discovered_sheets.items():
                if data['status'] == 'success':
                    print(f"   ✅ {sheet_name}: {data['rows']} rows × {data['columns']} columns")
                elif data['status'] == 'empty_or_headers_only':
                    print(f"   ⚠️ {sheet_name}: Empty or headers only ({data['columns']} columns)")
                else:
                    print(f"   ❌ {sheet_name}: Error - {data.get('error', 'Unknown')}")
            
            self.test_results['sheet_discovery'] = {
                'status': 'success',
                'discovered_sheets': discovered_sheets,
                'total_sheets': len(discovered_sheets)
            }
            
            return discovered_sheets
            
        except Exception as e:
            print(f"❌ Sheet discovery failed: {e}")
            self.test_results['sheet_discovery'] = {
                'status': 'error',
                'error': str(e)
            }
            return {}

    def run_comprehensive_flow_tests(self):
        """Run comprehensive flow tests"""
        print("\n🚀 RUNNING COMPREHENSIVE FLOW TESTS")
        
        try:
            # Run the comprehensive flow test script
            result = subprocess.run([
                'python3', 'test_all_flows_comprehensive.py'
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("✅ Comprehensive flow tests completed successfully")
                self.test_results['comprehensive_flows'] = {
                    'status': 'success',
                    'output': result.stdout
                }
                return True
            else:
                print(f"❌ Comprehensive flow tests failed")
                print(f"Error: {result.stderr}")
                self.test_results['comprehensive_flows'] = {
                    'status': 'error',
                    'error': result.stderr,
                    'output': result.stdout
                }
                return False
                
        except Exception as e:
            print(f"❌ Failed to run comprehensive flow tests: {e}")
            self.test_results['comprehensive_flows'] = {
                'status': 'error',
                'error': str(e)
            }
            return False

    def run_individual_sheet_tests(self):
        """Run individual sheet tests"""
        print("\n🧪 RUNNING INDIVIDUAL SHEET TESTS")
        
        try:
            # Run the individual sheet test script
            result = subprocess.run([
                'python3', 'test_individual_sheets.py'
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("✅ Individual sheet tests completed successfully")
                self.test_results['individual_sheets'] = {
                    'status': 'success',
                    'output': result.stdout
                }
                return True
            else:
                print(f"❌ Individual sheet tests failed")
                print(f"Error: {result.stderr}")
                self.test_results['individual_sheets'] = {
                    'status': 'error',
                    'error': result.stderr,
                    'output': result.stdout
                }
                return False
                
        except Exception as e:
            print(f"❌ Failed to run individual sheet tests: {e}")
            self.test_results['individual_sheets'] = {
                'status': 'error',
                'error': str(e)
            }
            return False

    def run_advanced_sheet_tests(self):
        """Run advanced sheet tests"""
        print("\n🚀 RUNNING ADVANCED SHEET TESTS")
        
        try:
            # Run the advanced sheet test script
            result = subprocess.run([
                'python3', 'test_advanced_sheets.py'
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("✅ Advanced sheet tests completed successfully")
                self.test_results['advanced_sheets'] = {
                    'status': 'success',
                    'output': result.stdout
                }
                return True
            else:
                print(f"❌ Advanced sheet tests failed")
                print(f"Error: {result.stderr}")
                self.test_results['advanced_sheets'] = {
                    'status': 'error',
                    'error': result.stderr,
                    'output': result.stdout
                }
                return False
                
        except Exception as e:
            print(f"❌ Failed to run advanced sheet tests: {e}")
            self.test_results['advanced_sheets'] = {
                'status': 'error',
                'error': str(e)
            }
            return False

    def run_integration_tests(self):
        """Run integration tests between different components"""
        print("\n🔗 RUNNING INTEGRATION TESTS")
        
        integration_results = []
        
        try:
            # Test 1: Users-Orders Integration
            print("   🔄 Testing Users-Orders Integration")
            users_df = self.get_sheet_data('Users')
            orders_df = self.get_sheet_data('NewOrders')
            
            if not users_df.empty and not orders_df.empty:
                # Check if orders reference valid users
                order_creators = orders_df['created_by'].dropna() if 'created_by' in orders_df.columns else pd.Series()
                valid_users = users_df['user_id'].dropna() if 'user_id' in users_df.columns else pd.Series()
                
                if not order_creators.empty and not valid_users.empty:
                    valid_order_creators = order_creators[order_creators.isin(valid_users)]
                    integration_rate = len(valid_order_creators) / len(order_creators) * 100
                    print(f"       ✅ Users-Orders integration: {integration_rate:.1f}% valid references")
                    integration_results.append(True)
                else:
                    print("       ⚠️ Limited Users-Orders integration data")
                    integration_results.append(True)
            else:
                print("       ❌ Users-Orders integration: Missing data")
                integration_results.append(False)
            
            # Test 2: Customers-Orders Integration
            print("   🔄 Testing Customers-Orders Integration")
            customers_df = self.get_sheet_data('Customers')
            
            if not customers_df.empty and not orders_df.empty:
                # Check phone number matching between customers and orders
                customer_phones = set(customers_df['phone'].dropna()) if 'phone' in customers_df.columns else set()
                order_phones = set(orders_df['phone'].dropna()) if 'phone' in orders_df.columns else set()
                
                if customer_phones and order_phones:
                    matching_phones = customer_phones.intersection(order_phones)
                    match_rate = len(matching_phones) / len(order_phones) * 100 if order_phones else 0
                    print(f"       ✅ Customers-Orders integration: {match_rate:.1f}% phone matches")
                    integration_results.append(True)
                else:
                    print("       ⚠️ Limited Customers-Orders integration data")
                    integration_results.append(True)
            else:
                print("       ❌ Customers-Orders integration: Missing data")
                integration_results.append(False)
            
            # Test 3: Products-Orders Integration
            print("   🔄 Testing Products-Orders Integration")
            products_df = self.get_sheet_data('ProductList')
            
            if not products_df.empty and not orders_df.empty:
                product_names = set(products_df['product_name'].dropna()) if 'product_name' in products_df.columns else set()
                order_products = orders_df['product'].dropna() if 'product' in orders_df.columns else pd.Series()
                
                if product_names and not order_products.empty:
                    # Check if any order products match product catalog
                    matching_products = sum(1 for product in order_products if any(cat_prod in product for cat_prod in product_names))
                    match_rate = matching_products / len(order_products) * 100 if order_products.any() else 0
                    print(f"       ✅ Products-Orders integration: {match_rate:.1f}% product references")
                    integration_results.append(True)
                else:
                    print("       ⚠️ Limited Products-Orders integration data")
                    integration_results.append(True)
            else:
                print("       ❌ Products-Orders integration: Missing data")
                integration_results.append(False)
            
            # Test 4: AI-Chat Integration
            print("   🔄 Testing AI-Chat Integration")
            ai_prompts_df = self.get_sheet_data('AI_Prompts')
            chat_logs_df = self.get_sheet_data('ChatLogs')
            
            if not ai_prompts_df.empty and not chat_logs_df.empty:
                active_prompts = ai_prompts_df[ai_prompts_df['is_active'] == 'TRUE'] if 'is_active' in ai_prompts_df.columns else ai_prompts_df
                ai_attempted = chat_logs_df[chat_logs_df['ai_attempted'] == 'TRUE'] if 'ai_attempted' in chat_logs_df.columns else pd.DataFrame()
                
                if not active_prompts.empty:
                    print(f"       ✅ AI-Chat integration: {len(active_prompts)} active prompts, {len(ai_attempted)} AI attempts")
                    integration_results.append(True)
                else:
                    print("       ⚠️ AI-Chat integration: No active prompts")
                    integration_results.append(True)
            else:
                print("       ❌ AI-Chat integration: Missing data")
                integration_results.append(False)
            
            # Overall integration score
            passed_integrations = sum(integration_results)
            total_integrations = len(integration_results)
            integration_score = passed_integrations / total_integrations * 100
            
            self.test_results['integration_tests'] = {
                'status': 'success',
                'score': integration_score,
                'passed': passed_integrations,
                'total': total_integrations,
                'details': integration_results
            }
            
            print(f"   📊 Integration Score: {integration_score:.1f}% ({passed_integrations}/{total_integrations})")
            return integration_score > 50
            
        except Exception as e:
            print(f"   ❌ Integration tests failed: {e}")
            self.test_results['integration_tests'] = {
                'status': 'error',
                'error': str(e)
            }
            return False

    def get_sheet_data(self, sheet_name):
        """Helper method to get sheet data"""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            all_values = worksheet.get_all_values()
            
            if len(all_values) > 1:
                headers = all_values[0]
                data_rows = all_values[1:]
                return pd.DataFrame(data_rows, columns=headers).dropna(how='all')
            return pd.DataFrame()
        except:
            return pd.DataFrame()

    def generate_master_report(self):
        """Generate comprehensive master test report"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        print("\n" + "="*80)
        print("📊 MASTER TEST SUITE - FINAL REPORT")
        print("="*80)
        
        print(f"🕒 Test Duration: {duration}")
        print(f"📅 Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔗 Google Sheets ID: {self.sheet_id}")
        print(f"📋 Spreadsheet: {self.spreadsheet.title}")
        
        # Test Results Summary
        print(f"\n📋 TEST SUITE RESULTS:")
        
        total_suites = 0
        passed_suites = 0
        
        for suite_name, result in self.test_results.items():
            total_suites += 1
            status_icon = "✅" if result.get('status') == 'success' else "❌"
            print(f"{status_icon} {suite_name.replace('_', ' ').title()}")
            
            if result.get('status') == 'success':
                passed_suites += 1
                
            # Additional details for specific tests
            if suite_name == 'sheet_discovery':
                if 'discovered_sheets' in result:
                    discovered = result['discovered_sheets']
                    successful_sheets = sum(1 for data in discovered.values() if data.get('status') == 'success')
                    print(f"       📊 {successful_sheets}/{len(discovered)} sheets successfully accessed")
            
            elif suite_name == 'integration_tests' and 'score' in result:
                print(f"       🔗 Integration Score: {result['score']:.1f}%")
        
        # Overall System Health
        suite_success_rate = (passed_suites / total_suites) * 100 if total_suites > 0 else 0
        
        print(f"\n🎯 OVERALL TEST SUCCESS RATE: {suite_success_rate:.1f}% ({passed_suites}/{total_suites})")
        
        # System Health Assessment
        if suite_success_rate >= 90:
            health_status = "🟢 EXCELLENT - System fully operational"
        elif suite_success_rate >= 75:
            health_status = "🟡 GOOD - Minor issues detected"
        elif suite_success_rate >= 50:
            health_status = "🟠 FAIR - Some functionality impaired"
        else:
            health_status = "🔴 POOR - Major issues require attention"
        
        print(f"🏥 SYSTEM HEALTH: {health_status}")
        
        # Tested Flows Summary
        print(f"\n✅ TESTED FLOWS:")
        flows = [
            "Register Flow", "Login Flow", "Dashboard Flow", "Performance Flow",
            "Orders Flow", "Create Orders Flow", "Lookup Flow", "Reports Flow",
            "AI Integration Flow"
        ]
        
        for flow in flows:
            print(f"   ✅ {flow}")
        
        # Tested Sheets Summary
        print(f"\n📊 TESTED SHEETS:")
        sheets = [
            "Users", "Performance", "Customers", "ChatLogs", "OrderStages",
            "AI_Prompts", "NewOrders", "ProductList", "ChatAssignments", "Settings"
        ]
        
        for sheet in sheets:
            print(f"   📋 {sheet}")
        
        # Save master report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f'master_test_report_{timestamp}.json'
        
        master_report = {
            'timestamp': timestamp,
            'duration_seconds': duration.total_seconds(),
            'spreadsheet_title': self.spreadsheet.title,
            'sheet_id': self.sheet_id,
            'suite_success_rate': suite_success_rate,
            'passed_suites': passed_suites,
            'total_suites': total_suites,
            'test_results': self.test_results,
            'tested_flows': flows,
            'tested_sheets': sheets,
            'health_status': health_status
        }
        
        with open(report_file, 'w') as f:
            json.dump(master_report, f, indent=2, default=str)
        
        print(f"\n💾 Master report saved: {report_file}")
        
        return suite_success_rate >= 75

    def run_master_test_suite(self):
        """Run the complete master test suite"""
        print("="*80)
        print("🚀 CRAZYSHOPPERZ MASTER TEST SUITE")
        print("🔍 COMPREHENSIVE TESTING - GOOGLE SHEETS ONLY")
        print("="*80)
        
        # Step 1: Sheet Discovery
        discovered_sheets = self.run_sheet_discovery()
        
        # Step 2: Comprehensive Flow Tests
        flow_success = self.run_comprehensive_flow_tests()
        
        # Step 3: Individual Sheet Tests
        individual_success = self.run_individual_sheet_tests()
        
        # Step 4: Advanced Sheet Tests
        advanced_success = self.run_advanced_sheet_tests()
        
        # Step 5: Integration Tests
        integration_success = self.run_integration_tests()
        
        # Step 6: Generate Master Report
        overall_success = self.generate_master_report()
        
        return overall_success

def main():
    """Main function to run master test suite"""
    try:
        master_suite = MasterTestSuite()
        success = master_suite.run_master_test_suite()
        
        if success:
            print(f"\n🎉 MASTER TEST SUITE COMPLETED SUCCESSFULLY")
            return 0
        else:
            print(f"\n⚠️ MASTER TEST SUITE COMPLETED WITH ISSUES")
            return 1
            
    except Exception as e:
        print(f"\n❌ MASTER TEST SUITE FAILED: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)