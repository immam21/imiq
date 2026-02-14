"""
Tests for IMIQ Authentication Service
Testing user authentication, registration, and session management
"""

import pytest
import bcrypt
import tempfile
import os
from unittest.mock import patch, MagicMock
import streamlit as st

from imiq.auth import AuthService
from imiq.storage import ExcelStorage
from imiq.utils import get_ist_now


class TestAuthService:
    """Test cases for AuthService class"""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage instance for testing"""
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, "test_auth_db.xlsx")
        storage = ExcelStorage(temp_file)
        yield storage
        
        # Cleanup
        try:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            os.rmdir(temp_dir)
        except:
            pass
    
    @pytest.fixture
    def auth_service(self, temp_storage):
        """Create AuthService instance with temporary storage"""
        return AuthService(temp_storage)
    
    @pytest.fixture(autouse=True)
    def clear_streamlit_session(self):
        """Clear streamlit session state before each test"""
        # Mock streamlit session_state
        with patch.object(st, 'session_state', {}):
            yield
    
    def test_create_account_success(self, auth_service):
        """Test successful account creation"""
        result = auth_service.create_account(
            email="testuser@example.com",
            userid="testuser123",
            password="securepassword",
            role="User"
        )
        
        assert result is True
        
        # Verify user was created
        users_df = auth_service.storage.read_sheet("Users")
        test_user = users_df[users_df['email'] == 'testuser@example.com']
        assert not test_user.empty
        assert test_user.iloc[0]['userid'] == 'testuser123'
        assert test_user.iloc[0]['role'] == 'User'
        
        # Verify password was hashed
        stored_hash = test_user.iloc[0]['password_hash']
        assert bcrypt.checkpw("securepassword".encode('utf-8'), stored_hash.encode('utf-8'))
    
    def test_create_account_duplicate_email(self, auth_service):
        """Test account creation with duplicate email fails"""
        # Create first account
        auth_service.create_account(
            email="duplicate@example.com",
            userid="user1",
            password="password123"
        )
        
        # Try to create second account with same email
        with pytest.raises(ValueError, match="Email already registered"):
            auth_service.create_account(
                email="duplicate@example.com",
                userid="user2",
                password="password123"
            )
    
    def test_create_account_duplicate_userid(self, auth_service):
        """Test account creation with duplicate user ID fails"""
        # Create first account
        auth_service.create_account(
            email="user1@example.com",
            userid="duplicateid",
            password="password123"
        )
        
        # Try to create second account with same user ID
        with pytest.raises(ValueError, match="User ID already taken"):
            auth_service.create_account(
                email="user2@example.com",
                userid="duplicateid",
                password="password123"
            )
    
    def test_create_account_invalid_email(self, auth_service):
        """Test account creation with invalid email fails"""
        with pytest.raises(ValueError, match="Invalid email format"):
            auth_service.create_account(
                email="invalid-email",
                userid="testuser",
                password="password123"
            )
    
    def test_create_account_short_password(self, auth_service):
        """Test account creation with short password fails"""
        with pytest.raises(ValueError, match="Password must be at least 6 characters"):
            auth_service.create_account(
                email="test@example.com",
                userid="testuser",
                password="12345"  # Only 5 characters
            )
    
    def test_create_account_invalid_role(self, auth_service):
        """Test account creation with invalid role fails"""
        with pytest.raises(ValueError, match="Invalid role"):
            auth_service.create_account(
                email="test@example.com",
                userid="testuser",
                password="password123",
                role="InvalidRole"
            )
    
    def test_authenticate_success(self, auth_service):
        """Test successful authentication"""
        # Create test account
        auth_service.create_account(
            email="auth@example.com",
            userid="authuser",
            password="testpassword123",
            role="Admin"
        )
        
        # Authenticate
        user = auth_service.authenticate("auth@example.com", "testpassword123")
        
        assert user is not None
        assert user['email'] == "auth@example.com"
        assert user['userid'] == "authuser"
        assert user['role'] == "Admin"
        assert 'created_at' in user
    
    def test_authenticate_wrong_password(self, auth_service):
        """Test authentication with wrong password fails"""
        # Create test account
        auth_service.create_account(
            email="auth@example.com",
            userid="authuser",
            password="correctpassword"
        )
        
        # Try to authenticate with wrong password
        user = auth_service.authenticate("auth@example.com", "wrongpassword")
        assert user is None
    
    def test_authenticate_nonexistent_user(self, auth_service):
        """Test authentication with non-existent user fails"""
        user = auth_service.authenticate("nonexistent@example.com", "password123")
        assert user is None
    
    @patch('streamlit.session_state', {})
    def test_login_success(self, auth_service):
        """Test successful login sets session state"""
        # Create test account
        auth_service.create_account(
            email="login@example.com",
            userid="loginuser",
            password="loginpassword"
        )
        
        # Mock streamlit session_state
        mock_session = {}
        with patch.object(st, 'session_state', mock_session):
            result = auth_service.login("login@example.com", "loginpassword")
            
            assert result is True
            assert mock_session['authenticated'] is True
            assert mock_session['user']['email'] == "login@example.com"
            assert mock_session['user']['userid'] == "loginuser"
            assert 'login_time' in mock_session['user']
    
    @patch('streamlit.session_state', {})
    def test_login_failure(self, auth_service):
        """Test failed login does not set session state"""
        mock_session = {}
        with patch.object(st, 'session_state', mock_session):
            result = auth_service.login("nonexistent@example.com", "wrongpassword")
            
            assert result is False
            assert 'authenticated' not in mock_session
            assert 'user' not in mock_session
    
    @patch('streamlit.session_state', {'authenticated': True, 'user': {'userid': 'testuser'}})
    def test_logout_clears_session(self, auth_service):
        """Test logout clears session state"""
        mock_session = {'authenticated': True, 'user': {'userid': 'testuser'}}
        
        with patch.object(st, 'session_state', mock_session):
            auth_service.logout()
            
            assert 'authenticated' not in mock_session
            assert 'user' not in mock_session
    
    @patch('streamlit.session_state', {'authenticated': True, 'user': {'userid': 'user1', 'role': 'User'}})
    def test_get_current_user(self, auth_service):
        """Test getting current user from session"""
        mock_session = {'authenticated': True, 'user': {'userid': 'user1', 'role': 'User'}}
        
        with patch.object(st, 'session_state', mock_session):
            user = auth_service.get_current_user()
            
            assert user is not None
            assert user['userid'] == 'user1'
            assert user['role'] == 'User'
    
    @patch('streamlit.session_state', {})
    def test_get_current_user_not_authenticated(self, auth_service):
        """Test getting current user when not authenticated returns None"""
        mock_session = {}
        
        with patch.object(st, 'session_state', mock_session):
            user = auth_service.get_current_user()
            assert user is None
    
    def test_is_admin_true(self, auth_service):
        """Test is_admin returns True for admin user"""
        admin_user = {'role': 'Admin'}
        assert auth_service.is_admin(admin_user) is True
    
    def test_is_admin_false(self, auth_service):
        """Test is_admin returns False for non-admin user"""
        regular_user = {'role': 'User'}
        assert auth_service.is_admin(regular_user) is False
    
    def test_is_admin_none_user(self, auth_service):
        """Test is_admin returns False for None user"""
        assert auth_service.is_admin(None) is False
    
    def test_update_user_role_success(self, auth_service):
        """Test successful user role update"""
        # Create test user
        auth_service.create_account(
            email="roletest@example.com",
            userid="roleuser",
            password="password123",
            role="User"
        )
        
        # Update role to Admin
        result = auth_service.update_user_role("roleuser", "Admin")
        assert result is True
        
        # Verify role was updated
        users_df = auth_service.storage.read_sheet("Users")
        updated_user = users_df[users_df['userid'] == 'roleuser']
        assert not updated_user.empty
        assert updated_user.iloc[0]['role'] == 'Admin'
    
    def test_update_user_role_invalid_role(self, auth_service):
        """Test user role update with invalid role fails"""
        with pytest.raises(ValueError, match="Invalid role"):
            auth_service.update_user_role("someuser", "InvalidRole")
    
    def test_update_user_role_nonexistent_user(self, auth_service):
        """Test user role update for nonexistent user returns False"""
        result = auth_service.update_user_role("nonexistent", "Admin")
        assert result is False
    
    def test_change_password_success(self, auth_service):
        """Test successful password change"""
        # Create test user
        auth_service.create_account(
            email="pwchange@example.com",
            userid="pwuser",
            password="oldpassword123"
        )
        
        # Change password
        result = auth_service.change_password("pwuser", "oldpassword123", "newpassword456")
        assert result is True
        
        # Verify new password works
        user = auth_service.authenticate("pwchange@example.com", "newpassword456")
        assert user is not None
        
        # Verify old password no longer works
        user = auth_service.authenticate("pwchange@example.com", "oldpassword123")
        assert user is None
    
    def test_change_password_wrong_old_password(self, auth_service):
        """Test password change with wrong old password fails"""
        # Create test user
        auth_service.create_account(
            email="pwfail@example.com",
            userid="pwfailuser",
            password="correctpassword"
        )
        
        # Try to change with wrong old password
        with pytest.raises(ValueError, match="Current password is incorrect"):
            auth_service.change_password("pwfailuser", "wrongoldpassword", "newpassword")
    
    def test_change_password_short_new_password(self, auth_service):
        """Test password change with short new password fails"""
        # Create test user
        auth_service.create_account(
            email="pwshort@example.com",
            userid="pwshortuser",
            password="correctpassword"
        )
        
        # Try to change to short password
        with pytest.raises(ValueError, match="New password must be at least 6 characters"):
            auth_service.change_password("pwshortuser", "correctpassword", "12345")
    
    def test_get_all_users_excludes_password_hash(self, auth_service):
        """Test get_all_users excludes password hash column"""
        # Create test users
        auth_service.create_account("user1@test.com", "user1", "password123")
        auth_service.create_account("user2@test.com", "user2", "password456")
        
        # Get all users
        users_df = auth_service.get_all_users()
        
        assert not users_df.empty
        assert 'password_hash' not in users_df.columns
        assert 'email' in users_df.columns
        assert 'userid' in users_df.columns
        assert 'role' in users_df.columns
    
    def test_get_user_stats(self, auth_service):
        """Test getting user statistics"""
        # Create test users with different roles
        auth_service.create_account("admin1@test.com", "admin1", "password", "Admin")
        auth_service.create_account("user1@test.com", "user1", "password", "User")
        auth_service.create_account("user2@test.com", "user2", "password", "User")
        
        stats = auth_service.get_user_stats()
        
        assert stats['total_users'] >= 3  # Including default admin
        assert stats['admin_count'] >= 2  # Including default admin + test admin
        assert stats['user_count'] >= 2  # Test users
        assert 'recent_registrations' in stats


@pytest.fixture
def mock_bcrypt():
    """Mock bcrypt for testing without actual hashing"""
    with patch('imiq.auth.bcrypt') as mock:
        # Mock hashpw to return a predictable hash
        mock.hashpw.return_value = b'mocked_hash'
        # Mock checkpw to return True for correct password
        mock.checkpw.return_value = True
        yield mock


def test_password_hashing_integration(auth_service):
    """Integration test for password hashing"""
    # Create account
    auth_service.create_account(
        email="hashtest@example.com",
        userid="hashuser",
        password="testpassword123"
    )
    
    # Verify the stored hash is different from the original password
    users_df = auth_service.storage.read_sheet("Users")
    user_row = users_df[users_df['userid'] == 'hashuser']
    stored_hash = user_row.iloc[0]['password_hash']
    
    # Hash should not equal original password
    assert stored_hash != "testpassword123"
    
    # But authentication should work
    user = auth_service.authenticate("hashtest@example.com", "testpassword123")
    assert user is not None


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])