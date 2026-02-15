#!/usr/bin/env python3
"""Test date-wise business analytics functionality"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_date_analytics():
    """Test the date-wise analytics"""
    print("🧪 Testing Date-wise Business Analytics...")
    
    try:
        from datetime import date
        from imiq.business_analytics import get_business_analytics_instance
        from imiq.storage import get_storage_instance
        
        # Initialize storage and analytics
        storage = get_storage_instance()
        analytics = get_business_analytics_instance(storage)
        
        # Test single date analytics
        test_date = date(2026, 2, 13)
        print(f"Testing analytics for {test_date}...")
        
        result = analytics.get_comprehensive_date_analytics(test_date)
        
        print("✅ Analytics generated successfully!")
        print(f"Date: {result['date']}")
        print(f"Orders: {result['orders']['order_count']}")
        print(f"Revenue: ₹{result['orders']['total_amount']:,.2f}")
        print(f"Ad Spend: ₹{result['revenue']['ad_spend']:,.2f}")
        print(f"Net Profit: ₹{result['analytics']['net_profit_after_expenses']:,.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_date_analytics()