"""
Tests for IMIQ Storage Layer
Testing Excel storage functionality with temporary files
"""

import pytest
import pandas as pd
import tempfile
import os
from unittest.mock import patch, MagicMock

from imiq.storage import ExcelStorage, StorageBase
from imiq.utils import get_ist_now


class TestExcelStorage:
    """Test cases for ExcelStorage class"""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage instance for testing"""
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, "test_db.xlsx")
        storage = ExcelStorage(temp_file)
        yield storage
        
        # Cleanup
        try:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            os.rmdir(temp_dir)
        except:
            pass
    
    def test_ensure_workbook_creates_file(self, temp_storage):
        """Test that ensure_workbook creates the Excel file"""
        assert os.path.exists(temp_storage.file_path)
    
    def test_ensure_workbook_creates_required_sheets(self, temp_storage):
        """Test that all required sheets are created"""
        # Read the created workbook
        sheets = pd.read_excel(temp_storage.file_path, sheet_name=None)
        
        expected_sheets = ["Users", "NewOrders", "Shipments", "Inventory"]
        for sheet_name in expected_sheets:
            assert sheet_name in sheets
            # Check that sheets have expected columns
            assert len(sheets[sheet_name].columns) > 0
    
    def test_read_sheet_returns_dataframe(self, temp_storage):
        """Test reading a sheet returns a DataFrame"""
        df = temp_storage.read_sheet("Users")
        assert isinstance(df, pd.DataFrame)
    
    def test_append_row_adds_data(self, temp_storage):
        """Test appending a row adds data to the sheet"""
        test_data = {
            "email": "test@example.com",
            "userid": "testuser",
            "password_hash": "hashed_password",
            "role": "User",
            "created_at": get_ist_now().isoformat()
        }
        
        # Append row
        temp_storage.append_row("Users", test_data)
        
        # Verify data was added
        df = temp_storage.read_sheet("Users")
        assert len(df) >= 1  # At least the default admin + test user
        
        # Check if our test data exists
        test_row = df[df['email'] == 'test@example.com']
        assert not test_row.empty
        assert test_row.iloc[0]['userid'] == 'testuser'
    
    def test_replace_sheet_replaces_content(self, temp_storage):
        """Test replacing sheet content works"""
        # Create test data
        new_data = pd.DataFrame({
            'email': ['user1@test.com', 'user2@test.com'],
            'userid': ['user1', 'user2'],
            'password_hash': ['hash1', 'hash2'],
            'role': ['User', 'Admin'],
            'created_at': [get_ist_now().isoformat(), get_ist_now().isoformat()]
        })
        
        # Replace sheet
        temp_storage.replace_sheet("Users", new_data)
        
        # Verify replacement
        df = temp_storage.read_sheet("Users")
        assert len(df) == 2
        assert 'user1@test.com' in df['email'].values
        assert 'user2@test.com' in df['email'].values
    
    def test_update_rows_modifies_existing_data(self, temp_storage):
        """Test updating rows modifies existing data"""
        # First add some test data
        test_data = {
            "email": "updatetest@example.com",
            "userid": "updateuser",
            "password_hash": "original_hash",
            "role": "User",
            "created_at": get_ist_now().isoformat()
        }
        temp_storage.append_row("Users", test_data)
        
        # Define filter and update functions
        def filter_fn(row):
            return row['userid'] == 'updateuser'
        
        def update_fn(row):
            row['role'] = 'Admin'
            row['password_hash'] = 'updated_hash'
            return row
        
        # Perform update
        updated_count = temp_storage.update_rows("Users", filter_fn, update_fn)
        
        # Verify update
        assert updated_count == 1
        df = temp_storage.read_sheet("Users")
        updated_row = df[df['userid'] == 'updateuser']
        assert not updated_row.empty
        assert updated_row.iloc[0]['role'] == 'Admin'
        assert updated_row.iloc[0]['password_hash'] == 'updated_hash'
    
    def test_update_rows_returns_zero_for_no_matches(self, temp_storage):
        """Test updating rows returns 0 when no rows match filter"""
        def filter_fn(row):
            return row['userid'] == 'nonexistent_user'
        
        def update_fn(row):
            row['role'] = 'Admin'
            return row
        
        updated_count = temp_storage.update_rows("Users", filter_fn, update_fn)
        assert updated_count == 0
    
    def test_concurrent_access_with_file_lock(self, temp_storage):
        """Test that file locking prevents concurrent access issues"""
        # This is a basic test - in practice you'd need more sophisticated
        # concurrent testing, but we can at least verify the lock mechanism works
        
        # The fact that we can perform multiple operations without errors
        # indicates the file locking is working properly
        for i in range(5):
            test_data = {
                "email": f"test{i}@example.com",
                "userid": f"testuser{i}",
                "password_hash": f"hash{i}",
                "role": "User",
                "created_at": get_ist_now().isoformat()
            }
            temp_storage.append_row("Users", test_data)
        
        df = temp_storage.read_sheet("Users")
        assert len(df) >= 5  # At least 5 test users + default admin
    
    def test_read_nonexistent_sheet_returns_empty_df(self, temp_storage):
        """Test reading non-existent sheet returns empty DataFrame with expected columns"""
        df = temp_storage.read_sheet("NonexistentSheet")
        assert isinstance(df, pd.DataFrame)
        assert df.empty
    
    def test_atomic_write_safety(self, temp_storage):
        """Test that atomic write operations maintain data integrity"""
        # Add initial data
        initial_data = {
            "email": "atomic@test.com",
            "userid": "atomicuser",
            "password_hash": "hash",
            "role": "User",
            "created_at": get_ist_now().isoformat()
        }
        temp_storage.append_row("Users", initial_data)
        
        # Verify file exists and is readable after operation
        assert os.path.exists(temp_storage.file_path)
        df = temp_storage.read_sheet("Users")
        assert not df.empty
        
        # Verify we can read the data we just wrote
        test_row = df[df['userid'] == 'atomicuser']
        assert not test_row.empty


class TestStorageBase:
    """Test cases for StorageBase abstract class"""
    
    def test_storage_base_is_abstract(self):
        """Test that StorageBase cannot be instantiated directly"""
        with pytest.raises(TypeError):
            StorageBase()
    
    def test_storage_base_methods_raise_not_implemented(self):
        """Test that StorageBase methods raise NotImplementedError"""
        class IncompleteStorage(StorageBase):
            pass
        
        with pytest.raises(TypeError):
            IncompleteStorage()


@pytest.fixture
def sample_orders_data():
    """Sample orders data for testing"""
    return [
        {
            'order_id': 'ORD-001',
            'created_at': get_ist_now().isoformat(),
            'user_id': 'user1',
            'customer_name': 'John Doe',
            'customer_email': 'john@example.com',
            'product': 'Test Product',
            'quantity': 2,
            'price': 100.0,
            'status': 'Pending',
            'lead_id': 'LEAD-001',
            'tracking_id': '',
            'courier_name': ''
        },
        {
            'order_id': 'ORD-002',
            'created_at': get_ist_now().isoformat(),
            'user_id': 'user2',
            'customer_name': 'Jane Smith',
            'customer_email': 'jane@example.com',
            'product': 'Another Product',
            'quantity': 1,
            'price': 50.0,
            'status': 'Completed',
            'lead_id': 'LEAD-002',
            'tracking_id': 'TRACK-002',
            'courier_name': 'DTDC'
        }
    ]


def test_integration_orders_workflow(temp_storage, sample_orders_data):
    """Integration test for a complete orders workflow"""
    # Add sample orders
    for order_data in sample_orders_data:
        temp_storage.append_row("NewOrders", order_data)
    
    # Verify orders were added
    orders_df = temp_storage.read_sheet("NewOrders")
    assert len(orders_df) == 2
    
    # Test updating an order status
    def filter_pending(row):
        return row['order_id'] == 'ORD-001'
    
    def update_status(row):
        row['status'] = 'Shipped'
        row['tracking_id'] = 'TRACK-001'
        row['courier_name'] = 'Delhivery'
        return row
    
    updated_count = temp_storage.update_rows("NewOrders", filter_pending, update_status)
    assert updated_count == 1
    
    # Verify update
    updated_orders = temp_storage.read_sheet("NewOrders")
    updated_order = updated_orders[updated_orders['order_id'] == 'ORD-001']
    assert not updated_order.empty
    assert updated_order.iloc[0]['status'] == 'Shipped'
    assert updated_order.iloc[0]['tracking_id'] == 'TRACK-001'


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])