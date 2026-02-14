"""
Admin Settings Module
Provides admin toggle functionality for controlling revenue visibility
"""

import streamlit as st
from typing import Optional


def render_admin_settings() -> bool:
    """
    Render admin settings section with revenue visibility toggle
    
    Returns:
        bool: Current admin mode status
    """
    st.markdown("### ⚙️ Admin Settings")
    
    # Admin revenue visibility toggle
    admin_mode = st.toggle(
        "🔐 Admin Mode (Show Revenue Metrics)",
        value=st.session_state.get('admin_mode', False),
        key="admin_mode_toggle",
        help="Toggle to show/hide revenue and amount related metrics throughout the application"
    )
    
    # Store admin mode in session state
    st.session_state['admin_mode'] = admin_mode
    
    if admin_mode:
        st.success("✅ Admin Mode: ON - Revenue metrics are visible")
    else:
        st.info("ℹ️ Admin Mode: OFF - Revenue metrics are hidden")
    
    st.markdown("---")
    
    return admin_mode


def is_admin_mode() -> bool:
    """
    Check if admin mode is enabled
    
    Returns:
        bool: True if admin mode is enabled, False otherwise
    """
    return st.session_state.get('admin_mode', False)


def format_revenue(amount: float, show_currency: bool = True) -> str:
    """
    Format revenue amount based on admin mode
    
    Args:
        amount: The revenue amount to format
        show_currency: Whether to show currency symbol
        
    Returns:
        str: Formatted revenue string or hidden placeholder
    """
    if not is_admin_mode():
        return "***" if show_currency else "Hidden"
    
    try:
        if show_currency:
            return f"₹{float(amount):,.2f}"
        else:
            return f"{float(amount):,.2f}"
    except (ValueError, TypeError):
        return "₹0.00" if show_currency else "0.00"


def format_amount_metric(amount: float, prefix: str = "", suffix: str = "") -> str:
    """
    Format amount metrics for display with admin mode consideration
    
    Args:
        amount: The amount to format
        prefix: Prefix text (e.g., "Total: ")
        suffix: Suffix text (e.g., " Orders")
        
    Returns:
        str: Formatted metric string
    """
    if not is_admin_mode():
        return f"{prefix}***{suffix}"
    
    try:
        return f"{prefix}₹{float(amount):,.2f}{suffix}"
    except (ValueError, TypeError):
        return f"{prefix}₹0.00{suffix}"


def should_show_revenue_metrics() -> bool:
    """
    Determine if revenue-related metrics should be shown
    
    Returns:
        bool: True if revenue metrics should be displayed
    """
    return is_admin_mode()


def get_admin_filtered_columns(columns: list, revenue_columns: Optional[list] = None) -> list:
    """
    Filter columns based on admin mode, hiding revenue columns when not in admin mode
    
    Args:
        columns: List of all columns
        revenue_columns: List of columns that contain revenue data
        
    Returns:
        list: Filtered list of columns
    """
    if revenue_columns is None:
        revenue_columns = [
            'total_revenue', 'revenue', 'amount', 'price', 'cost', 
            'avg_order_value', 'aov', 'value', 'Total Revenue', 
            'Average Order Value', 'Avg Order Value'
        ]
    
    if is_admin_mode():
        return columns
    else:
        return [col for col in columns if col not in revenue_columns]


def mask_revenue_dataframe(df, revenue_columns: Optional[list] = None):
    """
    Mask revenue columns in dataframe when not in admin mode
    
    Args:
        df: DataFrame to mask
        revenue_columns: List of revenue column names to mask
        
    Returns:
        DataFrame with masked revenue columns if not in admin mode
    """
    if revenue_columns is None:
        revenue_columns = [
            'total_revenue', 'revenue', 'amount', 'price', 'cost',
            'avg_order_value', 'aov', 'value', 'Total Revenue',
            'Average Order Value', 'Avg Order Value'
        ]
    
    if not is_admin_mode():
        df_copy = df.copy()
        for col in revenue_columns:
            if col in df_copy.columns:
                df_copy[col] = "***"
        return df_copy
    else:
        return df