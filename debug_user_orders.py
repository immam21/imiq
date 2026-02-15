"""
Debug orders for a specific user
"""
from imiq.storage import get_storage_instance
from imiq.orders import OrderService

def debug_user_orders():
    """Debug user orders for Sowmiya01"""
    
    # Initialize storage and orders service
    storage = get_storage_instance()
    orders_service = OrderService(storage)
    
    user_id = "Sowmiya01"
    
    print(f"🔍 Debugging orders for user: {user_id}")
    print("=" * 50)
    
    # Get raw orders data
    try:
        raw_orders_df = storage.read_sheet("NewOrders")
        print(f"📊 Total orders in sheet: {len(raw_orders_df)}")
        
        if raw_orders_df.empty:
            print("❌ No orders found in NewOrders sheet")
            return
        
        print(f"📋 Columns in NewOrders: {list(raw_orders_df.columns)}")
        
        # Check created_by column
        if 'created_by' in raw_orders_df.columns:
            created_by_values = raw_orders_df['created_by'].value_counts()
            print(f"\n🏷️ created_by values:")
            for value, count in created_by_values.items():
                print(f"  '{value}': {count} orders")
                
            # Check for user specifically
            user_orders_raw = raw_orders_df[raw_orders_df['created_by'] == user_id]
            user_orders_raw_stripped = raw_orders_df[raw_orders_df['created_by'].astype(str).str.strip() == user_id.strip()]
            
            print(f"\n👤 Orders for '{user_id}' (exact match): {len(user_orders_raw)}")
            print(f"👤 Orders for '{user_id}' (stripped match): {len(user_orders_raw_stripped)}")
            
            # Show recent orders for the user
            if not user_orders_raw_stripped.empty and 'timestamp' in user_orders_raw_stripped.columns:
                user_orders_raw_stripped['timestamp'] = user_orders_raw_stripped['timestamp'].astype(str)
                print(f"\n📅 Recent orders for {user_id}:")
                recent_orders = user_orders_raw_stripped.sort_values('timestamp', ascending=False).head(10)
                for idx, order in recent_orders.iterrows():
                    timestamp = order.get('timestamp', 'N/A')
                    order_id = order.get('order_id', 'N/A')
                    customer_name = order.get('customer_name', 'N/A')
                    print(f"  {timestamp}: {order_id} - {customer_name}")
        else:
            print("❌ No 'created_by' column found in NewOrders sheet")
            print("Available columns:", list(raw_orders_df.columns))
            
        # Test orders service
        print(f"\n🔧 Testing OrderService.get_user_orders():")
        user_orders_service = orders_service.get_user_orders(user_id)
        print(f"Orders returned by service: {len(user_orders_service)}")
        
        if not user_orders_service.empty:
            print("Service orders (first 5):")
            for idx, order in user_orders_service.head().iterrows():
                timestamp = order.get('timestamp', 'N/A')
                order_id = order.get('order_id', 'N/A')
                customer_name = order.get('customer_name', 'N/A')
                print(f"  {timestamp}: {order_id} - {customer_name}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_user_orders()