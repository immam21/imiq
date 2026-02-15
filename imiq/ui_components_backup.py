"""
IMIQ UI Components
Reusable UI components, styling, and animations for the IMIQ application
"""

import streamlit as st
from streamlit_lottie import st_lottie
import requests
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# IMIQ Color Palette - Modern and Professional
COLORS = {
    "primary": "#0f172a",      # Slate-900 - Deep navy for headers
    "secondary": "#1e293b",    # Slate-800 - Secondary dark
    "accent": "#06b6d4",       # Cyan-500 - Bright accent for CTAs
    "warm": "#f97316",         # Orange-500 - Warm accent for highlights
    "success": "#10b981",      # Emerald-500 - Success states
    "warning": "#f59e0b",      # Amber-500 - Warnings
    "error": "#ef4444",        # Red-500 - Errors
    "muted": "#64748b",        # Slate-500 - Muted text
    "light": "#f8fafc",        # Slate-50 - Light backgrounds
    "white": "#ffffff"
}

# Alternative color palettes (commented for easy switching)
"""
# Alternative Palette 1 - Corporate Blue
COLORS_ALT1 = {
    "primary": "#1e40af",      # Blue-700
    "accent": "#3b82f6",       # Blue-500
    "warm": "#f59e0b",         # Amber-500
}

# Alternative Palette 2 - Modern Purple
COLORS_ALT2 = {
    "primary": "#7c3aed",      # Violet-600
    "accent": "#a855f7",       # Purple-500
    "warm": "#ec4899",         # Pink-500
}
"""

def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app"""
    st.markdown(f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Header Styling */
    .imiq-header {{
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['secondary']});
        padding: 2rem 0;
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    .imiq-title {{
        color: {COLORS['white']};
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}
    
    .imiq-tagline {{
        color: {COLORS['accent']};
        font-size: 1.1rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }}
    
    /* Card Styling */
    .imiq-card {{
        background: {COLORS['white']};
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }}
    
    .imiq-card-header {{
        color: {COLORS['primary']};
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid {COLORS['accent']};
        padding-bottom: 0.5rem;
    }}
    
    /* Metric Cards */
    .metric-card {{
        background: linear-gradient(135deg, {COLORS['light']}, {COLORS['white']});
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid {COLORS['accent']};
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    
    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['accent']}, {COLORS['warm']});
        color: {COLORS['white']};
        border: none;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
    }}
    
    /* Form Styling */
    .stTextInput > div > div > input {{
        border-radius: 8px;
        border: 1px solid #d1d5db;
        transition: border-color 0.3s ease;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS['accent']};
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1);
    }}
    
    /* Sidebar Styling */
    .css-1d391kg {{
        background: linear-gradient(180deg, {COLORS['primary']}, {COLORS['secondary']});
    }}
    
    /* Alert Styling */
    .success-alert {{
        background: linear-gradient(135deg, {COLORS['success']}, #059669);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .warning-alert {{
        background: linear-gradient(135deg, {COLORS['warning']}, #d97706);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    /* Table Styling */
    .dataframe {{
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }}
    
    /* Animation Classes */
    .fade-in {{
        animation: fadeIn 0.5s ease-in;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .pulse {{
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}
    
    /* Status Badges */
    .status-pending {{
        background: {COLORS['warning']};
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }}
    
    .status-completed {{
        background: {COLORS['success']};
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }}
    
    .status-shipped {{
        background: {COLORS['accent']};
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }}
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the main IMIQ header with logo and tagline"""
    st.markdown(f"""
    <div class="imiq-header">
        <div class="imiq-title">📦 IMIQ</div>
        <div class="imiq-tagline">Order Management & E-commerce Excellence</div>
    </div>
    """, unsafe_allow_html=True)

def render_card(title: str, content: str, card_type: str = "default") -> None:
    """Render a styled card component"""
    card_class = "imiq-card"
    if card_type == "metric":
        card_class = "metric-card"
    
    st.markdown(f"""
    <div class="{card_class}">
        <div class="imiq-card-header">{title}</div>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

def render_status_badge(status: str) -> str:
    """Render a status badge with appropriate styling"""
    status_lower = status.lower()
    if status_lower in ['pending', 'new']:
        return f'<span class="status-pending">{status}</span>'
    elif status_lower in ['completed', 'delivered', 'success']:
        return f'<span class="status-completed">{status}</span>'
    elif status_lower in ['shipped', 'in transit', 'processing']:
        return f'<span class="status-shipped">{status}</span>'
    else:
        return f'<span class="status-pending">{status}</span>'

def render_metric_card(title: str, value: str, delta: Optional[str] = None) -> None:
    """Render an enhanced metric card"""
    delta_html = ""
    if delta:
        delta_color = COLORS['success'] if not delta.startswith('-') else COLORS['error']
        delta_html = f'<div style="color: {delta_color}; font-size: 0.9rem; margin-top: 0.5rem;">Δ {delta}</div>'
    
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div style="font-size: 0.9rem; color: {COLORS['muted']}; margin-bottom: 0.5rem;">{title}</div>
        <div style="font-size: 2rem; font-weight: 700; color: {COLORS['primary']};">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def load_lottie_url(url: str) -> Optional[Dict]:
    """Load Lottie animation from URL with error handling"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.warning(f"Failed to load Lottie animation: {e}")
    return None

def success_animation():
    """Display success animation"""
    # Sample Lottie URLs - replace with your preferred animations
    success_url = "https://assets2.lottiefiles.com/packages/lf20_jbrw3hcz.json"  # Success checkmark
    lottie_json = load_lottie_url(success_url)
    
    if lottie_json:
        st_lottie(lottie_json, height=100, key="success_animation")
    else:
        # Fallback to emoji
        st.markdown("### ✅ Success!")

def error_animation():
    """Display error animation"""
    error_url = "https://assets2.lottiefiles.com/packages/lf20_kcsr6fcp.json"  # Error animation
    lottie_json = load_lottie_url(error_url)
    
    if lottie_json:
        st_lottie(lottie_json, height=100, key="error_animation")
    else:
        # Fallback to emoji
        st.markdown("### ❌ Error!")

def loading_animation():
    """Display loading animation"""
    loading_url = "https://assets2.lottiefiles.com/packages/lf20_szlepvdj.json"  # Loading spinner
    lottie_json = load_lottie_url(loading_url)
    
    if lottie_json:
        st_lottie(lottie_json, height=100, key="loading_animation")
    else:
        # Fallback to spinner
        st.spinner("Loading...")

def render_login_form(auth_service) -> bool:
    """Render login form with styling"""
    with st.form("login_form", clear_on_submit=True):
        email = st.text_input("📧 Email", placeholder="your.email@company.com")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🔐 Login", use_container_width=True)
        
        if submitted:
            if not email or not password:
                st.error("Please enter both email and password")
                return False
            
            if auth_service.login(email, password):
                success_animation()
                return True
            else:
                st.error("Invalid email or password")
                error_animation()
                return False
    
    return False

def render_signup_form(auth_service) -> bool:
    """Render signup form with styling"""
    with st.form("signup_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            email = st.text_input("📧 Email*", placeholder="your.email@company.com")
            password = st.text_input("🔒 Password*", type="password", placeholder="Min 6 characters")
        
        with col2:
            userid = st.text_input("👤 User ID*", placeholder="unique_user_id")
            role = st.selectbox("👥 Role", ["User", "Admin"], index=0)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("📝 Create Account", use_container_width=True)
        
        if submitted:
            if not all([email, userid, password]):
                st.error("Please fill all required fields")
                return False
            
            try:
                auth_service.create_account(email, userid, password, role)
                success_animation()
                return True
            except Exception as e:
                st.error(f"Error creating account: {str(e)}")
                error_animation()
                return False
    
    return False

def render_data_table(df, title: str = "Data Table", show_index: bool = False):
    """Render an enhanced data table with styling"""
    if df.empty:
        st.info(f"No data available for {title}")
        return
    
    st.markdown(f"### {title}")
    
    # Add search functionality for large tables
    if len(df) > 10:
        search_term = st.text_input("🔍 Search in table", placeholder="Type to search...")
        if search_term:
            # Simple text search across all columns
            mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
            df = df[mask]
    
    # Style status columns if they exist
    if 'status' in df.columns:
        def style_status(row):
            status = str(row['status']).lower()
            if status in ['pending', 'new']:
                return [f'background-color: {COLORS["warning"]}30'] * len(row)
            elif status in ['completed', 'delivered']:
                return [f'background-color: {COLORS["success"]}30'] * len(row)
            elif status in ['shipped', 'processing']:
                return [f'background-color: {COLORS["accent"]}30'] * len(row)
            return [''] * len(row)
        
        styled_df = df.style.apply(style_status, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=not show_index)
    else:
        st.dataframe(df, use_container_width=True, hide_index=not show_index)

def show_toast(message: str, toast_type: str = "info"):
    """Show a toast notification"""
    if toast_type == "success":
        st.success(f"✅ {message}")
    elif toast_type == "warning":
        st.warning(f"⚠️ {message}")
    elif toast_type == "error":
        st.error(f"❌ {message}")
    else:
        st.info(f"ℹ️ {message}")

def render_kpi_grid(kpis: Dict[str, Any], columns: int = 4):
    """Render KPIs in a responsive grid"""
    kpi_items = list(kpis.items())
    
    # Create rows of columns
    for i in range(0, len(kpi_items), columns):
        cols = st.columns(columns)
        
        for j, col in enumerate(cols):
            if i + j < len(kpi_items):
                key, value = kpi_items[i + j]
                
                with col:
                    # Format value based on type
                    if isinstance(value, (int, float)):
                        if 'revenue' in key.lower() or 'value' in key.lower():
                            formatted_value = f"₹{value:,.2f}"
                        elif 'percentage' in key.lower() or key.endswith('%'):
                            formatted_value = f"{value:.1f}%"
                        else:
                            formatted_value = f"{value:,}"
                    else:
                        formatted_value = str(value)
                    
                    render_metric_card(key.replace('_', ' ').title(), formatted_value)

def create_progress_bar(value: float, max_value: float, label: str = "") -> None:
    """Create a styled progress bar"""
    percentage = (value / max_value) * 100 if max_value > 0 else 0
    
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 500;">{label}</span>
            <span style="color: {COLORS['muted']};">{value}/{max_value} ({percentage:.1f}%)</span>
        </div>
        <div style="background: {COLORS['light']}; border-radius: 10px; height: 10px; overflow: hidden;">
            <div style="background: linear-gradient(90deg, {COLORS['accent']}, {COLORS['warm']}); 
                        height: 100%; width: {percentage}%; transition: width 0.5s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)