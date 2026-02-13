"""
IMIQ KPI Service
Handles KPI calculations and performance metrics for dashboard analytics
"""

import pandas as pd
from datetime import datetime, timedelta, date
from typing import Dict, Any, List, Optional, Tuple
import logging
import pytz

from .storage import StorageBase
from .utils import get_ist_now

logger = logging.getLogger(__name__)

# Asia/Kolkata timezone for consistent date handling
IST = pytz.timezone('Asia/Kolkata')

class KPIService:
    """Service for calculating and managing KPIs and performance metrics"""
    
    def __init__(self, storage: StorageBase):
        self.storage = storage
    
    def get_daily_order_counts(self, days: int = 7, orders_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Get daily order counts for the last N days"""
        try:
            if orders_df is None:
                orders_df = self.storage.read_sheet("NewOrders")
            
            if orders_df.empty or 'timestamp' not in orders_df.columns:
                return pd.DataFrame(columns=['date', 'count'])
            
            # Convert to datetime with timezone awareness
            orders_df = orders_df.copy()
            orders_df['timestamp'] = pd.to_datetime(orders_df['timestamp'])
            
            # Filter to last N days
            end_date = get_ist_now().date()
            start_date = end_date - timedelta(days=days-1)
            
            orders_df['date'] = orders_df['timestamp'].dt.date
            filtered_orders = orders_df[
                (orders_df['date'] >= start_date) & 
                (orders_df['date'] <= end_date)
            ]
            
            # Count orders by date
            daily_counts = filtered_orders['date'].value_counts().reset_index()
            daily_counts.columns = ['date', 'count']
            daily_counts = daily_counts.sort_values('date')
            
            # Fill missing dates with 0
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            complete_range = pd.DataFrame({'date': date_range.date})
            
            daily_counts = complete_range.merge(daily_counts, on='date', how='left').fillna(0)
            daily_counts['count'] = daily_counts['count'].astype(int)
            
            return daily_counts
            
        except Exception as e:
            logger.error(f"Error calculating daily order counts: {e}")
            return pd.DataFrame(columns=['date', 'count'])
    
    def get_status_distribution(self, orders_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Get distribution of order statuses"""
        try:
            if orders_df is None:
                orders_df = self.storage.read_sheet("NewOrders")
            
            if orders_df.empty or 'status' not in orders_df.columns:
                return pd.DataFrame(columns=['status', 'count', 'percentage'])
            
            status_counts = orders_df['status'].value_counts().reset_index()
            status_counts.columns = ['status', 'count']
            
            total_orders = len(orders_df)
            status_counts['percentage'] = (status_counts['count'] / total_orders * 100).round(1)
            
            return status_counts
            
        except Exception as e:
            logger.error(f"Error calculating status distribution: {e}")
            return pd.DataFrame(columns=['status', 'count', 'percentage'])
    
    def get_revenue_metrics(self, orders_df: Optional[pd.DataFrame] = None) -> Dict[str, float]:
        """Calculate revenue-related metrics"""
        try:
            if orders_df is None:
                orders_df = self.storage.read_sheet("NewOrders")
            
            if orders_df.empty or 'price' not in orders_df.columns:
                return {
                    'total_revenue': 0.0,
                    'average_order_value': 0.0,
                    'monthly_revenue': 0.0,
                    'weekly_revenue': 0.0
                }
            
            # Ensure price is numeric
            orders_df['price'] = pd.to_numeric(orders_df['price'], errors='coerce').fillna(0)
            
            total_revenue = orders_df['price'].sum()
            average_order_value = orders_df['price'].mean()
            
            # Calculate monthly and weekly revenue
            monthly_revenue = 0.0
            weekly_revenue = 0.0
            
            if 'timestamp' in orders_df.columns:
                orders_df['timestamp'] = pd.to_datetime(orders_df['timestamp'])
                
                now = get_ist_now()
                month_ago = now - timedelta(days=30)
                week_ago = now - timedelta(days=7)
                
                monthly_orders = orders_df[orders_df['timestamp'] > month_ago]
                weekly_orders = orders_df[orders_df['timestamp'] > week_ago]
                
                monthly_revenue = monthly_orders['total'].sum() if 'total' in monthly_orders.columns else 0
                weekly_revenue = weekly_orders['total'].sum() if 'total' in weekly_orders.columns else 0
            
            return {
                'total_revenue': float(total_revenue),
                'average_order_value': float(average_order_value),
                'monthly_revenue': float(monthly_revenue),
                'weekly_revenue': float(weekly_revenue)
            }
            
        except Exception as e:
            logger.error(f"Error calculating revenue metrics: {e}")
            return {
                'total_revenue': 0.0,
                'average_order_value': 0.0,
                'monthly_revenue': 0.0,
                'weekly_revenue': 0.0
            }
    
    def get_user_performance_stats(self) -> pd.DataFrame:
        """Get performance statistics for all users"""
        try:
            orders_df = self.storage.read_sheet("NewOrders")
            
            if orders_df.empty or 'user_id' not in orders_df.columns:
                return pd.DataFrame(columns=['userid', 'total_orders', 'total_revenue', 'avg_order_value'])
            
            # Group by user
            user_stats = orders_df.groupby('user_id').agg({
                'order_id': 'count',
                'price': ['sum', 'mean']
            }).round(2)
            
            # Flatten column names
            user_stats.columns = ['total_orders', 'total_revenue', 'avg_order_value']
            user_stats = user_stats.reset_index()
            user_stats.columns = ['userid', 'total_orders', 'total_revenue', 'avg_order_value']
            
            # Add status breakdown
            status_breakdown = orders_df.groupby(['user_id', 'status']).size().unstack(fill_value=0)
            status_breakdown = status_breakdown.reset_index()
            
            # Merge with main stats
            user_stats = user_stats.merge(status_breakdown, left_on='userid', right_on='user_id', how='left')
            user_stats = user_stats.drop('user_id', axis=1, errors='ignore')
            
            # Calculate performance score (total orders * avg order value)
            user_stats['performance_score'] = (user_stats['total_orders'] * user_stats['avg_order_value']).round(2)
            
            return user_stats.sort_values('performance_score', ascending=False)
            
        except Exception as e:
            logger.error(f"Error calculating user performance stats: {e}")
            return pd.DataFrame(columns=['userid', 'total_orders', 'total_revenue', 'avg_order_value'])
    
    def get_conversion_metrics(self) -> Dict[str, float]:
        """Calculate conversion-related metrics (placeholder for lead-to-order conversion)"""
        try:
            orders_df = self.storage.read_sheet("NewOrders")
            
            if orders_df.empty:
                return {
                    'lead_to_order_rate': 0.0,
                    'order_to_delivery_rate': 0.0,
                    'completion_rate': 0.0
                }
            
            # Lead to order conversion (if lead_id exists)
            lead_to_order_rate = 0.0
            if 'lead_id' in orders_df.columns:
                orders_with_leads = orders_df[orders_df['lead_id'].notna() & (orders_df['lead_id'] != '')]
                if len(orders_with_leads) > 0:
                    # Placeholder calculation - in real implementation, 
                    # you'd compare with total leads from a leads table
                    lead_to_order_rate = len(orders_with_leads) / len(orders_df) * 100
            
            # Order to delivery conversion
            order_to_delivery_rate = 0.0
            if 'status' in orders_df.columns:
                delivered_orders = len(orders_df[orders_df['status'].isin(['Delivered', 'Completed'])])
                total_orders = len(orders_df)
                order_to_delivery_rate = (delivered_orders / total_orders * 100) if total_orders > 0 else 0
            
            # Overall completion rate
            completion_rate = order_to_delivery_rate  # Same as delivery rate for now
            
            return {
                'lead_to_order_rate': round(lead_to_order_rate, 1),
                'order_to_delivery_rate': round(order_to_delivery_rate, 1),
                'completion_rate': round(completion_rate, 1)
            }
            
        except Exception as e:
            logger.error(f"Error calculating conversion metrics: {e}")
            return {
                'lead_to_order_rate': 0.0,
                'order_to_delivery_rate': 0.0,
                'completion_rate': 0.0
            }
    
    def get_sla_metrics(self) -> Dict[str, Any]:
        """Calculate SLA-related metrics (placeholder for time-based metrics)"""
        try:
            orders_df = self.storage.read_sheet("NewOrders")
            shipments_df = self.storage.read_sheet("Shipments")
            
            metrics = {
                'avg_days_to_ship': 0.0,
                'avg_days_to_deliver': 0.0,
                'orders_on_time': 0,
                'orders_delayed': 0,
                'sla_compliance_rate': 0.0
            }
            
            if orders_df.empty:
                return metrics
            
            # Calculate average days to ship
            if not shipments_df.empty and 'timestamp' in orders_df.columns and 'created_at' in shipments_df.columns:
                # Merge orders with shipments
                merged = orders_df.merge(shipments_df, on='order_id', how='inner', suffixes=('_order', '_shipment'))
                
                if not merged.empty:
                    merged['order_date'] = pd.to_datetime(merged['timestamp_order'])
                    merged['ship_date'] = pd.to_datetime(merged['created_at_shipment'])
                    
                    # Calculate days to ship
                    merged['days_to_ship'] = (merged['ship_date'] - merged['order_date']).dt.days
                    
                    avg_days_to_ship = merged['days_to_ship'].mean()
                    metrics['avg_days_to_ship'] = round(avg_days_to_ship, 1) if not pd.isna(avg_days_to_ship) else 0.0
                    
                    # SLA compliance (assuming 3 days SLA for shipping)
                    sla_days = 3
                    on_time = len(merged[merged['days_to_ship'] <= sla_days])
                    delayed = len(merged[merged['days_to_ship'] > sla_days])
                    
                    metrics['orders_on_time'] = on_time
                    metrics['orders_delayed'] = delayed
                    
                    total_shipped = on_time + delayed
                    metrics['sla_compliance_rate'] = round((on_time / total_shipped * 100), 1) if total_shipped > 0 else 0.0
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating SLA metrics: {e}")
            return {
                'avg_days_to_ship': 0.0,
                'avg_days_to_deliver': 0.0,
                'orders_on_time': 0,
                'orders_delayed': 0,
                'sla_compliance_rate': 0.0
            }
    
    def get_product_performance(self) -> pd.DataFrame:
        """Get product performance metrics"""
        try:
            orders_df = self.storage.read_sheet("NewOrders")
            
            if orders_df.empty or 'product' not in orders_df.columns:
                return pd.DataFrame(columns=['product', 'total_orders', 'total_revenue', 'avg_price'])
            
            product_stats = orders_df.groupby('product').agg({
                'order_id': 'count',
                'price': ['sum', 'mean'],
                'quantity': 'sum'
            }).round(2)
            
            # Flatten column names
            product_stats.columns = ['total_orders', 'total_revenue', 'avg_price', 'total_quantity']
            product_stats = product_stats.reset_index()
            
            return product_stats.sort_values('total_revenue', ascending=False)
            
        except Exception as e:
            logger.error(f"Error calculating product performance: {e}")
            return pd.DataFrame(columns=['product', 'total_orders', 'total_revenue', 'avg_price'])
    
    def get_monthly_trends(self, months: int = 6) -> pd.DataFrame:
        """Get monthly order and revenue trends"""
        try:
            orders_df = self.storage.read_sheet("NewOrders")
            
            if orders_df.empty or 'timestamp' not in orders_df.columns:
                return pd.DataFrame(columns=['month', 'orders', 'revenue'])
            
            orders_df = orders_df.copy()
            orders_df['timestamp'] = pd.to_datetime(orders_df['timestamp'])
            orders_df['month'] = orders_df['timestamp'].dt.to_period('M')
            
            # Get last N months
            end_month = get_ist_now().to_period('M')
            start_month = end_month - months + 1
            
            monthly_stats = orders_df.groupby('month').agg({
                'order_id': 'count',
                'total': 'sum'
            }).round(2)
            
            monthly_stats.columns = ['orders', 'revenue']
            monthly_stats = monthly_stats.reset_index()
            monthly_stats['month'] = monthly_stats['month'].astype(str)
            
            # Filter to requested months
            monthly_stats = monthly_stats[
                (monthly_stats['month'] >= str(start_month)) & 
                (monthly_stats['month'] <= str(end_month))
            ]
            
            return monthly_stats.sort_values('month')
            
        except Exception as e:
            logger.error(f"Error calculating monthly trends: {e}")
            return pd.DataFrame(columns=['month', 'orders', 'revenue'])
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get comprehensive dashboard summary with all key metrics"""
        try:
            orders_df = self.storage.read_sheet("NewOrders")
            
            summary = {
                'total_orders': len(orders_df) if not orders_df.empty else 0,
                'pending_orders': 0,
                'completed_orders': 0,
                'total_revenue': 0.0,
                'avg_order_value': 0.0,
                'orders_today': 0,
                'revenue_today': 0.0
            }
            
            if orders_df.empty:
                return summary
            
            # Status counts
            if 'status' in orders_df.columns:
                summary['pending_orders'] = len(orders_df[orders_df['status'] == 'Pending'])
                summary['completed_orders'] = len(orders_df[orders_df['status'].isin(['Completed', 'Delivered'])])
            
            # Revenue metrics
            if 'price' in orders_df.columns:
                orders_df['price'] = pd.to_numeric(orders_df['price'], errors='coerce').fillna(0)
                summary['total_revenue'] = float(orders_df['total'].sum()) if 'total' in orders_df.columns else 0.0
                summary['avg_order_value'] = float(orders_df['total'].mean()) if 'total' in orders_df.columns else 0.0
            
            # Today's metrics
            if 'timestamp' in orders_df.columns:
                orders_df['timestamp'] = pd.to_datetime(orders_df['timestamp'])
                today = get_ist_now().date()
                
                today_orders = orders_df[orders_df['timestamp'].dt.date == today]
                summary['orders_today'] = len(today_orders)
                
                if 'total' in orders_df.columns and not today_orders.empty:
                    summary['revenue_today'] = float(today_orders['total'].sum())
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting dashboard summary: {e}")
            return {
                'total_orders': 0,
                'pending_orders': 0,
                'completed_orders': 0,
                'total_revenue': 0.0,
                'avg_order_value': 0.0,
                'orders_today': 0,
                'revenue_today': 0.0
            }


# Performance Analytics Helper Functions

def normalize_status(status: str) -> str:
    """Normalize order status strings for consistent comparison"""
    if pd.isna(status):
        return 'unknown'
    return str(status).lower().strip().replace('_', ' ').replace('-', ' ')

def user_time_series(orders_df: pd.DataFrame, userid: str, start_date: date, end_date: date) -> pd.DataFrame:
    """
    Get daily order counts for a specific user within date range
    
    Args:
        orders_df: Orders DataFrame
        userid: User ID to filter by
        start_date: Start date for analysis
        end_date: End date for analysis
        
    Returns:
        DataFrame with columns: date, order_count
    """
    try:
        # Filter orders for the user
        user_orders = orders_df[orders_df['created_by'].astype(str) == userid].copy()
        
        if user_orders.empty:
            return pd.DataFrame(columns=['date', 'order_count'])
        
        # Parse timestamps and convert to IST
        user_orders['timestamp'] = pd.to_datetime(user_orders['timestamp'], utc=True, errors='coerce')
        user_orders['date'] = user_orders['timestamp'].dt.tz_convert(IST).dt.date
        
        # Filter by date range
        mask = (user_orders['date'] >= start_date) & (user_orders['date'] <= end_date)
        filtered_orders = user_orders[mask]
        
        if filtered_orders.empty:
            return pd.DataFrame(columns=['date', 'order_count'])
        
        # Count orders by date
        daily_counts = filtered_orders.groupby('date').size().reset_index(name='order_count')
        
        # Fill missing dates with 0
        date_range = pd.date_range(start=start_date, end=end_date, freq='D').date
        all_dates = pd.DataFrame({'date': date_range})
        
        result = all_dates.merge(daily_counts, on='date', how='left').fillna(0)
        result['order_count'] = result['order_count'].astype(int)
        
        return result
        
    except Exception as e:
        logger.error(f"Error in user_time_series: {e}")
        return pd.DataFrame(columns=['date', 'order_count'])

def user_weekly_counts(orders_df: pd.DataFrame, userid: str, start_date: date, end_date: date) -> pd.DataFrame:
    """
    Get weekly order counts for a specific user within date range
    
    Returns:
        DataFrame with columns: week, order_count
    """
    try:
        daily_data = user_time_series(orders_df, userid, start_date, end_date)
        
        if daily_data.empty:
            return pd.DataFrame(columns=['week', 'order_count'])
        
        # Convert to pandas datetime for resampling
        daily_data['date'] = pd.to_datetime(daily_data['date'])
        daily_data.set_index('date', inplace=True)
        
        # Resample to weekly (Monday start)
        weekly_data = daily_data.resample('W-MON')['order_count'].sum().reset_index()
        weekly_data['week'] = weekly_data['date'].dt.strftime('%Y-W%U')
        weekly_data = weekly_data[['week', 'order_count']]
        
        return weekly_data
        
    except Exception as e:
        logger.error(f"Error in user_weekly_counts: {e}")
        return pd.DataFrame(columns=['week', 'order_count'])

def user_monthly_counts(orders_df: pd.DataFrame, userid: str, start_date: date, end_date: date) -> pd.DataFrame:
    """
    Get monthly order counts for a specific user within date range
    
    Returns:
        DataFrame with columns: month, order_count
    """
    try:
        daily_data = user_time_series(orders_df, userid, start_date, end_date)
        
        if daily_data.empty:
            return pd.DataFrame(columns=['month', 'order_count'])
        
        # Convert to pandas datetime for resampling
        daily_data['date'] = pd.to_datetime(daily_data['date'])
        daily_data.set_index('date', inplace=True)
        
        # Resample to monthly
        monthly_data = daily_data.resample('M')['order_count'].sum().reset_index()
        monthly_data['month'] = monthly_data['date'].dt.strftime('%Y-%m')
        monthly_data = monthly_data[['month', 'order_count']]
        
        return monthly_data
        
    except Exception as e:
        logger.error(f"Error in user_monthly_counts: {e}")
        return pd.DataFrame(columns=['month', 'order_count'])

def get_user_conversion_rate(performance_df: pd.DataFrame, userid: str, start_date: date, end_date: date) -> Optional[float]:
    """
    Calculate leads to orders conversion rate from Performance sheet
    
    Returns:
        Conversion rate as percentage or None if no data
    """
    try:
        if performance_df.empty:
            logger.warning("Performance DataFrame is empty")
            return None
        
        # Log available columns for debugging
        logger.info(f"Available columns in Performance sheet: {list(performance_df.columns)}")
        
        # Try different column names for user identification
        user_column = None
        for col in ['created_by', 'userid', 'user_id', 'name', 'email']:
            if col in performance_df.columns:
                user_column = col
                break
        
        if user_column is None:
            logger.warning("No user identification column found in Performance sheet")
            return None
        
        # Filter performance data for user and date range
        user_perf = performance_df[performance_df[user_column].astype(str) == str(userid)].copy()
        
        if user_perf.empty:
            logger.info(f"No performance data found for user: {userid}")
            return None
        
        # Parse dates - try different column names
        date_column = None
        for col in ['date', 'Date', 'timestamp', 'created_at', 'orderdate']:
            if col in user_perf.columns:
                date_column = col
                break
        
        if date_column is None:
            logger.warning("No date column found in Performance sheet")
            return None
            
        user_perf['parsed_date'] = pd.to_datetime(user_perf[date_column], errors='coerce').dt.date
        
        # Filter by date range
        mask = (user_perf['parsed_date'] >= start_date) & (user_perf['parsed_date'] <= end_date)
        filtered_perf = user_perf[mask]
        
        if filtered_perf.empty:
            logger.info(f"No performance data in date range {start_date} to {end_date} for user {userid}")
            return None
        
        # Try different column names for leads and orders
        leads_column = None
        orders_column = None
        
        for col in ['no_of_leads', 'leads', 'lead_count', 'num_leads', 'total_leads']:
            if col in filtered_perf.columns:
                leads_column = col
                break
                
        for col in ['no_of_orders', 'orders', 'order_count', 'num_orders', 'total_orders']:
            if col in filtered_perf.columns:
                orders_column = col
                break
        
        if leads_column is None or orders_column is None:
            logger.warning(f"Required columns not found. Available: {list(performance_df.columns)}")
            logger.warning(f"Looking for leads column (found: {leads_column}) and orders column (found: {orders_column})")
            return None
        
        # Calculate conversion rate
        total_leads = pd.to_numeric(filtered_perf[leads_column], errors='coerce').sum()
        total_orders = pd.to_numeric(filtered_perf[orders_column], errors='coerce').sum()
        
        logger.info(f"User {userid}: {total_leads} leads, {total_orders} orders in date range")
        
        if total_leads == 0:
            logger.info(f"No leads found for user {userid} in date range")
            return None
        
        conversion_rate = (total_orders / total_leads) * 100
        logger.info(f"Calculated conversion rate: {conversion_rate:.2f}% for user {userid}")
        return float(conversion_rate)
        
    except Exception as e:
        logger.error(f"Error calculating conversion rate for user {userid}: {e}")
        return None

def get_user_delivery_metrics(orders_df: pd.DataFrame, userid: str, start_date: date, end_date: date) -> Dict[str, float]:
    """
    Calculate delivery and fulfillment metrics for a user
    
    Returns:
        Dictionary with delivery metrics
    """
    default_metrics = {
        'delivered_count': 0,
        'returns_count': 0,
        'cancelled_count': 0,
        'in_transit_count': 0,
        'delivery_rate': 0.0,
        'return_rate': 0.0,
        'cancellation_rate': 0.0,
        'avg_order_value': 0.0,
        'total_revenue': 0.0
    }
    
    try:
        # Filter orders for user and date range
        user_orders = orders_df[orders_df['created_by'].astype(str) == userid].copy()
        
        if user_orders.empty:
            return default_metrics
        
        # Parse timestamps and filter by date
        user_orders['timestamp'] = pd.to_datetime(user_orders['timestamp'], utc=True, errors='coerce')
        user_orders['date'] = user_orders['timestamp'].dt.tz_convert(IST).dt.date
        
        mask = (user_orders['date'] >= start_date) & (user_orders['date'] <= end_date)
        filtered_orders = user_orders[mask]
        
        if filtered_orders.empty:
            return default_metrics
        
        total_orders = len(filtered_orders)
        
        # Normalize statuses for comparison
        filtered_orders['status_norm'] = filtered_orders['status'].apply(normalize_status)
        
        # Define status categories
        delivered_statuses = {'delivered', 'complete', 'completed'}
        return_statuses = {'return', 'returned', 'rto', 'refunded', 'refund'}
        cancelled_statuses = {'cancelled', 'canceled', 'cancel'}
        in_transit_statuses = {'shipped', 'in transit', 'out for delivery', 'dispatched', 'transit'}
        
        # Count by status categories
        delivered_count = filtered_orders['status_norm'].isin(delivered_statuses).sum()
        returns_count = filtered_orders['status_norm'].isin(return_statuses).sum()
        cancelled_count = filtered_orders['status_norm'].isin(cancelled_statuses).sum()
        in_transit_count = filtered_orders['status_norm'].isin(in_transit_statuses).sum()
        
        # Calculate rates
        delivery_rate = (delivered_count / total_orders * 100) if total_orders > 0 else 0.0
        return_rate = (returns_count / total_orders * 100) if total_orders > 0 else 0.0
        cancellation_rate = (cancelled_count / total_orders * 100) if total_orders > 0 else 0.0
        
        # Financial metrics
        if 'total' in filtered_orders.columns:
            filtered_orders['total'] = pd.to_numeric(filtered_orders['total'], errors='coerce').fillna(0)
            total_revenue = filtered_orders['total'].sum()
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0.0
        else:
            total_revenue = 0.0
            avg_order_value = 0.0
        
        return {
            'delivered_count': int(delivered_count),
            'returns_count': int(returns_count),
            'cancelled_count': int(cancelled_count),
            'in_transit_count': int(in_transit_count),
            'delivery_rate': float(delivery_rate),
            'return_rate': float(return_rate),
            'cancellation_rate': float(cancellation_rate),
            'avg_order_value': float(avg_order_value),
            'total_revenue': float(total_revenue)
        }
        
    except Exception as e:
        logger.error(f"Error calculating delivery metrics: {e}")
        return default_metrics

def compute_user_performance_score(orders_df: pd.DataFrame, performance_df: pd.DataFrame, 
                                 userid: str, start_date: date, end_date: date) -> Tuple[float, str, str, str]:
    """
    Calculate comprehensive performance score for a user
    
    Returns:
        Tuple of (score, rating_label, rating_color, comment)
    """
    try:
        # Get individual metrics
        conversion_rate = get_user_conversion_rate(performance_df, userid, start_date, end_date)
        delivery_metrics = get_user_delivery_metrics(orders_df, userid, start_date, end_date)
        
        # Get user's order count for normalization
        user_orders = len(orders_df[
            (orders_df['created_by'].astype(str) == userid) & 
            (pd.to_datetime(orders_df['timestamp'], utc=True, errors='coerce').dt.tz_convert(IST).dt.date >= start_date) &
            (pd.to_datetime(orders_df['timestamp'], utc=True, errors='coerce').dt.tz_convert(IST).dt.date <= end_date)
        ])
        
        # Get top performer order count for normalization
        all_user_orders = orders_df[
            (pd.to_datetime(orders_df['timestamp'], utc=True, errors='coerce').dt.tz_convert(IST).dt.date >= start_date) &
            (pd.to_datetime(orders_df['timestamp'], utc=True, errors='coerce').dt.tz_convert(IST).dt.date <= end_date)
        ]
        
        if not all_user_orders.empty:
            top_user_orders = all_user_orders.groupby('created_by').size().max()
            global_top_aov = orders_df.groupby('created_by')['total'].mean().max() if 'total' in orders_df.columns else 1
        else:
            top_user_orders = 1
            global_top_aov = 1
        
        # Normalize metrics (0-100 scale)
        
        # 1. Conversion Rate (35% weight)
        if conversion_rate is not None:
            conversion_norm = min(100, conversion_rate * 3.33)  # 30% conversion = 100 points
        else:
            conversion_norm = 0
        
        # 2. Delivery Rate (30% weight)
        delivered_norm = delivery_metrics['delivery_rate']
        
        # 3. Order Volume (15% weight)
        orders_norm = min(100, (user_orders / max(1, top_user_orders)) * 100)
        
        # 4. Average Order Value (10% weight)
        aov_norm = min(100, (delivery_metrics['avg_order_value'] / max(1, global_top_aov)) * 100)
        
        # 5. Penalty for cancellations and returns (10% weight)
        penalty = min(30, delivery_metrics['cancellation_rate'] + delivery_metrics['return_rate'])
        
        # Calculate weighted score
        score = (
            conversion_norm * 0.35 +
            delivered_norm * 0.30 +
            orders_norm * 0.15 +
            aov_norm * 0.10 -
            penalty * 0.10
        )
        
        # Clamp score between 0 and 100
        score = max(0, min(100, score))
        
        # Determine rating and color
        if score >= 90:
            rating_label = "A+"
            rating_color = "success"
            comment = "Exceptional performance"
        elif score >= 75:
            rating_label = "A"
            rating_color = "lime"
            comment = "Excellent work"
        elif score >= 60:
            rating_label = "B"
            rating_color = "warning"
            comment = "Good performance"
        elif score >= 40:
            rating_label = "C"
            rating_color = "warning"
            comment = "Needs improvement"
        else:
            rating_label = "D"
            rating_color = "danger"
            comment = "Requires attention"
        
        return float(score), rating_label, rating_color, comment
        
    except Exception as e:
        logger.error(f"Error computing performance score: {e}")
        return 0.0, "N/A", "secondary", "Error calculating score"

def top_performers(orders_df: pd.DataFrame, performance_df: pd.DataFrame, 
                  start_date: date, end_date: date, top_n: int = 10) -> pd.DataFrame:
    """
    Generate top performers leaderboard
    
    Returns:
        DataFrame with top performers ranked by performance score
    """
    try:
        # Get all unique user IDs from orders
        user_orders = orders_df.copy()
        user_orders['timestamp'] = pd.to_datetime(user_orders['timestamp'], utc=True, errors='coerce')
        user_orders['date'] = user_orders['timestamp'].dt.tz_convert(IST).dt.date
        
        # Filter by date range
        mask = (user_orders['date'] >= start_date) & (user_orders['date'] <= end_date)
        filtered_orders = user_orders[mask]
        
        if filtered_orders.empty:
            return pd.DataFrame()
        
        unique_users = filtered_orders['created_by'].dropna().astype(str).unique()
        
        performers = []
        
        for userid in unique_users:
            # Calculate metrics for each user
            conversion_rate = get_user_conversion_rate(performance_df, userid, start_date, end_date)
            delivery_metrics = get_user_delivery_metrics(orders_df, userid, start_date, end_date)
            score, rating, rating_color, comment = compute_user_performance_score(
                orders_df, performance_df, userid, start_date, end_date
            )
            
            # Count orders for this user
            user_order_count = len(filtered_orders[filtered_orders['created_by'].astype(str) == userid])
            
            performers.append({
                'userid': userid,
                'total_orders': user_order_count,
                'total_revenue': delivery_metrics['total_revenue'],
                'avg_order_value': delivery_metrics['avg_order_value'],
                'delivery_rate': delivery_metrics['delivery_rate'],
                'conversion_rate': conversion_rate if conversion_rate is not None else 0.0,
                'performance_score': score,
                'rating': rating,
                'rating_color': rating_color,
                'comment': comment
            })
        
        # Create DataFrame and sort by performance score
        performers_df = pd.DataFrame(performers)
        performers_df = performers_df.sort_values('performance_score', ascending=False)
        
        # Return top N performers
        return performers_df.head(top_n).reset_index(drop=True)
        
    except Exception as e:
        logger.error(f"Error generating top performers: {e}")
        return pd.DataFrame()


# Unit Test Scaffold Suggestions (for future testing):
"""
Test cases to implement:

1. test_user_time_series_empty_data():
   - Test with empty orders_df
   - Test with user having no orders
   - Verify returns empty DataFrame with correct columns

2. test_conversion_rate_edge_cases():
   - Test with zero leads (should return None)
   - Test with missing Performance sheet
   - Test with valid conversion calculation

3. test_performance_score_normalization():
   - Test score clamping between 0-100
   - Test with extreme values
   - Test rating label mapping accuracy

4. test_status_normalization():
   - Test various status formats: "Delivered", "DELIVERED", "delivered", "out_for_delivery"
   - Test handling of None/NaN values
   - Verify consistent lowercase normalization

5. test_top_performers_ranking():
   - Test with multiple users
   - Verify correct sorting by performance score
   - Test with edge case of single user

Example usage:
assert normalize_status("Out For Delivery") == "out for delivery"
assert normalize_status(None) == "unknown"

conversion = get_user_conversion_rate(empty_df, "user1", start_date, end_date)
assert conversion is None

score, label, color, comment = compute_user_performance_score(orders_df, perf_df, "user1", start, end)
assert 0 <= score <= 100
assert label in ["A+", "A", "B", "C", "D"]
"""