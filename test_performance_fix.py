"""
Test performance tab fixes
"""
import pandas as pd
from datetime import date, timedelta

def test_datetime_parsing():
    """Test datetime parsing with mixed formats"""
    
    # Create test data with mixed timestamp formats
    test_data = {
        'timestamp': [
            '2026-02-14T10:41:35.583074',
            '2026-02-13T16:08:24.056359', 
            '2026-02-12T12:58:26.708Z',
            '2026-02-11T15:30:00',
            'invalid_date'
        ],
        'created_by': ['Sowmiya01', 'Sowmiya01 ', 'Aamina10', 'Imam21', 'Azar03']
    }
    
    df = pd.DataFrame(test_data)
    print("Original data:")
    print(df)
    print("\nTesting datetime parsing...")
    
    try:
        # Apply the same logic as in the fixed code
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce', utc=True)
        
        if df['timestamp'].notna().any():
            df['date'] = df['timestamp'].dt.date
            print("✅ Datetime parsing successful!")
            print("Parsed dates:")
            print(df[['timestamp', 'date']])
        else:
            print("❌ No valid timestamps found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test user ID matching with strip
    print("\nTesting user ID matching...")
    df['created_by'] = df['created_by'].astype(str).str.strip()
    user_id = "Sowmiya01"
    clean_user_id = str(user_id).strip()
    
    matches = df[df['created_by'] == clean_user_id]
    print(f"Matches for '{user_id}': {len(matches)} rows")
    print(matches[['created_by']])

if __name__ == "__main__":
    test_datetime_parsing()