"""
IMIQ Settings Service
Handles application settings and configuration management
"""

import pandas as pd
from typing import Dict, Any, Optional
import logging
import os

from .storage import StorageBase
from .utils import get_ist_now

logger = logging.getLogger(__name__)

class SettingsService:
    """Service for managing application settings and configuration"""
    
    def __init__(self, storage: StorageBase):
        self.storage = storage
        self.settings_sheet = "Settings"
        
        # Initialize settings sheet if it doesn't exist
        self._ensure_settings_sheet()
    
    def _ensure_settings_sheet(self) -> None:
        """Ensure settings sheet exists with default values"""
        try:
            # Skip settings sheet initialization if not in CZ_MasterSheet
            # CZ_MasterSheet doesn't have a Settings sheet, so use in-memory defaults
            logger.info("Using default settings - Settings sheet not required for CZ_MasterSheet")
            return
        except Exception as e:
            logger.error(f"Error initializing settings: {e}")
            return
            
            # Create default settings
            default_settings = {
                'setting_key': 'use_google_sheets',
                'setting_value': 'false',
                'description': 'Enable Google Sheets integration',
                'category': 'integration',
                'updated_at': get_ist_now().isoformat(),
                'updated_by': 'system'
            }
            
            # Create sheet structure
            required_sheets = {
                self.settings_sheet: ['setting_key', 'setting_value', 'description', 'category', 'updated_at', 'updated_by']
            }
            self.storage.ensure_workbook(required_sheets)
            
            # Add default settings
            self.storage.append_row(self.settings_sheet, default_settings)
            
            # Add more default settings
            other_defaults = [
                {
                    'setting_key': 'google_sheet_id',
                    'setting_value': '',
                    'description': 'Google Sheet ID for data storage',
                    'category': 'integration',
                    'updated_at': get_ist_now().isoformat(),
                    'updated_by': 'system'
                },
                {
                    'setting_key': 'timezone',
                    'setting_value': 'Asia/Kolkata',
                    'description': 'Application timezone',
                    'category': 'regional',
                    'updated_at': get_ist_now().isoformat(),
                    'updated_by': 'system'
                },
                {
                    'setting_key': 'currency',
                    'setting_value': 'INR (₹)',
                    'description': 'Default currency for display',
                    'category': 'regional',
                    'updated_at': get_ist_now().isoformat(),
                    'updated_by': 'system'
                },
                {
                    'setting_key': 'company_name',
                    'setting_value': 'IMIQ',
                    'description': 'Company name for branding',
                    'category': 'branding',
                    'updated_at': get_ist_now().isoformat(),
                    'updated_by': 'system'
                },
                {
                    'setting_key': 'app_version',
                    'setting_value': '1.0.0',
                    'description': 'Application version',
                    'category': 'system',
                    'updated_at': get_ist_now().isoformat(),
                    'updated_by': 'system'
                }
            ]
            
            for setting in other_defaults:
                self.storage.append_row(self.settings_sheet, setting)
            
            logger.info("Settings sheet initialized with default values")
            
        except Exception as e:
            logger.error(f"Error initializing settings sheet: {e}")
    
    def get_settings(self) -> Dict[str, Any]:
        """Get all application settings as a dictionary"""
        try:
            # Start with default settings
            settings = self._get_default_settings()
            
            # Try to read from storage
            try:
                from .performance import get_cached_sheet_data
                settings_df = get_cached_sheet_data(self.storage, self.settings_sheet)
                if not settings_df.empty:
                    for _, row in settings_df.iterrows():
                        key = row['setting_key']
                        value = row['setting_value']
                        
                        # Convert boolean strings
                        if value.lower() in ['true', 'false']:
                            value = value.lower() == 'true'
                        
                        settings[key] = value
            except Exception as e:
                logger.warning(f"Could not read settings from storage: {e}")
            
            # Include memory settings as fallback
            if hasattr(self, '_memory_settings'):
                for key, value in self._memory_settings.items():
                    # Convert boolean strings
                    if isinstance(value, str) and value.lower() in ['true', 'false']:
                        value = value.lower() == 'true'
                    settings[key] = value
            
            return settings
            
        except Exception as e:
            logger.error(f"Error retrieving settings: {e}")
            return self._get_default_settings()
    
    def get_setting(self, setting_key: str, default_value: Any = None) -> Any:
        """Get a specific setting value"""
        try:
            settings = self.get_settings()
            return settings.get(setting_key, default_value)
            
        except Exception as e:
            logger.error(f"Error retrieving setting {setting_key}: {e}")
            return default_value
    
    def update_setting(self, setting_key: str, setting_value: Any, updated_by: str = 'user') -> bool:
        """Update a specific setting"""
        try:
            from .performance import get_cached_sheet_data
            settings_df = get_cached_sheet_data(self.storage, self.settings_sheet)
            
            if settings_df.empty:
                # Create new setting if sheet is empty
                return self._create_setting(setting_key, setting_value, updated_by)
            
            # Check if setting exists
            existing_setting = settings_df[settings_df['setting_key'] == setting_key]
            
            if len(existing_setting) > 0:
                # Update existing setting
                def update_fn(row):
                    if row['setting_key'] == setting_key:
                        row['setting_value'] = str(setting_value)
                        row['updated_at'] = get_ist_now().isoformat()
                        row['updated_by'] = updated_by
                    return row
                
                filter_fn = lambda row: row['setting_key'] == setting_key
                updated_count = self.storage.update_rows(self.settings_sheet, filter_fn, update_fn)
                
                if updated_count > 0:
                    logger.info(f"Setting {setting_key} updated successfully")
                    return True
                else:
                    logger.warning(f"Failed to update setting {setting_key}")
                    return False
            else:
                # Create new setting
                return self._create_setting(setting_key, setting_value, updated_by)
                
        except Exception as e:
            logger.error(f"Error updating setting {setting_key}: {e}")
            # For Google Sheets settings, we'll store in memory as fallback
            if not hasattr(self, '_memory_settings'):
                self._memory_settings = {}
            self._memory_settings[setting_key] = str(setting_value)
            logger.info(f"Setting {setting_key} stored in memory as fallback")
            return True
    
    def update_settings(self, settings_dict: Dict[str, Any], updated_by: str = 'user') -> bool:
        """Update multiple settings at once"""
        try:
            success_count = 0
            for key, value in settings_dict.items():
                if self.update_setting(key, value, updated_by):
                    success_count += 1
            
            logger.info(f"Updated {success_count}/{len(settings_dict)} settings successfully")
            return success_count == len(settings_dict)
            
        except Exception as e:
            logger.error(f"Error updating multiple settings: {e}")
            return False
    
    def _create_setting(self, setting_key: str, setting_value: Any, updated_by: str) -> bool:
        """Create a new setting"""
        try:
            setting_data = {
                'setting_key': setting_key,
                'setting_value': str(setting_value),
                'description': f'User-defined setting: {setting_key}',
                'category': 'custom',
                'updated_at': get_ist_now().isoformat(),
                'updated_by': updated_by
            }
            
            self.storage.append_row(self.settings_sheet, setting_data)
            logger.info(f"New setting created: {setting_key}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating setting {setting_key}: {e}")
            raise
    
    def delete_setting(self, setting_key: str) -> bool:
        """Delete a setting (use with caution)"""
        try:
            from .performance import get_cached_sheet_data
            settings_df = get_cached_sheet_data(self.storage, self.settings_sheet)
            
            if settings_df.empty:
                return False
            
            # Remove the setting
            filtered_df = settings_df[settings_df['setting_key'] != setting_key]
            
            # Check if any row was actually removed
            if len(filtered_df) == len(settings_df):
                logger.warning(f"Setting {setting_key} not found for deletion")
                return False
            
            # Replace the sheet with filtered data
            self.storage.replace_sheet(self.settings_sheet, filtered_df)
            
            logger.info(f"Setting {setting_key} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting setting {setting_key}: {e}")
            raise
    
    def get_google_sheets_config(self) -> Dict[str, Any]:
        """Get Google Sheets specific configuration"""
        try:
            settings = self.get_settings()
            
            return {
                'enabled': settings.get('use_google_sheets', False),
                'sheet_id': settings.get('google_sheet_id', ''),
                'credentials_path': os.getenv('GOOGLE_APPLICATION_CREDENTIALS', ''),
                'is_configured': self._is_google_sheets_configured(settings)
            }
            
        except Exception as e:
            logger.error(f"Error getting Google Sheets config: {e}")
            return {
                'enabled': False,
                'sheet_id': '',
                'credentials_path': '',
                'is_configured': False
            }
    
    def _is_google_sheets_configured(self, settings: Dict[str, Any]) -> bool:
        """Check if Google Sheets is properly configured"""
        try:
            required_items = [
                settings.get('use_google_sheets', False),
                settings.get('google_sheet_id', ''),
                os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
            ]
            
            return all(required_items)
            
        except:
            return False
    
    def get_regional_settings(self) -> Dict[str, str]:
        """Get regional and localization settings"""
        try:
            settings = self.get_settings()
            
            return {
                'timezone': settings.get('timezone', 'Asia/Kolkata'),
                'currency': settings.get('currency', 'INR (₹)'),
                'date_format': settings.get('date_format', 'DD/MM/YYYY'),
                'number_format': settings.get('number_format', 'en-IN')
            }
            
        except Exception as e:
            logger.error(f"Error getting regional settings: {e}")
            return {
                'timezone': 'Asia/Kolkata',
                'currency': 'INR (₹)',
                'date_format': 'DD/MM/YYYY',
                'number_format': 'en-IN'
            }
    
    def get_branding_settings(self) -> Dict[str, str]:
        """Get branding and UI settings"""
        try:
            settings = self.get_settings()
            
            return {
                'company_name': settings.get('company_name', 'IMIQ'),
                'app_title': settings.get('app_title', 'IMIQ - Order Management'),
                'logo_url': settings.get('logo_url', ''),
                'primary_color': settings.get('primary_color', '#0f172a'),
                'accent_color': settings.get('accent_color', '#06b6d4')
            }
            
        except Exception as e:
            logger.error(f"Error getting branding settings: {e}")
            return {
                'company_name': 'IMIQ',
                'app_title': 'IMIQ - Order Management',
                'logo_url': '',
                'primary_color': '#0f172a',
                'accent_color': '#06b6d4'
            }
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information and diagnostics"""
        try:
            settings = self.get_settings()
            
            # Check storage type
            storage_type = "Excel"
            if settings.get('use_google_sheets', False):
                storage_type = "Google Sheets"
            
            # Check data integrity (basic)
            data_integrity_ok = True
            try:
                from .performance import get_cached_sheet_data
                orders_df = get_cached_sheet_data(self.storage, "NewOrders")
                users_df = get_cached_sheet_data(self.storage, "Users")
                data_integrity_ok = not (orders_df is None or users_df is None)
            except:
                data_integrity_ok = False
            
            system_info = {
                'app_version': settings.get('app_version', '1.0.0'),
                'storage_type': storage_type,
                'data_integrity_ok': data_integrity_ok,
                'google_sheets_configured': self._is_google_sheets_configured(settings),
                'last_settings_update': settings.get('updated_at', 'Unknown'),
                'settings_count': len(settings)
            }
            
            return system_info
            
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {
                'app_version': '1.0.0',
                'storage_type': 'Excel',
                'data_integrity_ok': False,
                'google_sheets_configured': False,
                'last_settings_update': 'Unknown',
                'settings_count': 0
            }
    
    def export_settings(self) -> Dict[str, Any]:
        """Export all settings for backup or migration"""
        try:
            settings_df = self.storage.read_sheet(self.settings_sheet)
            
            if settings_df.empty:
                return {}
            
            # Convert to exportable format
            export_data = {
                'export_timestamp': get_ist_now().isoformat(),
                'settings': settings_df.to_dict('records')
            }
            
            logger.info("Settings exported successfully")
            return export_data
            
        except Exception as e:
            logger.error(f"Error exporting settings: {e}")
            return {}
    
    def import_settings(self, settings_data: Dict[str, Any], overwrite: bool = False) -> bool:
        """Import settings from backup or migration"""
        try:
            if 'settings' not in settings_data:
                raise ValueError("Invalid settings data format")
            
            success_count = 0
            
            for setting in settings_data['settings']:
                key = setting.get('setting_key')
                value = setting.get('setting_value')
                
                if key and value is not None:
                    if overwrite or not self.get_setting(key):
                        if self.update_setting(key, value, 'import'):
                            success_count += 1
            
            logger.info(f"Imported {success_count} settings successfully")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Error importing settings: {e}")
            raise
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings when none exist"""
        return {
            'use_google_sheets': False,
            'google_sheet_id': '',
            'timezone': 'Asia/Kolkata',
            'currency': 'INR (₹)',
            'company_name': 'IMIQ',
            'app_version': '1.0.0'
        }
    
    def reset_to_defaults(self) -> bool:
        """Reset all settings to default values"""
        try:
            # Get default settings
            defaults = self._get_default_settings()
            
            # Update each setting
            for key, value in defaults.items():
                self.update_setting(key, value, 'system_reset')
            
            logger.info("Settings reset to defaults")
            return True
            
        except Exception as e:
            logger.error(f"Error resetting settings to defaults: {e}")
            raise