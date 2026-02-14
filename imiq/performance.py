"""
IMIQ Performance Analytics Module
Comprehensive performance tracking and user analytics with KPIs, rankings, and export functionality.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import pytz
from typing import Optional, Dict, Any, List, Tuple
import io
import logging
import time
import hashlib

from .storage import get_storage_instance
from .kpis import (
    user_time_series, user_weekly_counts, user_monthly_counts,
    compute_user_performance_score, top_performers, get_user_conversion_rate,
    get_user_delivery_metrics, normalize_status
)
from .ui_components import render_metric_card, apply_custom_css
from .admin import (
    is_admin_mode, format_revenue, format_amount_metric,
    should_show_revenue_metrics, mask_revenue_dataframe,
    get_admin_filtered_columns
)

logger = logging.getLogger(__name__)

# Asia/Kolkata timezone
IST = pytz.timezone('Asia/Kolkata')

# Cache configuration
CACHE_TTL_SECONDS = 300  # 5 minute cache
MAX_RETRIES = 3
RETRY_DELAY = 2

def get_cache_key(sheet_name: str) -> str:
    """Generate cache key for sheet data"""
    return f"performance_cache_{sheet_name}_{int(time.time() // CACHE_TTL_SECONDS)}"

def get_cached_sheet_data(storage, sheet_name: str) -> pd.DataFrame:
    """Get sheet data with caching to reduce API calls"""
    cache_key = get_cache_key(sheet_name)
    
    # Check if data exists in session state cache
    if cache_key in st.session_state:
        logger.info(f"Using cached data for {sheet_name}")
        return st.session_state[cache_key]
    
    # Clear old cache entries
    keys_to_remove = [key for key in st.session_state.keys() 
                     if key.startswith(f"performance_cache_{sheet_name}_") and key != cache_key]
    for key in keys_to_remove:
        del st.session_state[key]
    
    # Try to read with retries
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Reading {sheet_name} from Google Sheets (attempt {attempt + 1})")
            df = storage.read_sheet(sheet_name)
            
            # Cache the data
            st.session_state[cache_key] = df
            return df
            
        except Exception as e:
            if "429" in str(e) or "Quota exceeded" in str(e):
                if attempt < MAX_RETRIES - 1:
                    wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Quota exceeded for {sheet_name}, waiting {wait_time}s before retry")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"Max retries exceeded for {sheet_name}: {e}")
                    # Return empty dataframe with expected structure
                    return get_fallback_dataframe(sheet_name)
            else:
                logger.error(f"Error reading {sheet_name}: {e}")
                return get_fallback_dataframe(sheet_name)
    
    return get_fallback_dataframe(sheet_name)

def get_fallback_dataframe(sheet_name: str) -> pd.DataFrame:
    """Return empty dataframe with expected columns when API fails"""
    if sheet_name == "Performance":
        return pd.DataFrame(columns=["date", "name", "no_of_leads", "no_of_orders", "ad_spend"])
    elif sheet_name == "Users":
        return pd.DataFrame(columns=["name", "userid", "role", "email"])
    elif sheet_name == "NewOrders":
        return pd.DataFrame(columns=["created_by", "timestamp", "total", "status", "delivery_status"])
    else:
        return pd.DataFrame()

def get_cache_status() -> Dict[str, Any]:
    """Get current cache status"""
    cached_sheets = [key for key in st.session_state.keys() if key.startswith("performance_cache_")]
    
    if not cached_sheets:
        return {"total_cached": 0, "last_updated": "Never"}
    
    # Get most recent cache timestamp
    latest_timestamp = 0
    for key in cached_sheets:
        parts = key.split("_")
        if len(parts) >= 4:
            try:
                timestamp = int(parts[-1]) * CACHE_TTL_SECONDS
                latest_timestamp = max(latest_timestamp, timestamp)
            except ValueError:
                continue
    
    last_updated = datetime.fromtimestamp(latest_timestamp).strftime("%H:%M:%S") if latest_timestamp > 0 else "Unknown"
    
    return {
        "total_cached": len(set(key.split("_")[2] for key in cached_sheets if len(key.split("_")) >= 4)),
        "last_updated": last_updated
    }

def clear_performance_cache():
    """Clear all performance-related cache"""
    keys_to_remove = [key for key in st.session_state.keys() if key.startswith("performance_cache_")]
    for key in keys_to_remove:
        del st.session_state[key]
    logger.info(f"Cleared {len(keys_to_remove)} cache entries")

def get_ist_today() -> date:
    """Get today's date in IST timezone"""
    return datetime.now(IST).date()

def render_performance_tab(storage=None):
    """Render the complete Performance Management system with multiple tabs"""
    apply_custom_css()
    
    st.markdown("## 📊 Performance Management System")
    
    # Cache status indicator
    col1, col2 = st.columns([3, 1])
    
    with col1:
        cache_info = get_cache_status()
        if cache_info["total_cached"] > 0:
            st.info(f"📊 Using cached data ({cache_info['total_cached']} sheets cached, last updated: {cache_info['last_updated']})")
    
    with col2:
        if st.button("🔄 Refresh Data", help="Clear cache and reload from Google Sheets"):
            clear_performance_cache()
            st.success("Cache cleared! Data will be refreshed on next load.")
            time.sleep(1)
            st.rerun()
    
    st.markdown("---")
    
    # Initialize storage
    try:
        if storage is None:
            storage = get_storage_instance()
    except Exception as e:
        st.error(f"Failed to initialize storage: {e}")
        return
        return
    
    # Create tabs for different performance functionalities
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Add Expenses", 
        "👤 View Staff Performance", 
        "🏆 Top Performers",
        "📊 Performance Analytics", 
        "📋 Manage Data"
    ])
    
    with tab1:
        render_add_expenses_tab(storage)
    
    with tab2:
        render_staff_performance_tab(storage)
    
    with tab3:
        render_top_performers_tab(storage)
    
    with tab4:
        render_performance_analytics_tab(storage)
    
    with tab5:
        render_manage_data_tab(storage)

def render_add_expenses_tab(storage):
    """Render the Add Expenses tab for performance data entry"""
    st.markdown("### 💰 Add Daily Performance & Expenses")
    st.markdown("Track daily leads, orders, and advertising spend for performance analysis")
    
    # Load required data
    try:
        users_df = get_cached_sheet_data(storage, "Users")
        orders_df = get_cached_sheet_data(storage, "NewOrders")
        performance_df = get_cached_sheet_data(storage, "Performance")
        
        if users_df.empty:
            st.error("No users found. Please add users first.")
            return
            
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return
    
    # Create form for data entry
    st.markdown("#### 📝 Enter Performance Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Date selection
        selected_date = st.date_input(
            "📅 Select Date",
            value=get_ist_today(),
            max_value=get_ist_today(),
            key="add_expenses_date_reactive",
            help="Choose the date for this performance record"
        )
        
        # User selection - use both user_id and name for display but match by user_id
        user_display_options = []
        user_id_mapping = {}
        
        for _, row in users_df.iterrows():
            if pd.notna(row.get('user_id')) and pd.notna(row.get('name')):
                display_text = f"{row['name']} ({row['user_id']})"
                user_display_options.append(display_text)
                user_id_mapping[display_text] = str(row['user_id']).strip()
        
        selected_user_display = st.selectbox(
            "👤 Select User",
            options=user_display_options,
            key="add_expenses_user_reactive",
            help="Choose the user for this performance record"
        )
        
        # Get the actual user_id for matching
        selected_user_id = user_id_mapping.get(selected_user_display, '') if selected_user_display else ''
        selected_user_name = selected_user_display.split(' (')[0] if selected_user_display else ''
        
    with col2:
        # Daily leads input
        daily_leads = st.number_input(
            "📈 Daily Leads Generated",
            min_value=0,
            value=0,
            step=1,
            key="add_expenses_leads_reactive",
            help="Enter the number of leads generated on this date"
        )
        
        # Ad spend input
        ad_spend = st.number_input(
            "💸 Ad Spend (₹)",
            min_value=0.0,
            value=0.0,
            step=10.0,
            format="%.2f",
            key="add_expenses_spend_reactive",
            help="Enter the amount spent on Meta/Facebook ads"
        )
    
    # Real-time order calculation outside the form
    if selected_user_id and selected_date:
        try:
            # Clean user IDs for consistent matching
            orders_df['created_by'] = orders_df['created_by'].astype(str).str.strip()
            user_orders = orders_df[orders_df['created_by'] == selected_user_id].copy()
            if not user_orders.empty and 'timestamp' in user_orders.columns:
                try:
                    user_orders['timestamp'] = pd.to_datetime(user_orders['timestamp'], format='mixed', errors='coerce', utc=True)
                    # Only apply .dt accessor if we have valid datetime values
                    valid_datetime_mask = user_orders['timestamp'].notna()
                    if valid_datetime_mask.any():
                        user_orders.loc[valid_datetime_mask, 'date'] = user_orders.loc[valid_datetime_mask, 'timestamp'].dt.date
                        date_orders = user_orders[user_orders['date'] == selected_date]
                        order_count = len(date_orders)
                    else:
                        st.warning("⚠️ Unable to parse timestamp data properly")
                        order_count = 0
                except Exception as dt_error:
                    st.warning(f"⚠️ Date parsing issue: {dt_error}")
                    order_count = 0
                
                # Show real-time calculation with enhanced styling
                col_info1, col_info2 = st.columns([2, 1])
                with col_info1:
                    st.info(f"🛍️ **Auto-calculated Orders**: {order_count} orders found for {selected_user_name} on {selected_date}")
                with col_info2:
                    if order_count > 0:
                        conversion_rate = (order_count / daily_leads * 100) if daily_leads > 0 else 0
                        st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
            else:
                order_count = 0
                st.warning(f"⚠️ No order data available for {selected_user_name}")
                
        except Exception as e:
            order_count = 0
            st.error(f"Could not calculate orders: {e}")
    else:
        order_count = 0
        if not selected_user_id:
            st.info("👤 Please select a user to see order calculations")
        elif not selected_date:
            st.info("📅 Please select a date to see order calculations")
    
    # Form for submission only
    with st.form("add_performance_form"):
        # Display current values
        col_summary1, col_summary2, col_summary3 = st.columns(3)
        with col_summary1:
            st.metric("📊 Leads", daily_leads)
        with col_summary2:
            st.metric("🛍️ Orders", order_count)
        with col_summary3:
            st.metric("💸 Ad Spend", f"₹{ad_spend:.2f}")
        
        # Submit button
        submitted = st.form_submit_button("✅ Add Performance Record", width='stretch')
        
        if submitted:
            if not selected_user_name or daily_leads < 0:
                st.error("Please fill in all required fields correctly.")
            else:
                try:
                    # Check if record already exists
                    existing_record = None
                    if not performance_df.empty:
                        datetime_col = pd.to_datetime(performance_df['date'], format='mixed', errors='coerce')
                        valid_datetime_mask = datetime_col.notna()
                        if valid_datetime_mask.any():
                            performance_df.loc[valid_datetime_mask, 'date'] = datetime_col.loc[valid_datetime_mask].dt.date
                        # Check for existing record using multiple possible user columns
                        existing_record = pd.DataFrame()
                        for col in ['user_id', 'userid', 'created_by', 'name']:
                            if col in performance_df.columns:
                                existing_record = performance_df[
                                    (performance_df[col].astype(str).str.strip() == str(selected_user_name).strip()) &
                                    (performance_df['date'] == selected_date)
                                ]
                                if not existing_record.empty:
                                    break
                    
                    # Prepare new record with both name and user_id for consistency
                    new_record = {
                        'date': selected_date.strftime('%Y-%m-%d'),
                        'name': selected_user_name,
                        'user_id': selected_user_id,  # Add user_id for consistent filtering
                        'no_of_leads': daily_leads,
                        'no_of_orders': order_count,
                        'ad_spend': ad_spend,
                        'created_at': datetime.now(IST).isoformat(),
                        'updated_at': datetime.now(IST).isoformat()
                    }
                    
                    if not existing_record.empty:
                        # Update existing record
                        st.warning("⚠️ Record already exists for this user and date. Updating...")
                        
                        # Update in Google Sheets
                        performance_df.loc[existing_record.index[0], 'no_of_leads'] = daily_leads
                        performance_df.loc[existing_record.index[0], 'no_of_orders'] = order_count
                        performance_df.loc[existing_record.index[0], 'ad_spend'] = ad_spend
                        performance_df.loc[existing_record.index[0], 'updated_at'] = new_record['updated_at']
                        
                        storage.replace_sheet("Performance", performance_df)
                        
                    else:
                        # Add new record
                        storage.append_row("Performance", new_record)
                    
                    st.success(f"✅ Performance record added successfully!")
                    st.balloons()
                    
                    # Show summary
                    st.markdown("#### 📋 Record Summary")
                    summary_data = {
                        "Field": ["Date", "User", "Leads", "Orders", "Ad Spend", "Conversion Rate"],
                        "Value": [
                            selected_date.strftime('%Y-%m-%d'),
                            selected_user_name,
                            f"{daily_leads:,}",
                            f"{order_count:,}",
                            f"₹{ad_spend:,.2f}",
                            f"{(order_count/daily_leads*100):.2f}%" if daily_leads > 0 else "N/A"
                        ]
                    }
                    st.table(pd.DataFrame(summary_data))
                    
                    # Refresh data after successful addition
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Failed to add record: {e}")
    
    # Display recent performance records
    st.markdown("---")
    st.markdown("### 📊 Recent Performance Records")
    
    try:
        current_performance = get_cached_sheet_data(storage, "Performance")
        if not current_performance.empty:
            # Add calculated columns
            current_performance['conversion_rate'] = (
                pd.to_numeric(current_performance['no_of_orders'], errors='coerce') /
                pd.to_numeric(current_performance['no_of_leads'], errors='coerce') * 100
            ).round(2)
            
            # Add cost per lead if ad_spend exists
            if 'ad_spend' in current_performance.columns:
                current_performance['cost_per_lead'] = (
                    pd.to_numeric(current_performance['ad_spend'], errors='coerce') /
                    pd.to_numeric(current_performance['no_of_leads'], errors='coerce')
                ).round(2)
                current_performance['cost_per_order'] = (
                    pd.to_numeric(current_performance['ad_spend'], errors='coerce') /
                    pd.to_numeric(current_performance['no_of_orders'], errors='coerce')
                ).round(2)
            
            # Format for display
            display_df = current_performance.copy()
            if 'date' in display_df.columns:
                datetime_col = pd.to_datetime(display_df['date'], format='mixed', errors='coerce')
                valid_datetime_mask = datetime_col.notna()
                if valid_datetime_mask.any():
                    display_df.loc[valid_datetime_mask, 'date'] = datetime_col.loc[valid_datetime_mask].dt.strftime('%Y-%m-%d')
            
            # Sort by date (newest first)
            if 'date' in display_df.columns:
                display_df = display_df.sort_values('date', ascending=False)
            
            st.dataframe(
                display_df,
                width='stretch',
                column_config={
                    "conversion_rate": st.column_config.NumberColumn(
                        "Conversion %",
                        format="%.2f%%"
                    ),
                    "cost_per_lead": st.column_config.NumberColumn(
                        "Cost/Lead",
                        format="₹%.2f"
                    ),
                    "cost_per_order": st.column_config.NumberColumn(
                        "Cost/Order", 
                        format="₹%.2f"
                    ),
                    "ad_spend": st.column_config.NumberColumn(
                        "Ad Spend",
                        format="₹%.2f"
                    )
                }
            )
        else:
            st.info("No performance records found. Add your first record above!")
            
    except Exception as e:
        st.error(f"Failed to display performance records: {e}")
    
def render_staff_performance_tab(storage):
    """Render individual staff performance analysis tab"""
    st.markdown("### 👤 Staff Performance Analysis")
    st.markdown("Comprehensive performance metrics for individual staff members")
    
    # Load data
    try:
        users_df = get_cached_sheet_data(storage, "Users") 
        orders_df = get_cached_sheet_data(storage, "NewOrders")
        performance_df = get_cached_sheet_data(storage, "Performance")
        
        if users_df.empty:
            st.error("No users found.")
            return
            
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return
    
    # User selection - use user_id instead of name
    user_options = users_df['user_id'].dropna().unique().tolist()
    selected_user = st.selectbox(
        "👤 Select Staff Member (User ID)",
        options=user_options,
        help="Choose a staff member by their User ID to view detailed performance"
    )
    
    if not selected_user:
        st.info("Please select a staff member to view performance metrics.")
        return
    
    # Date range filter with apply button
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        start_date = st.date_input(
            "📅 Start Date",
            value=get_ist_today() - timedelta(days=30),
            key="staff_performance_start_date"
        )
    with col2:
        end_date = st.date_input(
            "📅 End Date", 
            value=get_ist_today(),
            key="staff_performance_end_date"
        )
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
        apply_filter = st.button(
            "🔄 Apply Filter",
            help="Apply the selected date range filter",
            type="primary"
        )
    
    # Add auto-refresh toggle
    auto_refresh = st.checkbox(
        "🔄 Auto-refresh on date change", 
        value=True, 
        help="Automatically refresh data when date range changes"
    )
    
    st.markdown("---")
    
    # Only proceed with calculations if apply button is clicked or auto-refresh is enabled
    if not apply_filter and not auto_refresh:
        st.info("📊 Click 'Apply Filter' or enable 'Auto-refresh' to view performance data for the selected date range.")
        return
    
    # Calculate comprehensive KPIs for selected user
    user_kpis = calculate_user_kpis(storage, selected_user, start_date, end_date)
    
    # Display KPI Cards
    st.markdown("#### 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card(
            "Total Orders", 
            f"{user_kpis['total_orders']:,}", 
            "🛍️", 
            "primary"
        )
        
    with col2:
        render_metric_card(
            "Total Leads", 
            f"{user_kpis['total_leads']:,}", 
            "📈", 
            "info"
        )
        
    with col3:
        render_metric_card(
            "Conversion Rate", 
            f"{user_kpis['conversion_rate']:.2f}%", 
            "🎯", 
            "success" if user_kpis['conversion_rate'] > 15 else "warning"
        )
        
    with col4:
        render_metric_card(
            "Avg Order Value", 
            f"₹{user_kpis['avg_order_value']:,.2f}", 
            "💰", 
            "primary"
        )
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        render_metric_card(
            "Total Revenue", 
            f"₹{user_kpis['total_revenue']:,.2f}", 
            "💵", 
            "success"
        )
        
    with col6:
        render_metric_card(
            "Performance Score", 
            f"{user_kpis['performance_score']:,.0f}", 
            "⭐", 
            "primary"
        )
        
    with col7:
        render_metric_card(
            "Total Ad Spend", 
            f"₹{user_kpis['total_ad_spend']:,.2f}", 
            "💸", 
            "warning"
        )
        
    with col8:
        # Smart ROI display
        roi_value = user_kpis['roi']
        roi_display = (
            "N/A" if user_kpis['total_ad_spend'] == 0 else f"{roi_value:.1f}x"
        )
        roi_color = (
            "info" if user_kpis['total_ad_spend'] == 0 else
            "success" if roi_value > 2 else "warning"
        )
        
        render_metric_card(
            "ROI", 
            roi_display,
            "📈", 
            roi_color
        )
    
    # Add helpful message when no ad spend data is available
    if user_kpis['total_ad_spend'] == 0 and user_kpis['total_revenue'] > 0:
        st.info("💡 **Tip**: Add ad spend data in the 'Add Expenses' tab to calculate ROI and track advertising effectiveness!")
    
    st.markdown("---")
    
    # Detailed Performance Table
    st.markdown("#### 📋 Detailed Performance History")
    
    if not performance_df.empty:
        # Filter performance data for selected user by user_id
        # Try multiple possible user identification columns
        user_performance = pd.DataFrame()
        for col in ['user_id', 'userid', 'created_by', 'name']:
            if col in performance_df.columns:
                user_performance = performance_df[performance_df[col].astype(str).str.strip() == str(selected_user).strip()].copy()
                if not user_performance.empty:
                    break
        
        if not user_performance.empty:
            # Add calculated metrics
            user_performance['conversion_rate'] = (
                pd.to_numeric(user_performance['no_of_orders'], errors='coerce') /
                pd.to_numeric(user_performance['no_of_leads'], errors='coerce') * 100
            ).round(2)
            
            if 'ad_spend' in user_performance.columns:
                user_performance['cost_per_lead'] = (
                    pd.to_numeric(user_performance['ad_spend'], errors='coerce') /
                    pd.to_numeric(user_performance['no_of_leads'], errors='coerce')
                ).round(2)
                
                user_performance['cost_per_order'] = (
                    pd.to_numeric(user_performance['ad_spend'], errors='coerce') /
                    pd.to_numeric(user_performance['no_of_orders'], errors='coerce')
                ).round(2)
            
            # Format date
            if 'date' in user_performance.columns:
                datetime_col = pd.to_datetime(user_performance['date'], format='mixed', errors='coerce')
                valid_datetime_mask = datetime_col.notna()
                if valid_datetime_mask.any():
                    user_performance.loc[valid_datetime_mask, 'date'] = datetime_col.loc[valid_datetime_mask].dt.strftime('%Y-%m-%d')
            
            # Sort by date (newest first)
            user_performance = user_performance.sort_values('date', ascending=False)
            
            st.dataframe(
                user_performance,
                width='stretch',
                column_config={
                    "conversion_rate": st.column_config.NumberColumn(
                        "Conversion %",
                        format="%.2f%%"
                    ),
                    "cost_per_lead": st.column_config.NumberColumn(
                        "Cost/Lead",
                        format="₹%.2f"
                    ),
                    "cost_per_order": st.column_config.NumberColumn(
                        "Cost/Order",
                        format="₹%.2f"
                    ),
                    "ad_spend": st.column_config.NumberColumn(
                        "Ad Spend",
                        format="₹%.2f"
                    )
                }
            )
            
            # Performance trends chart
            st.markdown("#### 📈 Performance Trends")
            
            if len(user_performance) > 1:
                # Create trends chart
                fig = create_performance_trends_chart(user_performance)
                st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
            else:
                st.info("Need at least 2 records to show trends.")
                
        else:
            st.info(f"No performance records found for {selected_user}")
    else:
        st.info("No performance data available")

def render_top_performers_tab(storage):
    """Render top performers ranking tab"""
    st.markdown("### 🏆 Top Performers Dashboard")
    st.markdown("Rankings and comparisons of all staff performance")
    
    # Load data
    try:
        users_df = get_cached_sheet_data(storage, "Users") 
        orders_df = get_cached_sheet_data(storage, "NewOrders")
        performance_df = get_cached_sheet_data(storage, "Performance")
        
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return
    
    if users_df.empty:
        st.info("No users found.")
        return
    
    # Date range filter
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        start_date = st.date_input(
            "📅 Start Date",
            value=get_ist_today() - timedelta(days=30),
            key="top_performers_start_date"
        )
    with col2:
        end_date = st.date_input(
            "📅 End Date",
            value=get_ist_today(),
            key="top_performers_end_date"
        )
    with col3:
        ranking_metric = st.selectbox(
            "🎯 Rank By",
            options=[
                "Performance Score",
                "Conversion Rate", 
                "Total Revenue",
                "Total Orders",
                "ROI"
            ]
        )
    
    st.markdown("---")
    
    # Calculate rankings
    rankings = calculate_all_user_rankings(storage, start_date, end_date)
    
    if rankings.empty:
        st.info("No performance data found for the selected date range.")
        return
    
    # Sort by selected metric
    metric_mapping = {
        "Performance Score": "performance_score",
        "Conversion Rate": "conversion_rate", 
        "Total Revenue": "total_revenue",
        "Total Orders": "total_orders",
        "ROI": "roi"
    }
    
    sort_column = metric_mapping[ranking_metric]
    rankings = rankings.sort_values(sort_column, ascending=False).reset_index(drop=True)
    rankings.index += 1  # Start ranking from 1
    
    # Display top 3 performers
    st.markdown("#### 🥇 Top 3 Performers")
    
    if len(rankings) >= 3:
        col1, col2, col3 = st.columns(3)
        
        medals = ["🥇", "🥈", "🥉"]
        colors = ["success", "warning", "info"]
        
        for i, (col, medal, color) in enumerate(zip([col1, col2, col3], medals, colors)):
            if i < len(rankings):
                performer = rankings.iloc[i]
                with col:
                    st.markdown(f"### {medal} {performer['name']}")
                    render_metric_card(
                        ranking_metric,
                        f"{performer[sort_column]:,.2f}" + ("%" if "rate" in sort_column or "roi" in sort_column else ""),
                        "⭐",
                        color
                    )
    
    st.markdown("---")
    
    # Full rankings table
    st.markdown("#### 📊 Complete Performance Rankings")
    
    # Format the rankings table
    display_rankings = rankings.copy()
    display_rankings['rank'] = display_rankings.index
    
    # Format numeric columns
    numeric_columns = ['conversion_rate', 'total_revenue', 'avg_order_value', 'performance_score', 'roi']
    for col in numeric_columns:
        if col in display_rankings.columns:
            if col == 'conversion_rate':
                display_rankings[col] = display_rankings[col].apply(lambda x: f"{x:.2f}%")
            elif col == 'roi':
                display_rankings[col] = display_rankings[col].apply(lambda x: f"{x:.2f}x")
            elif col in ['total_revenue', 'avg_order_value', 'total_ad_spend']:
                display_rankings[col] = display_rankings[col].apply(lambda x: f"₹{x:,.2f}")
            else:
                display_rankings[col] = display_rankings[col].apply(lambda x: f"{x:,.0f}")
    
    st.dataframe(
        display_rankings,
        width='stretch',
        column_config={
            "rank": "Rank",
            "userid": st.column_config.TextColumn("User ID", width="small"),
            "name": "Staff Member", 
            "total_orders": "Orders",
            "total_leads": "Leads",
            "conversion_rate": "Conversion %",
            "total_revenue": "Revenue", 
            "avg_order_value": "AOV",
            "performance_score": "Score",
            "roi": "ROI"
        }
    )
    
    # Performance comparison chart
    st.markdown("#### 📈 Performance Comparison")
    
    if len(rankings) > 1:
        comparison_chart = create_performance_comparison_chart(rankings, sort_column)
        st.plotly_chart(comparison_chart, width='stretch', config={'displayModeBar': False})

def render_performance_analytics_tab(storage):
    """Render advanced performance analytics"""
    st.markdown("### 📊 Performance Analytics Dashboard")
    st.markdown("Advanced analytics and insights from performance data")
    
    # This will contain the original analytics functionality
    # Load data with spinner
    with st.spinner("Loading performance data..."):
        try:
            users_df = get_cached_sheet_data(storage, "Users")
            orders_df = get_cached_sheet_data(storage, "NewOrders") 
            performance_df = get_cached_sheet_data(storage, "Performance")
            
        except Exception as e:
            st.error(f"Failed to load data: {e}")
            return
    
    # Check if data exists
    if users_df.empty:
        st.warning("👥 No users found in Users sheet. Please add users first.")
        return
    
    # Date filter section
    st.markdown("### 📅 Analysis Period")
    col_date1, col_date2, col_date3 = st.columns([2, 2, 2])
    
    default_end = get_ist_today()
    default_start = default_end - timedelta(days=30)
    
    with col_date1:
        start_date = st.date_input(
            "Start Date",
            value=default_start,
            max_value=default_end,
            key="analytics_start_date"
        )
    
    with col_date2:
        end_date = st.date_input(
            "End Date", 
            value=default_end,
            key="analytics_end_date",
            min_value=start_date
        )
    
    with col_date3:
        st.markdown(f"**Analysis Period:** {(end_date - start_date).days + 1} days")
    
    st.markdown("---")
    
    # Overall metrics
    overall_metrics = calculate_overall_metrics(storage, start_date, end_date)
    
    st.markdown("#### 🎯 Overall Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric_card("Total Orders", f"{overall_metrics['total_orders']:,}", "🛍️", "primary")
    with col2:
        render_metric_card("Total Leads", f"{overall_metrics['total_leads']:,}", "📈", "info")
    with col3:
        render_metric_card("Overall Conversion", f"{overall_metrics['overall_conversion']:.2f}%", "🎯", "success")
    with col4:
        render_metric_card("Total Revenue", f"₹{overall_metrics['total_revenue']:,.2f}", "💰", "success")

def render_manage_data_tab(storage):
    """Render data management tab for editing/deleting performance records"""
    st.markdown("### 📋 Manage Performance Data")
    st.markdown("Edit, update, or delete performance records")
    
    # Load performance data
    try:
        performance_df = get_cached_sheet_data(storage, "Performance")
        if performance_df.empty:
            st.info("No performance records to manage.")
            return
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return
    
    # Add record ID if not exists
    if 'record_id' not in performance_df.columns:
        performance_df['record_id'] = range(1, len(performance_df) + 1)
    
    # Display editable dataframe
    st.markdown("#### ✏️ Edit Performance Records")
    st.markdown("Click on cells to edit values. Changes are applied immediately.")
    
    edited_df = st.data_editor(
        performance_df,
        width='stretch',
        num_rows="dynamic",
        disabled=["record_id"],
        column_config={
            "no_of_leads": st.column_config.NumberColumn("Leads", min_value=0),
            "no_of_orders": st.column_config.NumberColumn("Orders", min_value=0),
            "ad_spend": st.column_config.NumberColumn("Ad Spend", format="₹%.2f", min_value=0.0)
        },
        key="performance_editor"
    )
    
    # Save changes button
    if st.button("💾 Save Changes", type="primary"):
        try:
            storage.replace_sheet("Performance", edited_df)
            st.success("✅ Changes saved successfully!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            st.error(f"Failed to save changes: {e}")
    
    st.markdown("---")
    
    # Bulk operations
    st.markdown("#### 🔧 Bulk Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.session_state.get("confirm_clear", False):
                try:
                    # Keep only headers
                    empty_df = pd.DataFrame(columns=performance_df.columns)
                    storage.replace_sheet("Performance", empty_df)
                    st.success("✅ All performance data cleared!")
                    st.session_state["confirm_clear"] = False
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to clear data: {e}")
            else:
                st.session_state["confirm_clear"] = True
                st.warning("⚠️ Click again to confirm clearing all data!")
    
    with col2:
        if st.button("📥 Export Data", type="secondary"):
            try:
                csv = performance_df.to_csv(index=False)
                st.download_button(
                    label="📄 Download CSV",
                    data=csv,
                    file_name=f"performance_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Failed to export data: {e}")

# Helper functions for calculations

# Helper functions for calculations

def calculate_user_kpis(storage, user_id: str, start_date: date, end_date: date) -> Dict[str, float]:
    """Calculate comprehensive KPIs for a specific user"""
    try:
        # Load data
        orders_df = get_cached_sheet_data(storage, "NewOrders")
        performance_df = get_cached_sheet_data(storage, "Performance")
        
        # Initialize metrics
        kpis = {
            'total_orders': 0,
            'total_leads': 0,
            'total_revenue': 0.0,
            'avg_order_value': 0.0,
            'conversion_rate': 0.0,
            'performance_score': 0.0,
            'total_ad_spend': 0.0,
            'roi': 0.0
        }
        
        # Calculate from orders data
        if not orders_df.empty and 'created_by' in orders_df.columns:
            # Clean user IDs for consistent matching
            orders_df['created_by'] = orders_df['created_by'].astype(str).str.strip()
            clean_user_id = str(user_id).strip()
            user_orders = orders_df[orders_df['created_by'] == clean_user_id].copy()
            
            if not user_orders.empty:
                # Filter by date range if timestamp available
                if 'timestamp' in user_orders.columns:
                    try:
                        user_orders['timestamp'] = pd.to_datetime(user_orders['timestamp'], format='mixed', errors='coerce', utc=True)
                        if user_orders['timestamp'].notna().any():
                            user_orders['date'] = user_orders['timestamp'].dt.date
                            user_orders = user_orders[
                                (user_orders['date'] >= start_date) & 
                                (user_orders['date'] <= end_date)
                            ]
                        else:
                            # If no valid timestamps, can't filter by date
                            pass
                    except Exception:
                        # Skip date filtering if parsing fails
                        pass
                
                kpis['total_orders'] = len(user_orders)
                
                # Revenue calculations
                if 'total' in user_orders.columns:
                    revenue_values = pd.to_numeric(user_orders['total'], errors='coerce').fillna(0)
                    kpis['total_revenue'] = float(revenue_values.sum())
                    kpis['avg_order_value'] = float(revenue_values.mean()) if len(revenue_values) > 0 else 0.0
        
        # Calculate from performance data
        if not performance_df.empty:
            # Try different possible user identification columns
            user_performance = pd.DataFrame()
            for col in ['user_id', 'created_by', 'name']:
                if col in performance_df.columns:
                    user_performance = performance_df[performance_df[col].astype(str).str.strip() == str(user_id).strip()].copy()
                    if not user_performance.empty:
                        break
            
            if not user_performance.empty:
                # Filter by date range
                if 'date' in user_performance.columns:
                    try:
                        user_performance['date'] = pd.to_datetime(user_performance['date'], format='mixed', errors='coerce')
                        # Only use .dt accessor if we have valid datetime values
                        valid_datetime_mask = user_performance['date'].notna()
                        if valid_datetime_mask.any():
                            user_performance.loc[valid_datetime_mask, 'parsed_date'] = user_performance.loc[valid_datetime_mask, 'date'].dt.date
                            user_performance = user_performance[
                                (user_performance['parsed_date'] >= start_date) & 
                                (user_performance['parsed_date'] <= end_date)
                            ]
                        else:
                            # If no valid dates, can't filter
                            pass
                    except Exception:
                        # Skip date filtering if parsing fails
                        pass
                
                # Sum up performance metrics
                if 'no_of_leads' in user_performance.columns:
                    kpis['total_leads'] = int(pd.to_numeric(user_performance['no_of_leads'], errors='coerce').fillna(0).sum())
                
                if 'ad_spend' in user_performance.columns:
                    kpis['total_ad_spend'] = float(pd.to_numeric(user_performance['ad_spend'], errors='coerce').fillna(0).sum())
        
        # Calculate derived metrics
        if kpis['total_leads'] > 0:
            kpis['conversion_rate'] = (kpis['total_orders'] / kpis['total_leads']) * 100
        
        kpis['performance_score'] = kpis['total_orders'] * kpis['avg_order_value']
        
        # Calculate ROI - Handle zero ad spend case
        if kpis['total_ad_spend'] > 0:
            kpis['roi'] = kpis['total_revenue'] / kpis['total_ad_spend']
        else:
            kpis['roi'] = 0.0  # Cannot calculate ROI without ad spend data
        
        return kpis
        
    except Exception as e:
        logger.error(f"Error calculating user KPIs: {e}")
        return {
            'total_orders': 0,
            'total_leads': 0,
            'total_revenue': 0.0,
            'avg_order_value': 0.0,
            'conversion_rate': 0.0,
            'performance_score': 0.0,
            'total_ad_spend': 0.0,
            'roi': 0.0
        }

def calculate_all_user_rankings(storage, start_date: date, end_date: date) -> pd.DataFrame:
    """Calculate rankings for all users"""
    try:
        users_df = storage.read_sheet("Users")
        
        if users_df.empty:
            return pd.DataFrame()
        
        rankings_data = []
        
        for _, user in users_df.iterrows():
            user_id = user.get('user_id') or user.get('userid')
            if pd.notna(user_id):
                kpis = calculate_user_kpis(storage, user_id, start_date, end_date)
                
                rankings_data.append({
                    'userid': user_id,
                    'name': user.get('name', user_id),
                    'total_orders': kpis['total_orders'],
                    'total_leads': kpis['total_leads'],
                    'conversion_rate': kpis['conversion_rate'],
                    'total_revenue': kpis['total_revenue'],
                    'avg_order_value': kpis['avg_order_value'],
                    'performance_score': kpis['performance_score'],
                    'total_ad_spend': kpis['total_ad_spend'],
                    'roi': kpis['roi']
                })
        
        return pd.DataFrame(rankings_data)
        
    except Exception as e:
        logger.error(f"Error calculating rankings: {e}")
        return pd.DataFrame()

def calculate_overall_metrics(storage, start_date: date, end_date: date) -> Dict[str, float]:
    """Calculate overall system performance metrics"""
    try:
        orders_df = storage.read_sheet("NewOrders")
        performance_df = storage.read_sheet("Performance")
        
        metrics = {
            'total_orders': 0,
            'total_leads': 0,
            'overall_conversion': 0.0,
            'total_revenue': 0.0,
            'total_ad_spend': 0.0,
            'system_roi': 0.0
        }
        
        # Orders metrics
        if not orders_df.empty:
            filtered_orders = orders_df.copy()
            
            if 'timestamp' in filtered_orders.columns:
                try:
                    filtered_orders['timestamp'] = pd.to_datetime(filtered_orders['timestamp'], format='mixed', errors='coerce', utc=True)
                    # Only use .dt accessor if we have valid datetime values
                    valid_datetime_mask = filtered_orders['timestamp'].notna()
                    if valid_datetime_mask.any():
                        filtered_orders.loc[valid_datetime_mask, 'date'] = filtered_orders.loc[valid_datetime_mask, 'timestamp'].dt.date
                        filtered_orders = filtered_orders[
                            (filtered_orders['date'] >= start_date) & 
                            (filtered_orders['date'] <= end_date)
                        ]
                    # If no valid timestamps, keep all orders (no date filtering)
                except Exception:
                    # Skip date filtering if parsing fails
                    pass
            
            metrics['total_orders'] = len(filtered_orders)
            
            if 'total' in filtered_orders.columns:
                metrics['total_revenue'] = float(pd.to_numeric(filtered_orders['total'], errors='coerce').fillna(0).sum())
        
        # Performance metrics
        if not performance_df.empty:
            filtered_performance = performance_df.copy()
            
            if 'date' in filtered_performance.columns:
                try:
                    filtered_performance['date'] = pd.to_datetime(filtered_performance['date'], format='mixed', errors='coerce')
                    # Only use .dt accessor if we have valid datetime values
                    valid_datetime_mask = filtered_performance['date'].notna()
                    if valid_datetime_mask.any():
                        filtered_performance.loc[valid_datetime_mask, 'parsed_date'] = filtered_performance.loc[valid_datetime_mask, 'date'].dt.date
                        filtered_performance = filtered_performance[
                            (filtered_performance['parsed_date'] >= start_date) & 
                            (filtered_performance['parsed_date'] <= end_date)
                        ]
                    # If no valid dates, keep all performance data
                except Exception:
                    # Skip date filtering if parsing fails
                    pass
            
            if 'no_of_leads' in filtered_performance.columns:
                metrics['total_leads'] = int(pd.to_numeric(filtered_performance['no_of_leads'], errors='coerce').fillna(0).sum())
            
            if 'ad_spend' in filtered_performance.columns:
                metrics['total_ad_spend'] = float(pd.to_numeric(filtered_performance['ad_spend'], errors='coerce').fillna(0).sum())
        
        # Calculate derived metrics
        if metrics['total_leads'] > 0:
            metrics['overall_conversion'] = (metrics['total_orders'] / metrics['total_leads']) * 100
        
        # Calculate system ROI - Handle zero ad spend case
        if metrics['total_ad_spend'] > 0:
            metrics['system_roi'] = metrics['total_revenue'] / metrics['total_ad_spend']
        else:
            metrics['system_roi'] = 0.0  # Cannot calculate ROI without ad spend data
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error calculating overall metrics: {e}")
        return {
            'total_orders': 0,
            'total_leads': 0,
            'overall_conversion': 0.0,
            'total_revenue': 0.0,
            'total_ad_spend': 0.0,
            'system_roi': 0.0
        }

def create_performance_trends_chart(performance_data: pd.DataFrame):
    """Create performance trends chart for individual user"""
    try:
        fig = go.Figure()
        
        # Sort by date
        performance_data = performance_data.sort_values('date')
        
        # Add leads trend
        fig.add_trace(go.Scatter(
            x=performance_data['date'],
            y=pd.to_numeric(performance_data['no_of_leads'], errors='coerce'),
            mode='lines+markers',
            name='Leads Generated',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6)
        ))
        
        # Add orders trend
        fig.add_trace(go.Scatter(
            x=performance_data['date'],
            y=pd.to_numeric(performance_data['no_of_orders'], errors='coerce'),
            mode='lines+markers',
            name='Orders Converted',
            line=dict(color='#ff7f0e', width=2),
            marker=dict(size=6)
        ))
        
        # Add conversion rate on secondary y-axis
        fig.add_trace(go.Scatter(
            x=performance_data['date'],
            y=performance_data['conversion_rate'],
            mode='lines+markers',
            name='Conversion Rate (%)',
            line=dict(color='#2ca02c', width=2, dash='dash'),
            marker=dict(size=6),
            yaxis='y2'
        ))
        
        # Update layout
        fig.update_layout(
            title="Performance Trends Over Time",
            xaxis_title="Date",
            yaxis=dict(title="Leads & Orders", side='left'),
            yaxis2=dict(title="Conversion Rate (%)", side='right', overlaying='y'),
            legend=dict(x=0, y=1),
            hovermode='x unified'
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating trends chart: {e}")
        return go.Figure()

def create_performance_comparison_chart(rankings: pd.DataFrame, metric: str):
    """Create performance comparison chart"""
    try:
        fig = px.bar(
            rankings.head(10),  # Top 10 performers
            x='name',
            y=metric,
            title=f"Performance Comparison - {metric.replace('_', ' ').title()}",
            color=metric,
            color_continuous_scale='viridis'
        )
        
        fig.update_layout(
            xaxis_title="Staff Members",
            yaxis_title=metric.replace('_', ' ').title(),
            xaxis_tickangle=-45
        )
        
        return fig
        
    except Exception as e:
        logger.error(f"Error creating comparison chart: {e}")
        return go.Figure()

# Function declarations
def render_single_user_view(storage, users_df: pd.DataFrame, orders_df: pd.DataFrame, 
                          performance_df: pd.DataFrame, userid: str, start_date: date, end_date: date):
    
    # Get user info by user_id
    user_info = pd.DataFrame()
    for col in ['user_id', 'userid']:
        if col in users_df.columns:
            user_info = users_df[users_df[col].astype(str).str.strip() == str(userid).strip()]
            if not user_info.empty:
                break
    
    if user_info.empty:
        st.error(f"User {userid} not found in Users sheet")
        return
    
    user_info = user_info.iloc[0]
    
    # Employee Status Card
    st.markdown("### 👨‍💼 Employee Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        role = user_info.get('role', 'Not specified')
        render_metric_card("Role", str(role), "👔", "info")
    
    with col2:
        # Get last active date from orders
        # Clean user IDs for consistent matching
        orders_df['created_by'] = orders_df['created_by'].astype(str).str.strip()
        clean_userid = str(userid).strip()
        user_orders = orders_df[orders_df['created_by'] == clean_userid]
        if not user_orders.empty:
            try:
                user_orders['timestamp'] = pd.to_datetime(user_orders['timestamp'], format='mixed', errors='coerce', utc=True)
                last_active = user_orders['timestamp'].max().strftime('%Y-%m-%d')
            except:
                last_active = "Unknown"
        else:
            last_active = "No orders"
        render_metric_card("Last Active", last_active, "📅", "secondary")
    
    with col3:
        # Today's orders count
        today = get_ist_today()
        today_orders = get_today_orders_count(orders_df, userid, today)
        render_metric_card("Today's Orders", str(today_orders), "📋", "primary")
    
    st.markdown("---")
    
    # Time series and performance metrics
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        # Orders time series charts
        st.markdown("#### 📈 Orders Analytics")
        
        # Daily orders chart
        daily_data = user_time_series(orders_df, userid, start_date, end_date)
        if not daily_data.empty:
            fig_daily = px.line(
                daily_data, x='date', y='order_count'
            )
            fig_daily.update_layout(
                title='Daily Orders',
                xaxis_title='Date',
                yaxis_title='Orders',
                height=300
            )
            st.plotly_chart(fig_daily, width='stretch', config={'displayModeBar': False})
        else:
            st.info("No order data found for the selected period")
        
        # Weekly/Monthly aggregations
        tab1, tab2 = st.tabs(["📅 Weekly", "📆 Monthly"])
        
        with tab1:
            weekly_data = user_weekly_counts(orders_df, userid, start_date, end_date)
            if not weekly_data.empty:
                fig_weekly = px.bar(
                    weekly_data, x='week', y='order_count'
                )
                fig_weekly.update_layout(
                    title='Weekly Orders',
                    xaxis_title='Week',
                    yaxis_title='Orders',
                    height=250
                )
                st.plotly_chart(fig_weekly, width='stretch', config={'displayModeBar': False})
            else:
                st.info("No weekly data available")
        
        with tab2:
            monthly_data = user_monthly_counts(orders_df, userid, start_date, end_date)
            if not monthly_data.empty:
                fig_monthly = px.bar(
                    monthly_data, x='month', y='order_count'
                )
                fig_monthly.update_layout(
                    title='Monthly Orders',
                    xaxis_title='Month',
                    yaxis_title='Orders',
                    height=250
                )
                st.plotly_chart(fig_monthly, width='stretch', config={'displayModeBar': False})
            else:
                st.info("No monthly data available")
    
    with col_right:
        # Performance KPIs
        st.markdown("#### 🎯 Performance KPIs")
        
        # Leads → Orders conversion
        conversion_rate = get_user_conversion_rate(performance_df, userid, start_date, end_date)
        if conversion_rate is not None:
            if conversion_rate >= 30:
                conv_status = "Excellent"
                conv_color = "success"
                conv_comment = "Keep pushing — high conversion"
            elif conversion_rate >= 15:
                conv_status = "Good" 
                conv_color = "warning"
                conv_comment = "Good progress, aim higher"
            else:
                conv_status = "Needs Improvement"
                conv_color = "danger"
                conv_comment = "Focus on lead quality & follow-up"
            
            render_metric_card("Conversion Rate", f"{conversion_rate:.1f}%", "🎯", conv_color)
            st.markdown(f"**Status:** {conv_status}")
            st.markdown(f"*{conv_comment}*")
        else:
            render_metric_card("Conversion Rate", "No leads recorded", "🎯", "secondary")
        
        # Date-wise Conversion Rate Analysis
        st.markdown("---")
        st.markdown("#### 📊 Date-wise Conversion Analysis")
        
        if not performance_df.empty:
            # Get date-wise conversion data for this user
            # Find the correct user column
            user_column = None
            for col in ['created_by', 'userid', 'user_id', 'name', 'email']:
                if col in performance_df.columns:
                    user_column = col
                    break
            
            if user_column:
                user_perf_data = performance_df[
                    performance_df[user_column].astype(str) == str(userid)
                ].copy()
            else:
                user_perf_data = pd.DataFrame()  # Empty if no user column found
            
            if not user_perf_data.empty:
                # Parse dates and filter by date range
                try:
                    date_col = None
                    for col in ['date', 'Date', 'timestamp', 'created_at']:
                        if col in user_perf_data.columns:
                            date_col = col
                            break
                    
                    if date_col:
                        datetime_col = pd.to_datetime(user_perf_data[date_col], format='mixed', errors='coerce')
                        valid_datetime_mask = datetime_col.notna()
                        if valid_datetime_mask.any():
                            user_perf_data.loc[valid_datetime_mask, 'parsed_date'] = datetime_col.loc[valid_datetime_mask].dt.date
                        
                        # Filter by selected date range
                        mask = (user_perf_data['parsed_date'] >= start_date) & (user_perf_data['parsed_date'] <= end_date)
                        filtered_perf = user_perf_data[mask]
                        
                        if not filtered_perf.empty:
                            # Prepare data for chart
                            chart_data = []
                            for _, row in filtered_perf.iterrows():
                                leads = pd.to_numeric(row.get('no_of_leads', row.get('leads', 0)), errors='coerce')
                                orders = pd.to_numeric(row.get('no_of_orders', row.get('orders', 0)), errors='coerce')
                                
                                if pd.notna(leads) and pd.notna(orders) and leads > 0:
                                    conv_rate = (orders / leads) * 100
                                    chart_data.append({
                                        'Date': row['parsed_date'],
                                        'Leads': int(leads),
                                        'Orders': int(orders),
                                        'Conversion Rate (%)': round(conv_rate, 1)
                                    })
                            
                            if chart_data:
                                chart_df = pd.DataFrame(chart_data).sort_values('Date')
                                
                                # Create conversion rate trend chart
                                fig = px.line(
                                    chart_df, 
                                    x='Date', 
                                    y='Conversion Rate (%)', 
                                    markers=True,
                                    line_shape='spline'
                                )
                                fig.update_layout(
                                    title=f'Daily Conversion Rate Trend - {userid}',
                                    height=350,
                                    showlegend=False,
                                    xaxis_title="Date",
                                    yaxis_title="Conversion Rate (%)"
                                )
                                st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
                                
                                # Show detailed table
                                col_table1, col_table2 = st.columns([3, 1])
                                
                                with col_table1:
                                    st.markdown("**📋 Date-wise Performance Data**")
                                    st.dataframe(
                                        chart_df,
                                        width='stretch',
                                        hide_index=True
                                    )
                                
                                with col_table2:
                                    st.markdown("**📈 Summary Stats**")
                                    avg_conv = chart_df['Conversion Rate (%)'].mean()
                                    total_leads = chart_df['Leads'].sum()
                                    total_orders = chart_df['Orders'].sum()
                                    overall_conv = (total_orders / total_leads) * 100 if total_leads > 0 else 0
                                    
                                    st.metric("Average Daily", f"{avg_conv:.1f}%")
                                    st.metric("Overall Period", f"{overall_conv:.1f}%")
                                    st.metric("Total Leads", f"{total_leads:,}")
                                    st.metric("Total Orders", f"{total_orders:,}")
                                    
                            else:
                                st.info("📊 No valid conversion data found for selected date range")
                        else:
                            st.info("📅 No performance data found for selected date range")
                    else:
                        st.warning("⚠️ No date column found in Performance sheet")
                        
                except Exception as e:
                    st.error(f"Error processing date-wise conversion data: {str(e)}")
            else:
                st.info("📊 No performance data found for this user")
        else:
            st.warning("📊 Performance sheet is empty - please add conversion data")
        
        st.markdown("---")
        
        # Delivery metrics
        delivery_metrics = get_user_delivery_metrics(orders_df, userid, start_date, end_date)
        
        render_metric_card("Delivered", f"{delivery_metrics['delivered_count']}", "✅", "success")
        render_metric_card("Returns", f"{delivery_metrics['returns_count']}", "↩️", "danger")
        render_metric_card("Delivery Rate", f"{delivery_metrics['delivery_rate']:.1f}%", "📦", "info")
        render_metric_card("Cancellation Rate", f"{delivery_metrics['cancellation_rate']:.1f}%", "❌", "warning")
        render_metric_card("Avg Order Value", f"₹{delivery_metrics['avg_order_value']:.2f}", "💰", "primary")
        
        st.markdown("---")
        
        # Overall Performance Score
        score, rating_label, rating_color, comment = compute_user_performance_score(
            orders_df, performance_df, userid, start_date, end_date
        )
        
        st.markdown("#### 🏆 Overall Performance")
        render_metric_card("Performance Score", f"{score:.1f}/100", "📊", "primary")
        
        # Rating badge with color
        badge_colors = {
            "success": "#10b981",
            "lime": "#84cc16", 
            "warning": "#f59e0b",
            "danger": "#ef4444"
        }
        badge_color = badge_colors.get(rating_color, "#6b7280")
        
        st.markdown(f"""
        <div style="
            background: {badge_color};
            color: white;
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            font-weight: bold;
            font-size: 1.2rem;
            margin: 1rem 0;
        ">
            🏆 Rating: {rating_label}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**Comment:** {comment}")
    
    st.markdown("---")
    
    # Export Report
    st.markdown("### 📊 Export User Report")
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        if st.button("📥 Download Performance Report", key="download_user_report"):
            report_data = generate_user_report(orders_df, performance_df, userid, start_date, end_date)
            csv_buffer = io.StringIO()
            report_data.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="📄 Download CSV Report",
                data=csv_data,
                file_name=f"performance_report_{userid}_{start_date}_to_{end_date}.csv",
                mime="text/csv"
            )

def render_all_users_view(storage, users_df: pd.DataFrame, orders_df: pd.DataFrame,
                         performance_df: pd.DataFrame, start_date: date, end_date: date):
    """Render aggregated view for all users with top performers leaderboard"""
    
    st.markdown("### 🏆 Top Performers Leaderboard")
    
    with st.spinner("Computing performance rankings..."):
        top_performers_df = top_performers(orders_df, performance_df, start_date, end_date, top_n=10)
    
    if not top_performers_df.empty:
        # Display top 5 as cards
        st.markdown("#### 🥇 Top 5 Performers")
        cols = st.columns(5)
        
        for i, (_, performer) in enumerate(top_performers_df.head(5).iterrows()):
            if i < len(cols):
                with cols[i]:
                    rank_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]
                    render_metric_card(
                        f"{rank_emoji} {performer['userid']}",
                        f"{performer['performance_score']:.1f}/100",
                        "🏆",
                        "success" if i == 0 else "primary"
                    )
                    st.markdown(f"**Orders:** {performer['total_orders']}")
                    st.markdown(f"**Revenue:** ₹{performer['total_revenue']:.2f}")
                    st.markdown(f"**Conv. Rate:** {performer['conversion_rate']:.1f}%")
        
        st.markdown("---")
        
        # Full leaderboard table
        st.markdown("#### 📋 Complete Leaderboard")
        
        # Format the dataframe for display
        display_df = top_performers_df.copy()
        
        # Try to merge with users_df to get user names
        try:
            if not users_df.empty and 'userid' in users_df.columns:
                # Merge on userid to get names
                users_lookup = users_df[['userid', 'name']].drop_duplicates()
                display_df = pd.merge(
                    display_df, 
                    users_lookup, 
                    left_on='userid', 
                    right_on='userid', 
                    how='left'
                )
                # Fill missing names with userid
                display_df['name'] = display_df['name'].fillna(display_df['userid'])
            else:
                # If no userid column or empty users_df, use userid as name
                display_df['name'] = display_df['userid']
        except Exception as e:
            st.warning(f"Could not merge user names: {e}")
            # Fallback: use userid as name
            display_df['name'] = display_df['userid']
        
        display_df['Rank'] = range(1, len(display_df) + 1)
        display_df['Performance Score'] = display_df['performance_score'].round(1)
        display_df['Total Revenue'] = display_df['total_revenue'].round(2)
        display_df['Conversion Rate'] = display_df['conversion_rate'].round(1)
        display_df['Avg Order Value'] = display_df['avg_order_value'].round(2)
        
        # Select and reorder columns for display based on admin mode
        all_display_columns = [
            'Rank', 'name', 'Performance Score', 'total_orders', 
            'Total Revenue', 'Conversion Rate', 'Avg Order Value', 'rating'
        ]
        
        # Filter columns based on admin mode
        revenue_columns = ['Total Revenue', 'Avg Order Value']
        display_columns = get_admin_filtered_columns(all_display_columns, revenue_columns)
        
        # Apply revenue masking if not in admin mode
        display_data = mask_revenue_dataframe(display_df, ['Total Revenue', 'Avg Order Value'])
        
        st.dataframe(
            display_data[display_columns].rename(columns={
                'name': 'User Name',
                'total_orders': 'Total Orders',
                'rating': 'Rating'
            }),
            width='stretch',
            hide_index=True
        )
        
        # Overall stats
        st.markdown("#### 📊 Overall Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_users = len(top_performers_df)
            render_metric_card("Active Users", str(total_users), "👥", "info")
        
        with col2:
            total_orders = top_performers_df['total_orders'].sum()
            render_metric_card("Total Orders", str(total_orders), "📦", "primary")
        
        with col3:
            total_revenue = top_performers_df['total_revenue'].sum()
            if should_show_revenue_metrics():
                render_metric_card("Total Revenue", format_revenue(total_revenue), "💰", "success")
            else:
                render_metric_card("Total Revenue", "Admin Only", "🔒", "warning")
        
        with col4:
            avg_performance = top_performers_df['performance_score'].mean()
            render_metric_card("Avg Performance", f"{avg_performance:.1f}/100", "📊", "secondary")
        
        # Overall Conversion Rate Analysis
        st.markdown("---")
        st.markdown("#### 🎯 Overall Conversion Rate Analysis")
        
        if not performance_df.empty:
            conv_col1, conv_col2, conv_col3 = st.columns(3)
            
            try:
                # Parse dates and filter by date range
                date_col = None
                for col in ['date', 'Date', 'timestamp', 'created_at']:
                    if col in performance_df.columns:
                        date_col = col
                        break
                
                if date_col:
                    perf_filtered = performance_df.copy()
                    datetime_col = pd.to_datetime(perf_filtered[date_col], format='mixed', errors='coerce')
                    valid_datetime_mask = datetime_col.notna()
                    if valid_datetime_mask.any():
                        perf_filtered.loc[valid_datetime_mask, 'parsed_date'] = datetime_col.loc[valid_datetime_mask].dt.date
                    
                    # Filter by selected date range
                    mask = (perf_filtered['parsed_date'] >= start_date) & (perf_filtered['parsed_date'] <= end_date)
                    perf_filtered = perf_filtered[mask]
                    
                    if not perf_filtered.empty:
                        # Calculate overall metrics with safe column detection
                        leads_col = None
                        orders_col = None
                        
                        for col in ['no_of_leads', 'leads', 'lead_count', 'total_leads']:
                            if col in perf_filtered.columns:
                                leads_col = col
                                break
                        
                        for col in ['no_of_orders', 'orders', 'order_count', 'total_orders']:
                            if col in perf_filtered.columns:
                                orders_col = col
                                break
                        
                        if leads_col and orders_col:
                            total_leads = pd.to_numeric(perf_filtered[leads_col], errors='coerce').sum()
                            total_orders = pd.to_numeric(perf_filtered[orders_col], errors='coerce').sum()
                            overall_conv = (total_orders / total_leads) * 100 if total_leads > 0 else 0
                        else:
                            total_leads = 0
                            total_orders = 0
                            overall_conv = 0
                            st.warning(f"Required conversion columns not found. Available: {list(perf_filtered.columns)}")
                        
                        with conv_col1:
                            render_metric_card("Total Leads", f"{int(total_leads):,}", "📞", "info")
                        with conv_col2:
                            render_metric_card("Total Orders", f"{int(total_orders):,}", "📦", "success")
                        with conv_col3:
                            conv_color = "success" if overall_conv >= 20 else "warning" if overall_conv >= 10 else "danger"
                            render_metric_card("Overall Conversion", f"{overall_conv:.1f}%", "🎯", conv_color)
                        
                        # Date-wise conversion trend for all users
                        st.markdown("**📈 System-wide Daily Conversion Trends**")
                        
                        # Group by date and calculate daily conversion rates
                        leads_col = 'no_of_leads' if 'no_of_leads' in perf_filtered.columns else 'leads'
                        orders_col = 'no_of_orders' if 'no_of_orders' in perf_filtered.columns else 'orders'
                        
                        if leads_col in perf_filtered.columns and orders_col in perf_filtered.columns:
                            daily_conv = perf_filtered.groupby('parsed_date').agg({
                                leads_col: lambda x: pd.to_numeric(x, errors='coerce').sum(),
                                orders_col: lambda x: pd.to_numeric(x, errors='coerce').sum()
                            }).reset_index()
                            
                            # Rename columns for consistency
                            daily_conv.rename(columns={
                                leads_col: 'no_of_leads',
                                orders_col: 'no_of_orders'
                            }, inplace=True)
                        else:
                            st.warning(f"Required columns not found. Available: {list(perf_filtered.columns)}")
                            return
                        
                        # Calculate daily conversion rates
                        daily_conv['conversion_rate'] = daily_conv.apply(
                            lambda row: (row['no_of_orders'] / row['no_of_leads'] * 100) if row['no_of_leads'] > 0 else 0, 
                            axis=1
                        )
                        
                        if len(daily_conv) > 0:
                            # Create trend chart
                            fig = px.line(
                                daily_conv,
                                x='parsed_date',
                                y='conversion_rate',
                                markers=True,
                                line_shape='spline'
                            )
                            fig.update_layout(
                                title='System-wide Daily Conversion Rate',
                                height=400,
                                showlegend=False,
                                xaxis_title="Date",
                                yaxis_title="Conversion Rate (%)"
                            )
                            st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
                            
                            # Show top and bottom conversion days
                            conv_trend_col1, conv_trend_col2 = st.columns(2)
                            
                            with conv_trend_col1:
                                st.markdown("**🏆 Best Conversion Days**")
                                top_days = daily_conv.nlargest(5, 'conversion_rate')[['parsed_date', 'conversion_rate', 'no_of_leads', 'no_of_orders']]
                                top_days.columns = ['Date', 'Conv Rate (%)', 'Leads', 'Orders']
                                st.dataframe(top_days, hide_index=True)
                            
                            with conv_trend_col2:
                                st.markdown("**⚠️ Low Conversion Days**")
                                low_days = daily_conv.nsmallest(5, 'conversion_rate')[['parsed_date', 'conversion_rate', 'no_of_leads', 'no_of_orders']]
                                low_days.columns = ['Date', 'Conv Rate (%)', 'Leads', 'Orders']
                                st.dataframe(low_days, hide_index=True)
                        
                    else:
                        st.info("📅 No performance data found for selected date range")
                else:
                    st.warning("⚠️ No date column found in Performance sheet")
                    
            except Exception as e:
                st.error(f"Error calculating conversion rates: {str(e)}")
        else:
            st.warning("📊 Performance sheet is empty - please add conversion data")
    
    else:
        st.info("No performance data found for the selected date range")
    
    st.markdown("---")
    
    # Export Leaderboard
    st.markdown("### 📊 Export Leaderboard")
    if st.button("📥 Download Leaderboard Report", key="download_leaderboard"):
        if not top_performers_df.empty:
            csv_buffer = io.StringIO()
            top_performers_df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            
            st.download_button(
                label="📄 Download Leaderboard CSV",
                data=csv_data,
                file_name=f"leaderboard_{start_date}_to_{end_date}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data available to export")

def get_today_orders_count(orders_df: pd.DataFrame, userid: str, today: date) -> int:
    """Get count of orders created today by the user"""
    try:
        # Filter orders for the user
        # Clean user IDs for consistent matching
        orders_df['created_by'] = orders_df['created_by'].astype(str).str.strip()
        clean_userid = str(userid).strip()
        user_orders = orders_df[orders_df['created_by'] == clean_userid].copy()
        
        if user_orders.empty:
            return 0
        
        # Parse timestamps and convert to IST
        user_orders['timestamp'] = pd.to_datetime(user_orders['timestamp'], format='mixed', errors='coerce', utc=True)
        # Only use .dt accessor if we have valid datetime values
        valid_datetime_mask = user_orders['timestamp'].notna()
        if valid_datetime_mask.any():
            user_orders.loc[valid_datetime_mask, 'date_ist'] = user_orders.loc[valid_datetime_mask, 'timestamp'].dt.tz_convert(IST).dt.date
            # Count today's orders
            today_count = (user_orders['date_ist'] == today).sum()
            return int(today_count)
        else:
            return 0
        
    except Exception as e:
        logger.error(f"Error getting today's orders count: {e}")
        return 0

def generate_user_report(orders_df: pd.DataFrame, performance_df: pd.DataFrame, 
                        userid: str, start_date: date, end_date: date) -> pd.DataFrame:
    """Generate comprehensive user performance report as DataFrame"""
    
    # Get basic metrics
    # Clean user IDs for consistent matching
    orders_df['created_by'] = orders_df['created_by'].astype(str).str.strip()
    clean_userid = str(userid).strip()
    user_orders = orders_df[orders_df['created_by'] == clean_userid].copy()
    
    if user_orders.empty:
        return pd.DataFrame({"Metric": ["No data"], "Value": ["No orders found"]})
    
    # Parse timestamps
    user_orders['timestamp'] = pd.to_datetime(user_orders['timestamp'], format='mixed', errors='coerce', utc=True)
    # Only use .dt accessor if we have valid datetime values
    valid_datetime_mask = user_orders['timestamp'].notna()
    if valid_datetime_mask.any():
        user_orders.loc[valid_datetime_mask, 'date'] = user_orders.loc[valid_datetime_mask, 'timestamp'].dt.date
    else:
        # If no valid timestamps, return empty metrics
        return pd.DataFrame({"Metric": ["No data"], "Value": ["No valid timestamps found"]})
    
    # Filter by date range
    mask = (user_orders['date'] >= start_date) & (user_orders['date'] <= end_date)
    filtered_orders = user_orders[mask]
    
    # Calculate metrics
    total_orders = len(filtered_orders)
    total_revenue = filtered_orders['total'].sum() if 'total' in filtered_orders.columns else 0
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Status analysis
    delivery_metrics = get_user_delivery_metrics(orders_df, userid, start_date, end_date)
    conversion_rate = get_user_conversion_rate(performance_df, userid, start_date, end_date)
    score, rating, _, comment = compute_user_performance_score(orders_df, performance_df, userid, start_date, end_date)
    
    # Create report
    report_data = {
        "Metric": [
            "User Name",
            "Report Period",
            "Total Orders",
            "Total Revenue",
            "Average Order Value", 
            "Delivered Orders",
            "Returned Orders",
            "Delivery Rate (%)",
            "Cancellation Rate (%)",
            "Conversion Rate (%)",
            "Performance Score",
            "Rating",
            "Comment"
        ],
        "Value": [
            userid,
            f"{start_date} to {end_date}",
            total_orders,
            f"₹{total_revenue:.2f}",
            f"₹{avg_order_value:.2f}",
            delivery_metrics['delivered_count'],
            delivery_metrics['returns_count'], 
            f"{delivery_metrics['delivery_rate']:.1f}%",
            f"{delivery_metrics['cancellation_rate']:.1f}%",
            f"{conversion_rate:.1f}%" if conversion_rate is not None else "No data",
            f"{score:.1f}/100",
            rating,
            comment
        ]
    }
    
    return pd.DataFrame(report_data)

# Export functions for app.py integration
def render_performance_page(storage=None):
    """Main entry point for Performance tab - call this from app.py"""
    render_performance_tab(storage)

# Example usage in app.py:
"""
# In app.py, add to your page routing:

elif st.session_state.selected_page == 'Performance':
    from imiq.performance import render_performance_page
    render_performance_page()
"""