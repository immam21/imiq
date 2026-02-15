#!/usr/bin/env python3
"""
Advanced Sheet Testing for CrazyShopperz
Tests remaining sheets: OrderStages, AI_Prompts, NewOrders, ChatAssignments, Settings
Uses ONLY Google Sheets API
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

class AdvancedSheetTester:
    """Base class for advanced sheet testing"""
    
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

    def get_sheet_data(self, sheet_name):
        """Get data from specific sheet"""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            all_values = worksheet.get_all_values()
            
            if len(all_values) > 1:
                headers = all_values[0]
                data_rows = all_values[1:]
                return pd.DataFrame(data_rows, columns=headers).dropna(how='all')
            elif len(all_values) == 1:
                # Only headers row
                return pd.DataFrame(columns=all_values[0])
            return pd.DataFrame()
        except Exception as e:
            print(f"❌ Error getting {sheet_name} data: {e}")
            return pd.DataFrame()

class OrderStagesTester(AdvancedSheetTester):
    """Test OrderStages sheet functionality"""
    
    def test_order_stages_structure(self):
        """Test order stages data structure"""
        print("🔄 Testing OrderStages Structure")
        
        df = self.get_sheet_data('OrderStages')
        
        if df.empty:
            print("   ⚠️ OrderStages sheet is empty or has headers only")
            # Check if we have headers
            try:
                worksheet = self.spreadsheet.worksheet('OrderStages')
                all_values = worksheet.get_all_values()
                if len(all_values) >= 1:
                    headers = all_values[0]
                    print(f"   📋 Headers found: {headers}")
                    print(f"   📊 Structure ready for order stage tracking")
                    return True
                else:
                    print("   ❌ No headers found")
                    return False
            except Exception as e:
                print(f"   ❌ Error reading headers: {e}")
                return False
        else:
            print(f"   ✅ OrderStages data found: {len(df)} records")
            print(f"   📋 Columns: {list(df.columns)}")
            return True

    def test_stage_workflow(self):
        """Test order stage workflow"""
        print("\n🔄 Testing Order Stage Workflow")
        
        df = self.get_sheet_data('OrderStages')
        
        # Even if empty, we can test the workflow structure
        try:
            worksheet = self.spreadsheet.worksheet('OrderStages')
            all_values = worksheet.get_all_values()
            
            if len(all_values) >= 1:
                headers = all_values[0]
                
                # Look for stage-related columns
                stage_indicators = ['stage', 'status', 'confirmation', 'phone', 'customer']
                found_indicators = [col for col in headers if any(indicator in col.lower() for indicator in stage_indicators)]
                
                if found_indicators:
                    print(f"   ✅ Stage workflow structure present")
                    print(f"   🔄 Stage tracking fields: {found_indicators}")
                    return True
                else:
                    print("   ⚠️ No clear stage workflow structure")
                    return False
            else:
                print("   ❌ No structure found")
                return False
                
        except Exception as e:
            print(f"   ❌ Workflow test failed: {e}")
            return False

    def run_all_tests(self):
        """Run all OrderStages tests"""
        print("=" * 50)
        print("📋 ORDER STAGES TESTING")
        print("=" * 50)
        
        results = []
        results.append(self.test_order_stages_structure())
        results.append(self.test_stage_workflow())
        
        passed = sum(results)
        total = len(results)
        
        print(f"\n📋 OrderStages Tests: {passed}/{total} passed")
        return passed == total

class AIPromptsTester(AdvancedSheetTester):
    """Test AI_Prompts sheet functionality"""
    
    def test_ai_prompt_configuration(self):
        """Test AI prompt configuration"""
        print("🔄 Testing AI Prompt Configuration")
        
        df = self.get_sheet_data('AI_Prompts')
        
        if df.empty:
            print("   ❌ No AI prompts configured")
            return False
            
        # Test required fields
        required_fields = ['ai_provider', 'model', 'prompt_text', 'is_active']
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            print(f"   ❌ Missing required fields: {missing_fields}")
            return False
            
        # Test active prompts
        active_prompts = df[df['is_active'] == 'TRUE'] if 'is_active' in df.columns else df
        
        print(f"   ✅ AI prompt configuration valid")
        print(f"   🤖 {len(df)} total prompts configured")
        print(f"   ✅ {len(active_prompts)} active prompts")
        
        # Show prompt details
        if not active_prompts.empty:
            for _, prompt in active_prompts.iterrows():
                provider = prompt.get('ai_provider', 'Unknown')
                model = prompt.get('model', 'Unknown')
                print(f"   🔧 Active: {provider} - {model}")
        
        return True

    def test_prompt_quality(self):
        """Test prompt quality and completeness"""
        print("\n🔄 Testing Prompt Quality")
        
        df = self.get_sheet_data('AI_Prompts')
        
        if df.empty:
            print("   ❌ No prompts to analyze")
            return False
            
        # Test prompt completeness
        prompts_with_text = df[df['prompt_text'].notna() & (df['prompt_text'] != '')]
        
        if not prompts_with_text.empty:
            # Analyze prompt lengths
            prompt_lengths = prompts_with_text['prompt_text'].str.len()
            avg_length = prompt_lengths.mean()
            
            print(f"   ✅ Prompt quality analysis")
            print(f"   📝 {len(prompts_with_text)} prompts with content")
            print(f"   📊 Average prompt length: {avg_length:.0f} characters")
            
            # Check for comprehensive prompts (>1000 chars indicates detailed instructions)
            comprehensive_prompts = prompt_lengths[prompt_lengths > 1000]
            print(f"   🎯 {len(comprehensive_prompts)} comprehensive prompts (>1000 chars)")
            
            return True
        else:
            print("   ❌ No prompts with content found")
            return False

    def test_ai_integration_readiness(self):
        """Test AI integration readiness"""
        print("\n🔄 Testing AI Integration Readiness")
        
        df = self.get_sheet_data('AI_Prompts')
        
        if df.empty:
            print("   ❌ AI integration not ready - no prompts")
            return False
            
        # Test for production-ready prompts
        active_prompts = df[df['is_active'] == 'TRUE'] if 'is_active' in df.columns else df
        
        if not active_prompts.empty:
            # Check for different AI providers
            providers = active_prompts['ai_provider'].unique() if 'ai_provider' in active_prompts.columns else []
            models = active_prompts['model'].unique() if 'model' in active_prompts.columns else []
            
            print(f"   ✅ AI integration ready")
            print(f"   🏭 {len(providers)} AI providers configured: {list(providers)}")
            print(f"   🧠 {len(models)} models available: {list(models)}")
            
            # Test for fallback configurations
            if len(providers) > 1:
                print("   🔄 Multiple providers - fallback capability available")
            
            return True
        else:
            print("   ⚠️ AI integration limited - no active prompts")
            return False

    def run_all_tests(self):
        """Run all AI_Prompts tests"""
        print("=" * 50)
        print("🤖 AI PROMPTS TESTING")
        print("=" * 50)
        
        results = []
        results.append(self.test_ai_prompt_configuration())
        results.append(self.test_prompt_quality())
        results.append(self.test_ai_integration_readiness())
        
        passed = sum(results)
        total = len(results)
        
        print(f"\n📋 AI Prompts Tests: {passed}/{total} passed")
        return passed == total

class NewOrdersTester(AdvancedSheetTester):
    """Test NewOrders sheet functionality"""
    
    def test_order_management(self):
        """Test order management functionality"""
        print("🔄 Testing Order Management")
        
        df = self.get_sheet_data('NewOrders')
        
        if df.empty:
            print("   ❌ No orders found")
            return False
            
        # Test required fields
        required_fields = ['order_id', 'phone', 'customer_name', 'product', 'total', 'status']
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            print(f"   ❌ Missing required fields: {missing_fields}")
            return False
            
        # Test order data quality
        orders_with_id = df[df['order_id'].notna()]
        orders_with_customer = df[df['customer_name'].notna()]
        orders_with_amount = df[df['total'].notna()]
        
        print(f"   ✅ Order management structure valid")
        print(f"   📦 {len(orders_with_id)} orders with unique IDs")
        print(f"   👤 {len(orders_with_customer)} orders with customer info")
        print(f"   💰 {len(orders_with_amount)} orders with amounts")
        
        return True

    def test_order_fulfillment(self):
        """Test order fulfillment tracking"""
        print("\n🔄 Testing Order Fulfillment")
        
        df = self.get_sheet_data('NewOrders')
        
        if df.empty:
            print("   ❌ No orders for fulfillment testing")
            return False
            
        # Test fulfillment fields
        fulfillment_fields = ['tracking_id', 'courier_name', 'status']
        fulfillment_data = []
        
        for field in fulfillment_fields:
            if field in df.columns:
                field_data = df[df[field].notna() & (df[field] != '')]
                fulfillment_data.append((field, len(field_data)))
        
        if fulfillment_data:
            print(f"   ✅ Order fulfillment tracking available")
            for field, count in fulfillment_data:
                print(f"   📋 {count} orders with {field}")
            
            # Test status distribution
            if 'status' in df.columns:
                status_counts = df['status'].value_counts()
                print(f"   📊 Order status distribution:")
                for status, count in status_counts.items():
                    print(f"       {status}: {count} orders")
            
            return True
        else:
            print("   ⚠️ Limited fulfillment tracking")
            return False

    def test_payment_tracking(self):
        """Test payment tracking"""
        print("\n🔄 Testing Payment Tracking")
        
        df = self.get_sheet_data('NewOrders')
        
        if df.empty:
            print("   ❌ No orders for payment testing")
            return False
            
        # Test payment fields
        payment_fields = ['payment_method', 'advance_paid', 'balance_to_pay', 'total']
        payment_data = []
        
        for field in payment_fields:
            if field in df.columns:
                field_data = df[df[field].notna() & (df[field] != '')]
                payment_data.append((field, len(field_data)))
        
        if payment_data:
            print(f"   ✅ Payment tracking available")
            for field, count in payment_data:
                print(f"   💳 {count} orders with {field}")
            
            # Calculate payment analytics
            if 'payment_method' in df.columns:
                payment_methods = df['payment_method'].value_counts()
                print(f"   📊 Payment methods:")
                for method, count in payment_methods.items():
                    print(f"       {method}: {count} orders")
            
            return True
        else:
            print("   ⚠️ Limited payment tracking")
            return False

    def run_all_tests(self):
        """Run all NewOrders tests"""
        print("=" * 50)
        print("📦 NEW ORDERS TESTING")
        print("=" * 50)
        
        results = []
        results.append(self.test_order_management())
        results.append(self.test_order_fulfillment())
        results.append(self.test_payment_tracking())
        
        passed = sum(results)
        total = len(results)
        
        print(f"\n📋 NewOrders Tests: {passed}/{total} passed")
        return passed == total

class ChatAssignmentsTester(AdvancedSheetTester):
    """Test ChatAssignments sheet functionality"""
    
    def test_chat_assignment_system(self):
        """Test chat assignment system"""
        print("🔄 Testing Chat Assignment System")
        
        df = self.get_sheet_data('ChatAssignments')
        
        if df.empty:
            print("   ⚠️ No chat assignments found")
            return False
            
        # Test required fields
        required_fields = ['phone', 'assigned_user']
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            print(f"   ❌ Missing required fields: {missing_fields}")
            return False
            
        # Test assignment data
        assignments_with_phone = df[df['phone'].notna()]
        assignments_with_user = df[df['assigned_user'].notna()]
        
        print(f"   ✅ Chat assignment system active")
        print(f"   📱 {len(assignments_with_phone)} phone numbers assigned")
        print(f"   👤 {len(assignments_with_user)} user assignments")
        
        # Show assignment distribution
        if 'assigned_user' in df.columns:
            user_assignments = df['assigned_user'].value_counts()
            print(f"   📊 Assignment distribution:")
            for user, count in user_assignments.items():
                if user and str(user).strip():
                    print(f"       {user}: {count} assignments")
        
        return True

    def test_workload_distribution(self):
        """Test workload distribution"""
        print("\n🔄 Testing Workload Distribution")
        
        df = self.get_sheet_data('ChatAssignments')
        
        if df.empty:
            print("   ❌ No data for workload testing")
            return False
            
        # Analyze workload distribution
        if 'assigned_user' in df.columns:
            user_counts = df['assigned_user'].value_counts()
            
            if len(user_counts) > 0:
                total_assignments = len(df)
                avg_assignments = total_assignments / len(user_counts)
                
                print(f"   ✅ Workload distribution analysis")
                print(f"   👥 {len(user_counts)} active users")
                print(f"   📊 {avg_assignments:.1f} average assignments per user")
                
                # Check for balanced distribution
                max_assignments = user_counts.max()
                min_assignments = user_counts.min()
                balance_ratio = min_assignments / max_assignments if max_assignments > 0 else 0
                
                if balance_ratio >= 0.5:
                    print(f"   ✅ Well-balanced workload (ratio: {balance_ratio:.2f})")
                else:
                    print(f"   ⚠️ Unbalanced workload detected (ratio: {balance_ratio:.2f})")
                
                return True
            else:
                print("   ❌ No user assignments found")
                return False
        else:
            print("   ❌ No assignment data available")
            return False

    def test_assignment_status(self):
        """Test assignment status tracking"""
        print("\n🔄 Testing Assignment Status")
        
        df = self.get_sheet_data('ChatAssignments')
        
        if df.empty:
            print("   ❌ No assignments for status testing")
            return False
            
        # Test status tracking
        if 'status' in df.columns:
            status_data = df[df['status'].notna()]
            
            if not status_data.empty:
                status_counts = status_data['status'].value_counts()
                
                print(f"   ✅ Assignment status tracking")
                print(f"   📋 {len(status_data)} assignments with status")
                print(f"   📊 Status distribution:")
                for status, count in status_counts.items():
                    if status and str(status).strip():
                        print(f"       {status}: {count} assignments")
                
                return True
            else:
                print("   ⚠️ No status data available")
                return False
        else:
            print("   ⚠️ Status tracking not configured")
            return False

    def run_all_tests(self):
        """Run all ChatAssignments tests"""
        print("=" * 50)
        print("👥 CHAT ASSIGNMENTS TESTING")
        print("=" * 50)
        
        results = []
        results.append(self.test_chat_assignment_system())
        results.append(self.test_workload_distribution())
        results.append(self.test_assignment_status())
        
        passed = sum(results)
        total = len(results)
        
        print(f"\n📋 ChatAssignments Tests: {passed}/{total} passed")
        return passed == total

class SettingsTester(AdvancedSheetTester):
    """Test Settings sheet functionality"""
    
    def test_system_configuration(self):
        """Test system configuration"""
        print("🔄 Testing System Configuration")
        
        df = self.get_sheet_data('Settings')
        
        if df.empty:
            print("   ❌ No system settings found")
            return False
            
        # Test required fields
        required_fields = ['setting_key', 'setting_value']
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            print(f"   ❌ Missing required fields: {missing_fields}")
            return False
            
        # Test configuration data
        settings_with_key = df[df['setting_key'].notna()]
        settings_with_value = df[df['setting_value'].notna()]
        
        print(f"   ✅ System configuration available")
        print(f"   🔧 {len(settings_with_key)} configuration keys")
        print(f"   📊 {len(settings_with_value)} configured values")
        
        # Show some key settings
        if not df.empty:
            print(f"   📋 Configuration overview:")
            for _, setting in df.head(5).iterrows():
                key = setting.get('setting_key', 'Unknown')
                value = setting.get('setting_value', 'Unknown')
                print(f"       {key}: {value}")
        
        return True

    def test_configuration_categories(self):
        """Test configuration categories"""
        print("\n🔄 Testing Configuration Categories")
        
        df = self.get_sheet_data('Settings')
        
        if df.empty:
            print("   ❌ No settings for category testing")
            return False
            
        # Test categories
        if 'category' in df.columns:
            categories = df['category'].dropna().value_counts()
            
            if len(categories) > 0:
                print(f"   ✅ Configuration categories available")
                print(f"   📂 {len(categories)} different categories")
                print(f"   📊 Category distribution:")
                for category, count in categories.items():
                    print(f"       {category}: {count} settings")
                
                return True
            else:
                print("   ⚠️ No category data available")
                return False
        else:
            print("   ⚠️ Categories not configured")
            return False

    def test_configuration_history(self):
        """Test configuration change history"""
        print("\n🔄 Testing Configuration History")
        
        df = self.get_sheet_data('Settings')
        
        if df.empty:
            print("   ❌ No settings for history testing")
            return False
            
        # Test history tracking
        history_fields = ['updated_at', 'updated_by']
        history_data = []
        
        for field in history_fields:
            if field in df.columns:
                field_data = df[df[field].notna() & (df[field] != '')]
                history_data.append((field, len(field_data)))
        
        if history_data:
            print(f"   ✅ Configuration history tracking")
            for field, count in history_data:
                print(f"   📅 {count} settings with {field}")
            
            # Recent updates
            if 'updated_at' in df.columns:
                recent_updates = df[df['updated_at'].notna()]
                if not recent_updates.empty:
                    print(f"   🕒 {len(recent_updates)} settings with update timestamps")
            
            return True
        else:
            print("   ⚠️ No change history tracking")
            return False

    def run_all_tests(self):
        """Run all Settings tests"""
        print("=" * 50)
        print("⚙️ SETTINGS TESTING")
        print("=" * 50)
        
        results = []
        results.append(self.test_system_configuration())
        results.append(self.test_configuration_categories())
        results.append(self.test_configuration_history())
        
        passed = sum(results)
        total = len(results)
        
        print(f"\n📋 Settings Tests: {passed}/{total} passed")
        return passed == total

def main():
    """Run all advanced sheet tests"""
    print("=" * 70)
    print("🚀 ADVANCED SHEET TESTING - GOOGLE SHEETS ONLY")
    print("=" * 70)
    
    all_results = []
    testers = [
        ("OrderStages", OrderStagesTester),
        ("AI_Prompts", AIPromptsTester),
        ("NewOrders", NewOrdersTester),
        ("ChatAssignments", ChatAssignmentsTester),
        ("Settings", SettingsTester)
    ]
    
    for sheet_name, tester_class in testers:
        try:
            tester = tester_class()
            result = tester.run_all_tests()
            all_results.append((sheet_name, result))
            print("\n" + "="*70)
        except Exception as e:
            print(f"❌ {sheet_name} testing failed: {e}")
            all_results.append((sheet_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("📊 ADVANCED SHEET TESTING SUMMARY")
    print("="*70)
    
    passed_sheets = sum(1 for _, result in all_results if result)
    total_sheets = len(all_results)
    
    print(f"✅ PASSED SHEETS: {passed_sheets}/{total_sheets}")
    
    for sheet_name, result in all_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {sheet_name} Sheet Testing")
    
    return passed_sheets == total_sheets

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)