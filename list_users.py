"""
List all users in the database
"""
from imiq.storage import get_storage_instance

def list_users():
    """List all users"""
    try:
        storage = get_storage_instance()
        users_df = storage.read_sheet("Users")
        
        if users_df.empty:
            print("❌ No users found in database")
            return
        
        print(f"✅ Found {len(users_df)} users:")
        print("-" * 50)
        
        for index, user in users_df.iterrows():
            user_id = user.get('user_id', 'N/A')
            role = user.get('role', 'N/A')
            name = user.get('name', 'N/A')
            has_plain_password = bool(user.get('plain_password', ''))
            has_password_hash = bool(user.get('password_hash', ''))
            
            print(f"User ID: {user_id}")
            print(f"  Name: {name}")
            print(f"  Role: {role}")
            print(f"  Has plain password: {has_plain_password}")
            print(f"  Has password hash: {has_password_hash}")
            if has_plain_password:
                plain_pwd = user.get('plain_password', '')
                print(f"  Plain password: {plain_pwd}")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Error listing users: {e}")

if __name__ == "__main__":
    list_users()