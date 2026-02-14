"""
IMIQ Authentication Service
Handles user authentication, registration, and session management
"""

import streamlit as st
from typing import Optional, Dict, Any
import pandas as pd
import logging

from .storage import StorageBase
from .utils import get_ist_now, generate_id

logger = logging.getLogger(__name__)

class AuthService:
    """Authentication service with plain text password storage"""
    
    def __init__(self, storage: StorageBase):
        self.storage = storage
    
    def create_account(self, user_id: str, password: str, role: str = "user", name: str = "", email: str = "") -> bool:
        """Create a new user account with plain text password"""
        try:
            logger.info(f"Creating account for user_id: {user_id}")
            
            # Check if user already exists
            users_df = self.storage.read_sheet("Users")
            logger.info(f"Current users count: {len(users_df)}")
            
            if not users_df.empty:
                if user_id in users_df['user_id'].values:
                    raise ValueError("User ID already taken")
                # Only check email if provided
                if email and email in users_df['email'].values:
                    raise ValueError("Email already registered")
            
            # Validate inputs
            if email and not self._validate_email(email):
                raise ValueError("Invalid email format")
            
            if len(password) < 6:
                raise ValueError("Password must be at least 6 characters")
            
            if role.lower() not in ["admin", "user"]:
                raise ValueError("Invalid role")
            
            logger.info("Using plain text password storage")
            
            # Create user record matching CZ_MasterSheet schema
            user_data = {
                "user_id": user_id,
                "email": email or "",  # Optional email
                "password_hash": "",  # Keep empty since we're not using hashing
                "plain_password": password,  # Store plain password
                "role": role.lower(),
                "name": name or user_id,
                "created_at": get_ist_now().isoformat(),
                "is_active": True
            }
            
            logger.info(f"User data prepared: {user_data}")
            self.storage.append_row("Users", user_data)
            logger.info(f"User appended to storage successfully")
            logger.info(f"User created: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating account: {e}")
            raise
    
    def authenticate(self, user_id: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with user_id and plain text password"""
        try:
            users_df = self.storage.read_sheet("Users")
            
            if users_df.empty:
                logger.info("No users found in database")
                return None
            
            # Clean up user_id input and database values
            clean_user_id = user_id.strip()
            users_df['user_id'] = users_df['user_id'].astype(str).str.strip()
            
            # Find user by user_id only
            user_rows = users_df[users_df['user_id'] == clean_user_id]
            
            if user_rows.empty:
                logger.info(f"User {clean_user_id} not found in database")
                return None
            
            user_row = user_rows.iloc[0]
            stored_password = user_row.get('plain_password', '')
            
            logger.info(f"User {clean_user_id} found. Has plain_password: {bool(stored_password)}")
            logger.info(f"Stored password length: {len(stored_password) if stored_password else 0}")
            logger.info(f"Input password length: {len(password)}")
            
            # Verify password - simple string comparison
            if password == stored_password:
                logger.info(f"Password match successful for user {clean_user_id}")
                return {
                    "email": user_row['email'],
                    "user_id": user_row['user_id'].strip(),
                    "role": user_row['role'],
                    "name": user_row.get('name', user_row['user_id']).strip(),
                    "created_at": user_row['created_at'],
                    "is_active": user_row.get('is_active', True)
                }
            else:
                logger.info(f"Password mismatch for user {clean_user_id}")
            
            return None
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None
    
    def update_user_to_plain_password(self, user_id: str, new_password: str) -> bool:
        """Update existing user to use plain password authentication"""
        try:
            def filter_fn(row):
                return row.get('user_id') == user_id
            
            def update_fn(row):
                row['plain_password'] = new_password
                row['password_hash'] = ""  # Clear any old hash
                return row
            
            updated_count = self.storage.update_rows("Users", filter_fn, update_fn)
            
            if updated_count > 0:
                logger.info(f"Updated user {user_id} to use plain password")
                return True
            else:
                logger.error(f"User {user_id} not found for update")
                return False
                
        except Exception as e:
            logger.error(f"Error updating user password: {e}")
            return False
    
    def login(self, user_id: str, password: str) -> bool:
        """Login user and set session state"""
        user = self.authenticate(user_id, password)
        
        if user:
            st.session_state.authenticated = True
            st.session_state.user = user
            st.session_state.user['login_time'] = get_ist_now().isoformat()
            logger.info(f"User logged in: {user['user_id']}")
            return True
        
        return False
    
    def logout(self):
        """Clear user session"""
        if 'user' in st.session_state and st.session_state.user:
            logger.info(f"User logged out: {st.session_state.user['user_id']}")
        
        # Clear session state
        for key in ['authenticated', 'user', 'selected_page']:
            if key in st.session_state:
                del st.session_state[key]
        
        # Clear session persistence parameters
        params_to_clear = ['session', 'user_email']
        for param in params_to_clear:
            if param in st.query_params:
                del st.query_params[param]
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get currently logged in user"""
        if st.session_state.get('authenticated', False):
            return st.session_state.get('user')
        return None
    
    def is_admin(self, user: Optional[Dict[str, Any]] = None) -> bool:
        """Check if current user or provided user is admin"""
        if user is None:
            user = self.get_current_user()
        
        return user is not None and user.get('role', '').lower() == 'admin'
    
    def require_auth(self):
        """Decorator/helper to require authentication"""
        if not st.session_state.get('authenticated', False):
            st.error("Please log in to access this page")
            st.stop()
    
    def require_admin(self):
        """Decorator/helper to require admin role"""
        self.require_auth()
        
        user = self.get_current_user()
        if not self.is_admin(user):
            st.error("Admin access required")
            st.stop()
    
    def get_all_users(self) -> pd.DataFrame:
        """Get all users (admin only, excluding password hashes)"""
        users_df = self.storage.read_sheet("Users")
        
        if not users_df.empty:
            # Remove password_hash column for security
            return users_df.drop(columns=['password_hash'], errors='ignore')
        
        return users_df
    
    def update_user_role(self, user_id: str, new_role: str) -> bool:
        """Update user role (admin only)"""
        if new_role.lower() not in ["admin", "user"]:
            raise ValueError("Invalid role")
        
        def filter_fn(row):
            return row['user_id'] == user_id
        
        def update_fn(row):
            row['role'] = new_role.lower()
            return row
        
        updated_count = self.storage.update_rows("Users", filter_fn, update_fn)
        
        if updated_count > 0:
            logger.info(f"Updated role for user {user_id} to {new_role}")
            return True
        
        return False
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            users_df = self.storage.read_sheet("Users")
            user_rows = users_df[users_df['user_id'] == user_id]
            
            if user_rows.empty:
                raise ValueError("User not found")
            
            user_row = user_rows.iloc[0]
            stored_password = user_row.get('plain_password', '')
            
            # Verify old password
            if old_password != stored_password:
                raise ValueError("Current password is incorrect")
            
            # Validate new password
            if len(new_password) < 6:
                raise ValueError("New password must be at least 6 characters")
            
            # Update password
            def filter_fn(row):
                return row['user_id'] == user_id
            
            def update_fn(row):
                row['plain_password'] = new_password
                row['password_hash'] = ""  # Clear hash field since we're not using it
                return row
            
            updated_count = self.storage.update_rows("Users", filter_fn, update_fn)
            
            if updated_count > 0:
                logger.info(f"Password changed for user: {user_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            raise
    
    def _validate_email(self, email: str) -> bool:
        """Simple email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get user statistics for admin dashboard"""
        try:
            users_df = self.storage.read_sheet("Users")
            
            if users_df.empty:
                return {
                    "total_users": 0,
                    "admin_count": 0,
                    "user_count": 0,
                    "recent_registrations": 0
                }
            
            stats = {
                "total_users": len(users_df),
                "admin_count": len(users_df[users_df['role'] == 'admin']),
                "user_count": len(users_df[users_df['role'] == 'user']),
                "recent_registrations": 0
            }
            
            # Count recent registrations (last 7 days)
            if 'created_at' in users_df.columns:
                from datetime import timedelta
                week_ago = get_ist_now() - timedelta(days=7)
                
                users_df['created_at'] = pd.to_datetime(users_df['created_at'])
                recent_users = users_df[users_df['created_at'] > week_ago]
                stats["recent_registrations"] = len(recent_users)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {
                "total_users": 0,
                "admin_count": 0,
                "user_count": 0,
                "recent_registrations": 0
            }