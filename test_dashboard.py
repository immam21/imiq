"""
Test dashboard functionality for Sowmiya01
"""
from imiq.storage import get_storage_instance
from imiq.orders import OrderService
from imiq.auth import AuthService

def test_dashboard():
    """Test dashboard data loading"""
    
    # Initialize services
    storage = get_storage_instance()
    orders_service = OrderService(storage)
    auth_service = AuthService(storage)
    
    user_id = "Sowmiya01"
    
    print(f"🔍 Testing dashboard for user: {user_id}")
    print("=" * 50)
    
    try:
        # Simulate user data
        user = {
            'user_id': user_id,
            'role': 'user'
        }
        
        # Test orders retrieval (same as dashboard)
        print("📊 Testing orders retrieval...")
        is_user = user.get('role', '').lower() == 'user'
        orders_df = orders_service.get_user_orders(user['user_id']) if is_user else orders_service.get_all_orders()
        
        print(f"Orders found: {len(orders_df)}")
        
        if orders_df.empty:
            print("❌ Orders DataFrame is empty - this would cause dashboard to be empty")
            return
        
        print("✅ Orders loaded successfully")
        
        # Test KPI generation
        print("\n📈 Testing KPI generation...")
        try:
            from kpis import generate_full_kpi_report
            full_kpi_report = generate_full_kpi_report(orders_df)
            print("✅ KPI generation successful")
            
            # Show some basic KPI info
            core_kpis = full_kpi_report.get('core_kpis', {})
            print(f"Total orders: {core_kpis.get('total_orders', 'N/A')}")
            print(f"Total revenue: {core_kpis.get('total_revenue', 'N/A')}")
            
        except Exception as kpi_error:
            print(f"❌ KPI generation failed: {kpi_error}")
            import traceback
            traceback.print_exc()
        
        # Test date parsing in orders
        print("\n📅 Testing timestamp parsing...")
        if 'timestamp' in orders_df.columns:
            try:
                import pandas as pd
                orders_df['Order Date'] = pd.to_datetime(orders_df['timestamp'], errors='coerce').dt.date
                unique_dates = orders_df['Order Date'].nunique()
                print(f"✅ Timestamp parsing successful - {unique_dates} unique dates found")
            except Exception as date_error:
                print(f"❌ Date parsing failed: {date_error}")
        else:
            print("❌ No timestamp column found")
            
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dashboard()