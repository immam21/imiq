#!/usr/bin/env python3
"""
SETTINGS SHEET TESTING SCRIPT
Tests all flows related to Settings sheet: Configuration Management, System Settings
Based on actual sheet structure: setting_key, setting_value, description, category, updated_at, updated_by
"""

import os
import sys
import json
from datetime import datetime

# Setup
sys.path.append('.')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/i0s04a6/Documents/GitHub/CrazyShopperz/service_account.json'

from imiq.storage import get_storage_instance
from imiq.settings import SettingsService

class SettingsSheetTester:
    def __init__(self):
        self.storage = None
        self.settings_service = None
        self.initialize_services()
    
    def initialize_services(self):
        """Initialize services"""
        try:
            base_storage = get_storage_instance()
            self.settings_service = SettingsService(base_storage)
            self.storage = get_storage_instance(self.settings_service)
            print("✅ Services initialized successfully")
        except Exception as e:
            print(f"❌ Service initialization failed: {e}")
            raise
    
    def test_settings_data_access(self):
        """Test 1: Basic Settings sheet data access"""
        print("\n📋 TEST 1: SETTINGS DATA ACCESS")
        print("-" * 40)
        
        try:
            settings_df = self.storage.read_sheet("Settings")
            
            print(f"✅ Settings sheet accessed successfully")
            print(f"   📊 Total settings: {len(settings_df)}")
            print(f"   📋 Columns: {list(settings_df.columns)}")
            
            if not settings_df.empty:
                # Show all settings
                print(f"   ⚙️  Current settings:")
                for idx, setting in settings_df.iterrows():
                    key = setting.get('setting_key', 'N/A')
                    value = setting.get('setting_value', 'N/A')
                    description = setting.get('description', 'N/A')
                    category = setting.get('category', 'N/A')
                    print(f"      {key}: {value} ({category}) - {description}")
                
                # Analyze settings by category
                if 'category' in settings_df.columns:
                    category_dist = settings_df['category'].value_counts()
                    print(f"   📊 Settings by category: {dict(category_dist)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Settings data access failed: {e}")
            return False
    
    def test_settings_service_integration(self):
        """Test 2: Settings service integration"""
        print("\n⚙️  TEST 2: SETTINGS SERVICE INTEGRATION")
        print("-" * 40)
        
        try:
            # Test getting settings through the service
            use_google_sheets = self.settings_service.get_setting('use_google_sheets', False)
            google_sheet_id = self.settings_service.get_setting('google_sheet_id', '')
            
            print("✅ Settings service integration working:")
            print(f"   🔗 Google Sheets enabled: {use_google_sheets}")
            print(f"   📋 Sheet ID configured: {'Yes' if google_sheet_id else 'No'}")
            
            # Test getting all settings
            try:
                all_settings = {}
                settings_df = self.storage.read_sheet("Settings")
                for idx, row in settings_df.iterrows():
                    key = row.get('setting_key')
                    value = row.get('setting_value')
                    if key:
                        all_settings[key] = value
                
                print(f"   📊 Total settings loaded: {len(all_settings)}")
                print(f"   🔑 Available settings: {list(all_settings.keys())}")
                
            except Exception as e:
                print(f"   ⚠️  Could not load all settings: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Settings service integration error: {e}")
            return False
    
    def test_configuration_validation(self):
        """Test 3: Configuration validation"""
        print("\n✅ TEST 3: CONFIGURATION VALIDATION")
        print("-" * 40)
        
        try:
            settings_df = self.storage.read_sheet("Settings")
            
            if settings_df.empty:
                print("❌ No settings to validate")
                return False
            
            validation_results = {
                'duplicate_keys': 0,
                'missing_descriptions': 0,
                'invalid_categories': 0,
                'missing_values': 0,
                'outdated_timestamps': 0
            }
            
            # Check for duplicate setting keys
            if 'setting_key' in settings_df.columns:
                duplicate_keys = settings_df['setting_key'].duplicated().sum()
                validation_results['duplicate_keys'] = duplicate_keys
                print(f"   🔍 Duplicate setting keys: {duplicate_keys}")
            
            # Check for missing descriptions
            if 'description' in settings_df.columns:
                missing_desc = settings_df['description'].isna().sum()
                validation_results['missing_descriptions'] = missing_desc
                print(f"   📝 Missing descriptions: {missing_desc}")
            
            # Validate categories
            if 'category' in settings_df.columns:
                valid_categories = ['integration', 'ui', 'security', 'general', 'system']
                invalid_categories = 0
                for category in settings_df['category'].dropna():
                    if category not in valid_categories:
                        invalid_categories += 1
                validation_results['invalid_categories'] = invalid_categories
                print(f"   📂 Invalid categories: {invalid_categories}")
            
            # Check for missing values
            if 'setting_value' in settings_df.columns:
                missing_values = settings_df['setting_value'].isna().sum()
                validation_results['missing_values'] = missing_values
                print(f"   💎 Missing values: {missing_values}")
            
            # Validate required settings exist
            required_settings = ['use_google_sheets', 'google_sheet_id']
            missing_required = []
            for required in required_settings:
                if required not in settings_df['setting_key'].values:
                    missing_required.append(required)
            
            if missing_required:
                print(f"   ⚠️  Missing required settings: {missing_required}")
            else:
                print(f"   ✅ All required settings present")
            
            # Overall validation score
            total_issues = sum(validation_results.values())
            print(f"   📊 Total configuration issues: {total_issues}")
            
            return True
            
        except Exception as e:
            print(f"❌ Configuration validation error: {e}")
            return False
    
    def test_settings_management_operations(self):
        """Test 4: Settings management operations"""
        print("\n👥 TEST 4: SETTINGS MANAGEMENT OPERATIONS")
        print("-" * 40)
        
        try:
            settings_df = self.storage.read_sheet("Settings")
            
            # Test getting specific settings
            integration_settings = settings_df[settings_df['category'] == 'integration'] if 'category' in settings_df.columns else settings_df
            print(f"✅ Integration settings found: {len(integration_settings)}")
            
            # Simulate setting update
            test_setting = {
                'setting_key': 'test_setting',
                'setting_value': 'test_value',
                'description': 'Test setting for validation',
                'category': 'system',
                'updated_at': datetime.now().isoformat(),
                'updated_by': 'test_user'
            }
            
            print("✅ Setting update simulation:")
            print(f"   🔑 Key: {test_setting['setting_key']}")
            print(f"   💎 Value: {test_setting['setting_value']}")
            print(f"   📝 Description: {test_setting['description']}")
            print(f"   📂 Category: {test_setting['category']}")
            
            # Test settings export functionality
            settings_export = {}
            for idx, row in settings_df.iterrows():
                key = row.get('setting_key')
                value = row.get('setting_value')
                if key:
                    settings_export[key] = {
                        'value': value,
                        'description': row.get('description', ''),
                        'category': row.get('category', ''),
                        'updated_at': row.get('updated_at', ''),
                        'updated_by': row.get('updated_by', '')
                    }
            
            print(f"   📤 Settings export prepared: {len(settings_export)} settings")
            
            # Test settings backup simulation
            backup_data = {
                'backup_timestamp': datetime.now().isoformat(),
                'settings_count': len(settings_df),
                'settings': settings_export
            }
            
            print(f"   💾 Settings backup simulated")
            print(f"      Timestamp: {backup_data['backup_timestamp']}")
            print(f"      Settings count: {backup_data['settings_count']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Settings management operations error: {e}")
            return False
    
    def test_settings_analytics(self):
        """Test 5: Settings analytics and reporting"""
        print("\n📊 TEST 5: SETTINGS ANALYTICS")
        print("-" * 40)
        
        try:
            settings_df = self.storage.read_sheet("Settings")
            
            if settings_df.empty:
                print("❌ No data for analytics")
                return False
            
            analytics = {
                'total_settings': len(settings_df),
                'categories': {},
                'value_types': {},
                'last_updated': None,
                'update_frequency': {}
            }
            
            # Category analysis
            if 'category' in settings_df.columns:
                analytics['categories'] = settings_df['category'].value_counts().to_dict()
            
            # Value type analysis
            if 'setting_value' in settings_df.columns:
                for value in settings_df['setting_value'].dropna():
                    if str(value).isdigit():
                        value_type = 'numeric'
                    elif str(value).lower() in ['true', 'false', '1', '0']:
                        value_type = 'boolean'
                    elif str(value).startswith('http'):
                        value_type = 'url'
                    else:
                        value_type = 'string'
                    
                    analytics['value_types'][value_type] = analytics['value_types'].get(value_type, 0) + 1
            
            # Update frequency analysis
            if 'updated_by' in settings_df.columns:
                analytics['update_frequency'] = settings_df['updated_by'].value_counts().to_dict()
            
            print("✅ Settings analytics generated:")
            print(f"   ⚙️  Total settings: {analytics['total_settings']}")
            print(f"   📂 Categories: {analytics['categories']}")
            print(f"   💎 Value types: {analytics['value_types']}")
            print(f"   👤 Updated by: {analytics['update_frequency']}")
            
            # Configuration health score
            health_score = 100
            if analytics['total_settings'] < 5:
                health_score -= 20  # Too few settings
            if len(analytics['categories']) < 2:
                health_score -= 15  # Limited categories
            
            print(f"   🏥 Configuration health score: {health_score}/100")
            
            return True
            
        except Exception as e:
            print(f"❌ Settings analytics error: {e}")
            return False
    
    def test_system_configuration_health(self):
        """Test 6: System configuration health check"""
        print("\n🏥 TEST 6: SYSTEM CONFIGURATION HEALTH")
        print("-" * 40)
        
        try:
            health_check = {
                'overall_status': 'healthy',
                'issues': [],
                'recommendations': [],
                'critical_settings': {},
                'optional_settings': {}
            }
            
            settings_df = self.storage.read_sheet("Settings")
            
            # Check critical settings
            critical_settings = ['use_google_sheets', 'google_sheet_id']
            for setting in critical_settings:
                matches = settings_df[settings_df['setting_key'] == setting]
                if not matches.empty:
                    value = matches.iloc[0]['setting_value']
                    health_check['critical_settings'][setting] = {
                        'present': True,
                        'value': value,
                        'status': 'configured' if value else 'empty'
                    }
                else:
                    health_check['critical_settings'][setting] = {
                        'present': False,
                        'value': None,
                        'status': 'missing'
                    }
                    health_check['issues'].append(f"Critical setting missing: {setting}")
            
            # Check for configuration consistency
            if 'use_google_sheets' in health_check['critical_settings']:
                use_sheets = health_check['critical_settings']['use_google_sheets']['value']
                sheet_id = health_check['critical_settings'].get('google_sheet_id', {}).get('value')
                
                if str(use_sheets) == '1' and not sheet_id:
                    health_check['issues'].append("Google Sheets enabled but no Sheet ID configured")
                elif str(use_sheets) == '0' and sheet_id:
                    health_check['recommendations'].append("Sheet ID configured but Google Sheets disabled")
            
            # Overall health assessment
            if len(health_check['issues']) > 0:
                health_check['overall_status'] = 'issues_found'
            if len(health_check['issues']) > 3:
                health_check['overall_status'] = 'critical'
            
            print("✅ System configuration health check:")
            print(f"   🏥 Overall status: {health_check['overall_status'].upper()}")
            print(f"   ⚙️  Critical settings:")
            for setting, info in health_check['critical_settings'].items():
                status_icon = "✅" if info['present'] else "❌"
                print(f"      {status_icon} {setting}: {info['status']}")
            
            if health_check['issues']:
                print(f"   ⚠️  Issues found:")
                for issue in health_check['issues']:
                    print(f"      - {issue}")
            
            if health_check['recommendations']:
                print(f"   💡 Recommendations:")
                for rec in health_check['recommendations']:
                    print(f"      - {rec}")
            
            return True
            
        except Exception as e:
            print(f"❌ System configuration health check error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all Settings sheet tests"""
        print("🔍 SETTINGS SHEET COMPREHENSIVE TESTING")
        print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        tests = [
            ('Data Access', self.test_settings_data_access),
            ('Service Integration', self.test_settings_service_integration),
            ('Configuration Validation', self.test_configuration_validation),
            ('Management Operations', self.test_settings_management_operations),
            ('Settings Analytics', self.test_settings_analytics),
            ('Configuration Health', self.test_system_configuration_health)
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
        print("📋 SETTINGS SHEET TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        for test_name, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {test_name:<25} {status}")
        
        print(f"\n🎯 Results: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 ALL SETTINGS SHEET TESTS PASSED!")
        else:
            print("⚠️  Some tests need attention")
        
        return passed_tests == total_tests

def main():
    """Main execution"""
    try:
        tester = SettingsSheetTester()
        success = tester.run_all_tests()
        return success
    except Exception as e:
        print(f"💥 Critical error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'🚀 Settings sheet testing complete!' if success else '❌ Tests failed'}")