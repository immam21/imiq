#!/usr/bin/env python3
"""
USERS SHEET TESTING SCRIPT
Tests all flows related to Users sheet: Authentication, Registration, User Management
Based on actual sheet structure: user_id, email, password_hash, plain_password, role, name, created_at, is_active
"""

import os
import sys
import time
from datetime import datetime

# Setup
sys.path.append('.')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService
from imiq.auth import AuthService

class UsersSheetTester:
    def __init__(self):
        self.storage = None
        self.auth_service = None
        self.initialize_services()
    
    def initialize_services(self):
        """Initialize services"""
        try:
            base_storage = get_storage_instance()
            settings_service = SettingsService(base_storage)
            self.storage = get_storage_instance(settings_service)
            self.auth_service = AuthService(self.storage)
            print("✅ Services initialized successfully")
        except Exception as e:
            print(f"❌ Service initialization failed: {e}")
            raise
    
    def test_users_data_access(self):
        """Test 1: Basic Users sheet data access"""
        print("\n📋 TEST 1: USERS DATA ACCESS")
        print("-" * 40)
        
        try:
            users_df = self.storage.read_sheet("Users")
            
            print(f"✅ Users sheet accessed successfully")
            print(f"   📊 Total users: {len(users_df)}")
            print(f"   📋 Columns: {list(users_df.columns)}")
            
            if not users_df.empty:
                # Analyze user roles
                if 'role' in users_df.columns:
                    role_dist = users_df['role'].value_counts()
                    print(f"   👤 Role distribution: {dict(role_dist)}")
                
                # Check active users
                if 'is_active' in users_df.columns:
                    active_users = users_df[users_df['is_active'] == 'true']
                    print(f"   ✅ Active users: {len(active_users)}")
                
                # Show sample user data (without passwords)
                print(f"   📝 Sample users:")
                for idx, user in users_df.head(2).iterrows():
                    user_id = user.get('user_id', 'N/A')
                    role = user.get('role', 'N/A')
                    name = user.get('name', 'N/A')
                    print(f"      - {user_id} ({role}): {name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Users data access failed: {e}")
            return False
    
    def test_admin_login(self):
        """Test 2: Admin login flow"""
        print("\n🔐 TEST 2: ADMIN LOGIN")
        print("-" * 40)
        
        try:
            # Test with known admin credentials from the data
            result = self.auth_service.authenticate('imam21', 'Iqrit@2024')
            
            if result.get('success'):
                user = result['user']
                print("✅ Admin login successful")
                print(f"   👤 User: {user.get('name', 'N/A')}")
                print(f"   📧 Email: {user.get('email', 'N/A')}")
                print(f"   🎭 Role: {user.get('role', 'N/A')}")
                return True
            else:
                print(f"❌ Admin login failed: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Admin login test error: {e}")
            return False
    
    def test_user_login(self):
        """Test 3: Regular user login flow"""
        print("\n👤 TEST 3: USER LOGIN")
        print("-" * 40)
        
        try:
            # Test with known user credentials from the data
            result = self.auth_service.authenticate('Sowmiya01', 'Sow0112')
            
            if result.get('success'):
                user = result['user']
                print("✅ User login successful")
                print(f"   👤 User: {user.get('name', 'N/A')}")
                print(f"   📧 Email: {user.get('email', 'N/A')}")
                print(f"   🎭 Role: {user.get('role', 'N/A')}")
                return True
            else:
                print(f"❌ User login failed: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ User login test error: {e}")
            return False
    
    def test_registration_flow(self):
        """Test 4: New user registration"""
        print("\n📝 TEST 4: USER REGISTRATION")
        print("-" * 40)
        
        try:
            # Create unique test user
            timestamp = int(time.time())
            test_user_data = {
                'user_id': f'testuser_{timestamp}',
                'password': 'TestPass123',
                'name': f'Test User {timestamp}',
                'email': f'test_{timestamp}@example.com'
            }
            
            result = self.auth_service.create_account(
                test_user_data['user_id'],
                test_user_data['password'],
                test_user_data['name'],
                test_user_data['email']
            )
            
            if result.get('success'):
                print("✅ User registration successful")
                print(f"   👤 User ID: {test_user_data['user_id']}")
                print(f"   📧 Email: {test_user_data['email']}")
                print(f"   📅 Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                # Test immediate login with new user
                login_result = self.auth_service.authenticate(
                    test_user_data['user_id'],
                    test_user_data['password']
                )
                
                if login_result.get('success'):
                    print("   ✅ New user login verification successful")
                else:
                    print("   ⚠️  New user login verification failed")
                
                return True
            else:
                print(f"❌ User registration failed: {result.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Registration test error: {e}")
            return False
    
    def test_user_lookup(self):
        """Test 5: User lookup and search functionality"""
        print("\n🔍 TEST 5: USER LOOKUP")
        print("-" * 40)
        
        try:
            users_df = self.storage.read_sheet("Users")
            
            if users_df.empty:
                print("❌ No users to search")
                return False
            
            # Test lookup by user_id
            test_user_id = 'imam21'
            user_matches = users_df[users_df['user_id'] == test_user_id]
            
            if not user_matches.empty:
                user = user_matches.iloc[0]
                print(f"✅ User lookup by ID successful")
                print(f"   🔍 Searched for: {test_user_id}")
                print(f"   👤 Found: {user.get('name', 'N/A')} ({user.get('role', 'N/A')})")
            else:
                print(f"❌ User lookup failed for ID: {test_user_id}")
                return False
            
            # Test lookup by role
            admin_users = users_df[users_df['role'] == 'admin']
            user_users = users_df[users_df['role'] == 'user']
            
            print(f"   📊 Lookup by role:")
            print(f"      Admins: {len(admin_users)}")
            print(f"      Users: {len(user_users)}")
            
            # Test lookup by email domain
            gmail_users = users_df[users_df['email'].str.contains('@gmail.com', na=False)]
            print(f"      Gmail users: {len(gmail_users)}")
            
            return True
            
        except Exception as e:
            print(f"❌ User lookup test error: {e}")
            return False
    
    def test_user_analytics(self):
        """Test 6: User analytics and reporting"""
        print("\n📊 TEST 6: USER ANALYTICS")
        print("-" * 40)
        
        try:
            users_df = self.storage.read_sheet("Users")
            
            if users_df.empty:
                print("❌ No data for analytics")
                return False
            
            # Basic analytics
            analytics = {
                'total_users': len(users_df),
                'active_users': len(users_df[users_df['is_active'] == 'true']) if 'is_active' in users_df.columns else 'N/A',
                'role_distribution': users_df['role'].value_counts().to_dict() if 'role' in users_df.columns else {},
                'email_domains': users_df['email'].str.split('@').str[1].value_counts().to_dict() if 'email' in users_df.columns else {}
            }
            
            print("✅ User analytics generated:")
            print(f"   👥 Total users: {analytics['total_users']}")
            print(f"   ✅ Active users: {analytics['active_users']}")
            print(f"   🎭 Roles: {analytics['role_distribution']}")
            print(f"   📧 Email domains: {analytics['email_domains']}")
            
            # Time-based analytics if created_at is available
            if 'created_at' in users_df.columns:
                try:
                    # Convert to datetime and analyze
                    users_df['created_at_parsed'] = pd.to_datetime(users_df['created_at'])
                    recent_users = users_df[users_df['created_at_parsed'] >= pd.Timestamp.now() - pd.Timedelta(days=30)]
                    print(f"   📅 Recent registrations (30 days): {len(recent_users)}")
                except:
                    print("   📅 Recent registrations: Unable to parse dates")
            
            return True
            
        except Exception as e:
            print(f"❌ User analytics error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all Users sheet tests"""
        print("🔍 USERS SHEET COMPREHENSIVE TESTING")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        tests = [
            ('Data Access', self.test_users_data_access),
            ('Admin Login', self.test_admin_login),
            ('User Login', self.test_user_login),
            ('Registration', self.test_registration_flow),
            ('User Lookup', self.test_user_lookup),
            ('User Analytics', self.test_user_analytics)
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
        print("📋 USERS SHEET TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {test_name:<20} {status}")
        
        print(f"\n🎯 Results: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL USERS SHEET TESTS PASSED!")
        else:
            print("⚠️  Some tests need attention")
        
        return passed_tests == total_tests

def main():
    """Main execution"""
    try:
        tester = UsersSheetTester()
        success = tester.run_all_tests()
        return success
    except Exception as e:
        print(f"💥 Critical error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'🚀 Users sheet testing complete!' if success else '❌ Tests failed'}")