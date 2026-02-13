"""
IMIQ Storage Layer
Handles Excel and Google Sheets data persistence with concurrency safety
"""

import pandas as pd
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
import tempfile
import shutil
from filelock import FileLock
from datetime import datetime
import logging

try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False

from .utils import get_ist_now, generate_id

logger = logging.getLogger(__name__)

class StorageBase:
    """Abstract base class for storage implementations"""
    
    def ensure_workbook(self, required_sheets: Dict[str, List[str]]) -> None:
        """Ensure workbook exists with required sheets and columns"""
        raise NotImplementedError
    
    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        """Read a sheet and return as DataFrame"""
        raise NotImplementedError
    
    def append_row(self, sheet_name: str, row_data: Dict[str, Any]) -> None:
        """Append a single row to a sheet"""
        raise NotImplementedError
    
    def replace_sheet(self, sheet_name: str, df: pd.DataFrame) -> None:
        """Replace entire sheet content with DataFrame"""
        raise NotImplementedError
    
    def update_rows(self, sheet_name: str, filter_fn: Callable, update_fn: Callable) -> int:
        """Update rows matching filter function with update function"""
        raise NotImplementedError

class ExcelStorage(StorageBase):
    """Excel-based storage with file locking for concurrency safety"""
    
    def __init__(self, file_path: str = "CZ_MasterSheet.xlsx"):
        self.file_path = file_path
        self.lock_path = f"{file_path}.lock"
        
        # Define schema matching existing CZ_MasterSheet.xlsx
        self.default_sheets = {
            "Users": ["user_id", "email", "password_hash", "plain_password", "role", "name", "created_at", "is_active"],
            "NewOrders": [
                "order_id", "phone", "customer_name", "product", "quantity", "balance_to_pay", 
                "advance_paid", "total", "address", "city", "pincode", "payment_method", 
                "status", "timestamp", "ai_order_id", "tracking_id", "courier_name", 
                "created_by", "advance_screenshot", "PICKUP LOCATION", "Remarks", "Last Update Date"
            ],
            "Customers": [
                "customer_id", "phone", "name", "email", "address", "city", "pincode", "created_at"
            ],
            "ProductList": [
                "product_name", "price", "description", "stock", "category", "sku", "status", "image_url"
            ],
            "ChatLogs": [
                "message_id", "phone", "message", "direction", "timestamp", "assigned_user", 
                "source", "message_id_dup", "status", "timestamp_dup", "ai_attempted", 
                "ai_success", "failure_reason"
            ],
            "ChatAssignments": [
                "phone", "assigned_user", "assigned_at", "status"
            ],
            "Revenue": [
                "date", "ad_spend", "courier_expenses", "other_expenses", "notes", "created_by", "timestamp"
            ]
        }
        
        # Verify existing workbook structure
        self.ensure_workbook(self.default_sheets)
    
    def ensure_workbook(self, required_sheets: Dict[str, List[str]]) -> None:
        """Verify existing workbook has required structure"""
        if os.path.exists(self.file_path):
            # Verify existing sheets have required columns
            with FileLock(self.lock_path):
                try:
                    existing_sheets = pd.read_excel(self.file_path, sheet_name=None)
                    for sheet_name, required_cols in required_sheets.items():
                        if sheet_name in existing_sheets:
                            existing_cols = existing_sheets[sheet_name].columns.tolist()
                            missing_cols = [col for col in required_cols if col not in existing_cols]
                            if missing_cols:
                                logger.warning(f"Sheet {sheet_name} missing columns: {missing_cols}")
                        else:
                            logger.warning(f"Sheet {sheet_name} not found in workbook")
                except Exception as e:
                    logger.error(f"Error reading existing workbook: {e}")
        else:
            logger.error(f"Workbook {self.file_path} does not exist")
            raise FileNotFoundError(f"Excel file {self.file_path} not found")
        
        logger.info(f"Using existing workbook at {self.file_path}")
    
    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        """Read sheet with file locking"""
        with FileLock(self.lock_path):
            try:
                df = pd.read_excel(self.file_path, sheet_name=sheet_name)
                return df
            except Exception as e:
                logger.error(f"Error reading sheet {sheet_name}: {e}")
                # Return empty DataFrame with expected columns
                if sheet_name in self.default_sheets:
                    return pd.DataFrame(columns=self.default_sheets[sheet_name])
                raise
    
    def append_row(self, sheet_name: str, row_data: Dict[str, Any]) -> None:
        """Append row with atomic write"""
        logger.info(f"Attempting to append row to sheet: {sheet_name}")
        logger.info(f"Row data: {row_data}")
        
        with FileLock(self.lock_path):
            # Read existing data
            try:
                all_sheets = pd.read_excel(self.file_path, sheet_name=None)
                logger.info(f"Successfully read existing Excel file with {len(all_sheets)} sheets")
            except FileNotFoundError:
                logger.info("Excel file not found, creating new one")
                all_sheets = {}
            except Exception as e:
                logger.error(f"Error reading Excel file: {e}")
                raise
            
            # Update target sheet
            if sheet_name in all_sheets:
                df = all_sheets[sheet_name]
                logger.info(f"Found existing sheet '{sheet_name}' with {len(df)} rows")
            else:
                df = pd.DataFrame(columns=self.default_sheets.get(sheet_name, list(row_data.keys())))
                logger.info(f"Created new sheet '{sheet_name}' with columns: {list(df.columns)}")
            
            # Add new row
            new_row = pd.DataFrame([row_data])
            logger.info(f"Created new row DataFrame: {new_row}")
            
            df = pd.concat([df, new_row], ignore_index=True)
            all_sheets[sheet_name] = df
            logger.info(f"Sheet now has {len(df)} rows")
            
            # Atomic write
            logger.info("Starting atomic write to Excel file")
            self._atomic_write_excel(all_sheets)
            logger.info("Atomic write completed successfully")
    
    def replace_sheet(self, sheet_name: str, df: pd.DataFrame) -> None:
        """Replace entire sheet content"""
        with FileLock(self.lock_path):
            try:
                all_sheets = pd.read_excel(self.file_path, sheet_name=None)
            except FileNotFoundError:
                all_sheets = {}
            
            all_sheets[sheet_name] = df
            self._atomic_write_excel(all_sheets)
    
    def update_rows(self, sheet_name: str, filter_fn: Callable, update_fn: Callable) -> int:
        """Update rows matching filter condition"""
        with FileLock(self.lock_path):
            try:
                all_sheets = pd.read_excel(self.file_path, sheet_name=None)
                if sheet_name not in all_sheets:
                    return 0
                
                df = all_sheets[sheet_name]
                
                # Find matching rows
                mask = df.apply(filter_fn, axis=1)
                matching_rows = df.loc[mask]
                
                if len(matching_rows) == 0:
                    return 0
                
                # Apply update function
                for idx in matching_rows.index:
                    row = df.loc[idx].to_dict()
                    updated_row = update_fn(row)
                    for col, value in updated_row.items():
                        df.loc[idx, col] = value
                
                all_sheets[sheet_name] = df
                self._atomic_write_excel(all_sheets)
                
                return len(matching_rows)
                
            except Exception as e:
                logger.error(f"Error updating rows in {sheet_name}: {e}")
                raise
    
    def _atomic_write_excel(self, all_sheets: Dict[str, pd.DataFrame]) -> None:
        """Perform atomic write using temporary file"""
        temp_path = None
        try:
            logger.info(f"Starting atomic write with {len(all_sheets)} sheets")
            # Write to temporary file
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False) as temp_file:
                temp_path = temp_file.name
                logger.info(f"Created temporary file: {temp_path}")
                
                with pd.ExcelWriter(temp_path, engine='openpyxl') as writer:
                    for sheet_name, df in all_sheets.items():
                        logger.info(f"Writing sheet '{sheet_name}' with {len(df)} rows")
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            logger.info(f"Temporary file written successfully")
            # Atomic move
            logger.info(f"Moving temp file to final location: {self.file_path}")
            shutil.move(temp_path, self.file_path)
            temp_path = None  # Successfully moved, don't delete
            logger.info("Atomic move completed successfully")
            
        except Exception as e:
            logger.error(f"Error during atomic write: {e}")
            # Cleanup temp file if error occurred
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
                logger.info("Cleaned up temporary file")
            raise e

class GoogleSheetsStorage(StorageBase):
    """Google Sheets storage implementation (requires setup)"""
    
    def __init__(self, sheet_id: str, credentials_path: Optional[str] = None):
        if not GOOGLE_SHEETS_AVAILABLE:
            raise ImportError("Google Sheets integration requires 'gspread' and 'oauth2client' packages")
        
        self.sheet_id = sheet_id
        self.credentials_path = credentials_path or os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        
        # Define schema matching existing CZ_MasterSheet.xlsx
        self.default_sheets = {
            "Users": ["user_id", "email", "password_hash", "plain_password", "role", "name", "created_at", "is_active"],
            "NewOrders": [
                "order_id", "phone", "customer_name", "product", "quantity", "balance_to_pay", 
                "advance_paid", "total", "address", "city", "pincode", "payment_method", 
                "status", "timestamp", "ai_order_id", "tracking_id", "courier_name", 
                "created_by", "advance_screenshot", "PICKUP LOCATION", "Remarks", "Last Update Date"
            ],
            "Customers": [
                "customer_id", "phone", "name", "email", "address", "city", "pincode", "created_at"
            ],
            "ProductList": [
                "product_name", "price", "description", "stock", "category", "sku", "status", "image_url"
            ],
            "ChatLogs": [
                "message_id", "phone", "message", "direction", "timestamp", "assigned_user", 
                "source", "message_id_dup", "status", "timestamp_dup", "ai_attempted", 
                "ai_success", "failure_reason"
            ],
            "ChatAssignments": [
                "phone", "assigned_user", "assigned_at", "status"
            ],
            "Revenue": [
                "date", "ad_spend", "courier_expenses", "other_expenses", "notes", "created_by", "timestamp"
            ]
        }
        
        # Initialize Google Sheets client
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        try:
            # Try different credential methods
            credentials = None
            
            # Method 1: Direct JSON content from environment variable (preferred for deployment)
            if os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'):
                import json
                service_account_info = json.loads(os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'))
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
                logger.info("Using credentials from GOOGLE_SERVICE_ACCOUNT_JSON environment variable")
            
            # Method 2: File path (local development or deployment with file)
            elif self.credentials_path and os.path.exists(self.credentials_path):
                credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, scope)
                logger.info(f"Using credentials from file: {self.credentials_path}")
            
            else:
                raise ValueError("Google Sheets credentials not found. Set either GOOGLE_APPLICATION_CREDENTIALS (file path) or GOOGLE_SERVICE_ACCOUNT_JSON (JSON content) environment variable")
            
            if not credentials:
                raise ValueError("Failed to initialize Google Sheets credentials")
            self.client = gspread.authorize(credentials)
            self.spreadsheet = self.client.open_by_key(sheet_id)
            logger.info(f"Connected to Google Sheet: {sheet_id}")
            
            # Ensure workbook has required structure
            self.ensure_workbook(self.default_sheets)
            
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {e}")
            raise
    
    def ensure_workbook(self, required_sheets: Dict[str, List[str]]) -> None:
        """Ensure required sheets exist in Google Sheets"""
        try:
            existing_worksheets = {ws.title for ws in self.spreadsheet.worksheets()}
            logger.info(f"Found existing worksheets: {existing_worksheets}")
            
            for sheet_name, required_cols in required_sheets.items():
                if sheet_name not in existing_worksheets:
                    # Create new worksheet
                    worksheet = self.spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=20)
                    # Add headers
                    worksheet.insert_row(required_cols, 1)
                    logger.info(f"Created new worksheet: {sheet_name}")
                else:
                    # Verify headers exist
                    worksheet = self.spreadsheet.worksheet(sheet_name)
                    try:
                        existing_headers = worksheet.row_values(1)
                        missing_headers = [col for col in required_cols if col not in existing_headers]
                        if missing_headers:
                            logger.warning(f"Sheet {sheet_name} missing headers: {missing_headers}")
                    except Exception as e:
                        logger.warning(f"Could not verify headers for {sheet_name}: {e}")
                        
            logger.info("Google Sheets workbook verification completed")
            
        except Exception as e:
            logger.error(f"Error ensuring Google Sheets workbook: {e}")
            raise
    
    def read_sheet(self, sheet_name: str) -> pd.DataFrame:
        """Read data from Google Sheet"""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            records = worksheet.get_all_records()
            df = pd.DataFrame(records)
            
            # Clean data for specific sheets
            if sheet_name == "NewOrders" and not df.empty:
                # Convert numeric columns properly
                numeric_columns = ['quantity', 'balance_to_pay', 'advance_paid', 'total']
                for col in numeric_columns:
                    if col in df.columns:
                        # Convert to numeric, replacing empty strings and invalid values with 0
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            logger.info(f"Read {len(df)} rows from Google Sheet '{sheet_name}'")
            return df
        except Exception as e:
            logger.error(f"Error reading Google Sheet '{sheet_name}': {e}")
            # Return empty DataFrame with expected columns if sheet doesn't exist
            if sheet_name in getattr(self, 'default_sheets', {}):
                return pd.DataFrame(columns=self.default_sheets[sheet_name])
            raise
    
    def append_row(self, sheet_name: str, row_data: Dict[str, Any]) -> None:
        """Append row to Google Sheet"""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            
            # Get headers to ensure proper column order
            headers = worksheet.row_values(1)
            if not headers:
                # If no headers, create them from row_data keys
                headers = list(row_data.keys())
                worksheet.insert_row(headers, 1)
            
            # Create row with values in correct order
            row_values = [str(row_data.get(header, '')) for header in headers]
            
            # Append the row
            worksheet.append_row(row_values)
            logger.info(f"Appended row to Google Sheet '{sheet_name}'")
            
        except Exception as e:
            logger.error(f"Error appending to Google Sheet '{sheet_name}': {e}")
            raise
    
    def replace_sheet(self, sheet_name: str, df: pd.DataFrame) -> None:
        """Replace Google Sheet content"""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            
            # Clear existing content
            worksheet.clear()
            
            # Prepare data with headers, cleaning data for JSON compliance
            if not df.empty:
                # Clean the dataframe for Google Sheets compatibility
                df_clean = df.copy()
                
                # Replace NaN values with empty strings
                df_clean = df_clean.fillna('')
                
                # Handle numeric columns properly for NewOrders sheet
                if sheet_name == "NewOrders":
                    numeric_columns = ['quantity', 'balance_to_pay', 'advance_paid', 'total']
                    for col in numeric_columns:
                        if col in df_clean.columns:
                            # Convert to numeric, replacing non-numeric with 0
                            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
                            # Convert to string for Google Sheets
                            df_clean[col] = df_clean[col].astype(str)
                
                # Convert all other columns to strings to avoid JSON issues
                for col in df_clean.columns:
                    df_clean[col] = df_clean[col].astype(str)
                
                # Replace 'nan' strings with empty strings
                df_clean = df_clean.replace(['nan', 'None'], '')
                
                data_to_update = [df_clean.columns.tolist()] + df_clean.values.tolist()
            else:
                data_to_update = [df.columns.tolist()]
            
            # Update the sheet
            worksheet.update(data_to_update)
            logger.info(f"Replaced Google Sheet '{sheet_name}' with {len(df)} rows")
            
        except Exception as e:
            logger.error(f"Error replacing Google Sheet '{sheet_name}': {e}")
            raise
    
    def update_rows(self, sheet_name: str, filter_fn: Callable, update_fn: Callable) -> int:
        """Update rows in Google Sheet"""
        try:
            # Read current data
            df = self.read_sheet(sheet_name)
            
            if df.empty:
                return 0
            
            # Find matching rows
            mask = df.apply(filter_fn, axis=1)
            matching_rows = df.loc[mask]
            
            if len(matching_rows) == 0:
                return 0
            
            # Apply updates
            updated_count = 0
            for idx in matching_rows.index:
                row = df.loc[idx].to_dict()
                updated_row = update_fn(row)
                for col, value in updated_row.items():
                    df.loc[idx, col] = value
                updated_count += 1
            
            # Replace the entire sheet with updated data
            self.replace_sheet(sheet_name, df)
            
            logger.info(f"Updated {updated_count} rows in Google Sheet '{sheet_name}'")
            return updated_count
            
        except Exception as e:
            logger.error(f"Error updating rows in Google Sheet '{sheet_name}': {e}")
            raise

def get_storage_instance(settings_service=None) -> StorageBase:
    """Factory function to get storage instance based on settings"""
    import streamlit as st
    import json
    # Prefer Google Sheets if running on Streamlit Cloud (GOOGLE_SERVICE_ACCOUNT in secrets)
    if "GOOGLE_SERVICE_ACCOUNT" in st.secrets:
        # Patch gspread/credentials to use st.secrets
        try:
            info = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
            import gspread
            from google.oauth2.service_account import Credentials
            creds = Credentials.from_service_account_info(info, scopes=[
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/spreadsheets',
            ])
            gspread_client = gspread.authorize(creds)
            # You may want to get the sheet_id from st.secrets or settings_service
            sheet_id = None
            if settings_service is not None:
                sheet_id = settings_service.get_setting('google_sheet_id', '')
            if not sheet_id:
                sheet_id = st.secrets.get('GOOGLE_SHEET_ID', '')
            if not sheet_id:
                raise ValueError("Google Sheets enabled but no Sheet ID provided.")
            logger.info(f"Initializing Google Sheets storage with Sheet ID: {sheet_id}")
            return GoogleSheetsStorage(sheet_id, gspread_client=gspread_client)
        except Exception as e:
            logger.error(f"Error initializing Google Sheets storage: {e}. Falling back to Excel.")
            return ExcelStorage()
    # Fallback to Excel for local/dev
    if settings_service is None:
        return ExcelStorage()
    
    try:
        # Check if Google Sheets is enabled in settings
        use_google_sheets = settings_service.get_setting('use_google_sheets', False)
        
        if use_google_sheets:
            sheet_id = settings_service.get_setting('google_sheet_id', '')
            
            if not sheet_id:
                logger.warning("Google Sheets enabled but no Sheet ID provided. Falling back to Excel.")
                return ExcelStorage()
            
            if not GOOGLE_SHEETS_AVAILABLE:
                logger.error("Google Sheets enabled but required packages not installed. Falling back to Excel.")
                return ExcelStorage()
            
            # Check for credentials (file path or JSON content)
            if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS') and not os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'):
                logger.error("Google Sheets enabled but no credentials found. Set either GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_SERVICE_ACCOUNT_JSON. Falling back to Excel.")
                return ExcelStorage()
            
            logger.info(f"Initializing Google Sheets storage with Sheet ID: {sheet_id}")
            return GoogleSheetsStorage(sheet_id)
        
        else:
            logger.info("Using Excel storage (Google Sheets disabled)")
            return ExcelStorage()
            
    except Exception as e:
        logger.error(f"Error determining storage type: {e}. Falling back to Excel.")
        return ExcelStorage()