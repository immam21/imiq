"""
IMIQ KPI Analytics Module
========================

Production-ready KPI calculation module for IMIQ Streamlit application.

HOW TO INTEGRATE INTO STREAMLIT:
-------------------------------
from kpis import generate_full_kpi_report, get_core_order_kpis

# In your Streamlit app:
orders_df = load_orders_data()  # Your existing data loading
performance_df = load_performance_data()

# Get all KPIs at once
full_report = generate_full_kpi_report(orders_df, performance_df)

# Or get specific KPIs
core_kpis = get_core_order_kpis(orders_df)
st.metric("Total Orders", core_kpis['total_orders'])
st.metric("Total Revenue", f"₹{core_kpis['total_revenue']:,.2f}")

FEATURES:
--------
- Handles empty DataFrames safely
- Defensive column checking
- Timezone Asia/Kolkata support
- Optimized with groupby operations
- Type hints and comprehensive docstrings
- No Streamlit dependencies (pure analytics)

Author: GitHub Copilot
Version: 1.0
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import pytz

# Set timezone
IST = pytz.timezone('Asia/Kolkata')

def _safe_column_check(df: pd.DataFrame, required_columns: list) -> list:
    """
    Safely check which required columns exist in the DataFrame.
    
    Args:
        df: Input DataFrame
        required_columns: List of column names to check
    
    Returns:
        List of existing columns
    """
    if df is None or df.empty:
        return []
    return [col for col in required_columns if col in df.columns]

def _safe_sum(series: pd.Series) -> float:
    """Safely sum a series, handling NaN values and string conversion."""
    if series.empty:
        return 0.0
    try:
        # Convert to numeric, replacing invalid values with 0
        numeric_series = pd.to_numeric(series, errors='coerce').fillna(0)
        return float(numeric_series.sum())
    except Exception:
        return 0.0

def _safe_mean(series: pd.Series) -> float:
    """Safely calculate mean of a series, handling NaN values and string conversion."""
    if series.empty:
        return 0.0
    try:
        # Convert to numeric, replacing invalid values with 0
        numeric_series = pd.to_numeric(series, errors='coerce').fillna(0)
        return float(numeric_series.mean())
    except Exception:
        return 0.0

def _convert_to_datetime(df: pd.DataFrame, timestamp_col: str = 'timestamp') -> pd.DataFrame:
    """
    Convert timestamp column to datetime with IST timezone.
    
    Args:
        df: Input DataFrame
        timestamp_col: Name of timestamp column
    
    Returns:
        DataFrame with converted timestamp
    """
    if df is None or df.empty or timestamp_col not in df.columns:
        return df.copy() if df is not None else pd.DataFrame()
    
    df_copy = df.copy()
    try:
        # Handle different timestamp formats safely
        timestamp_series = df_copy[timestamp_col]
        
        # Skip if already datetime
        if pd.api.types.is_datetime64_any_dtype(timestamp_series):
            return df_copy
            
        # Convert to datetime with UTC first to avoid mixed timezone warning
        df_copy[timestamp_col] = pd.to_datetime(df_copy[timestamp_col], utc=True, errors='coerce')
        
        # Convert to IST
        df_copy[timestamp_col] = df_copy[timestamp_col].dt.tz_convert(IST)
        
        return df_copy
    except Exception:
        # If conversion fails, return original dataframe
        return df_copy

def get_core_order_kpis(orders_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate core order KPIs.
    
    Args:
        orders_df: DataFrame with order data
    
    Returns:
        Dictionary containing core KPIs
    """
    if orders_df is None or orders_df.empty:
        return {
            'total_orders': 0,
            'total_quantity': 0,
            'total_revenue': 0.0,
            'avg_order_value': 0.0,
            'total_advance_collected': 0.0,
            'total_balance_pending': 0.0,
            'advance_collection_rate': 0.0,
            'outstanding_percentage': 0.0
        }
    
    required_cols = _safe_column_check(orders_df, [
        'order_id', 'quantity', 'total', 'advance_paid', 'balance_to_pay'
    ])
    
    total_orders = len(orders_df)
    total_quantity = _safe_sum(orders_df['quantity']) if 'quantity' in required_cols else 0
    total_revenue = _safe_sum(orders_df['total']) if 'total' in required_cols else 0.0
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0
    
    total_advance = _safe_sum(orders_df['advance_paid']) if 'advance_paid' in required_cols else 0.0
    total_balance = _safe_sum(orders_df['balance_to_pay']) if 'balance_to_pay' in required_cols else 0.0
    
    advance_rate = (total_advance / total_revenue * 100) if total_revenue > 0 else 0.0
    outstanding_pct = (total_balance / total_revenue * 100) if total_revenue > 0 else 0.0
    
    return {
        'total_orders': total_orders,
        'total_quantity': int(total_quantity),
        'total_revenue': float(total_revenue),
        'avg_order_value': float(avg_order_value),
        'total_advance_collected': float(total_advance),
        'total_balance_pending': float(total_balance),
        'advance_collection_rate': float(advance_rate),
        'outstanding_percentage': float(outstanding_pct)
    }

def get_daily_trends(orders_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate daily trends and growth metrics.
    
    Args:
        orders_df: DataFrame with order data
    
    Returns:
        Dictionary containing daily trends
    """
    if orders_df is None or orders_df.empty or 'timestamp' not in orders_df.columns:
        return {
            'daily_orders': pd.DataFrame(),
            'daily_revenue': pd.DataFrame(),
            'revenue_growth_percent': 0.0,
            'orders_growth_percent': 0.0
        }
    
    df_copy = _convert_to_datetime(orders_df, 'timestamp')
    
    # Only proceed if we have valid datetime data
    if df_copy[df_copy['timestamp'].notna()].empty:
        return {
            'daily_orders': pd.DataFrame(),
            'daily_revenue': pd.DataFrame(),
            'revenue_growth_percent': 0.0,
            'orders_growth_percent': 0.0
        }
    
    # Extract date from datetime
    df_copy = df_copy[df_copy['timestamp'].notna()].copy()  # Remove NaT values
    df_copy['date'] = df_copy['timestamp'].dt.date
    
    # Daily aggregations
    daily_orders = df_copy.groupby('date').size().reset_index(name='orders_count')
    daily_orders['date'] = pd.to_datetime(daily_orders['date'])
    
    daily_revenue = df_copy.groupby('date').agg({
        'total': lambda x: _safe_sum(x)
    }).reset_index()
    daily_revenue.columns = ['date', 'revenue']
    daily_revenue['date'] = pd.to_datetime(daily_revenue['date'])
    
    # Growth calculations
    today = datetime.now(IST).date()
    yesterday = today - timedelta(days=1)
    
    today_orders = daily_orders[daily_orders['date'].dt.date == today]['orders_count'].sum()
    yesterday_orders = daily_orders[daily_orders['date'].dt.date == yesterday]['orders_count'].sum()
    
    today_revenue = daily_revenue[daily_revenue['date'].dt.date == today]['revenue'].sum()
    yesterday_revenue = daily_revenue[daily_revenue['date'].dt.date == yesterday]['revenue'].sum()
    
    revenue_growth = ((today_revenue - yesterday_revenue) / yesterday_revenue * 100) if yesterday_revenue > 0 else 0.0
    orders_growth = ((today_orders - yesterday_orders) / yesterday_orders * 100) if yesterday_orders > 0 else 0.0
    
    return {
        'daily_orders': daily_orders,
        'daily_revenue': daily_revenue,
        'revenue_growth_percent': float(revenue_growth),
        'orders_growth_percent': float(orders_growth)
    }

def get_status_kpis(orders_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate status-based KPIs.
    
    Args:
        orders_df: DataFrame with order data
    
    Returns:
        Dictionary containing status KPIs
    """
    if orders_df is None or orders_df.empty or 'status' not in orders_df.columns:
        return {
            'status_distribution': pd.DataFrame(),
            'delivered_percentage': 0.0,
            'cancelled_percentage': 0.0,
            'rto_percentage': 0.0,
            'in_transit_count': 0,
            'orders_without_tracking': 0
        }
    
    status_dist = orders_df['status'].value_counts().reset_index()
    status_dist.columns = ['status', 'count']
    status_dist['percentage'] = (status_dist['count'] / len(orders_df) * 100).round(2)
    
    total_orders = len(orders_df)
    delivered_count = orders_df[orders_df['status'].str.contains('delivered', case=False, na=False)]['status'].count()
    cancelled_count = orders_df[orders_df['status'].str.contains('cancel', case=False, na=False)]['status'].count()
    rto_count = orders_df[orders_df['status'].str.contains('rto', case=False, na=False)]['status'].count()
    in_transit_count = orders_df[orders_df['status'].str.contains('transit|shipped|dispatch', case=False, na=False)]['status'].count()
    
    # Orders without tracking
    no_tracking = 0
    if 'tracking_id' in orders_df.columns:
        no_tracking = orders_df['tracking_id'].isna().sum()
    
    return {
        'status_distribution': status_dist,
        'delivered_percentage': float(delivered_count / total_orders * 100) if total_orders > 0 else 0.0,
        'cancelled_percentage': float(cancelled_count / total_orders * 100) if total_orders > 0 else 0.0,
        'rto_percentage': float(rto_count / total_orders * 100) if total_orders > 0 else 0.0,
        'in_transit_count': int(in_transit_count),
        'orders_without_tracking': int(no_tracking)
    }

def get_payment_kpis(orders_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate payment method KPIs.
    
    Args:
        orders_df: DataFrame with order data
    
    Returns:
        Dictionary containing payment KPIs
    """
    if orders_df is None or orders_df.empty or 'payment_method' not in orders_df.columns:
        return {
            'payment_distribution': pd.DataFrame(),
            'prepaid_percentage': 0.0,
            'cod_percentage': 0.0
        }
    
    payment_dist = orders_df['payment_method'].value_counts().reset_index()
    payment_dist.columns = ['payment_method', 'count']
    payment_dist['percentage'] = (payment_dist['count'] / len(orders_df) * 100).round(2)
    
    total_orders = len(orders_df)
    prepaid_count = orders_df[orders_df['payment_method'].str.contains('prepaid|online|upi|card', case=False, na=False)]['payment_method'].count()
    cod_count = orders_df[orders_df['payment_method'].str.contains('cod|cash', case=False, na=False)]['payment_method'].count()
    
    return {
        'payment_distribution': payment_dist,
        'prepaid_percentage': float(prepaid_count / total_orders * 100) if total_orders > 0 else 0.0,
        'cod_percentage': float(cod_count / total_orders * 100) if total_orders > 0 else 0.0
    }

def get_geographic_kpis(orders_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate geographic and city-based KPIs.
    
    Args:
        orders_df: DataFrame with order data
    
    Returns:
        Dictionary containing geographic KPIs
    """
    if orders_df is None or orders_df.empty:
        return {
            'top_cities_by_revenue': pd.DataFrame(),
            'revenue_by_city': pd.DataFrame(),
            'orders_by_city': pd.DataFrame()
        }
    
    city_col = None
    for col in ['city', 'City', 'CITY']:
        if col in orders_df.columns:
            city_col = col
            break
    
    if city_col is None:
        return {
            'top_cities_by_revenue': pd.DataFrame(),
            'revenue_by_city': pd.DataFrame(),
            'orders_by_city': pd.DataFrame()
        }
    
    # Revenue by city
    revenue_by_city = orders_df.groupby(city_col).agg({
        'total': lambda x: _safe_sum(x)
    }).reset_index()
    revenue_by_city.columns = ['city', 'revenue']
    revenue_by_city = revenue_by_city.sort_values('revenue', ascending=False)
    
    # Orders by city
    orders_by_city = orders_df.groupby(city_col).size().reset_index(name='orders_count')
    orders_by_city = orders_by_city.sort_values('orders_count', ascending=False)
    
    # Top cities by revenue (top 10)
    top_cities = revenue_by_city.head(10)
    
    return {
        'top_cities_by_revenue': top_cities,
        'revenue_by_city': revenue_by_city,
        'orders_by_city': orders_by_city
    }

def get_product_kpis(orders_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate product-based KPIs.
    
    Args:
        orders_df: DataFrame with order data
    
    Returns:
        Dictionary containing product KPIs
    """
    if orders_df is None or orders_df.empty or 'product' not in orders_df.columns:
        return {
            'top_products_by_revenue': pd.DataFrame(),
            'quantity_by_product': pd.DataFrame(),
            'revenue_by_product': pd.DataFrame()
        }
    
    # Revenue by product
    revenue_by_product = orders_df.groupby('product').agg({
        'total': lambda x: _safe_sum(x)
    }).reset_index()
    revenue_by_product.columns = ['product', 'revenue']
    revenue_by_product = revenue_by_product.sort_values('revenue', ascending=False)
    
    # Quantity by product
    quantity_cols = _safe_column_check(orders_df, ['quantity'])
    if quantity_cols:
        quantity_by_product = orders_df.groupby('product').agg({
            'quantity': lambda x: _safe_sum(x)
        }).reset_index()
        quantity_by_product.columns = ['product', 'quantity_sold']
        quantity_by_product = quantity_by_product.sort_values('quantity_sold', ascending=False)
    else:
        quantity_by_product = pd.DataFrame()
    
    # Top products by revenue (top 10)
    top_products = revenue_by_product.head(10)
    
    return {
        'top_products_by_revenue': top_products,
        'quantity_by_product': quantity_by_product,
        'revenue_by_product': revenue_by_product
    }

def get_employee_order_kpis(orders_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate employee performance KPIs.
    
    Args:
        orders_df: DataFrame with order data
    
    Returns:
        Dictionary containing employee KPIs
    """
    if orders_df is None or orders_df.empty or 'created_by' not in orders_df.columns:
        return {
            'orders_per_employee': pd.DataFrame(),
            'revenue_per_employee': pd.DataFrame(),
            'avg_order_value_per_employee': pd.DataFrame(),
            'delivered_rate_per_employee': pd.DataFrame(),
            'cancellation_rate_per_employee': pd.DataFrame()
        }
    
    # Basic employee metrics
    emp_orders = orders_df.groupby('created_by').size().reset_index(name='orders_count')
    
    emp_revenue = orders_df.groupby('created_by').agg({
        'total': lambda x: _safe_sum(x)
    }).reset_index()
    emp_revenue.columns = ['created_by', 'total_revenue']
    
    # Merge and calculate avg order value
    emp_metrics = emp_orders.merge(emp_revenue, on='created_by', how='left')
    emp_metrics['avg_order_value'] = emp_metrics['total_revenue'] / emp_metrics['orders_count']
    
    # Delivery and cancellation rates
    if 'status' in orders_df.columns:
        emp_delivered = orders_df[orders_df['status'].str.contains('delivered', case=False, na=False)].groupby('created_by').size().reset_index(name='delivered_count')
        emp_cancelled = orders_df[orders_df['status'].str.contains('cancel', case=False, na=False)].groupby('created_by').size().reset_index(name='cancelled_count')
        
        emp_delivery_rate = emp_orders.merge(emp_delivered, on='created_by', how='left').fillna(0)
        emp_delivery_rate['delivery_rate'] = (emp_delivery_rate['delivered_count'] / emp_delivery_rate['orders_count'] * 100)
        
        emp_cancel_rate = emp_orders.merge(emp_cancelled, on='created_by', how='left').fillna(0)
        emp_cancel_rate['cancellation_rate'] = (emp_cancel_rate['cancelled_count'] / emp_cancel_rate['orders_count'] * 100)
    else:
        emp_delivery_rate = pd.DataFrame()
        emp_cancel_rate = pd.DataFrame()
    
    return {
        'orders_per_employee': emp_orders.sort_values('orders_count', ascending=False),
        'revenue_per_employee': emp_revenue.sort_values('total_revenue', ascending=False),
        'avg_order_value_per_employee': emp_metrics[['created_by', 'avg_order_value']].sort_values('avg_order_value', ascending=False),
        'delivered_rate_per_employee': emp_delivery_rate,
        'cancellation_rate_per_employee': emp_cancel_rate
    }

def get_conversion_kpis(performance_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate conversion rate KPIs from performance data.
    
    Args:
        performance_df: DataFrame with performance data
    
    Returns:
        Dictionary containing conversion KPIs
    """
    if performance_df is None or performance_df.empty:
        return {
            'conversion_rate_per_user': pd.DataFrame(),
            'overall_conversion_rate': 0.0,
            'best_performing_user': None,
            'worst_performing_user': None
        }
    
    required_cols = _safe_column_check(performance_df, ['userid', 'no_of_leads', 'no_of_orders'])
    if len(required_cols) < 3:
        return {
            'conversion_rate_per_user': pd.DataFrame(),
            'overall_conversion_rate': 0.0,
            'best_performing_user': None,
            'worst_performing_user': None
        }
    
    # User-wise conversion rates
    user_conv = performance_df.groupby('userid').agg({
        'no_of_leads': 'sum',
        'no_of_orders': 'sum'
    }).reset_index()
    
    user_conv['conversion_rate'] = (user_conv['no_of_orders'] / user_conv['no_of_leads'] * 100).fillna(0)
    user_conv = user_conv.sort_values('conversion_rate', ascending=False)
    
    # Overall conversion rate
    total_leads = _safe_sum(performance_df['no_of_leads'])
    total_orders = _safe_sum(performance_df['no_of_orders'])
    overall_rate = (total_orders / total_leads * 100) if total_leads > 0 else 0.0
    
    # Best and worst performers
    best_user = user_conv.iloc[0]['userid'] if not user_conv.empty else None
    worst_user = user_conv.iloc[-1]['userid'] if not user_conv.empty else None
    
    return {
        'conversion_rate_per_user': user_conv,
        'overall_conversion_rate': float(overall_rate),
        'best_performing_user': best_user,
        'worst_performing_user': worst_user
    }

def get_advanced_kpis(orders_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate advanced business KPIs.
    
    Args:
        orders_df: DataFrame with order data
    
    Returns:
        Dictionary containing advanced KPIs
    """
    if orders_df is None or orders_df.empty:
        return {
            'order_aging_report': pd.DataFrame(),
            'high_risk_orders': pd.DataFrame(),
            'revenue_realization_rate': 0.0,
            'courier_performance': pd.DataFrame()
        }
    
    df_copy = _convert_to_datetime(orders_df, 'timestamp')
    now = datetime.now(IST)
    
    # Order aging (orders older than 7 days)
    aging_orders = pd.DataFrame()
    if 'timestamp' in df_copy.columns:
        valid_timestamp_orders = df_copy[df_copy['timestamp'].notna()]
        if not valid_timestamp_orders.empty:
            valid_timestamp_orders = valid_timestamp_orders.copy()
            valid_timestamp_orders['days_old'] = (now - valid_timestamp_orders['timestamp']).dt.days
            aging_orders = valid_timestamp_orders[valid_timestamp_orders['days_old'] > 7][['order_id', 'days_old', 'status', 'total']].sort_values('days_old', ascending=False)
    
    # High risk orders (COD + high balance)
    high_risk = pd.DataFrame()
    payment_col = _safe_column_check(orders_df, ['payment_method'])
    balance_col = _safe_column_check(orders_df, ['balance_to_pay'])
    
    if payment_col and balance_col:
        try:
            median_balance = orders_df['balance_to_pay'].median()
            if pd.notna(median_balance):
                high_risk = orders_df[
                    (orders_df['payment_method'].str.contains('cod', case=False, na=False)) &
                    (orders_df['balance_to_pay'] > median_balance)
                ][['order_id', 'customer_name', 'balance_to_pay', 'status']]
        except Exception:
            pass
    
    # Revenue realization rate
    total_revenue = _safe_sum(orders_df['total']) if 'total' in orders_df.columns else 0
    delivered_revenue = 0
    if 'status' in orders_df.columns and 'total' in orders_df.columns:
        delivered_orders = orders_df[orders_df['status'].str.contains('delivered', case=False, na=False)]
        delivered_revenue = _safe_sum(delivered_orders['total'])
    
    realization_rate = (delivered_revenue / total_revenue * 100) if total_revenue > 0 else 0.0
    
    # Courier performance
    courier_perf = pd.DataFrame()
    if 'courier_name' in orders_df.columns and 'status' in orders_df.columns:
        courier_orders = orders_df.groupby('courier_name').size().reset_index(name='total_orders')
        courier_delivered = orders_df[orders_df['status'].str.contains('delivered', case=False, na=False)].groupby('courier_name').size().reset_index(name='delivered_orders')
        
        courier_perf = courier_orders.merge(courier_delivered, on='courier_name', how='left').fillna(0)
        courier_perf['delivery_rate'] = (courier_perf['delivered_orders'] / courier_perf['total_orders'] * 100)
        courier_perf = courier_perf.sort_values('delivery_rate', ascending=False)
    
    return {
        'order_aging_report': aging_orders,
        'high_risk_orders': high_risk,
        'revenue_realization_rate': float(realization_rate),
        'courier_performance': courier_perf
    }

def generate_full_kpi_report(orders_df: pd.DataFrame, performance_df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Generate comprehensive KPI report combining all analytics.
    
    Args:
        orders_df: DataFrame with order data
        performance_df: Optional DataFrame with performance data
    
    Returns:
        Dictionary containing all KPI categories
    """
    report = {
        'timestamp': datetime.now(IST).isoformat(),
        'data_summary': {
            'total_orders_in_dataset': len(orders_df) if orders_df is not None else 0,
            'performance_records': len(performance_df) if performance_df is not None else 0
        }
    }
    
    # Core metrics
    report['core_order_kpis'] = get_core_order_kpis(orders_df)
    report['daily_trends'] = get_daily_trends(orders_df)
    report['status_kpis'] = get_status_kpis(orders_df)
    report['payment_kpis'] = get_payment_kpis(orders_df)
    report['geographic_kpis'] = get_geographic_kpis(orders_df)
    report['product_kpis'] = get_product_kpis(orders_df)
    report['employee_kpis'] = get_employee_order_kpis(orders_df)
    report['advanced_kpis'] = get_advanced_kpis(orders_df)
    
    # Performance metrics (if data available)
    if performance_df is not None:
        report['conversion_kpis'] = get_conversion_kpis(performance_df)
    else:
        report['conversion_kpis'] = {
            'conversion_rate_per_user': pd.DataFrame(),
            'overall_conversion_rate': 0.0,
            'best_performing_user': None,
            'worst_performing_user': None
        }
    
    return report

# Helper function for Streamlit integration
def format_kpi_for_display(value: Any, kpi_type: str = 'number') -> str:
    """
    Format KPI values for display in Streamlit.
    
    Args:
        value: The KPI value to format
        kpi_type: Type of KPI ('currency', 'percentage', 'number')
    
    Returns:
        Formatted string
    """
    if pd.isna(value) or value is None:
        return "N/A"
    
    if kpi_type == 'currency':
        return f"₹{float(value):,.2f}"
    elif kpi_type == 'percentage':
        return f"{float(value):.1f}%"
    elif kpi_type == 'number':
        return f"{int(value):,}" if isinstance(value, (int, float)) else str(value)
    else:
        return str(value)

if __name__ == "__main__":
    # Example usage for testing
    print("IMIQ KPI Module - Test Mode")
    
    # Create sample data for testing
    sample_orders = pd.DataFrame({
        'order_id': ['ORD001', 'ORD002', 'ORD003'],
        'total': [1000, 1500, 800],
        'quantity': [2, 3, 1],
        'status': ['delivered', 'pending', 'cancelled'],
        'timestamp': pd.date_range('2024-01-01', periods=3, freq='D')
    })
    
    # Test core KPIs
    core_kpis = get_core_order_kpis(sample_orders)
    print("Core KPIs:", core_kpis)
    
    print("KPI module ready for integration!")