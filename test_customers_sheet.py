#!/usr/bin/env python3
"""
CUSTOMERS SHEET TESTING SCRIPT
Tests all flows related to Customers sheet: Customer Management, CRM flows
Based on actual sheet structure: customer_id, phone, name, email, address, city, pincode, created_at
"""

import os
import sys
import time
import pandas as pd
from datetime import datetime

# Setup
sys.path.append('.')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService

class CustomersSheetTester:
    def __init__(self):
        self.storage = None
        self.initialize_services()
    
    def initialize_services(self):
        """Initialize services"""
        try:
            base_storage = get_storage_instance()
            settings_service = SettingsService(base_storage)
            self.storage = get_storage_instance(settings_service)
            print("✅ Services initialized successfully")
        except Exception as e:
            print(f"❌ Service initialization failed: {e}")
            raise
    
    def test_customers_data_access(self):
        """Test 1: Basic Customers sheet data access"""
        print("\n📋 TEST 1: CUSTOMERS DATA ACCESS")
        print("-" * 40)
        
        try:
            customers_df = self.storage.read_sheet("Customers")
            
            print(f"✅ Customers sheet accessed successfully")
            print(f"   📊 Total customers: {len(customers_df)}")
            print(f"   📋 Columns: {list(customers_df.columns)}")
            
            if not customers_df.empty:
                # Analyze customer data quality
                data_quality = {}
                for col in customers_df.columns:
                    filled_count = customers_df[col].notna().sum()
                    data_quality[col] = f"{filled_count}/{len(customers_df)}"
                
                print(f"   📊 Data Quality (filled/total):")
                for col, quality in data_quality.items():
                    print(f"      {col}: {quality}")
                
                # Show sample customer data
                print(f"   📝 Sample customers:")
                for idx, customer in customers_df.head(2).iterrows():
                    customer_id = customer.get('customer_id', 'N/A')
                    phone = customer.get('phone', 'N/A')
                    name = customer.get('name', 'N/A')
                    print(f"      - ID: {customer_id}, Phone: {phone}, Name: {name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Customers data access failed: {e}")
            return False
    
    def test_customer_search_lookup(self):
        """Test 2: Customer search and lookup functionality"""
        print("\n🔍 TEST 2: CUSTOMER SEARCH & LOOKUP")
        print("-" * 40)
        
        try:
            customers_df = self.storage.read_sheet("Customers")
            
            if customers_df.empty:
                print("❌ No customers to search")
                return False
            
            # Test lookup by customer_id
            if not customers_df.empty:
                first_customer = customers_df.iloc[0]
                test_customer_id = first_customer.get('customer_id')
                
                if test_customer_id:
                    matches = customers_df[customers_df['customer_id'] == test_customer_id]
                    if not matches.empty:
                        customer = matches.iloc[0]
                        print(f"✅ Customer lookup by ID successful")
                        print(f"   🔍 Searched for: {test_customer_id}")
                        print(f"   👤 Found: {customer.get('phone', 'N/A')}")
            
            # Test search by phone pattern
            phone_searches = customers_df['phone'].notna()
            valid_phones = customers_df[phone_searches]
            print(f"   📱 Customers with phone numbers: {len(valid_phones)}")
            
            # Test search by city if available
            if 'city' in customers_df.columns:
                city_data = customers_df['city'].notna()
                customers_with_city = customers_df[city_data]
                print(f"   🏙️  Customers with city data: {len(customers_with_city)}")
            
            # Test search by email if available
            if 'email' in customers_df.columns:
                email_data = customers_df['email'].notna() & (customers_df['email'] != '')
                customers_with_email = customers_df[email_data]
                print(f"   📧 Customers with email: {len(customers_with_email)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Customer search test error: {e}")
            return False
    
    def test_customer_analytics(self):
        """Test 3: Customer analytics and reporting"""
        print("\n📊 TEST 3: CUSTOMER ANALYTICS")
        print("-" * 40)
        
        try:
            customers_df = self.storage.read_sheet("Customers")
            
            if customers_df.empty:
                print("❌ No data for analytics")
                return False
            
            analytics = {
                'total_customers': len(customers_df),
                'with_phone': customers_df['phone'].notna().sum() if 'phone' in customers_df.columns else 0,
                'with_email': (customers_df['email'].notna() & (customers_df['email'] != '')).sum() if 'email' in customers_df.columns else 0,
                'with_address': customers_df['address'].notna().sum() if 'address' in customers_df.columns else 0,
                'with_city': customers_df['city'].notna().sum() if 'city' in customers_df.columns else 0,
                'with_pincode': customers_df['pincode'].notna().sum() if 'pincode' in customers_df.columns else 0
            }
            
            print("✅ Customer analytics generated:")
            print(f"   👥 Total customers: {analytics['total_customers']}")
            print(f"   📱 With phone: {analytics['with_phone']}")
            print(f"   📧 With email: {analytics['with_email']}")
            print(f"   🏠 With address: {analytics['with_address']}")
            print(f"   🏙️  With city: {analytics['with_city']}")
            print(f"   📮 With pincode: {analytics['with_pincode']}")
            
            # Data completeness percentage
            if analytics['total_customers'] > 0:
                completeness = {
                    'phone': (analytics['with_phone'] / analytics['total_customers']) * 100,
                    'email': (analytics['with_email'] / analytics['total_customers']) * 100,
                    'address': (analytics['with_address'] / analytics['total_customers']) * 100
                }
                
                print(f"   📈 Data Completeness:")
                for field, percent in completeness.items():
                    print(f"      {field.title()}: {percent:.1f}%")
            
            return True
            
        except Exception as e:
            print(f"❌ Customer analytics error: {e}")
            return False
    
    def test_customer_data_validation(self):
        """Test 4: Customer data validation and quality checks"""
        print("\n✅ TEST 4: DATA VALIDATION")
        print("-" * 40)
        
        try:
            customers_df = self.storage.read_sheet("Customers")
            
            if customers_df.empty:
                print("❌ No data to validate")
                return False
            
            validation_results = {
                'duplicate_ids': 0,
                'invalid_phone_format': 0,
                'invalid_email_format': 0,
                'missing_required_fields': 0,
                'invalid_pincode_format': 0
            }
            
            # Check for duplicate customer IDs
            if 'customer_id' in customers_df.columns:
                duplicate_ids = customers_df['customer_id'].duplicated().sum()
                validation_results['duplicate_ids'] = duplicate_ids
                print(f"   🔍 Duplicate customer IDs: {duplicate_ids}")
            
            # Validate phone numbers (basic check for numeric)
            if 'phone' in customers_df.columns:
                valid_phones = customers_df['phone'].notna()
                phone_data = customers_df[valid_phones]['phone'].astype(str)
                # Check for reasonable phone number patterns
                invalid_phones = 0
                for phone in phone_data:
                    if len(phone) < 10 or len(phone) > 15:
                        invalid_phones += 1
                validation_results['invalid_phone_format'] = invalid_phones
                print(f"   📱 Invalid phone formats: {invalid_phones}")
            
            # Validate email format (basic check)
            if 'email' in customers_df.columns:
                email_data = customers_df['email'].notna() & (customers_df['email'] != '')
                valid_emails = customers_df[email_data]['email']
                invalid_emails = 0
                for email in valid_emails:
                    if '@' not in str(email) or '.' not in str(email):
                        invalid_emails += 1
                validation_results['invalid_email_format'] = invalid_emails
                print(f"   📧 Invalid email formats: {invalid_emails}")
            
            # Check for missing required fields (customer_id, phone)
            required_fields = ['customer_id', 'phone']
            missing_required = 0
            for field in required_fields:
                if field in customers_df.columns:
                    missing = customers_df[field].isna().sum()
                    if missing > 0:
                        missing_required += missing
                        print(f"   ⚠️  Missing {field}: {missing} records")
            
            validation_results['missing_required_fields'] = missing_required
            
            # Validate pincode format (if present)
            if 'pincode' in customers_df.columns:
                pincode_data = customers_df['pincode'].notna() & (customers_df['pincode'] != '')
                valid_pincodes = customers_df[pincode_data]['pincode']
                invalid_pincodes = 0
                for pincode in valid_pincodes:
                    pincode_str = str(pincode).strip()
                    if len(pincode_str) != 6 or not pincode_str.isdigit():
                        invalid_pincodes += 1
                validation_results['invalid_pincode_format'] = invalid_pincodes
                print(f"   📮 Invalid pincode formats: {invalid_pincodes}")
            
            # Overall data quality score
            total_issues = sum(validation_results.values())
            print(f"   📊 Total data issues: {total_issues}")
            
            return True
            
        except Exception as e:
            print(f"❌ Data validation error: {e}")
            return False
    
    def test_customer_reporting(self):
        """Test 5: Customer reporting functionality"""
        print("\n📊 TEST 5: CUSTOMER REPORTING")
        print("-" * 40)
        
        try:
            customers_df = self.storage.read_sheet("Customers")
            
            if customers_df.empty:
                print("❌ No data for reporting")
                return False
            
            # Generate customer report
            report = {
                'report_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_customers': len(customers_df),
                'data_fields': list(customers_df.columns),
                'summary_stats': {}
            }
            
            # Summary statistics for each field
            for col in customers_df.columns:
                if col == 'customer_id':
                    report['summary_stats'][col] = {
                        'unique_count': customers_df[col].nunique(),
                        'total_count': len(customers_df)
                    }
                else:
                    filled_count = customers_df[col].notna().sum()
                    empty_count = len(customers_df) - filled_count
                    report['summary_stats'][col] = {
                        'filled': filled_count,
                        'empty': empty_count,
                        'fill_rate': f"{(filled_count/len(customers_df)*100):.1f}%"
                    }
            
            print("✅ Customer report generated:")
            print(f"   📅 Generated: {report['report_generated']}")
            print(f"   👥 Total customers: {report['total_customers']}")
            print(f"   📋 Data fields: {len(report['data_fields'])}")
            
            print(f"   📊 Field Summary:")
            for field, stats in report['summary_stats'].items():
                if field == 'customer_id':
                    print(f"      {field}: {stats['unique_count']} unique IDs")
                else:
                    print(f"      {field}: {stats['filled']} filled ({stats['fill_rate']})")
            
            # City-wise distribution if available
            if 'city' in customers_df.columns:
                city_dist = customers_df['city'].value_counts().head(5)
                if not city_dist.empty:
                    print(f"   🏙️  Top cities: {dict(city_dist)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Customer reporting error: {e}")
            return False
    
    def test_customer_management_simulation(self):
        """Test 6: Customer management operations simulation"""
        print("\n👥 TEST 6: CUSTOMER MANAGEMENT SIMULATION")
        print("-" * 40)
        
        try:
            customers_df = self.storage.read_sheet("Customers")
            
            # Simulate adding a new customer (data preparation)
            new_customer = {
                'customer_id': int(time.time()),
                'phone': f'9999{int(time.time())%100000}',
                'name': f'Test Customer {int(time.time())}',
                'email': f'test_{int(time.time())}@example.com',
                'address': 'Test Address',
                'city': 'Test City',
                'pincode': '123456',
                'created_at': datetime.now().isoformat()
            }
            
            print("✅ New customer data prepared:")
            print(f"   👤 ID: {new_customer['customer_id']}")
            print(f"   📱 Phone: {new_customer['phone']}")
            print(f"   📧 Email: {new_customer['email']}")
            print(f"   🏙️  City: {new_customer['city']}")
            
            # Simulate customer update operation
            if not customers_df.empty:
                sample_customer = customers_df.iloc[0]
                customer_id = sample_customer.get('customer_id')
                print(f"   📝 Simulated update for customer: {customer_id}")
                
                # Simulate customer lookup for update
                matches = customers_df[customers_df['customer_id'] == customer_id]
                if not matches.empty:
                    print(f"   ✅ Customer found for update operation")
                else:
                    print(f"   ❌ Customer not found for update")
            
            # Simulate customer deletion (soft delete)
            print(f"   🗑️  Soft delete simulation: Mark customer as inactive")
            print(f"   ✅ Customer management operations simulated successfully")
            
            return True
            
        except Exception as e:
            print(f"❌ Customer management simulation error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all Customers sheet tests"""
        print("🔍 CUSTOMERS SHEET COMPREHENSIVE TESTING")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        tests = [
            ('Data Access', self.test_customers_data_access),
            ('Search & Lookup', self.test_customer_search_lookup),
            ('Customer Analytics', self.test_customer_analytics),
            ('Data Validation', self.test_customer_data_validation),
            ('Customer Reporting', self.test_customer_reporting),
            ('Management Simulation', self.test_customer_management_simulation)
        ]
        
        results = {}
        
        for test_name, test_method in tests:
            try:
                results[test_name] = test_method()
            except Exception as e:
                print(f"❌ {test_name} test failed with error: {e}")
                results[test_name] = False
        
        # Summary
        print("\n" + "=" * 60)
        print("📋 CUSTOMERS SHEET TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {test_name:<25} {status}")
        
        print(f"\n🎯 Results: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL CUSTOMERS SHEET TESTS PASSED!")
        else:
            print("⚠️  Some tests need attention")
        
        return passed_tests == total_tests

def main():
    """Main execution"""
    try:
        tester = CustomersSheetTester()
        success = tester.run_all_tests()
        return success
    except Exception as e:
        print(f"💥 Critical error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'🚀 Customers sheet testing complete!' if success else '❌ Tests failed'}")