#!/usr/bin/env python3

import bcrypt
from imiq.storage import ExcelStorage
import pandas as pd

def fix_imam_password():
    """Fix imam21 password hash in Excel"""
    
    # Generate proper hash
    plain_password = 'Iqrit@2024'
    proper_hash = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    print(f'Generated proper hash: {proper_hash}')
    
    # Update the Excel file
    storage = ExcelStorage('CZ_MasterSheet.xlsx')
    
    def update_imam_password(row):
        if row['user_id'] == 'imam21':
            row['password_hash'] = proper_hash
        return row
    
    # Read Users sheet
    users_df = storage.read_sheet('Users')
    imam_before = users_df[users_df['user_id'] == 'imam21'].iloc[0]
    print(f'Before update - imam21 hash: {imam_before["password_hash"]}')
    
    # Update the password hash
    updated_users_df = users_df.apply(update_imam_password, axis=1)
    
    # Replace the entire Users sheet
    storage.replace_sheet('Users', updated_users_df)
    print('✅ Updated imam21 password hash in Excel')
    
    # Verify the update
    users_df = storage.read_sheet('Users')
    imam_user = users_df[users_df['user_id'] == 'imam21'].iloc[0]
    print(f'After update - imam21 hash: {imam_user["password_hash"][:30]}...')
    print(f'Hash length: {len(imam_user["password_hash"])}')
    
    # Test the hash works
    is_valid = bcrypt.checkpw(plain_password.encode('utf-8'), imam_user['password_hash'].encode('utf-8'))
    print(f'Hash verification test: {is_valid}')
    
    return is_valid

if __name__ == "__main__":
    fix_imam_password()