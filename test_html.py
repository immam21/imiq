import streamlit as st
from imiq.ui_components import render_metric_card, apply_custom_css

st.set_page_config(page_title="HTML Test", layout="wide")
apply_custom_css()

st.title("🔧 HTML Rendering Test")

# Test metric cards to see if HTML tags show up
col1, col2, col3 = st.columns(3)

with col1:
    render_metric_card("Test Metric 1", "42", "📊", "primary")

with col2:
    render_metric_card("Test Metric 2", "₹1,234.56", "💰", "success", delta="+5.2%")

with col3:
    render_metric_card("Test Metric 3", "100", "📈", "info", delta="-2.1%")

st.markdown("---")
st.write("✅ If you don't see any `<div>` tags above, the HTML rendering is fixed!")
st.write("❌ If you see `<div>` tags, there's still an issue with HTML rendering.")