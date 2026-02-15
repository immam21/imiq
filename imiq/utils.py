"""
IMIQ Utilities
Common utility functions for the IMIQ application
"""

import uuid
import pytz
from datetime import datetime
from typing import Any, Optional, Dict
import logging
import os
import tempfile
import shutil

logger = logging.getLogger(__name__)

# Timezone configuration
IST = pytz.timezone('Asia/Kolkata')

def generate_id(prefix: str = "", length: int = 8) -> str:
    """Generate a unique ID with optional prefix"""
    try:
        # Use UUID4 for uniqueness, take first 'length' characters
        unique_id = str(uuid.uuid4()).replace('-', '')[:length].upper()
        
        if prefix:
            return f"{prefix}-{unique_id}"
        return unique_id
        
    except Exception as e:
        logger.error(f"Error generating ID: {e}")
        # Fallback to timestamp-based ID
        fallback_id = str(int(datetime.now().timestamp()))[-length:]
        return f"{prefix}-{fallback_id}" if prefix else fallback_id

def get_ist_now() -> datetime:
    """Get current datetime in IST timezone"""
    try:
        return datetime.now(IST)
    except Exception as e:
        logger.error(f"Error getting IST time: {e}")
        # Fallback to UTC
        return datetime.utcnow().replace(tzinfo=pytz.UTC)

def convert_to_ist(dt: datetime) -> datetime:
    """Convert datetime to IST timezone"""
    try:
        if dt.tzinfo is None:
            # Assume UTC if no timezone info
            dt = dt.replace(tzinfo=pytz.UTC)
        
        return dt.astimezone(IST)
    except Exception as e:
        logger.error(f"Error converting to IST: {e}")
        return dt

def format_datetime(dt: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string with IST timezone"""
    try:
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.UTC)
        
        ist_dt = dt.astimezone(IST)
        return ist_dt.strftime(format_string)
    except Exception as e:
        logger.error(f"Error formatting datetime: {e}")
        return str(dt)

def format_currency(amount: float, currency: str = "INR") -> str:
    """Format amount as currency string"""
    try:
        if currency == "INR":
            return f"₹{amount:,.2f}"
        elif currency == "USD":
            return f"${amount:,.2f}"
        elif currency == "EUR":
            return f"€{amount:,.2f}"
        else:
            return f"{currency} {amount:,.2f}"
    except Exception as e:
        logger.error(f"Error formatting currency: {e}")
        return str(amount)

def validate_email(email: str) -> bool:
    """Validate email address format"""
    try:
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    except Exception as e:
        logger.error(f"Error validating email: {e}")
        return False

def validate_phone(phone: str) -> bool:
    """Validate Indian phone number format"""
    try:
        import re
        # Remove spaces and special characters
        clean_phone = re.sub(r'[^\d+]', '', phone)
        
        # Indian phone number patterns
        patterns = [
            r'^\+91[6-9]\d{9}$',  # +91 followed by 10 digits starting with 6-9
            r'^91[6-9]\d{9}$',    # 91 followed by 10 digits starting with 6-9
            r'^[6-9]\d{9}$'       # 10 digits starting with 6-9
        ]
        
        return any(re.match(pattern, clean_phone) for pattern in patterns)
    except Exception as e:
        logger.error(f"Error validating phone: {e}")
        return False

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    try:
        import re
        # Remove or replace invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove leading/trailing spaces and dots
        sanitized = sanitized.strip(' .')
        # Ensure it's not empty
        if not sanitized:
            sanitized = "unnamed_file"
        return sanitized
    except Exception as e:
        logger.error(f"Error sanitizing filename: {e}")
        return "safe_filename"

def safe_division(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Perform safe division with default value for zero denominator"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except Exception as e:
        logger.error(f"Error in division: {e}")
        return default

def calculate_percentage(part: float, whole: float, precision: int = 2) -> float:
    """Calculate percentage with safe division"""
    try:
        if whole == 0:
            return 0.0
        percentage = (part / whole) * 100
        return round(percentage, precision)
    except Exception as e:
        logger.error(f"Error calculating percentage: {e}")
        return 0.0

def atomic_write(file_path: str, content: str, mode: str = 'w', encoding: str = 'utf-8') -> bool:
    """Perform atomic write operation using temporary file"""
    temp_path = None
    try:
        # Create temporary file in the same directory
        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)
        
        with tempfile.NamedTemporaryFile(
            mode=mode, 
            encoding=encoding if 'b' not in mode else None,
            dir=directory,
            delete=False
        ) as temp_file:
            temp_path = temp_file.name
            temp_file.write(content)
        
        # Atomic move
        shutil.move(temp_path, file_path)
        temp_path = None  # Successfully moved, don't delete
        
        logger.debug(f"Atomic write successful: {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error in atomic write to {file_path}: {e}")
        
        # Cleanup temp file if error occurred
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except:
                pass
        
        return False

def ensure_directory(directory_path: str) -> bool:
    """Ensure directory exists, create if necessary"""
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error ensuring directory {directory_path}: {e}")
        return False

def get_file_size(file_path: str) -> int:
    """Get file size in bytes, return 0 if file doesn't exist"""
    try:
        if os.path.exists(file_path):
            return os.path.getsize(file_path)
        return 0
    except Exception as e:
        logger.error(f"Error getting file size for {file_path}: {e}")
        return 0

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    try:
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        
        return f"{s} {size_names[i]}"
    except Exception as e:
        logger.error(f"Error formatting file size: {e}")
        return f"{size_bytes} B"

def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate string to maximum length with suffix"""
    try:
        if len(text) <= max_length:
            return text
        
        truncated_length = max_length - len(suffix)
        if truncated_length < 0:
            truncated_length = max_length
            suffix = ""
        
        return text[:truncated_length] + suffix
    except Exception as e:
        logger.error(f"Error truncating string: {e}")
        return str(text)

def extract_domain_from_email(email: str) -> str:
    """Extract domain from email address"""
    try:
        if '@' in email:
            return email.split('@')[1].lower()
        return ""
    except Exception as e:
        logger.error(f"Error extracting domain from email: {e}")
        return ""

def calculate_age_in_days(start_date: datetime, end_date: Optional[datetime] = None) -> int:
    """Calculate age in days between two dates"""
    try:
        if end_date is None:
            end_date = get_ist_now()
        
        # Ensure both dates have timezone info
        if start_date.tzinfo is None:
            start_date = start_date.replace(tzinfo=IST)
        if end_date.tzinfo is None:
            end_date = end_date.replace(tzinfo=IST)
        
        delta = end_date - start_date
        return delta.days
    except Exception as e:
        logger.error(f"Error calculating age in days: {e}")
        return 0

def parse_iso_datetime(datetime_string: str) -> Optional[datetime]:
    """Parse ISO format datetime string"""
    try:
        from dateutil.parser import parse
        return parse(datetime_string)
    except Exception as e:
        logger.error(f"Error parsing datetime string {datetime_string}: {e}")
        return None

def get_quarter_from_date(date_obj: datetime) -> str:
    """Get quarter string from date (Q1, Q2, Q3, Q4)"""
    try:
        month = date_obj.month
        if month <= 3:
            return "Q1"
        elif month <= 6:
            return "Q2"
        elif month <= 9:
            return "Q3"
        else:
            return "Q4"
    except Exception as e:
        logger.error(f"Error getting quarter from date: {e}")
        return "Q1"

def clean_numeric_string(value: str) -> float:
    """Clean and convert string to numeric value"""
    try:
        if not value:
            return 0.0
        
        # Remove common currency symbols and separators
        cleaned = str(value).replace(',', '').replace('₹', '').replace('$', '').replace('€', '')
        cleaned = cleaned.strip()
        
        return float(cleaned)
    except Exception as e:
        logger.error(f"Error cleaning numeric string '{value}': {e}")
        return 0.0

def generate_order_number() -> str:
    """Generate a formatted order number"""
    try:
        now = get_ist_now()
        timestamp = now.strftime("%Y%m%d")
        unique_id = generate_id("", 4)
        return f"ORD-{timestamp}-{unique_id}"
    except Exception as e:
        logger.error(f"Error generating order number: {e}")
        return f"ORD-{generate_id('', 8)}"

def generate_shipment_number() -> str:
    """Generate a formatted shipment number"""
    try:
        now = get_ist_now()
        timestamp = now.strftime("%Y%m%d")
        unique_id = generate_id("", 4)
        return f"SHIP-{timestamp}-{unique_id}"
    except Exception as e:
        logger.error(f"Error generating shipment number: {e}")
        return f"SHIP-{generate_id('', 8)}"

def mask_sensitive_data(data: str, mask_char: str = "*", visible_chars: int = 4) -> str:
    """Mask sensitive data showing only first few characters"""
    try:
        if not data or len(data) <= visible_chars:
            return mask_char * len(data) if data else ""
        
        visible_part = data[:visible_chars]
        masked_part = mask_char * (len(data) - visible_chars)
        return visible_part + masked_part
    except Exception as e:
        logger.error(f"Error masking sensitive data: {e}")
        return mask_char * 8

def create_backup_filename(original_path: str, suffix: str = "backup") -> str:
    """Create backup filename with timestamp"""
    try:
        directory = os.path.dirname(original_path)
        filename = os.path.basename(original_path)
        name, ext = os.path.splitext(filename)
        
        timestamp = get_ist_now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{name}_{suffix}_{timestamp}{ext}"
        
        return os.path.join(directory, backup_filename)
    except Exception as e:
        logger.error(f"Error creating backup filename: {e}")
        return f"{original_path}.backup"

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Setup logging configuration for the application"""
    try:
        level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        
        # Setup root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        root_logger.addHandler(console_handler)
        
        # Setup file handler if specified
        if log_file:
            ensure_directory(os.path.dirname(log_file))
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        logger.info("Logging setup completed")
        
    except Exception as e:
        print(f"Error setting up logging: {e}")

def get_environment_info() -> Dict[str, Any]:
    """Get information about the current environment"""
    try:
        import platform
        import sys
        
        return {
            'python_version': sys.version,
            'platform': platform.platform(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'current_time': get_ist_now().isoformat(),
            'timezone': str(IST),
            'working_directory': os.getcwd(),
            'home_directory': os.path.expanduser('~')
        }
    except Exception as e:
        logger.error(f"Error getting environment info: {e}")
        return {
            'error': str(e),
            'current_time': get_ist_now().isoformat()
        }