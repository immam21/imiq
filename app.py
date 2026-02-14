st.set_page_config(
def main():
import streamlit as st
import re
from datetime import datetime

st.set_page_config(
    page_title="IMIQ - Intelligent Order Management",
    page_icon="🚀",
    layout="wide"
)

# --- Session State ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None

def main():
    st.title("🚀 IMIQ - Intelligent Order Management")
    if not st.session_state.authenticated:
        tabs = st.tabs(["🔐 Login", "📝 Sign Up / Order"])
        with tabs[0]:
            st.subheader("Login")
            user_id = st.text_input("User ID")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if user_id and password:
                    st.session_state.authenticated = True
                    st.session_state.user = {'user_id': user_id, 'role': 'user', 'name': user_id}
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Please enter both User ID and Password.")
        with tabs[1]:
            st.subheader("Sign Up / Create Order")
            template_text = st.text_area("Order Template (optional)")
            extract_clicked = st.button("Extract from Template")
            order_fields = ["Order ID", "Customer Name", "Product", "Quantity", "Price", "Shipping Address", "Order Date"]
            if "extracted_order_data" not in st.session_state:
                st.session_state["extracted_order_data"] = {field: "" for field in order_fields}
            if extract_clicked and template_text:
                extracted = {}
                for field in order_fields:
                    match = re.search(rf"{field}\s*:\s*(.+)", template_text, re.IGNORECASE)
                    extracted[field] = match.group(1).strip() if match else ""
                st.session_state["extracted_order_data"] = extracted
                st.success("Fields extracted from template!")
            with st.form("order_form"):
                order_data = {}
                for field in order_fields:
                    default_val = st.session_state["extracted_order_data"].get(field, "")
                    order_data[field] = st.text_input(field, value=default_val)
                submitted = st.form_submit_button("Create Order")
                if submitted:
                    st.success("Order created (stub logic)")
    else:
        user = st.session_state.user
        st.sidebar.title(f"👋 {user.get('name', user.get('user_id', 'User'))}")
        st.sidebar.write(f"Role: {user.get('role', 'user').title()}")
        page = st.sidebar.radio("Go to", ["Dashboard", "Orders", "Inventory", "Analytics", "Logout"])
        if page == "Dashboard":
            st.header("📊 Dashboard")
            st.info("Dashboard content goes here.")
        elif page == "Orders":
            st.header("📦 Orders")
            st.info("Order management page (stub)")
        elif page == "Inventory":
            st.header("📋 Inventory")
            st.info("Inventory management page (stub)")
        elif page == "Analytics":
            st.header("📈 Analytics")
            st.info("Analytics and KPI dashboard (stub)")
        elif page == "Logout":
            st.session_state.authenticated = False
            st.session_state.user = None
            st.success("Logged out!")
            st.rerun()

if __name__ == "__main__":
    main()
            st.subheader("Login")
            user_id = st.text_input("User ID")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if user_id and password:
                    st.session_state.authenticated = True
                    st.session_state.user = {'user_id': user_id, 'role': 'user', 'name': user_id}
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Please enter both User ID and Password.")
        with tabs[1]:
            st.subheader("Sign Up / Create Order")
            template_text = st.text_area("Order Template (optional)")
            extract_clicked = st.button("Extract from Template")
            order_fields = ["Order ID", "Customer Name", "Product", "Quantity", "Price", "Shipping Address", "Order Date"]
            if "extracted_order_data" not in st.session_state:
                st.session_state["extracted_order_data"] = {field: "" for field in order_fields}
            if extract_clicked and template_text:
                extracted = {}
                for field in order_fields:
                    match = re.search(rf"{field}\s*:\s*(.+)", template_text, re.IGNORECASE)
                    extracted[field] = match.group(1).strip() if match else ""
                st.session_state["extracted_order_data"] = extracted
                st.success("Fields extracted from template!")
            with st.form("order_form"):
                order_data = {}
                for field in order_fields:
                    default_val = st.session_state["extracted_order_data"].get(field, "")
                    order_data[field] = st.text_input(field, value=default_val)
                submitted = st.form_submit_button("Create Order")
                if submitted:
                    st.success("Order created (stub logic)")
    else:
        user = st.session_state.user
        st.sidebar.title(f"👋 {user.get('name', user.get('user_id', 'User'))}")
        st.sidebar.write(f"Role: {user.get('role', 'user').title()}")
        page = st.sidebar.radio("Go to", ["Dashboard", "Orders", "Inventory", "Analytics", "Logout"])
        if page == "Dashboard":
            st.header("📊 Dashboard")
            st.info("Dashboard content goes here.")
        elif page == "Orders":
            st.header("📦 Orders")
            st.info("Order management page (stub)")
        elif page == "Inventory":
            st.header("📋 Inventory")
            st.info("Inventory management page (stub)")
        elif page == "Analytics":
            st.header("📈 Analytics")
            st.info("Analytics and KPI dashboard (stub)")
        elif page == "Logout":
            st.session_state.authenticated = False
            st.session_state.user = None
            st.success("Logged out!")
            st.rerun()

if __name__ == "__main__":
    main()

import os
import streamlit as st
import pandas as pd
from datetime import datetime

# --- Service Initialization (Stub) ---
def get_services():
    # Replace with your actual service initialization
    return {
        'orders': None,
        'auth': None,
        'kpis': None,
        'inventory': None,
        'shipments': None,
        'settings': None,
        'storage': None
    }
services = get_services()

# --- Session State ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None

# --- Page Config ---
st.set_page_config(
    page_title="IMIQ - Intelligent Order Management",
    page_icon="🚀",
    layout="wide"
)

# --- Main App ---
def main():
    st.title("🚀 IMIQ - Intelligent Order Management")
    if not st.session_state.authenticated:
        tabs = st.tabs(["🔐 Login", "📝 Sign Up"])
        with tabs[0]:
            st.subheader("Login")
            user_id = st.text_input("User ID")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                # Replace with real authentication
                if user_id and password:
                    st.session_state.authenticated = True
                    st.session_state.user = {'user_id': user_id, 'role': 'user', 'name': user_id}
                    st.success("Logged in!")
                    st.rerun()
                else:
                    st.error("Please enter both User ID and Password.")
        with tabs[1]:
            st.subheader("Sign Up / Create Order")
            template_text = st.text_area("Order Template (optional)")
            extract_clicked = st.button("Extract from Template")
            order_fields = ["Order ID", "Customer Name", "Product", "Quantity", "Price", "Shipping Address", "Order Date"]
            if "extracted_order_data" not in st.session_state:
                st.session_state["extracted_order_data"] = {field: "" for field in order_fields}
            import re
            if extract_clicked and template_text:
                extracted = {}
                for field in order_fields:
                    match = re.search(rf"{field}\s*:\s*(.+)", template_text, re.IGNORECASE)
                    extracted[field] = match.group(1).strip() if match else ""
                st.session_state["extracted_order_data"] = extracted
                st.success("Fields extracted from template!")
            with st.form("order_form"):
                order_data = {}
                for field in order_fields:
                    default_val = st.session_state["extracted_order_data"].get(field, "")
                    order_data[field] = st.text_input(field, value=default_val)
                submitted = st.form_submit_button("Create Order")
                if submitted:
                    st.success("Order created (stub logic)")
    else:
        user = st.session_state.user
        st.sidebar.title(f"👋 {user.get('name', user.get('user_id', 'User'))}")
        st.sidebar.write(f"Role: {user.get('role', 'user').title()}")
        page = st.sidebar.radio("Go to", ["Dashboard", "Orders", "Inventory", "Analytics", "Logout"])
        if page == "Dashboard":
            st.header("📊 Dashboard")
            st.info("Dashboard content goes here.")
        elif page == "Orders":
            st.header("📦 Orders")
            st.info("Order management page (stub)")
        elif page == "Inventory":
            st.header("📋 Inventory")
            st.info("Inventory management page (stub)")
        elif page == "Analytics":
            st.header("📈 Analytics")
            st.info("Analytics and KPI dashboard (stub)")
        elif page == "Logout":
            st.session_state.authenticated = False
            st.session_state.user = None
            st.success("Logged out!")
            st.rerun()

if __name__ == "__main__":
    main()

def render_dashboard(services, user):
    """Render comprehensive KPI-powered dashboard with advanced analytics"""
    is_user = user.get('role', '').lower() == 'user'
    render_header(
        "📊 Dashboard", 
        "Comprehensive business intelligence and analytics powered by advanced KPIs",
        show_time=True,
        icon="🚀"
    )
    # Show current status of orders (admin: all, user: own) WITHIN dashboard, not at the top
    orders_df = services['orders'].get_user_orders(user['user_id']) if is_user else services['orders'].get_all_orders()
    st.markdown('### 📦 Current Order Status')
    # Ensure phone column is string type for Arrow compatibility
    if not orders_df.empty and 'phone' in orders_df.columns:
        orders_df['phone'] = orders_df['phone'].astype(str)
    if not orders_df.empty and 'status' in orders_df.columns:
        status_counts = orders_df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        st.dataframe(status_counts, width='stretch', hide_index=True)
    else:
        st.info('No order status data available.')

    # For user role, show datewise orders table
    if is_user and not orders_df.empty and 'timestamp' in orders_df.columns:
        st.markdown('### 📅 Your Orders by Date')
        orders_df['Order Date'] = pd.to_datetime(orders_df['timestamp'], errors='coerce').dt.date
        datewise_orders = orders_df.groupby('Order Date').size().reset_index(name='Order Count')
        st.dataframe(datewise_orders, width='stretch', hide_index=True)
    # Date Filters
    start_date, end_date, selected_filter = render_date_filters("dashboard")
    # Import KPI module
    from kpis import generate_full_kpi_report, format_kpi_for_display
    try:
        # Get data
        orders_df = services['orders'].get_user_orders(user['user_id']) if is_user else services['orders'].get_all_orders()
        inventory_df = services['inventory'].get_all_inventory()
        
        if orders_df.empty:
            st.info("📈 No orders found yet. Create your first order in the Orders section to get started with analytics!")
            return
        
        # Generate comprehensive KPI report using the new module
        with st.spinner('📊 Analyzing your data...'):
            full_kpi_report = generate_full_kpi_report(orders_df)
            
            # Apply date filtering for filtered metrics
            filtered_orders_df = orders_df.copy()
            if not orders_df.empty and start_date is not None and end_date is not None:
                filtered_orders_df = filter_dataframe_by_date(orders_df, start_date, end_date)
            
            filtered_kpi_report = generate_full_kpi_report(filtered_orders_df) if not filtered_orders_df.empty else None
        
        # ============================================================================
        # SECTION 1: DATE-FILTERED ANALYTICS
        # ============================================================================
        # Format dates for display
        start_display = start_date.strftime('%Y-%m-%d') if start_date else 'None'
        end_display = end_date.strftime('%Y-%m-%d') if end_date else 'None'
        # Enhanced Date-Filtered Analytics with User-wise Order Count
        date_filtered_orders = get_filtered_orders_data(services, selected_filter, start_date, end_date)
        
        if not date_filtered_orders.empty:
            if is_user:
                # For user role, only show their own order count, no other users
                st.markdown("#### 👤 Your Order Performance")
                st.metric(label="Your Orders", value=f"{len(date_filtered_orders)} orders")
            else:
                # Calculate user-wise order counts
                user_order_counts = date_filtered_orders.groupby('created_by').size().reset_index(name='order_count')
                user_order_counts = user_order_counts.sort_values('order_count', ascending=False)
                st.markdown("#### 👥 User-wise Order Performance")
                if len(user_order_counts) > 0:
                    col_count = min(len(user_order_counts), 5)  # Max 5 columns
                    user_cols = st.columns(col_count)
                    for i, (_, row) in enumerate(user_order_counts.head(5).iterrows()):
                        with user_cols[i % col_count]:
                            st.metric(
                                label=f"👤 {row['created_by']}",
                                value=f"{row['order_count']} orders"
                            )
                    if len(user_order_counts) > 1:
                        fig_users = px.bar(
                            user_order_counts.head(10), 
                            x='created_by', 
                            y='order_count',
                            title=f'Orders by User ({selected_filter})',
                            color='order_count',
                            color_continuous_scale='Blues'
                        )
                        fig_users.update_layout(xaxis_title="User", yaxis_title="Order Count")
                        st.plotly_chart(fig_users, use_container_width=True)
                    with st.expander("📊 Detailed User Breakdown"):
                        user_details = date_filtered_orders.groupby('created_by').agg({
                            'total': ['count', 'sum', 'mean'],
                            'timestamp': 'count'
                        }).round(2)
                        user_details.columns = ['Orders', 'Total Revenue', 'Avg Order Value', 'Activity Count']
                        user_details = user_details.sort_values('Orders', ascending=False)
                        st.dataframe(user_details, use_container_width=True)
                else:
                    st.info("No user data found for the selected period")
        else:
            st.info("📈 No orders found for the selected period. User performance metrics will appear here once orders are created.")
        
        st.markdown(f"### 📅 Date-Filtered Analytics ({selected_filter}: {start_display} to {end_display})")
        
        if filtered_kpi_report:
            # Core KPIs (Filtered)
            core_kpis = filtered_kpi_report['core_order_kpis']
            daily_trends = filtered_kpi_report['daily_trends']
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                render_metric_card("Orders", format_kpi_for_display(core_kpis['total_orders'], 'number'), "📦", "primary")
            if not is_user:
                with col2:
                    if should_show_revenue_metrics():
                        render_metric_card("Revenue", format_kpi_for_display(core_kpis['total_revenue'], 'currency'), "💰", "success")
                    else:
                        render_metric_card("Revenue", "Admin Only", "🔒", "warning")
                with col3:
                    if should_show_revenue_metrics():
                        render_metric_card("Avg Order Value", format_kpi_for_display(core_kpis['avg_order_value'], 'currency'), "📈", "info")
                    else:
                        render_metric_card("Avg Order Value", "***", "🔒", "warning")
            with col4:
                render_metric_card("Collection Rate", format_kpi_for_display(core_kpis['advance_collection_rate'], 'percentage'), "💳", "warning")
            if not is_user:
                # Yesterday vs Today Growth
                st.markdown("#### 📊 Growth Metrics")
                growth_col1, growth_col2, growth_col3, growth_col4 = st.columns(4)
                with growth_col1:
                    growth_val = daily_trends['orders_growth_percent']
                    delta = f"{growth_val:+.1f}%" if growth_val != 0 else "0%"
                    render_metric_card("Orders Growth", delta, "📈", "success" if growth_val >= 0 else "danger")
                with growth_col2:
                    if should_show_revenue_metrics():
                        revenue_growth = daily_trends['revenue_growth_percent'] 
                        delta = f"{revenue_growth:+.1f}%" if revenue_growth != 0 else "0%"
                        render_metric_card("Revenue Growth", delta, "💹", "success" if revenue_growth >= 0 else "danger")
                    else:
                        render_metric_card("Revenue Growth", "***", "🔒", "warning")
                with growth_col3:
                    render_metric_card("Total Quantity", format_kpi_for_display(core_kpis['total_quantity'], 'number'), "📦", "info")
                with growth_col4:
                    render_metric_card("Outstanding", format_kpi_for_display(core_kpis['outstanding_percentage'], 'percentage'), "⚠️", "warning")
                # Orders per User (Filtered)
                st.markdown("#### 👥 Top Customers (Filtered Period)")
                geographic_kpis = filtered_kpi_report['geographic_kpis']
                if not geographic_kpis['orders_by_city'].empty:
                    user_col1, user_col2 = st.columns(2)
                    with user_col1:
                        st.bar_chart(geographic_kpis['orders_by_city'].set_index('city').head(10))
                    with user_col2:
                        st.dataframe(geographic_kpis['orders_by_city'].head(10), width='stretch')
                # Order Status Distribution (Filtered)
                st.markdown("#### 📋 Order Status Analysis (Filtered)")
                status_kpis = filtered_kpi_report['status_kpis']
                if not status_kpis['status_distribution'].empty:
                    status_col1, status_col2 = st.columns(2)
                    with status_col1:
                        fig = px.pie(
                            values=status_kpis['status_distribution']['count'],
                            names=status_kpis['status_distribution']['status']
                        )
                        fig.update_layout(title="Status Distribution")
                        st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
                    with status_col2:
                        st.markdown("**Status Metrics:**")
                        st.metric("🚚 Delivered", f"{status_kpis['delivered_percentage']:.1f}%")
                        st.metric("❌ Cancelled", f"{status_kpis['cancelled_percentage']:.1f}%")
                        st.metric("↩️ RTO Rate", f"{status_kpis['rto_percentage']:.1f}%")
                        st.metric("📦 In Transit", str(status_kpis['in_transit_count']))
        else:
            st.info("No data available for the selected date range")
        
        st.markdown("---")
        
        # ============================================================================
        # SECTION 2: ALL-TIME ANALYTICS (No Date Filters)
        # ============================================================================
        st.markdown("### 📈 All-Time Business Intelligence")
        
        # Core Business Metrics
        core_kpis_all = full_kpi_report['core_order_kpis']
        st.markdown("#### 💼 Core Business KPIs")
        biz_col1, biz_col2, biz_col3, biz_col4, biz_col5 = st.columns(5)
        with biz_col1:
            render_metric_card("Total Orders", format_kpi_for_display(core_kpis_all['total_orders'], 'number'), "📦", "primary")
        if not is_user:
            with biz_col2:
                if should_show_revenue_metrics():
                    render_metric_card("Total Revenue", format_kpi_for_display(core_kpis_all['total_revenue'], 'currency'), "💰", "success")
                else:
                    render_metric_card("Total Revenue", "Admin Only", "🔒", "warning")
            with biz_col3:
                if should_show_revenue_metrics():
                    render_metric_card("Avg Order Value", format_kpi_for_display(core_kpis_all['avg_order_value'], 'currency'), "📊", "info")
                else:
                    render_metric_card("Avg Order Value", "***", "🔒", "warning")
            with biz_col4:
                if should_show_revenue_metrics():
                    render_metric_card("Advance Collected", format_kpi_for_display(core_kpis_all['total_advance_collected'], 'currency'), "💳", "success")
                else:
                    render_metric_card("Advance Collected", "***", "🔒", "warning")
            with biz_col5:
                if should_show_revenue_metrics():
                    render_metric_card("Balance Pending", format_kpi_for_display(core_kpis_all['total_balance_pending'], 'currency'), "⏳", "warning")
                else:
                    render_metric_card("Balance Pending", "***", "🔒", "warning")
        
        # Customer Analysis
        st.markdown("#### 👥 Customer Analytics")
        geographic_all = full_kpi_report['geographic_kpis']
        if not geographic_all['top_cities_by_revenue'].empty:
            customer_col1, customer_col2 = st.columns(2)
            with customer_col1:
                st.markdown("**🏆 Top Cities by Revenue:**")
                st.bar_chart(geographic_all['top_cities_by_revenue'].set_index('city')['revenue'])
            with customer_col2:
                st.markdown("**📊 Customer Distribution:**")
                st.dataframe(geographic_all['top_cities_by_revenue'], width='stretch')
        
        # Product Performance
        st.markdown("#### 🏆 Top Selling Products")
        product_kpis = full_kpi_report['product_kpis']
        if not product_kpis['top_products_by_revenue'].empty:
            prod_col1, prod_col2 = st.columns(2)
            with prod_col1:
                st.markdown("**💰 Revenue by Product:**")
                st.bar_chart(product_kpis['top_products_by_revenue'].set_index('product')['revenue'])
            with prod_col2:
                st.markdown("**🎯 Top Products Table:**")
                st.dataframe(product_kpis['top_products_by_revenue'], width='stretch')
        
        # Payment & Status Analysis
        st.markdown("#### 💳 Payment & Status Intelligence")
        payment_kpis = full_kpi_report['payment_kpis']
        status_kpis_all = full_kpi_report['status_kpis']
        
        payment_col1, payment_col2, payment_col3 = st.columns(3)
        with payment_col1:
            st.markdown("**Payment Methods:**")
            if not payment_kpis['payment_distribution'].empty:
                fig = px.bar(payment_kpis['payment_distribution'], x='payment_method', y='count')
                fig.update_layout(title="Payment Distribution")
                st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
        
        with payment_col2:
            st.markdown("**Payment Metrics:**")
            st.metric("💳 Prepaid %", f"{payment_kpis['prepaid_percentage']:.1f}%")
            st.metric("💰 COD %", f"{payment_kpis['cod_percentage']:.1f}%")
            st.metric("🚫 No Tracking", str(status_kpis_all['orders_without_tracking']))
        
        with payment_col3:
            st.markdown("**Advanced KPIs:**")
            advanced_kpis = full_kpi_report['advanced_kpis']
            st.metric("💎 Revenue Realization", f"{advanced_kpis['revenue_realization_rate']:.1f}%")
            st.metric("⏰ Aged Orders", str(len(advanced_kpis['order_aging_report'])))
            st.metric("⚠️ High Risk Orders", str(len(advanced_kpis['high_risk_orders'])))
        
        # Employee Performance (if applicable)
        employee_kpis = full_kpi_report['employee_kpis']
        if not employee_kpis['orders_per_employee'].empty:
            st.markdown("#### 👨‍💼 Employee Performance")
            emp_col1, emp_col2 = st.columns(2)
            with emp_col1:
                st.markdown("**📊 Orders by Employee:**")
                st.bar_chart(employee_kpis['orders_per_employee'].set_index('created_by'))
            with emp_col2:
                st.markdown("**💰 Revenue by Employee:**")
                st.dataframe(employee_kpis['revenue_per_employee'], width='stretch')
        
        # Daily Trends
        daily_trends_all = full_kpi_report['daily_trends']
        if not daily_trends_all['daily_revenue'].empty:
            st.markdown("#### 📈 Daily Trends")
            trend_col1, trend_col2 = st.columns(2)
            with trend_col1:
                st.markdown("**💰 Daily Revenue Trend:**")
                st.line_chart(daily_trends_all['daily_revenue'].set_index('date'))
            with trend_col2:
                st.markdown("**📦 Daily Orders Trend:**")
                st.line_chart(daily_trends_all['daily_orders'].set_index('date'))
        
        # Inventory Integration
        if not inventory_df.empty:
            low_stock_count = len(services['inventory'].get_low_stock_alerts())
            st.markdown("#### 📦 Inventory Alerts")
            inv_col1, inv_col2 = st.columns(2)
            with inv_col1:
                render_metric_card("Low Stock Items", str(low_stock_count), "⚠️", "warning")
            with inv_col2:
                render_metric_card("Total Products", str(len(inventory_df)), "📦", "info")
                
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        logger.error(f"Dashboard error: {e}")

def render_orders_page(services, user):
    """Render orders management page"""
    from datetime import datetime
    import uuid
    
    st.markdown("## 📦 Orders Management")
    
    tab1, tab2, tab3 = st.tabs(["📋 View Orders", "➕ Create Order", "🔍 Search Orders"])
    
    # ...existing code...
    # --- Template Extraction UI ---
    # (Assume previous code sets up template_text, extract_clicked, template_fields, etc.)
    if extract_clicked and template_text:
        extracted = {}
        debug_lines = []
        for key, patterns in template_fields.items():
            value = ""
            for pattern in patterns:
                match = re.search(rf"{pattern}\s*:\s*(.+)", template_text, re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    debug_lines.append(f"Matched {pattern} for {key}: {value}")
                    break
            # Fallback: try exact field name (strip #, upper/lower)
            if not value:
                for line in template_text.splitlines():
                    line_clean = line.strip()
                    if line_clean.lower().startswith(f"#{key}".lower()):
                        parts = line_clean.split(":", 1)
                        if len(parts) == 2:
                            value = parts[1].strip()
                            debug_lines.append(f"Fallback matched #{key} for {key}: {value}")
                            break
            extracted[key] = value
        st.session_state["order_form_extracted"] = extracted
        try:
            st.session_state.balance_amount = float(extracted.get("balance_to_pay", "0") or "0")
        except ValueError:
            st.session_state.balance_amount = 0.0
        try:
            st.session_state.advance_amount = float(extracted.get("advance_paid", "0") or "0")
        except ValueError:
            st.session_state.advance_amount = 0.0
        # Always calculate total as sum
        st.session_state.total_amount = st.session_state.balance_amount + st.session_state.advance_amount
        st.info("\n".join(debug_lines))
        st.success("Fields extracted from template!")
        st.rerun()
    # --- End Template Extraction UI ---
    # Initialize session state for real-time calculations and order processing
    if 'balance_amount' not in st.session_state:
        st.session_state.balance_amount = 0.0
    if 'advance_amount' not in st.session_state:
        st.session_state.advance_amount = 0.0
    if 'total_amount' not in st.session_state:
        st.session_state.total_amount = 0.0
    if 'creating_order' not in st.session_state:
        st.session_state.creating_order = False
    # ...existing code...
    # Show loading spinner if creating order
    # --- Template Extraction UI ---
    # (Assume previous code sets up template_text, extract_clicked, template_fields, etc.)
    if extract_clicked and template_text:
        extracted = {}
        debug_lines = []
        for key, patterns in template_fields.items():
            value = ""
            for pattern in patterns:
                match = re.search(rf"{pattern}\s*:\s*(.+)", template_text, re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    debug_lines.append(f"Matched {pattern} for {key}: {value}")
                    break
            # Fallback: try exact field name (strip #, upper/lower)
            if not value:
                for line in template_text.splitlines():
                    line_clean = line.strip()
                    if line_clean.lower().startswith(f"#{key}".lower()):
                        parts = line_clean.split(":", 1)
                        if len(parts) == 2:
                            value = parts[1].strip()
                            debug_lines.append(f"Fallback matched #{key} for {key}: {value}")
                            break
            extracted[key] = value
        st.session_state["order_form_extracted"] = extracted
        try:
            st.session_state.balance_amount = float(extracted.get("balance_to_pay", "0") or "0")
        except ValueError:
            st.session_state.balance_amount = 0.0
        try:
            st.session_state.advance_amount = float(extracted.get("advance_paid", "0") or "0")
        except ValueError:
            st.session_state.advance_amount = 0.0
        # Always calculate total as sum
        st.session_state.total_amount = st.session_state.balance_amount + st.session_state.advance_amount
        st.info("\n".join(debug_lines))
        st.success("Fields extracted from template!")
        st.rerun()
    # --- End Template Extraction UI ---
    # Initialize session state for real-time calculations and order processing
    if 'balance_amount' not in st.session_state:
        st.session_state.balance_amount = 0.0
    if 'advance_amount' not in st.session_state:
        st.session_state.advance_amount = 0.0
    if 'total_amount' not in st.session_state:
        st.session_state.total_amount = 0.0
    if 'creating_order' not in st.session_state:
        st.session_state.creating_order = False
    # Show loading spinner if creating order
    if st.session_state.creating_order:
        from imiq.ui_components import render_loading_spinner
        render_loading_spinner("Creating your order... Please wait!")
        return  # Don't show the form while processing
    with st.form("create_order"):
        # --- Amount fields moved inside the form ---
        col_balance, col_advance, col_total = st.columns([1, 1, 1])
        extracted_balance = st.session_state["order_form_extracted"].get("balance_to_pay", None)
        if extracted_balance is not None and extracted_balance != "":
            balance_default = str(extracted_balance)
        else:
            balance_default = str(st.session_state.balance_amount) if st.session_state.balance_amount != 0 else ""
        # Row 1: Customer Name and Phone
        st.markdown("#### 👤 Customer Information")
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("Customer Name *", placeholder="Enter customer name", value=st.session_state["order_form_extracted"].get("customer_name", ""), disabled=st.session_state.creating_order)
        with col2:
            phone = st.text_input("Phone Number *", placeholder="1234567890 (10 digits)", value=st.session_state["order_form_extracted"].get("phone", ""), disabled=st.session_state.creating_order)
        # Row 2: Address and City
        col3, col4 = st.columns(2)
        with col3:
            address = st.text_area("Address *", placeholder="Full address", height=100, value=st.session_state["order_form_extracted"].get("address", ""), disabled=st.session_state.creating_order)
        with col4:
            city = st.text_input("City *", placeholder="City name", value=st.session_state["order_form_extracted"].get("city", ""), disabled=st.session_state.creating_order)
        # Row 3: Pincode and Product
        col5, col6 = st.columns(2)
        with col5:
            pincode = st.text_input("Pincode *", placeholder="123456 (6 digits)", value=st.session_state["order_form_extracted"].get("pincode", ""), disabled=st.session_state.creating_order)
        with col6:
            product = st.text_area("Product Description *", placeholder="Product details", height=100, value=st.session_state["order_form_extracted"].get("product", ""), disabled=st.session_state.creating_order)
        # --- Amount fields just above Payment Mode ---
        col_balance, col_advance, col_total = st.columns([1, 1, 1])
        extracted_balance = st.session_state["order_form_extracted"].get("balance_to_pay", None)
        balance_default = str(extracted_balance) if extracted_balance not in (None, "") else str(st.session_state.balance_amount)
        with col_balance:
            st.markdown(f"<span style='color:black;'>Extracted Balance: {extracted_balance}, Session: {st.session_state.balance_amount}</span>", unsafe_allow_html=True)
            balance_input = st.text_input(
                "Balance to Pay *",
                value=str(st.session_state["order_form_extracted"].get("balance_to_pay", "")),
                disabled=st.session_state.creating_order
            )
        extracted_advance = st.session_state["order_form_extracted"].get("advance_paid", None)
        advance_default = str(extracted_advance) if extracted_advance not in (None, "") else str(st.session_state.advance_amount)
        with col_advance:
            st.markdown(f"<span style='color:black;'>Extracted Advance: {extracted_advance}, Session: {st.session_state.advance_amount}</span>", unsafe_allow_html=True)
            advance_input = st.text_input(
                "Advance Paid",
                value=str(st.session_state["order_form_extracted"].get("advance_paid", "")),
                disabled=st.session_state.creating_order
            )
        # Payment type dropdown
        payment_types = ["COD", "Prepaid"]
        extracted_payment = st.session_state["order_form_extracted"].get("payment_method", "")
        # Case-insensitive match for extracted payment type
        payment_index = 0
        for i, p in enumerate(payment_types):
            if extracted_payment.strip().lower() == p.lower():
                payment_index = i
                break
        payment_method = st.selectbox(
            "Payment Type *",
            payment_types,
            index=payment_index,
            disabled=st.session_state.creating_order
        )
        # Calculate and show total
        balance_val = balance_input if balance_input not in (None, "") else extracted_balance
        advance_val = advance_input if advance_input not in (None, "") else extracted_advance
        try:
            st.session_state.balance_amount = float(balance_val) if balance_val not in (None, "") else 0.0
        except ValueError:
            st.session_state.balance_amount = 0.0
        try:
            st.session_state.advance_amount = float(advance_val) if advance_val not in (None, "") else 0.0
        except ValueError:
            st.session_state.advance_amount = 0.0
        st.session_state.total_amount = st.session_state.balance_amount + st.session_state.advance_amount
        with col_total:
            st.metric("💰 Total Amount", f"₹{st.session_state.total_amount:.2f}")
        # Enable Create Order button only if all required fields are filled and total_amount > 0
        required_fields_filled = all([
            customer_name,
            phone,
            address,
            city,
            pincode,
            product,
            st.session_state.total_amount > 0
        ])
        submitted = st.form_submit_button(
            "🛒 Create Order", 
            width='stretch', 
            type="primary", 
            disabled=st.session_state.creating_order or not required_fields_filled
        )
        if submitted:
            # Set loading state
            st.session_state.creating_order = True
            # Get financial values from session state
            balance_to_pay = st.session_state.balance_amount
            advance_paid = st.session_state.advance_amount
            total_amount = st.session_state.total_amount
            # Validation
            required_fields = [customer_name, phone, address, city, pincode, product]
            if not all(required_fields) or balance_to_pay <= 0:
                st.session_state.creating_order = False
                st.error("❌ Please fill all required fields and ensure balance to pay is greater than 0")
            else:
                try:
                    # Generate order ID
                    order_id = f"ORD{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
                    # Show spinner while processing
                    with st.spinner("Creating order..."):
                        # Prepare order data matching Excel schema
                        order_data = {
                            'order_id': order_id,
                            'phone': phone,
                            'customer_name': customer_name,
                            'product': product,
                            'quantity': 1,  # Default quantity
                            'balance_to_pay': balance_to_pay,
                            'advance_paid': advance_paid,
                            'total': total_amount,
                            'address': address,
                            'city': city,
                            'pincode': pincode,
                            'payment_method': payment_method,
                            'status': 'Pending',
                            'timestamp': datetime.now().isoformat(),
                            'ai_order_id': '',
                            'tracking_id': '',
                            'courier_name': '',
                            'created_by': user.get('user_id'),
                        }
                        # Save to Excel with delay to show spinner effect
                        import time
                        time.sleep(1)  # Brief delay to show spinner
                        success = services['orders'].create_order(order_data)
                    # Reset loading state
                    st.session_state.creating_order = False
                    if success:
                        st.session_state["order_success"] = {
                            "order_id": order_id,
                            "total_amount": total_amount,
                            "customer_name": customer_name,
                            "phone": phone
                        }
                        # Reset amount session state
                        st.session_state.balance_amount = 0.0
                        st.session_state.advance_amount = 0.0
                        st.session_state.total_amount = 0.0
                        st.session_state["order_form_extracted"] = {k: "" for k in template_fields}
                        success_animation()
                    else:
                        st.error("❌ Failed to create order. Please try again.")
                except Exception as e:
                    st.session_state.creating_order = False
                    st.error(f"❌ Error creating order: {str(e)}")
                    error_animation()

    # Show order success popup and refresh button outside the form
    if "order_success" in st.session_state:
        order_info = st.session_state["order_success"]
        st.success(f"✅ Order created successfully!")
        st.info(f"📦 Order ID: **{order_info['order_id']}**")
        st.info(f"💰 Total Amount: **₹{order_info['total_amount']:.2f}**")
        st.info(f"📱 Customer: **{order_info['customer_name']}** ({order_info['phone']})")
        if st.button("🔄 Refresh Form", key="refresh_order_form_btn"):
            del st.session_state["order_success"]
            st.rerun()
    
    with tab3:
        st.markdown("### Search Orders")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_term = st.text_input("Search Term", placeholder="Order ID, customer name, etc.")
        with col2:
            search_field = st.selectbox("Search Field", 
                                      ["All", "order_id", "customer_name", "phone", "product", "status"])
        with col3:
            date_range = st.date_input("Date Range", value=[], max_value=datetime.now().date())
        
        if st.button("🔍 Search", key="search_orders_btn"):
            results = services['orders'].search_orders(
                search_term, search_field, 
                date_range, user['userid'] if user['role'] == 'User' else None
            )
            
            if not results.empty:
                st.success(f"Found {len(results)} matching orders")
                st.dataframe(results, width='stretch', hide_index=True)
            else:
                st.info("No matching orders found")

def render_inventory_page(services, user):
    """Render inventory management page"""
    st.markdown("## 📋 Inventory Management")
    
    tab1, tab2 = st.tabs(["📦 View Inventory", "➕ Add/Update Item"])
    
    with tab1:
        st.markdown("### Current Inventory")
        
        with st.spinner('📦 Loading inventory data...'):
            inventory = services['inventory'].get_all_inventory()
        
        if not inventory.empty:
            # Color-code low stock items
            def highlight_low_stock(row):
                if 'stock' in row:
                    if row['stock'] <= 5:  # Low stock threshold
                        return ['background-color: #ffebee'] * len(row)
                return [''] * len(row)
            
            styled_inventory = inventory.style.apply(highlight_low_stock, axis=1)
            st.dataframe(styled_inventory, width='stretch', hide_index=True)
            
            st.caption("🔴 Red background indicates items with stock ≤ 5")
        else:
            st.info("No inventory items found.")
    
    with tab2:
        if user['role'].lower() != 'admin':
            st.warning("Only administrators can add/update inventory items.")
            return
        
        st.markdown("### Add/Update Inventory Item")
        with st.form("inventory_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                sku = st.text_input("SKU*", placeholder="PROD-001")
                product_name = st.text_input("Product Name*", placeholder="Product name")
                stock = st.number_input("Stock*", min_value=0, value=0)
            
            with col2:
                category = st.text_input("Category", placeholder="Electronics, Clothing, etc.")
                price = st.number_input("Price (₹)*", min_value=0.0, format="%.2f")
                description = st.text_area("Description", placeholder="Product description")
            
            submitted = st.form_submit_button("💾 Save Item", width='stretch')
            
            if submitted:
                if not all([sku, product_name]):
                    st.error("SKU and Product Name are required")
                else:
                    try:
                        item_data = {
                            'sku': sku,
                            'product_name': product_name,
                            'stock': stock,
                            'category': category,
                            'price': price,
                            'description': description
                        }
                        
                        services['inventory'].upsert_item(item_data)
                        st.success("✅ Inventory item saved successfully!")
                        success_animation()
                        
                    except Exception as e:
                        st.error(f"Error saving item: {str(e)}")

def render_shipments_page(services, user):
    """Render shipments page (Admin only)"""
    st.markdown("## 🚚 Shipments Management")
    
    tab1, tab2 = st.tabs(["📋 View Shipments", "➕ Create Shipment"])
    
    with tab1:
        st.markdown("### All Shipments")
        
        with st.spinner('🚚 Loading shipments data...'):
            shipments = services['shipments'].get_all_shipments()
        
        if not shipments.empty:
            st.dataframe(shipments, width='stretch', hide_index=True)
        else:
            st.info("No shipments found.")
    
    with tab2:
        st.markdown("### Create New Shipment")
        
        # Get orders without shipments
        pending_orders = services['shipments'].get_orders_without_shipments()
        
        if pending_orders.empty:
            st.info("No orders available for shipment.")
            return
        
        with st.form("create_shipment"):
            order_id = st.selectbox("Select Order*", 
                                  options=pending_orders['order_id'].tolist(),
                                  format_func=lambda x: f"{x} - {pending_orders[pending_orders['order_id']==x]['customer_name'].iloc[0]}")
            
            col1, col2 = st.columns(2)
            with col1:
                courier = st.selectbox("Courier*", ["DTDC", "Delhivery", "Blue Dart", "Other"])
                tracking_id = st.text_input("Tracking ID*", placeholder="Enter tracking number")
            
            with col2:
                status = st.selectbox("Status*", ["Shipped", "In Transit", "Out for Delivery"])
            
            submitted = st.form_submit_button("🚚 Create Shipment", width='stretch')
            
            if submitted:
                if not all([order_id, courier, tracking_id]):
                    st.error("Please fill all required fields")
                else:
                    try:
                        shipment_data = {
                            'order_id': order_id,
                            'courier': courier,
                            'tracking_id': tracking_id,
                            'status': status
                        }
                        
                        shipment_id = services['shipments'].create_shipment(shipment_data)
                        st.success(f"✅ Shipment created successfully! Shipment ID: {shipment_id}")
                        success_animation()
                        
                    except Exception as e:
                        st.error(f"Error creating shipment: {str(e)}")

def render_performance_page(services, user):
    """Render comprehensive performance analytics page (Admin only)"""
    from imiq.performance import render_performance_page as render_performance_module
    render_performance_module(services['storage'])

def render_settings_page(services, user):
    """Render settings page (Admin only)"""
    st.markdown("## ⚙️ Settings")
    
    settings = services['settings'].get_settings()
    
    # Display current storage information
    current_storage_type = "Excel" if not settings.get('use_google_sheets', False) else "Google Sheets"
    
    st.info(f"🗄️ **Current Storage**: {current_storage_type}")
    
    if settings.get('use_google_sheets', False) and settings.get('google_sheet_id'):
        st.success(f"✅ **Google Sheets ID**: {settings['google_sheet_id'][:20]}...")
    
    # Debug information
    with st.expander("🔍 Storage Debug Info", expanded=False):
        st.write("**Current Settings:**")
        st.json(settings)
        
        st.write("**Environment Variables:**")
        import os
        creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'Not Set')
        st.write(f"GOOGLE_APPLICATION_CREDENTIALS: {creds_path}")
        
        if settings.get('use_google_sheets', False):
            try:
                from imiq.storage import GOOGLE_SHEETS_AVAILABLE
                st.write(f"Google Sheets packages available: {GOOGLE_SHEETS_AVAILABLE}")
                
                if settings.get('google_sheet_id') and creds_path != 'Not Set':
                    # Test connection
                    st.write("**Connection Test:**")
                    with st.spinner("Testing Google Sheets connection..."):
                        try:
                            from imiq.storage import GoogleSheetsStorage
                            test_storage = GoogleSheetsStorage(settings['google_sheet_id'])
                            st.success("✅ Google Sheets connection successful!")
                        except Exception as e:
                            st.error(f"❌ Connection failed: {e}")
                            
            except Exception as e:
                st.error(f"Debug error: {e}")
    
    with st.form("settings_form"):
        st.markdown("### 🔧 Application Settings")
        
        # Google Sheets integration
        use_google_sheets = st.checkbox("Enable Google Sheets Integration", 
                                      value=settings.get('use_google_sheets', False))
        
        if use_google_sheets:
            st.info("📝 **Google Sheets Setup Required:**\n"
                   "1. Create a Google Cloud project and enable Sheets API\n"
                   "2. Create a service account and download credentials JSON\n"
                   "3. Share your Google Sheet with the service account email\n"
                   "4. Set GOOGLE_APPLICATION_CREDENTIALS environment variable\n"
                   "5. **Provide your Google Sheet ID below**")
            
            google_sheet_id = st.text_input("Google Sheet ID", 
                                          value=settings.get('google_sheet_id', ''),
                                          placeholder="Enter your Google Sheet ID here",
                                          help="The ID from your Google Sheets URL: docs.google.com/spreadsheets/d/[SHEET_ID]/edit")
            
            if google_sheet_id:
                st.success(f"✅ Sheet ID configured: {google_sheet_id}")
        else:
            google_sheet_id = ""
        
        # Other settings
        st.markdown("### 🌍 Regional Settings")
        timezone = st.selectbox("Timezone", ["Asia/Kolkata", "UTC", "Asia/Dubai"], 
                               index=0)
        
        currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)"], 
                               index=0)
        
        submitted = st.form_submit_button("💾 Save Settings", width='stretch')
        
        if submitted:
            # Validate Google Sheets settings
            if use_google_sheets and not google_sheet_id:
                st.error("❌ Google Sheet ID is required when Google Sheets integration is enabled")
                return
            
            new_settings = {
                'use_google_sheets': use_google_sheets,
                'google_sheet_id': google_sheet_id,
                'timezone': timezone,
                'currency': currency,
                'updated_at': get_ist_now().isoformat()
            }
            
            try:
                # Save settings
                services['settings'].update_settings(new_settings)
                
                st.success("✅ Settings saved successfully!")
                success_animation()
                
                # Show storage change warning
                if use_google_sheets != settings.get('use_google_sheets', False):
                    if use_google_sheets:
                        st.warning("🔄 **Storage switched to Google Sheets**\n"
                                 "Please refresh the page to apply changes.")
                        st.info("💡 **Note**: Your existing Excel data remains intact. "
                               "New operations will use Google Sheets.")
                    else:
                        st.warning("🔄 **Storage switched to Excel**\n"
                                 "Please refresh the page to apply changes.")
                
                # Add refresh button
                if st.button("🔄 Refresh Application", type="primary", key="refresh_app_btn"):
                    st.rerun()
                    
            except Exception as e:
                st.error(f"❌ Error saving settings: {str(e)}")
                st.exception(e)

def get_filtered_orders_data(services, selected_filter, start_date, end_date):
    """Get filtered orders data based on date range and filter type"""
    try:
        # Get orders from storage
        if isinstance(services, dict):
            orders_service = services.get('orders')
            storage = services.get('storage')
        else:
            orders_service = services.orders
            storage = services.storage
        
        if orders_service:
            orders_df = orders_service.get_all_orders()
        else:
            # Fallback to direct storage access
            orders_df = storage.read_sheet("NewOrders")
        
        if orders_df.empty:
            return pd.DataFrame()
        
        # Ensure timestamp column exists and convert to datetime
        if 'timestamp' in orders_df.columns:
            orders_df['timestamp'] = pd.to_datetime(orders_df['timestamp'], format='mixed', errors='coerce')
            orders_df = orders_df.dropna(subset=['timestamp'])
            
            # Filter by date range if provided
            if start_date and end_date:
                mask = (orders_df['timestamp'].dt.date >= start_date) & (orders_df['timestamp'].dt.date <= end_date)
                orders_df = orders_df[mask]
        
        # Ensure created_by column exists, if not use a default
        if 'created_by' not in orders_df.columns:
            orders_df['created_by'] = 'System'
        
        # Fill missing created_by values
        orders_df['created_by'] = orders_df['created_by'].fillna('Unknown')
        
        return orders_df
        
    except Exception as e:
        st.error(f"Error fetching orders data: {str(e)}")
        return pd.DataFrame()


def compute_kpis(data: dict) -> dict:
    """
    Comprehensive KPI calculation module for e-commerce business analytics.
    
    Args:
        data (dict): Input data containing all business parameters
        
    Returns:
        dict: Comprehensive KPIs and business metrics
        
    Raises:
        ValueError: If negative values are provided for costs or invalid data
    """
    
    def validate_non_negative(value: float, field_name: str) -> float:
        """Validate that a value is non-negative."""
        if value < 0:
            raise ValueError(f"{field_name} cannot be negative: {value}")
        return value
    
    def validate_rate(rate: float, field_name: str) -> float:
        """Validate that a rate is between 0 and 1."""
        if not 0 <= rate <= 1:
            raise ValueError(f"{field_name} must be between 0 and 1: {rate}")
        return rate
    
    def calculate_product_cost(sku_mix: list) -> dict:
        """Calculate total product cost and units from SKU mix."""
        total_cost = 0.0
        total_units = 0
        total_selling_value = 0.0
        
        for sku in sku_mix:
            units = validate_non_negative(sku['units'], f"Units for SKU {sku['sku']}")
            product_cost = validate_non_negative(sku['product_cost'], f"Product cost for SKU {sku['sku']}")
            selling_price = validate_non_negative(sku['selling_price'], f"Selling price for SKU {sku['sku']}")
            
            total_cost += units * product_cost
            total_units += units
            total_selling_value += units * selling_price
            
        return {
            'total_product_cost': round(total_cost, 2),
            'total_units': total_units,
            'total_selling_value': round(total_selling_value, 2)
        }
    
    def calculate_salary_cost(salary_per_person_per_week: float, num_employees: int, days: int) -> float:
        """Calculate prorated salary cost for the period."""
        daily_salary_per_person = salary_per_person_per_week / 7
        return round(daily_salary_per_person * num_employees * days, 2)
    
    def calculate_cod_metrics(total_orders: int, total_revenue: float, cod_return_rate: float, 
                            net_profit: float) -> dict:
        """Calculate COD-adjusted metrics."""
        delivered_orders = int(total_orders * (1 - cod_return_rate))
        delivered_revenue = round(total_revenue * (1 - cod_return_rate), 2)
        delivered_profit = round(net_profit * (1 - cod_return_rate), 2)  # Simplified assumption
        
        return {
            'delivered_orders': delivered_orders,
            'delivered_revenue': delivered_revenue,
            'delivered_profit': delivered_profit
        }
    
    def calculate_monthly_projections(current_metrics: dict, days: int) -> dict:
        """Scale current period performance to 30-day projections."""
        scale_factor = 30 / days if days > 0 else 0
        
        return {
            'monthly_orders': int(current_metrics.get('delivered_orders', 0) * scale_factor),
            'monthly_revenue': round(current_metrics.get('delivered_revenue', 0) * scale_factor, 2),
            'monthly_profit': round(current_metrics.get('delivered_profit', 0) * scale_factor, 2),
            'monthly_ad_spend': round(current_metrics.get('total_ad_spend', 0) * scale_factor, 2)
        }
    
    try:
        # Input validation
        days = validate_non_negative(data['days'], 'Days')
        if days == 0:
            raise ValueError("Days cannot be zero")
            
        ad_spend_per_day = validate_non_negative(data['ad_spend_per_day'], 'Ad spend per day')
        courier_per_day = validate_non_negative(data['courier_per_day'], 'Courier cost per day')
        sourcing_payment = validate_non_negative(data['sourcing_payment'], 'Sourcing payment')
        salary_per_person_per_week = validate_non_negative(data['salary_per_person_per_week'], 'Salary per person per week')
        num_employees = validate_non_negative(data['num_employees'], 'Number of employees')
        orders = validate_non_negative(data['orders'], 'Orders')
        total_order_value = validate_non_negative(data['total_order_value'], 'Total order value')
        cod_return_rate = validate_rate(data['cod_return_rate'], 'COD return rate')
        
        # Basic calculations
        total_ad_spend = round(ad_spend_per_day * days, 2)
        total_courier_cost = round(courier_per_day * days, 2)
        salary_cost = calculate_salary_cost(salary_per_person_per_week, num_employees, days)
        
        # Show loading spinner if creating order
        if st.session_state.creating_order:
            from imiq.ui_components import render_loading_spinner
            render_loading_spinner("Creating your order... Please wait!")
            return  # Don't show the form while processing

        with st.form("create_order"):
            # Row 1: Customer Name and Phone
            st.markdown("#### 👤 Customer Information")
            col1, col2 = st.columns(2)
            with col1:
                customer_name = st.text_input("Customer Name *", placeholder="Enter customer name", disabled=st.session_state.creating_order)
            with col2:
                phone = st.text_input("Phone Number *", placeholder="1234567890 (10 digits)", disabled=st.session_state.creating_order)

            # Row 2: Address and City
            col3, col4 = st.columns(2)
            with col3:
                address = st.text_area("Address *", placeholder="Full address", height=100, disabled=st.session_state.creating_order)
            with col4:
                city = st.text_input("City *", placeholder="City name", disabled=st.session_state.creating_order)

            # Row 3: Pincode and Product
            col5, col6 = st.columns(2)
            with col5:
                pincode = st.text_input("Pincode *", placeholder="123456 (6 digits)", disabled=st.session_state.creating_order)
            with col6:
                product = st.text_area("Product Description *", placeholder="Product details", height=100, disabled=st.session_state.creating_order)

            # Row 4: Payment Mode and Amounts
            st.markdown("#### 💰 Payment Information")
            pay_col1, pay_col2, pay_col3 = st.columns(3)
            with pay_col1:
                balance_input = st.text_input(
                    "Balance to Pay *", 
                    value="0" if st.session_state.balance_amount == 0 else str(st.session_state.balance_amount),
                    placeholder="0",
                    key="balance_realtime",
                    disabled=st.session_state.creating_order
                )
                try:
                    st.session_state.balance_amount = float(balance_input) if balance_input and balance_input != "0" else 0.0
                except ValueError:
                    st.session_state.balance_amount = 0.0
            with pay_col2:
                advance_input = st.text_input(
                    "Advance Paid", 
                    value="0" if st.session_state.advance_amount == 0 else str(st.session_state.advance_amount),
                    placeholder="0",
                    key="advance_realtime",
                    disabled=st.session_state.creating_order
                )
                try:
                    st.session_state.advance_amount = float(advance_input) if advance_input and advance_input != "0" else 0.0
                except ValueError:
                    st.session_state.advance_amount = 0.0
            with pay_col3:
                st.session_state.total_amount = st.session_state.balance_amount + st.session_state.advance_amount
                st.metric("💰 Total Amount", f"₹{st.session_state.total_amount:.2f}")
            payment_method = st.selectbox("Payment Mode *", ["COD", "Prepaid"], disabled=st.session_state.creating_order)
        
        return kpis
        
    except Exception as e:
        raise ValueError(f"KPI calculation failed: {str(e)}")


def render_analytics_page(services, user):
    """Render comprehensive Business Analytics page with KPI calculator"""
    render_header(
        "📊 Business Analytics", 
        "Advanced KPI calculator and business intelligence dashboard",
        show_time=True,
        icon="📊"
    )
    
    # Create tabs for different analytics sections
    tab1, tab2, tab3, tab4 = st.tabs(["🧮 KPI Calculator", "📅 Date-wise Analytics", "📈 Business Intelligence", "📊 Reports"])
    
    with tab1:
        st.markdown("### 🧮 Comprehensive KPI Calculator")
        st.markdown("Calculate detailed business metrics including profit, COD adjustments, and monthly projections")
        
        # KPI Calculator Form
        with st.form("kpi_calculator"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 📅 Period & Volume")
                days = st.number_input("Period (Days)", min_value=1, value=4, step=1)
                orders = st.number_input("Total Orders", min_value=1, value=58, step=1)
                total_order_value = st.number_input("Total Order Value (₹)", min_value=0.0, value=56313.0, step=100.0, format="%.2f")
                cod_return_rate = st.number_input("COD Return Rate", min_value=0.0, max_value=1.0, value=0.2, step=0.01, format="%.2f")
            
            with col2:
                st.markdown("#### 💸 Daily Costs")
                ad_spend_per_day = st.number_input("Ad Spend per Day (₹)", min_value=0.0, value=1750.0, step=50.0, format="%.2f")
                courier_per_day = st.number_input("Courier Cost per Day (₹)", min_value=0.0, value=1000.0, step=50.0, format="%.2f")
                
                st.markdown("#### 👥 Team Costs")
                salary_per_person_per_week = st.number_input("Salary per Person/Week (₹)", min_value=0.0, value=1500.0, step=100.0, format="%.2f")
                num_employees = st.number_input("Number of Employees", min_value=1, value=2, step=1)
                sourcing_payment = st.number_input("Sourcing Payment (₹)", min_value=0.0, value=40000.0, step=1000.0, format="%.2f")
            
            with col3:
                st.markdown("#### 📦 Product Mix")
                st.markdown("**SKU A:**")
                sku_a_units = st.number_input("SKU A Units", min_value=0, value=30, step=1, key="sku_a_units")
                sku_a_cost = st.number_input("SKU A Product Cost (₹)", min_value=0.0, value=800.0, step=10.0, format="%.2f", key="sku_a_cost")
                sku_a_price = st.number_input("SKU A Selling Price (₹)", min_value=0.0, value=1299.0, step=10.0, format="%.2f", key="sku_a_price")
                
                st.markdown("**SKU B:**")
                sku_b_units = st.number_input("SKU B Units", min_value=0, value=28, step=1, key="sku_b_units")
                sku_b_cost = st.number_input("SKU B Product Cost (₹)", min_value=0.0, value=400.0, step=10.0, format="%.2f", key="sku_b_cost")
                sku_b_price = st.number_input("SKU B Selling Price (₹)", min_value=0.0, value=899.0, step=10.0, format="%.2f", key="sku_b_price")
            
            calculate_button = st.form_submit_button("🧮 Calculate KPIs", use_container_width=True, type="primary")
            
            if calculate_button:
                try:
                    # Prepare data for KPI calculation
                    kpi_data = {
                        'days': days,
                        'ad_spend_per_day': ad_spend_per_day,
                        'courier_per_day': courier_per_day,
                        'sourcing_payment': sourcing_payment,
                        'salary_per_person_per_week': salary_per_person_per_week,
                        'num_employees': num_employees,
                        'orders': orders,
                        'total_order_value': total_order_value,
                        'cod_return_rate': cod_return_rate,
                        'sku_mix': [
                            {'sku': 'A', 'units': sku_a_units, 'product_cost': sku_a_cost, 'selling_price': sku_a_price},
                            {'sku': 'B', 'units': sku_b_units, 'product_cost': sku_b_cost, 'selling_price': sku_b_price},
                        ],
                                extracted_balance = st.session_state["order_form_extracted"].get("balance_to_pay", None)
                                if extracted_balance is not None and extracted_balance != "":
                                    balance_default = str(extracted_balance)
                                else:
                                    balance_default = str(st.session_state.balance_amount) if st.session_state.balance_amount != 0 else ""
                                # Row 1: Customer Name and Phone
                                st.markdown("#### 👤 Customer Information")
                                col1, col2 = st.columns(2)
                                with col1:
                                    customer_name = st.text_input("Customer Name *", placeholder="Enter customer name", value=st.session_state["order_form_extracted"].get("customer_name", ""), disabled=st.session_state.creating_order)
                                with col2:
                                    phone = st.text_input("Phone Number *", placeholder="1234567890 (10 digits)", value=st.session_state["order_form_extracted"].get("phone", ""), disabled=st.session_state.creating_order)
                                # Row 2: Address and City
                                col3, col4 = st.columns(2)
                                with col3:
                                    address = st.text_area("Address *", placeholder="Full address", height=100, value=st.session_state["order_form_extracted"].get("address", ""), disabled=st.session_state.creating_order)
                                with col4:
                                    city = st.text_input("City *", placeholder="City name", value=st.session_state["order_form_extracted"].get("city", ""), disabled=st.session_state.creating_order)
                                # Row 3: Pincode and Product
                                col5, col6 = st.columns(2)
                                with col5:
                                    pincode = st.text_input("Pincode *", placeholder="123456 (6 digits)", value=st.session_state["order_form_extracted"].get("pincode", ""), disabled=st.session_state.creating_order)
                                with col6:
                                    product = st.text_area("Product Description *", placeholder="Product details", height=100, value=st.session_state["order_form_extracted"].get("product", ""), disabled=st.session_state.creating_order)
                                # --- Amount fields just above Payment Mode ---
                                col_balance, col_advance, col_total = st.columns([1, 1, 1])
                                extracted_balance = st.session_state["order_form_extracted"].get("balance_to_pay", None)
                                balance_default = str(extracted_balance) if extracted_balance not in (None, "") else str(st.session_state.balance_amount)
                                with col_balance:
                                    st.markdown(f"<span style='color:black;'>Extracted Balance: {extracted_balance}, Session: {st.session_state.balance_amount}</span>", unsafe_allow_html=True)
                                    balance_input = st.text_input(
                                        "Balance to Pay *",
                                        value=str(st.session_state["order_form_extracted"].get("balance_to_pay", "")),
                                        disabled=st.session_state.creating_order
                                    )
                                extracted_advance = st.session_state["order_form_extracted"].get("advance_paid", None)
                                advance_default = str(extracted_advance) if extracted_advance not in (None, "") else str(st.session_state.advance_amount)
                                with col_advance:
                                    st.markdown(f"<span style='color:black;'>Extracted Advance: {extracted_advance}, Session: {st.session_state.advance_amount}</span>", unsafe_allow_html=True)
                                    advance_input = st.text_input(
                                        "Advance Paid",
                                        value=str(st.session_state["order_form_extracted"].get("advance_paid", "")),
                                        disabled=st.session_state.creating_order
                                    )
                                # Payment type dropdown
                                payment_types = ["COD", "Prepaid"]
                                extracted_payment = st.session_state["order_form_extracted"].get("payment_method", "")
                                # Case-insensitive match for extracted payment type
                                payment_index = 0
                                for i, p in enumerate(payment_types):
                                    if extracted_payment.strip().lower() == p.lower():
                                        payment_index = i
                                        break
                                payment_method = st.selectbox(
                                    "Payment Type *",
                                    payment_types,
                                    index=payment_index,
                                    disabled=st.session_state.creating_order
                                )
                                # Calculate and show total
                                balance_val = balance_input if balance_input not in (None, "") else extracted_balance
                                advance_val = advance_input if advance_input not in (None, "") else extracted_advance
                                try:
                                    st.session_state.balance_amount = float(balance_val) if balance_val not in (None, "") else 0.0
                                except ValueError:
                                    st.session_state.balance_amount = 0.0
                                try:
                                    st.session_state.advance_amount = float(advance_val) if advance_val not in (None, "") else 0.0
                                except ValueError:
                                    st.session_state.advance_amount = 0.0
                                st.session_state.total_amount = st.session_state.balance_amount + st.session_state.advance_amount
                                with col_total:
                                    st.metric("💰 Total Amount", f"₹{st.session_state.total_amount:.2f}")
                                # Enable Create Order button only if all required fields are filled and total_amount > 0
                                required_fields_filled = all([
                                    customer_name,
                                    phone,
                                    address,
                                    city,
                                    pincode,
                                    product,
                                    st.session_state.total_amount > 0
                                ])
                                submitted = st.form_submit_button(
                                    "🛒 Create Order", 
                                    width='stretch', 
                                    type="primary", 
                                    disabled=st.session_state.creating_order or not required_fields_filled
                                )
                                if submitted:
                                    # Set loading state
                                    st.session_state.creating_order = True
                                    # Get financial values from session state
                                    balance_to_pay = st.session_state.balance_amount
                                    advance_paid = st.session_state.advance_amount
                                    total_amount = st.session_state.total_amount
                                    # Validation
                                    required_fields = [customer_name, phone, address, city, pincode, product]
                                    if not all(required_fields) or balance_to_pay <= 0:
                                        st.session_state.creating_order = False
                                        st.error("❌ Please fill all required fields and ensure balance to pay is greater than 0")
                                    else:
                                        try:
                                            # Generate order ID
                                            order_id = f"ORD{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
                                            # Show spinner while processing
                                            with st.spinner("Creating order..."):
                                                # Prepare order data matching Excel schema
                                                order_data = {
                                                    'order_id': order_id,
                                                    'phone': phone,
                                                    'customer_name': customer_name,
                                                    'product': product,
                                                    'quantity': 1,  # Default quantity
                                                    'balance_to_pay': balance_to_pay,
                                                    'advance_paid': advance_paid,
                                                    'total': total_amount,
                                                    'address': address,
                                                    'city': city,
                                                    'pincode': pincode,
                                                    'payment_method': payment_method,
                                                    'status': 'Pending',
                                                    'timestamp': datetime.now().isoformat(),
                                                    'ai_order_id': '',
                                                    'tracking_id': '',
                                                    'courier_name': '',
                                                    'created_by': user.get('user_id'),
                                                }
                                                # Save to Excel with delay to show spinner effect
                                                import time
                                                time.sleep(1)  # Brief delay to show spinner
                                                success = services['orders'].create_order(order_data)
                                            # Reset loading state
                                            st.session_state.creating_order = False
                                            if success:
                                                st.session_state["order_success"] = {
                                                    "order_id": order_id,
                                                    "total_amount": total_amount,
                                                    "customer_name": customer_name,
                                                    "phone": phone
                                                }
                                                # Reset amount session state
                                                st.session_state.balance_amount = 0.0
                                                st.session_state.advance_amount = 0.0
                                                st.session_state.total_amount = 0.0
                                                st.session_state["order_form_extracted"] = {k: "" for k in template_fields}
                                                success_animation()
                                            else:
                                                st.error("❌ Failed to create order. Please try again.")
                                        except Exception as e:
                                            st.session_state.creating_order = False
                                            st.error(f"❌ Error creating order: {str(e)}")
                                            error_animation()
                    
                    # Revenue and Profit chart
                    st.line_chart(chart_df.set_index('Date')[['Revenue', 'Net Profit']])
                    
                    # Order count chart
                    st.markdown("#### 📊 Daily Order Count")
                    st.bar_chart(chart_df.set_index('Date')['Orders'])
            else:
                st.error(f"❌ Error: {data['error']}")
        
        # Revenue Entry Form
        st.markdown("---")
        st.markdown("### 💰 Add Revenue Entry")
        
        with st.form("revenue_entry"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                entry_date = st.date_input("Date", value=datetime.now().date())
                ad_spend = st.number_input("Ad Spend (₹)", min_value=0.0, step=100.0, format="%.2f")
            
            with col2:
                courier_expenses = st.number_input("Courier Expenses (₹)", min_value=0.0, step=50.0, format="%.2f")
                other_expenses = st.number_input("Other Expenses (₹)", min_value=0.0, step=50.0, format="%.2f")
            
            with col3:
                notes = st.text_area("Notes", height=100)
            
            if st.form_submit_button("💾 Add Revenue Entry", type="primary", use_container_width=True):
                try:
                    success = business_analytics.add_revenue_entry(
                        entry_date, ad_spend, courier_expenses, other_expenses, 
                        notes, user.get('name', 'Unknown')
                    )
                    
                    if success:
                        st.success("✅ Revenue entry added successfully!")
                    else:
                        st.error("❌ Failed to add revenue entry")
                        
                except Exception as e:
                    st.error(f"❌ Error adding revenue entry: {str(e)}")
    
    with tab3:
        st.markdown("### 📈 Business Intelligence Dashboard")
        st.info("🚧 Advanced analytics dashboard coming soon with trend analysis, forecasting, and competitive insights.")
        
        # Placeholder for future BI features
        if st.button("🔮 Generate Business Insights", key="tab3_business_insights"):
            st.success("📊 Business Intelligence features will include:")
            st.markdown("- 📈 Revenue trend analysis")
            st.markdown("- 🎯 Customer acquisition cost optimization") 
            st.markdown("- 📊 Profit margin optimization")
            st.markdown("- 🔍 Market opportunity analysis")
            st.markdown("- 📅 Seasonal performance patterns")
    
    with tab4:
        st.markdown("### 📈 Business Intelligence Dashboard")
        st.info("🚧 Advanced analytics dashboard coming soon with trend analysis, forecasting, and competitive insights.")
        
        # Placeholder for future BI features
        if st.button("🔮 Generate Business Insights", key="duplicate_bi_insights"):
            st.success("📊 Business Intelligence features will include:")
            st.markdown("- 📈 Revenue trend analysis")
            st.markdown("- 🎯 Customer acquisition cost optimization") 
            st.markdown("- 📊 Profit margin optimization")
            st.markdown("- 🔍 Market opportunity analysis")
            st.markdown("- 📅 Seasonal performance patterns")
    
    with tab3:
        st.markdown("### 📊 Advanced Reports")
        st.info("🚧 Comprehensive reporting suite under development.")
        
        # Placeholder for reports
        if st.button("📑 Generate Reports", key="generate_reports_btn"):
            st.success("📋 Advanced reports will include:")
            st.markdown("- 💰 Financial performance reports")
            st.markdown("- 📈 Growth analysis reports")
            st.markdown("- 🎯 Marketing efficiency reports")
            st.markdown("- 📦 Operational cost reports")
            st.markdown("- 📊 Competitive analysis reports")


def render_reports_page(services, user):
    """Render reports page with date filtering"""
    render_header(
        "📈 Business Reports", 
        "Generate and download comprehensive business reports with date filtering",
        show_time=True
    )
    
    # Date Filters for Reports
    start_date, end_date, selected_filter = render_date_filters("reports")
    
    # Show current filter info
    start_display = start_date.strftime('%Y-%m-%d') if start_date else 'None'
    end_display = end_date.strftime('%Y-%m-%d') if end_date else 'None'
    st.info(f"📅 Showing data for: **{selected_filter}** ({start_display} to {end_display})")
    
    # Get filtered data
    try:
        orders_df = services['orders'].get_user_orders(user['user_id']) if user['role'] == 'user' else services['orders'].get_all_orders()
        inventory_df = services['inventory'].get_all_inventory()
        
        # Apply date filtering to orders
        if not orders_df.empty and start_date is not None and end_date is not None:
            orders_df = filter_dataframe_by_date(orders_df, start_date, end_date)
        
        # Report sections
        tab1, tab2, tab3, tab4 = st.tabs(["📦 Order Reports", "📋 Inventory Reports", "💰 Financial Reports", "📊 Summary Report"])
        
        with tab1:
            st.markdown("### 📦 Order Analysis Report")
            if not orders_df.empty:
                col1, col2, col3 = st.columns(3)
                with col1:
                    total_orders = len(orders_df)
                    render_metric_card("Total Orders", str(total_orders), "📦")
                
                with col2:
                    total_revenue = orders_df['total'].sum() if 'total' in orders_df.columns else 0
                    render_metric_card("Total Revenue", f"₹{total_revenue:,.2f}", "💰")
                
                with col3:
                    avg_order_value = orders_df['total'].mean() if 'total' in orders_df.columns and len(orders_df) > 0 else 0
                    render_metric_card("Avg Order Value", f"₹{avg_order_value:.2f}", "📊")
                
                # Order status distribution
                if 'status' in orders_df.columns:
                    st.markdown("#### Order Status Distribution")
                    status_counts = orders_df['status'].value_counts()
                    st.bar_chart(status_counts)
                
                # Daily order trends
                if 'timestamp' in orders_df.columns:
                    st.markdown("#### Daily Order Trends")
                    orders_df['date'] = pd.to_datetime(orders_df['timestamp']).dt.date
                    daily_orders = orders_df.groupby('date').size()
                    st.line_chart(daily_orders)
                
                # Download order report
                if st.button("📥 Download Order Report", key="download_orders"):
                    csv = orders_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"order_report_{start_date}_{end_date}.csv",
                        mime="text/csv"
                    )
            else:
                st.warning("No orders found for the selected date range.")
        
        with tab2:
            st.markdown("### 📋 Inventory Analysis Report")
            if not inventory_df.empty:
                col1, col2, col3 = st.columns(3)
                with col1:
                    total_products = len(inventory_df)
                    render_metric_card("Total Products", str(total_products), "📋")
                
                with col2:
                    total_stock = inventory_df['Available_Quantity'].sum() if 'Available_Quantity' in inventory_df.columns else 0
                    render_metric_card("Total Stock", str(int(total_stock)), "📦")
                
                with col3:
                    low_stock_items = len(services['inventory'].get_low_stock_alerts())
                    render_metric_card("Low Stock Items", str(low_stock_items), "⚠️")
                
                # Product categories
                if 'Category' in inventory_df.columns:
                    st.markdown("#### Product Categories")
                    category_counts = inventory_df['Category'].value_counts()
                    st.bar_chart(category_counts)
                
                # Download inventory report
                if st.button("📥 Download Inventory Report", key="download_inventory"):
                    csv = inventory_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"inventory_report_{start_date}_{end_date}.csv",
                        mime="text/csv"
                    )
            else:
                st.warning("No inventory data found.")
        
        with tab3:
            st.markdown("### 💰 Financial Analysis Report")
            if not orders_df.empty and 'total' in orders_df.columns:
                # Financial metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    total_revenue = orders_df['total'].sum()
                    render_metric_card("Total Revenue", f"₹{total_revenue:,.2f}", "💰")
                
                with col2:
                    completed_orders = orders_df[orders_df['status'] == 'Delivered'] if 'status' in orders_df.columns else orders_df
                    completed_revenue = completed_orders['total'].sum() if not completed_orders.empty else 0
                    render_metric_card("Completed Revenue", f"₹{completed_revenue:,.2f}", "✅")
                
                with col3:
                    pending_orders = orders_df[orders_df['status'].isin(['Pending', 'In Transit'])] if 'status' in orders_df.columns else pd.DataFrame()
                    pending_revenue = pending_orders['total'].sum() if not pending_orders.empty else 0
                    render_metric_card("Pending Revenue", f"₹{pending_revenue:,.2f}", "⏳")
                
                with col4:
                    avg_daily_revenue = total_revenue / max(1, (end_date - start_date).days + 1)
                    render_metric_card("Daily Avg Revenue", f"₹{avg_daily_revenue:.2f}", "📈")
                
                # Revenue trends
                if 'timestamp' in orders_df.columns:
                    st.markdown("#### Daily Revenue Trends")
                    orders_df['date'] = pd.to_datetime(orders_df['timestamp']).dt.date
                    daily_revenue = orders_df.groupby('date')['total'].sum()
                    st.line_chart(daily_revenue)
            else:
                st.warning("No financial data available for the selected period.")
        
        with tab4:
            st.markdown("### 📊 Executive Summary Report")
            
            # Create comprehensive summary
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📈 Key Performance Indicators")
                if not orders_df.empty:
                    kpi_data = {
                        "Metric": ["Total Orders", "Total Revenue", "Average Order Value", "Conversion Rate"],
                        "Value": [
                            len(orders_df),
                            f"₹{orders_df['total'].sum():,.2f}" if 'total' in orders_df.columns else "₹0",
                            f"₹{orders_df['total'].mean():.2f}" if 'total' in orders_df.columns else "₹0",
                            "85%"  # Placeholder - would calculate from actual data
                        ]
                    }
                    st.table(pd.DataFrame(kpi_data))
            
            with col2:
                st.markdown("#### 🎯 Business Insights")
                insights = [
                    f"📊 {len(orders_df)} orders processed in selected period" if not orders_df.empty else "📊 No orders in selected period",
                    f"📦 {len(inventory_df)} products in inventory" if not inventory_df.empty else "📦 No inventory data",
                    f"⚠️ {len(services['inventory'].get_low_stock_alerts())} items need restocking",
                    f"🎯 Peak performance on {selected_filter.lower()}"
                ]
                for insight in insights:
                    st.write(insight)
            
            # Generate comprehensive report
            if st.button("📋 Generate Complete Summary Report", key="summary_report"):
                st.success("📋 Summary report generated successfully!")
                
                # Create summary data
                summary_data = {
                    "Report Period": [f"{start_date} to {end_date}"],
                    "Total Orders": [len(orders_df) if not orders_df.empty else 0],
                    "Total Revenue": [orders_df['total'].sum() if not orders_df.empty and 'total' in orders_df.columns else 0],
                    "Products in Inventory": [len(inventory_df) if not inventory_df.empty else 0],
                    "Low Stock Alerts": [len(services['inventory'].get_low_stock_alerts())]
                }
                
                summary_df = pd.DataFrame(summary_data)
                csv = summary_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Summary Report",
                    data=csv,
                    file_name=f"executive_summary_{start_date}_{end_date}.csv",
                    mime="text/csv"
                )
        
    except Exception as e:
        st.error(f"Error generating reports: {e}")
        logger.error(f"Reports error: {e}")


if __name__ == "__main__":
    main()