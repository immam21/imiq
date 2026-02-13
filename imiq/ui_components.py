"""
IMIQ UI Components - Professional Mobile-Responsive Design
Modern, attractive UI components with desktop and mobile support
"""

import streamlit as st
from streamlit_lottie import st_lottie
import requests
from typing import Optional, Dict, Any, List
import logging
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

logger = logging.getLogger(__name__)

# Modern Professional Color Palette with Gradients
COLORS = {
    'primary': '#667eea',
    'primary_dark': '#4c51bf',
    'secondary': '#764ba2',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'light': '#f8fafc',
    'dark': '#1e293b',
    'accent': '#8b5cf6',
    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'card_bg': '#ffffff',
    'sidebar': 'linear-gradient(180deg, #f1f5f9 0%, #e2e8f0 100%)',
    'text_primary': '#1e293b',
    'text_secondary': '#64748b',
    'border': '#e2e8f0',
    'shadow': '0 10px 25px rgba(0, 0, 0, 0.1)',
    'glassmorphism': 'rgba(255, 255, 255, 0.95)'
}

def apply_custom_css():
    """Apply minimal CSS for basic functionality"""
    st.markdown("""
    <style>
    /* Minimal CSS for testing */
    body {
        font-family: 'Inter', sans-serif;
    }
    
    /* Ensure input visibility */
    .stTextInput > div > div > input {
        color: #1a202c !important;
        background-color: #ffffff !important;
    }
    
    /* Basic button styling */
    .stButton > button {
        background-color: #0066cc;
        color: white;
        border: 1px solid #0066cc;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header(title: str, subtitle: str = "", show_time: bool = True, icon: str = "🚀"):
    """Render a simple header"""
    from imiq.utils import get_ist_now
    current_time = get_ist_now().strftime("%B %d, %Y - %I:%M %p IST") if show_time else ""
    
    st.markdown(f"""
    <div style="padding: 2rem 0; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 2.5rem;">{icon} {title}</h1>
        {f'<p style="margin: 0.5rem 0; font-size: 1.2rem;">{subtitle}</p>' if subtitle else ''}
        {f'<p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">{current_time}</p>' if show_time else ''}
    </div>
    """, unsafe_allow_html=True)


# Color constants for consistent theming
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'accent': '#f093fb',
    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'sidebar': 'rgba(255, 255, 255, 0.95)',
    'border': 'rgba(0, 0, 0, 0.1)',
    'text': '#1a202c',
    'text_light': '#4a5568',
    'text_primary': '#1a202c',
    'text_secondary': '#4a5568',
    'card_bg': 'rgba(255, 255, 255, 0.98)',
    'light': '#f7fafc',
    'success': '#48bb78',
    'warning': '#ed8936',
    'error': '#e53e3e',
    'danger': '#e53e3e',
    'info': '#4299e1',
    'shadow': '0 4px 20px rgba(0, 0, 0, 0.1)',
    'glassmorphism': 'rgba(255, 255, 255, 0.1)'
}
def render_enhanced_login_form():
    """Render a clean login form"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Login</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                return username, password
    return None, None

def render_enhanced_signup_form():
    """Render a clean signup form"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Sign Up</h2>", unsafe_allow_html=True)
        
        with st.form("signup_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Sign Up")
            
            if submit:
                if password == confirm_password:
                    return username, email, password
                else:
                    st.error("Passwords don't match!")
    return None, None, None

def render_header(title: str, subtitle: str = "", show_time: bool = True, icon: str = "🚀"):
    """Render a modern professional header with advanced 3D animations and parallax effects"""
    from imiq.utils import get_ist_now
    current_time = get_ist_now().strftime("%B %d, %Y - %I:%M %p IST")
    
    # Enhanced header CSS with 3D effects
    header_css = """
    <style>
    /* Advanced 3D Header Styles */
    .custom-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        padding: 2.5rem 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.25),
            0 15px 30px rgba(102, 126, 234, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(255,255,255,0.2);
        animation: 
            headerFloat 6s ease-in-out infinite,
            headerGradient 15s ease infinite,
            headerGlow 4s ease-in-out infinite alternate;
        transform-style: preserve-3d;
        perspective: 1000px;
    }
    
    /* Multiple animated layers for depth */
    .custom-header::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: conic-gradient(
            from 45deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            rgba(102, 126, 234, 0.2),
            rgba(118, 75, 162, 0.1),
            transparent 60%
        );
        animation: headerRotate 20s linear infinite;
        z-index: 0;
        filter: blur(1px);
    }
    
    .custom-header::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: 
            radial-gradient(circle at 20% 30%, rgba(255,255,255,0.15) 2px, transparent 2px),
            radial-gradient(circle at 80% 70%, rgba(255,255,255,0.12) 1px, transparent 1px),
            radial-gradient(circle at 60% 20%, rgba(240,147,251,0.1) 1.5px, transparent 1.5px);
        background-size: 80px 80px, 60px 60px, 100px 100px;
        animation: sparkleMove 30s linear infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes headerFloat {
        0%, 100% { transform: translateY(0) rotateX(0deg) scale(1); }
        33% { transform: translateY(-8px) rotateX(2deg) scale(1.02); }
        66% { transform: translateY(4px) rotateX(-1deg) scale(0.98); }
    }
    
    @keyframes headerGradient {
        0% { background-position: 0% 50%; }
        25% { background-position: 100% 25%; }
        50% { background-position: 100% 75%; }
        75% { background-position: 0% 100%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes headerGlow {
        from { 
            box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.25),
                0 15px 30px rgba(102, 126, 234, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }
        to { 
            box-shadow: 
                0 35px 70px rgba(0, 0, 0, 0.35),
                0 20px 40px rgba(102, 126, 234, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.5),
                0 0 50px rgba(102, 126, 234, 0.3);
        }
    }
    
    @keyframes headerRotate {
        0% { transform: rotate(0deg) scale(1); }
        100% { transform: rotate(360deg) scale(1.1); }
    }
    
    @keyframes sparkleMove {
        0% { transform: translateY(0) translateX(0); opacity: 0.6; }
        50% { transform: translateY(-20px) translateX(10px); opacity: 1; }
        100% { transform: translateY(0) translateX(0); opacity: 0.6; }
    }
    
    /* Enhanced header content */
    .custom-header h1 {
        margin: 0;
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 50%, #ffffff 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 3;
        text-shadow: none;
        animation: 
            titleShimmer 8s ease-in-out infinite,
            titleFloat 5s ease-in-out infinite;
        transform-style: preserve-3d;
    }
    
    .custom-header h1::before {
        content: attr(data-text);
        position: absolute;
        top: 3px; left: 3px;
        background: linear-gradient(135deg, rgba(0,0,0,0.3), rgba(0,0,0,0.1));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        z-index: -1;
        transform: translateZ(-10px);
        filter: blur(1px);
    }
    
    @keyframes titleShimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes titleFloat {
        0%, 100% { transform: translateY(0) rotateX(0deg); }
        50% { transform: translateY(-5px) rotateX(2deg); }
    }
    
    /* Enhanced subtitle styling */
    .header-subtitle {
        font-weight: 400;
        margin-top: 1rem;
        opacity: 0.95;
        font-size: clamp(1rem, 2.5vw, 1.3rem);
        position: relative;
        z-index: 3;
        animation: subtitleGlow 6s ease-in-out infinite alternate;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    @keyframes subtitleGlow {
        from { opacity: 0.9; text-shadow: 0 2px 10px rgba(0,0,0,0.2); }
        to { opacity: 1; text-shadow: 0 4px 20px rgba(255,255,255,0.3); }
    }
    
    /* Enhanced time display */
    .header-time {
        margin-top: 1.5rem;
        opacity: 0.85;
        font-size: 0.9rem;
        font-weight: 300;
        position: relative;
        z-index: 3;
        padding: 0.5rem 1rem;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 50px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        display: inline-block;
        animation: timeFloat 4s ease-in-out infinite;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    
    @keyframes timeFloat {
        0%, 100% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-3px) scale(1.05); }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .custom-header {
            padding: 2rem 1.5rem;
            margin-bottom: 1.5rem;
            border-radius: 20px;
        }
        .custom-header h1 {
            font-size: 2rem;
        }
        .header-subtitle {
            font-size: 1rem;
        }
        .header-time {
            font-size: 0.8rem;
            padding: 0.4rem 0.8rem;
        }
    }
    </style>
    """
    
    header_html = f"""
    {header_css}
    <div class="custom-header">
        <div style="position: relative; z-index: 3;">
            <h1 data-text="{icon} {title}">{icon} {title}</h1>
            {f'<div class="header-subtitle">{subtitle}</div>' if subtitle else ''}
            {f'<div class="header-time">📅 {current_time}</div>' if show_time else ''}
        </div>
    </div>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)

def render_login_form():
    """Render ultra-minimal animated login form with advanced 3D effects"""
    
    # Ultra-minimal CSS with advanced 3D effects and particle systems
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Advanced animated background with particles */
    .stApp {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe, #00f2fe);
        background-size: 500% 500%;
        animation: gradientShift 20s ease infinite;
        font-family: 'Poppins', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(255,255,255,0.15) 2px, transparent 2px),
            radial-gradient(circle at 80% 20%, rgba(255,255,255,0.12) 1.5px, transparent 1.5px),
            radial-gradient(circle at 40% 40%, rgba(255,255,255,0.08) 1px, transparent 1px),
            radial-gradient(circle at 60% 90%, rgba(102,126,234,0.1) 3px, transparent 3px);
        background-size: 120px 120px, 80px 80px, 60px 60px, 150px 150px;
        animation: particleMove 25s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes particleMove {
        0% { transform: translate(0, 0) rotate(0deg); opacity: 0.6; }
        25% { transform: translate(-30px, -30px) rotate(90deg); opacity: 1; }
        50% { transform: translate(30px, -60px) rotate(180deg); opacity: 0.8; }
        75% { transform: translate(-60px, 30px) rotate(270deg); opacity: 1; }
        100% { transform: translate(0, 0) rotate(360deg); opacity: 0.6; }
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        25% { background-position: 100% 0%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Ultra-minimal container with 3D perspective */
    .main .block-container {
        padding: 1rem !important;
        max-width: 450px !important;
        margin: 0 auto !important;
        perspective: 1200px;
        transform-style: preserve-3d;
    }
    
    /* Advanced 3D branding */
    .brand-minimal {
        text-align: center;
        margin: 1rem 0;
        animation: brandFloat 4s ease-in-out infinite;
        transform-style: preserve-3d;
    }
    
    .brand-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 
            0 0 25px rgba(255,255,255,0.8),
            0 4px 15px rgba(0,0,0,0.3),
            0 8px 30px rgba(102,126,234,0.4);
        animation: 
            textGlow 3s ease-in-out infinite alternate,
            text3D 6s ease-in-out infinite;
        letter-spacing: 1px;
        position: relative;
        transform-style: preserve-3d;
    }
    
    .brand-title::before {
        content: '🚀 IMIQ';
        position: absolute;
        top: 2px; left: 2px;
        color: rgba(0,0,0,0.3);
        z-index: -1;
        transform: translateZ(-20px) rotateX(5deg);
        animation: shadow3D 6s ease-in-out infinite;
    }
    
    @keyframes brandFloat {
        0%, 100% { transform: translateY(0) rotateX(0deg); }
        50% { transform: translateY(-15px) rotateX(5deg); }
    }
    
    @keyframes textGlow {
        from { 
            text-shadow: 0 0 20px rgba(255,255,255,0.5),
                        0 4px 15px rgba(0,0,0,0.3),
                        0 8px 30px rgba(102,126,234,0.3); 
        }
        to { 
            text-shadow: 0 0 40px rgba(255,255,255,0.9),
                        0 4px 25px rgba(0,0,0,0.4),
                        0 8px 50px rgba(118,75,162,0.6); 
        }
    }
    
    @keyframes text3D {
        0%, 100% { transform: rotateY(0deg) rotateX(0deg); }
        25% { transform: rotateY(3deg) rotateX(2deg); }
        75% { transform: rotateY(-3deg) rotateX(-2deg); }
    }
    
    @keyframes shadow3D {
        0%, 100% { transform: translateZ(-20px) rotateX(5deg) rotateY(0deg); opacity: 0.3; }
        50% { transform: translateZ(-25px) rotateX(8deg) rotateY(2deg); opacity: 0.5; }
    }
    
    /* Ultra-compact form with advanced 3D transforms */
    .ultra-form {
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(30px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.35);
        border-radius: 20px;
        padding: 2rem 1.8rem;
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.25),
            0 15px 30px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.6);
        animation: slideUp3D 1s cubic-bezier(0.175, 0.885, 0.32, 1.275),
                   formFloat3D 8s ease-in-out infinite;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
    }
    
    @keyframes slideUp3D {
        0% { 
            opacity: 0; 
            transform: translateY(60px) translateZ(-100px) rotateX(25deg) scale(0.8); 
        }
        100% { 
            opacity: 1; 
            transform: translateY(0) translateZ(0) rotateX(0deg) scale(1); 
        }
    }
    
    @keyframes formFloat3D {
        0%, 100% { transform: translateY(0) rotateX(0deg) rotateY(0deg); }
        33% { transform: translateY(-8px) rotateX(2deg) rotateY(1deg); }
        66% { transform: translateY(4px) rotateX(-1deg) rotateY(-1deg); }
    }
    
    /* Multiple rotating borders with 3D effect */
    .ultra-form::before {
        content: '';
        position: absolute;
        top: -3px; left: -3px; right: -3px; bottom: -3px;
        background: conic-gradient(
            transparent, 
            rgba(255, 255, 255, 0.4), 
            rgba(102, 126, 234, 0.6),
            rgba(118, 75, 162, 0.5),
            transparent 60%
        );
        border-radius: 23px;
        animation: rotate3D 10s linear infinite, borderPulse 3s ease-in-out infinite;
        z-index: -2;
        filter: blur(1px);
    }
    
    .ultra-form::after {
        content: '';
        position: absolute;
        top: -2px; left: -2px; right: -2px; bottom: -2px;
        background: conic-gradient(
            from 180deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            rgba(240, 147, 251, 0.4),
            transparent 40%
        );
        border-radius: 22px;
        animation: rotate3D 15s linear infinite reverse, innerGlow 2s ease-in-out infinite alternate;
        z-index: -1;
    }
    
    @keyframes rotate3D {
        0% { transform: rotate(0deg) scale(1); }
        25% { transform: rotate(90deg) scale(1.05); }
        50% { transform: rotate(180deg) scale(1); }
        75% { transform: rotate(270deg) scale(1.05); }
        100% { transform: rotate(360deg) scale(1); }
    }
    
    @keyframes borderPulse {
        0%, 100% { filter: blur(1px) brightness(1); }
        50% { filter: blur(3px) brightness(1.5); }
    }
    
    @keyframes innerGlow {
        from { opacity: 0.6; filter: brightness(1); }
        to { opacity: 1; filter: brightness(1.3); }
    }
    
    /* Advanced 3D input styling with morphing effects */
    .stTextInput > label {
        display: none !important;
    }
    
    .stTextInput input {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        padding: 1rem 1.2rem !important;
        color: white !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(15px) !important;
        margin-bottom: 1rem !important;
        position: relative;
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
        transform-style: preserve-3d;
    }
    
    .stTextInput input:focus {
        border-color: rgba(255, 255, 255, 0.7) !important;
        background: rgba(255, 255, 255, 0.25) !important;
        box-shadow: 
            0 0 30px rgba(255, 255, 255, 0.4),
            0 15px 35px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
        transform: translateY(-3px) translateZ(10px) rotateX(2deg) !important;
        backdrop-filter: blur(20px) !important;
    }
    
    .stTextInput input:hover {
        transform: translateY(-1px) translateZ(5px) !important;
        box-shadow: 
            0 12px 30px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.8) !important;
        font-weight: 300 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
        transform: translateX(5px);
    }
    
    /* Advanced 3D button styling with morphing effects */
    .stButton button {
        border-radius: 15px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 1rem 1.8rem !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        border: none !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        margin-top: 0.8rem !important;
        position: relative;
        overflow: hidden;
        transform-style: preserve-3d;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.3), 
            transparent);
        transition: left 0.6s;
    }
    
    .stButton button:hover::before {
        left: 100%;
    }
    
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        color: white !important;
        box-shadow: 
            0 10px 30px rgba(102, 126, 234, 0.4),
            0 5px 15px rgba(118, 75, 162, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    .stButton button[kind="primary"]:hover {
        transform: translateY(-5px) translateZ(20px) rotateX(5deg) !important;
        box-shadow: 
            0 20px 50px rgba(102, 126, 234, 0.6),
            0 10px 25px rgba(118, 75, 162, 0.4),
            0 5px 15px rgba(240, 147, 251, 0.3) !important;
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 50%, #de7be8 100%) !important;
    }
    
    .stButton button[kind="primary"]:active {
        transform: translateY(-2px) translateZ(10px) rotateX(2deg) !important;
    }
    
    .stButton button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.12) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.35) !important;
        backdrop-filter: blur(10px);
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .stButton button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.7) !important;
        transform: translateY(-4px) translateZ(15px) rotateX(3deg) !important;
        box-shadow: 
            0 15px 40px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.5);
    }
    
    .stButton button[kind="secondary"]:active {
        transform: translateY(-1px) translateZ(8px) rotateX(1deg) !important;
    }
    
    /* Mobile optimization with enhanced 3D effects */
    @media (max-width: 768px) {
        .ultra-form { 
            padding: 1.5rem 1.3rem; 
            animation: slideUp3D 0.8s ease-out, formFloat3D 10s ease-in-out infinite;
        }
        .brand-title { 
            font-size: 1.8rem; 
            animation: textGlow 2s ease-in-out infinite alternate;
        }
        .stTextInput input {
            padding: 0.9rem 1rem !important;
        }
        .stButton button {
            padding: 0.9rem 1.5rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Ultra-minimal branding
    st.markdown("""
    <div class="brand-minimal">
        <h1 class="brand-title">🚀 IMIQ</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Centered ultra-compact form
    col1, col2, col3 = st.columns([1, 2.5, 1])
    
    with col2:
        st.markdown('<div class="ultra-form">', unsafe_allow_html=True)
        
        # No-label form
        with st.form("login_form", clear_on_submit=False):
            user_id = st.text_input("", placeholder="Enter your user ID", label_visibility="hidden")
            password = st.text_input("", type="password", placeholder="Enter your password", label_visibility="hidden")
            
            # Compact buttons
            col_a, col_b = st.columns(2)
            with col_a:
                login_button = st.form_submit_button("Login", type="primary", width='stretch')
            with col_b:
                signup_button = st.form_submit_button("Sign Up", type="secondary", width='stretch')
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    return user_id, password, login_button

def render_signup_form():
    """Render clean centered signup form matching login design"""
    
    # Clean centered signup design
    st.markdown("""
    <style>
    .signup-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem 1rem;
        min-height: 60vh;
    }
    
    .signup-card {
        background: white;
        border-radius: 12px;
        padding: 2.5rem 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(229, 231, 235, 0.8);
        width: 100%;
        max-width: 420px;
        text-align: center;
    }
    
    .signup-title {
        color: #1f2937;
        margin: 0 0 2rem 0;
        font-weight: 600;
        font-size: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    @media (max-width: 480px) {
        .signup-card {
            margin: 1rem;
            padding: 2rem 1.5rem;
        }
    }
    </style>
    
    <div class="signup-container">
        <div class="signup-card">
            <h1 class="signup-title">👤 Create IMIQ Account</h1>
    """, unsafe_allow_html=True)
    
    with st.form("signup_form", clear_on_submit=False):
        name = st.text_input(
            "Full Name:", 
            placeholder="Enter your full name",
            label_visibility="visible"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            user_id = st.text_input(
                "User ID:", 
                placeholder="unique_id",
                label_visibility="visible"
            )
        with col2:
            password = st.text_input(
                "Password:", 
                type="password", 
                placeholder="Create a secure password",
                label_visibility="visible"
            )
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        signup_button = st.form_submit_button(
            "Create Account", 
            width='stretch',
            type="primary"
        )
        
        st.markdown("""
        <div class="form-footer">
            Already have an account?<br>
            <strong>Switch to Sign In tab</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return name, user_id, password, signup_button

def render_metric_card(title: str, value: str, icon: str = "📊", color: str = "primary", delta: str = None, trend_data: list = None):
    """Render a clean metric card with proper styling"""
    card_color = COLORS.get(color, COLORS['primary'])
    
    # Simple, clean CSS that works
    metric_card_css = f"""
    <style>
    .metric-card-clean {{
        background: {COLORS['card_bg']};
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid {COLORS['border']};
        border-left: 4px solid {card_color};
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .metric-card-clean:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }}
    
    .card-title {{
        color: {COLORS['text_secondary']};
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.8rem;
    }}
    
    .card-value {{
        color: {COLORS['text_primary']};
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }}
    
    .card-icon {{
        background: {card_color}20;
        width: 48px;
        height: 48px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        float: right;
        margin-top: -10px;
    }}
    
    .card-delta {{
        font-size: 0.85rem;
        font-weight: 600;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        display: inline-block;
    }}
    
    .card-delta.positive {{
        background: {COLORS['success']}20;
        color: {COLORS['success']};
    }}
    
    .card-delta.negative {{
        background: {COLORS['error']}20;
        color: {COLORS['error']};
    }}
    </style>
    """
    
    # Build card HTML
    card_html = f"""
    {metric_card_css}
    <div class="metric-card-clean">
        <div class="card-icon">
            {icon}
        </div>
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>"""
    
    # Add delta if provided
    if delta:
        is_positive = "+" in str(delta) or (isinstance(delta, (int, float)) and delta > 0)
        delta_class = "positive" if is_positive else "negative"
        delta_icon = "↗️" if is_positive else "↘️"
        card_html += f"""
        <div class="card-delta {delta_class}">
            {delta_icon} {delta}
        </div>"""
    
    card_html += "</div>"
    
    st.markdown(card_html, unsafe_allow_html=True)

def render_card(title: str, content: str, icon: str = "📋", color: str = "primary"):
    """Render a modern card with icon and content"""
    card_color = COLORS.get(color, COLORS['primary'])
    
    card_html = f"""
    <div class="metric-card">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <div style="background: {card_color}20; padding: 8px; border-radius: 8px; margin-right: 12px;">
                <span style="font-size: 1.2rem;">{icon}</span>
            </div>
            <h3 style="margin: 0; color: {COLORS['text_primary']}; font-weight: 600;">{title}</h3>
        </div>
        <div style="color: {COLORS['text_secondary']}; line-height: 1.6;">
            {content}
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def success_animation():
    """Display advanced success animation with 3D effects"""
    st.markdown("""
    <div class="success-animation" style="
        position: fixed; top: 50%; left: 50%; 
        transform: translate(-50%, -50%);
        z-index: 9999;
        animation: successBounce 1.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
    ">
        <div style="
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 2rem 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(16, 185, 129, 0.4);
            text-align: center;
            border: 2px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(20px);
            animation: successGlow 2s ease-in-out infinite alternate;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem; animation: iconSpin 2s ease-in-out;">✅</div>
            <div style="font-size: 1.2rem; font-weight: 700;">Success!</div>
        </div>
    </div>
    
    <style>
    @keyframes successBounce {
        0% { opacity: 0; transform: translate(-50%, -50%) scale(0.3) rotateY(180deg); }
        50% { opacity: 1; transform: translate(-50%, -50%) scale(1.1) rotateY(0deg); }
        100% { opacity: 0; transform: translate(-50%, -50%) scale(0.8) rotateY(-180deg); }
    }
    @keyframes successGlow {
        from { box-shadow: 0 20px 60px rgba(16, 185, 129, 0.4); }
        to { box-shadow: 0 25px 80px rgba(16, 185, 129, 0.8), 0 0 50px rgba(16, 185, 129, 0.6); }
    }
    @keyframes iconSpin {
        0%, 100% { transform: rotateY(0deg) scale(1); }
        50% { transform: rotateY(360deg) scale(1.2); }
    }
    </style>
    """, unsafe_allow_html=True)
    st.balloons()

def error_animation():
    """Display advanced error animation with 3D effects"""
    st.markdown("""
    <div class="error-animation" style="
        position: fixed; top: 50%; left: 50%; 
        transform: translate(-50%, -50%);
        z-index: 9999;
        animation: errorShake 1.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
    ">
        <div style="
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            padding: 2rem 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(239, 68, 68, 0.4);
            text-align: center;
            border: 2px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(20px);
            animation: errorPulse 2s ease-in-out infinite alternate;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem; animation: iconShake 1s ease-in-out;">❌</div>
            <div style="font-size: 1.2rem; font-weight: 700;">Error Occurred!</div>
        </div>
    </div>
    
    <style>
    @keyframes errorShake {
        0% { opacity: 0; transform: translate(-50%, -50%) scale(0.3) rotateX(180deg); }
        25% { transform: translate(-45%, -50%) scale(1.1) rotateX(0deg); }
        50% { transform: translate(-55%, -50%) scale(1.1) rotateX(0deg); }
        75% { transform: translate(-45%, -50%) scale(1.1) rotateX(0deg); }
        100% { opacity: 0; transform: translate(-50%, -50%) scale(0.8) rotateX(-180deg); }
    }
    @keyframes errorPulse {
        from { box-shadow: 0 20px 60px rgba(239, 68, 68, 0.4); }
        to { box-shadow: 0 25px 80px rgba(239, 68, 68, 0.8), 0 0 50px rgba(239, 68, 68, 0.6); }
    }
    @keyframes iconShake {
        0%, 100% { transform: rotateZ(0deg); }
        25% { transform: rotateZ(-15deg); }
        75% { transform: rotateZ(15deg); }
    }
    </style>
    """, unsafe_allow_html=True)

def render_loading_spinner(message: str = "Loading..."):
    """Render advanced 3D loading spinner with particle effects"""
    st.markdown(f"""
    <div class="advanced-loading" style="
        text-align: center; 
        padding: 4rem 2rem;
        position: relative;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-radius: 25px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(102, 126, 234, 0.1);
        margin: 2rem 0;
    ">
        <!-- Particle Background -->
        <div style="
            position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: 
                radial-gradient(circle at 20% 30%, rgba(102,126,234,0.1) 2px, transparent 2px),
                radial-gradient(circle at 80% 70%, rgba(118,75,162,0.1) 1.5px, transparent 1.5px);
            background-size: 60px 60px, 80px 80px;
            animation: loadingParticles 20s linear infinite;
            border-radius: 25px;
        "></div>
        
        <!-- 3D Loader -->
        <div class="spinner-3d" style="
            width: 80px; height: 80px;
            margin: 0 auto 2rem auto;
            position: relative;
            animation: spinnerFloat 3s ease-in-out infinite;
        ">
            <div style="
                width: 100%; height: 100%;
                border: 6px solid rgba(102, 126, 234, 0.2);
                border-top: 6px solid #667eea;
                border-radius: 50%;
                animation: spin3D 2s linear infinite;
                position: absolute;
                box-shadow: 0 0 30px rgba(102, 126, 234, 0.4);
            "></div>
            <div style="
                width: 60px; height: 60px;
                border: 4px solid rgba(118, 75, 162, 0.2);
                border-right: 4px solid #764ba2;
                border-radius: 50%;
                animation: spin3DReverse 1.5s linear infinite;
                position: absolute;
                top: 10px; left: 10px;
                box-shadow: 0 0 20px rgba(118, 75, 162, 0.4);
            "></div>
            <div style="
                width: 40px; height: 40px;
                border: 3px solid rgba(240, 147, 251, 0.2);
                border-bottom: 3px solid #f093fb;
                border-radius: 50%;
                animation: spin3D 1s linear infinite;
                position: absolute;
                top: 20px; left: 20px;
                box-shadow: 0 0 15px rgba(240, 147, 251, 0.4);
            "></div>
        </div>
        
        <!-- Animated Message -->
        <div style="
            color: {COLORS['text_primary']};
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            animation: textGlow 2s ease-in-out infinite alternate;
        ">{message}</div>
        
        <!-- Progress Dots -->
        <div class="loading-dots" style="display: flex; justify-content: center; gap: 8px;">
            <div style="
                width: 12px; height: 12px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea, #764ba2);
                animation: dot1 1.5s ease-in-out infinite;
            "></div>
            <div style="
                width: 12px; height: 12px;
                border-radius: 50%;
                background: linear-gradient(135deg, #764ba2, #f093fb);
                animation: dot2 1.5s ease-in-out infinite;
            "></div>
            <div style="
                width: 12px; height: 12px;
                border-radius: 50%;
                background: linear-gradient(135deg, #f093fb, #667eea);
                animation: dot3 1.5s ease-in-out infinite;
            "></div>
        </div>
    </div>
    
    <style>
    @keyframes loadingParticles {{
        0% {{ transform: translate(0, 0) rotate(0deg); }}
        25% {{ transform: translate(-10px, -10px) rotate(90deg); }}
        50% {{ transform: translate(10px, -20px) rotate(180deg); }}
        75% {{ transform: translate(-20px, 10px) rotate(270deg); }}
        100% {{ transform: translate(0, 0) rotate(360deg); }}
    }}
    @keyframes spinnerFloat {{
        0%, 100% {{ transform: translateY(0) rotateX(0deg); }}
        50% {{ transform: translateY(-10px) rotateX(10deg); }}
    }}
    @keyframes spin3D {{
        0% {{ transform: rotate(0deg) rotateY(0deg); }}
        50% {{ transform: rotate(180deg) rotateY(180deg); }}
        100% {{ transform: rotate(360deg) rotateY(360deg); }}
    }}
    @keyframes spin3DReverse {{
        0% {{ transform: rotate(360deg) rotateX(0deg); }}
        50% {{ transform: rotate(180deg) rotateX(180deg); }}
        100% {{ transform: rotate(0deg) rotateX(360deg); }}
    }}
    @keyframes textGlow {{
        from {{ 
            color: {COLORS['text_primary']};
            text-shadow: 0 0 10px rgba(102, 126, 234, 0.3);
        }}
        to {{ 
            color: #667eea;
            text-shadow: 0 0 20px rgba(102, 126, 234, 0.6);
        }}
    }}
    @keyframes dot1 {{
        0%, 80%, 100% {{ opacity: 0.3; transform: scale(1); }}
        40% {{ opacity: 1; transform: scale(1.3); }}
    }}
    @keyframes dot2 {{
        0%, 80%, 100% {{ opacity: 0.3; transform: scale(1); }}
        40% {{ opacity: 1; transform: scale(1.3); }}
    }}
    @keyframes dot3 {{
        0%, 80%, 100% {{ opacity: 0.3; transform: scale(1); }}
        40% {{ opacity: 1; transform: scale(1.3); }}
    }}
    .loading-dots div:nth-child(1) {{ animation-delay: 0s; }}
    .loading-dots div:nth-child(2) {{ animation-delay: 0.2s; }}
    .loading-dots div:nth-child(3) {{ animation-delay: 0.4s; }}
    </style>
    """, unsafe_allow_html=True)

def render_progress_loader(progress: float = 0.0, message: str = "Processing..."):
    """Render advanced 3D progress loader with morphing effects"""
    progress_percent = min(100, max(0, progress * 100))
    
    st.markdown(f"""
    <div class="progress-loader-3d" style="
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border-radius: 25px;
        margin: 2rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: conic-gradient(
                from {progress_percent * 3.6}deg,
                rgba(102, 126, 234, 0.1),
                rgba(118, 75, 162, 0.05),
                transparent 60%
            );
            animation: progressRotate 15s linear infinite;
        "></div>
        
        <div style="
            position: relative;
            z-index: 2;
            color: {COLORS['text_primary']};
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 2rem;
            animation: messageFloat 3s ease-in-out infinite;
        ">{message}</div>
        
        <!-- 3D Progress Ring -->
        <div class="progress-ring" style="
            position: relative;
            width: 120px; height: 120px;
            margin: 0 auto 2rem auto;
            animation: ringFloat 4s ease-in-out infinite;
        ">
            <svg width="120" height="120" style="transform: rotate(-90deg);">
                <!-- Background Ring -->
                <circle cx="60" cy="60" r="50" 
                    fill="none" 
                    stroke="rgba(102, 126, 234, 0.2)" 
                    stroke-width="8"
                    filter="drop-shadow(0 0 10px rgba(102, 126, 234, 0.3))">
                </circle>
                <!-- Progress Ring -->
                <circle cx="60" cy="60" r="50" 
                    fill="none" 
                    stroke="url(#progressGradient)" 
                    stroke-width="8" 
                    stroke-linecap="round"
                    stroke-dasharray="314"
                    stroke-dashoffset="{314 - (314 * progress_percent / 100)}"
                    style="transition: stroke-dashoffset 0.5s ease-in-out;"
                    filter="drop-shadow(0 0 15px rgba(102, 126, 234, 0.6))">
                </circle>
                <defs>
                    <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#667eea"/>
                        <stop offset="50%" style="stop-color:#764ba2"/>
                        <stop offset="100%" style="stop-color:#f093fb"/>
                    </linearGradient>
                </defs>
            </svg>
            
            <!-- Percentage Display -->
            <div style="
                position: absolute;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                font-size: 1.5rem;
                font-weight: 800;
                color: #667eea;
                text-shadow: 0 2px 10px rgba(102, 126, 234, 0.4);
                animation: percentGlow 2s ease-in-out infinite alternate;
            ">{progress_percent:.0f}%</div>
        </div>
        
        <!-- Progress Bar -->
        <div style="
            width: 100%;
            height: 8px;
            background: rgba(102, 126, 234, 0.2);
            border-radius: 10px;
            overflow: hidden;
            box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
        ">
            <div style="
                width: {progress_percent}%;
                height: 100%;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                border-radius: 10px;
                transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 0 20px rgba(102, 126, 234, 0.6);
                animation: progressPulse 2s ease-in-out infinite alternate;
            "></div>
        </div>
    </div>
    
    <style>
    @keyframes progressRotate {{
        0% {{ transform: rotate(0deg); opacity: 0.6; }}
        100% {{ transform: rotate(360deg); opacity: 0.8; }}
    }}
    @keyframes messageFloat {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
    }}
    @keyframes ringFloat {{
        0%, 100% {{ transform: translateY(0) rotateZ(0deg); }}
        50% {{ transform: translateY(-8px) rotateZ(5deg); }}
    }}
    @keyframes percentGlow {{
        from {{ 
            color: #667eea;
            text-shadow: 0 2px 10px rgba(102, 126, 234, 0.4);
        }}
        to {{ 
            color: #764ba2;
            text-shadow: 0 4px 20px rgba(118, 75, 162, 0.6);
        }}
    }}
    @keyframes progressPulse {{
        from {{ box-shadow: 0 0 20px rgba(102, 126, 234, 0.6); }}
        to {{ box-shadow: 0 0 30px rgba(118, 75, 162, 0.8); }}
    }}
    </style>
    """, unsafe_allow_html=True)

def render_animated_chart_container(chart_title: str = "", chart_subtitle: str = ""):
    """Render an enhanced animated chart container with 3D effects"""
    container_id = f"chart_container_{hash(chart_title) % 10000}"
    
    st.markdown(f"""
    <div id="{container_id}" class="animated-chart-container" style="
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        border-radius: 25px;
        padding: 2.5rem 2rem;
        margin: 2rem 0;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.1),
            0 10px 25px rgba(102, 126, 234, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(102, 126, 234, 0.15);
        position: relative;
        overflow: hidden;
        animation: chartContainerEntry 1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        transform-style: preserve-3d;
    ">
        <!-- Animated Background Layers -->
        <div style="
            position: absolute; top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: conic-gradient(
                from 0deg,
                transparent,
                rgba(102, 126, 234, 0.05),
                rgba(118, 75, 162, 0.03),
                transparent 40%
            );
            animation: containerRotate 25s linear infinite;
            z-index: 0;
        "></div>
        
        <div style="
            position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background: 
                radial-gradient(circle at 15% 25%, rgba(102,126,234,0.06) 2px, transparent 2px),
                radial-gradient(circle at 85% 75%, rgba(118,75,162,0.04) 1.5px, transparent 1.5px),
                radial-gradient(circle at 50% 50%, rgba(240,147,251,0.03) 1px, transparent 1px);
            background-size: 80px 80px, 60px 60px, 40px 40px;
            animation: containerParticles 30s linear infinite;
            border-radius: 25px;
            z-index: 1;
        "></div>
        
        <!-- Chart Header -->
        {f'''
        <div class="chart-header" style="
            position: relative; z-index: 3;
            text-align: center;
            margin-bottom: 2rem;
        ">
            <h2 style="
                color: {COLORS['text_primary']};
                font-size: 1.6rem;
                font-weight: 800;
                margin: 0 0 0.5rem 0;
                background: linear-gradient(135deg, {COLORS['text_primary']} 0%, #667eea 100%);
                background-size: 200% 200%;
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                animation: titleShimmer 8s ease-in-out infinite;
            ">{chart_title}</h2>
            {f'<p style="color: {COLORS["text_secondary"]}; font-size: 1rem; margin: 0; animation: subtitleFloat 4s ease-in-out infinite;">{chart_subtitle}</p>' if chart_subtitle else ''}
        </div>
        ''' if chart_title else ''}
        
        <!-- Chart Content Area -->
        <div class="chart-content" style="
            position: relative;
            z-index: 2;
            min-height: 400px;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            padding: 1rem;
            animation: contentSlideIn 0.8s ease-out 0.3s both;
        ">
    """, unsafe_allow_html=True)
    
    # Add the CSS for animations
    st.markdown("""
    <style>
    @keyframes chartContainerEntry {
        0% { 
            opacity: 0; 
            transform: translateY(40px) translateZ(-50px) rotateX(15deg) scale(0.9); 
        }
        100% { 
            opacity: 1; 
            transform: translateY(0) translateZ(0) rotateX(0deg) scale(1); 
        }
    }
    @keyframes containerRotate {
        0% { transform: rotate(0deg) scale(0.8); opacity: 0.6; }
        50% { transform: rotate(180deg) scale(1.2); opacity: 1; }
        100% { transform: rotate(360deg) scale(0.8); opacity: 0.6; }
    }
    @keyframes containerParticles {
        0% { transform: translate(0, 0) rotate(0deg); opacity: 0.7; }
        25% { transform: translate(-15px, -15px) rotate(90deg); opacity: 1; }
        50% { transform: translate(15px, -30px) rotate(180deg); opacity: 0.8; }
        75% { transform: translate(-30px, 15px) rotate(270deg); opacity: 1; }
        100% { transform: translate(0, 0) rotate(360deg); opacity: 0.7; }
    }
    @keyframes titleShimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    @keyframes subtitleFloat {
        0%, 100% { transform: translateY(0); opacity: 0.8; }
        50% { transform: translateY(-3px); opacity: 1; }
    }
    @keyframes contentSlideIn {
        from { 
            opacity: 0; 
            transform: translateY(20px) translateZ(-20px); 
            filter: blur(2px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0) translateZ(0); 
            filter: blur(0); 
        }
    }
    
    .animated-chart-container:hover {
        transform: translateY(-8px) translateZ(30px) rotateX(2deg) scale(1.01);
        box-shadow: 
            0 30px 60px rgba(0, 0, 0, 0.15),
            0 15px 35px rgba(102, 126, 234, 0.12),
            inset 0 1px 0 rgba(255, 255, 255, 0.95),
            0 0 50px rgba(102, 126, 234, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def close_animated_chart_container():
    """Close the animated chart container"""
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    """Render modern navigation pills"""
    if not selected:
        selected = options[0]
    
    pills_html = '<div style="display: flex; gap: 8px; margin-bottom: 2rem; flex-wrap: wrap;">'
    
    for option in options:
        is_active = option == selected
        bg_color = COLORS['primary'] if is_active else 'transparent'
        text_color = 'white' if is_active else COLORS['text_secondary']
        border_color = COLORS['primary'] if is_active else COLORS['border']
        
        pills_html += f'''
        <div style="background: {bg_color}; color: {text_color}; 
                   padding: 8px 16px; border-radius: 20px; 
                   border: 1px solid {border_color};
                   font-size: 0.85rem; font-weight: 500;
                   cursor: pointer; transition: all 0.3s ease;">
            {option}
        </div>
        '''
    
    pills_html += '</div>'
    st.markdown(pills_html, unsafe_allow_html=True)

def render_stats_grid(stats: Dict[str, Any]):
    """Render a responsive stats grid"""
    if not stats:
        return
    
    # Calculate number of columns based on stats count
    num_stats = len(stats)
    if num_stats <= 2:
        cols = st.columns(num_stats)
    elif num_stats <= 4:
        cols = st.columns(2)
    else:
        cols = st.columns(3)
    
    for i, (key, value) in enumerate(stats.items()):
        col_index = i % len(cols)
        
        with cols[col_index]:
            if isinstance(value, dict):
                render_metric_card(
                    title=key.replace('_', ' ').title(),
                    value=str(value.get('value', '0')),
                    icon=value.get('icon', '📊'),
                    color=value.get('color', 'primary'),
                    delta=value.get('delta')
                )
            else:
                render_metric_card(
                    title=key.replace('_', ' ').title(),
                    value=str(value),
                    icon='📊'
                )

def render_mobile_nav(current_page: str, pages: Dict[str, str]):
    """Render mobile-friendly navigation"""
    st.markdown("""
    <style>
    .mobile-nav {
        display: flex;
        gap: 4px;
        margin-bottom: 1rem;
        overflow-x: auto;
        padding: 4px;
        background: rgba(248, 250, 252, 0.8);
        border-radius: 12px;
    }
    
    .nav-item {
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 500;
        white-space: nowrap;
        transition: all 0.3s ease;
        cursor: pointer;
        text-decoration: none;
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .nav-item:not(.active) {
        color: #64748b;
        background: transparent;
    }
    
    .nav-item:hover:not(.active) {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
    }
    </style>
    """, unsafe_allow_html=True)
    
    nav_html = '<div class="mobile-nav">'
    for page_name, page_icon in pages.items():
        is_active = page_name == current_page
        nav_html += f'<div class="nav-item {"active" if is_active else ""}">{page_icon} {page_name}</div>'
    nav_html += '</div>'
    
    st.markdown(nav_html, unsafe_allow_html=True)


def render_dark_sidebar(services, user):
    """Render professional dark mode sidebar with advanced 3D animations and morphing effects"""
    
    # Advanced 3D sidebar CSS
    st.sidebar.markdown("""
    <style>
        /* Advanced 3D Dark Mode Sidebar Styling */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 30%, #0f3460 60%, #1a1a2e 100%);
            background-size: 100% 400%;
            animation: sidebarGradientFlow 20s ease infinite;
            color: #ffffff;
            padding: 0;
            position: relative;
            overflow: hidden;
            transform-style: preserve-3d;
            perspective: 1000px;
        }
        
        .sidebar .sidebar-content::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: 
                radial-gradient(circle at 10% 20%, rgba(102,126,234,0.08) 2px, transparent 2px),
                radial-gradient(circle at 80% 80%, rgba(118,75,162,0.06) 1.5px, transparent 1.5px),
                radial-gradient(circle at 50% 50%, rgba(255,255,255,0.04) 1px, transparent 1px);
            background-size: 60px 60px, 80px 80px, 40px 40px;
            animation: sidebarParticles 30s linear infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes sidebarGradientFlow {
            0%, 100% { background-position: 0% 0%; }
            25% { background-position: 0% 25%; }
            50% { background-position: 0% 50%; }
            75% { background-position: 0% 75%; }
        }
        
        @keyframes sidebarParticles {
            0% { transform: translateY(0) rotate(0deg); opacity: 0.6; }
            50% { transform: translateY(-20px) rotate(180deg); opacity: 1; }
            100% { transform: translateY(0) rotate(360deg); opacity: 0.6; }
        }
        
        /* Enhanced 3D Header */
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            background-size: 200% 200%;
            color: white;
            padding: 2.5rem 1.5rem 2rem 1.5rem;
            margin: -1rem -1rem 0 -1rem;
            border-radius: 0 0 25px 25px;
            text-align: center;
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.4),
                0 8px 20px rgba(102, 126, 234, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            position: relative;
            overflow: hidden;
            animation: 
                headerMove 8s ease-in-out infinite,
                headerGradientShift 12s ease infinite;
            transform-style: preserve-3d;
        }
        
        .sidebar-header::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: conic-gradient(
                from 0deg,
                transparent,
                rgba(255, 255, 255, 0.15),
                rgba(102, 126, 234, 0.2),
                transparent 40%
            );
            animation: headerRotate 15s linear infinite;
            z-index: 1;
        }
        
        .sidebar-header::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(15px);
            z-index: 2;
        }
        
        @keyframes headerMove {
            0%, 100% { transform: translateY(0) rotateX(0deg); }
            50% { transform: translateY(-5px) rotateX(2deg); }
        }
        
        @keyframes headerGradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        @keyframes headerRotate {
            0% { transform: rotate(0deg) scale(0.8); opacity: 0.6; }
            50% { transform: rotate(180deg) scale(1.2); opacity: 1; }
            100% { transform: rotate(360deg) scale(0.8); opacity: 0.6; }
        }
        
        .sidebar-header-content {
            position: relative;
            z-index: 3;
            animation: contentFadeIn 1s ease-out;
        }
        
        @keyframes contentFadeIn {
            from { opacity: 0; transform: translateY(20px) translateZ(-20px); }
            to { opacity: 1; transform: translateY(0) translateZ(0); }
        }
        
        /* Enhanced 3D Logo */
        .sidebar-logo {
            font-size: 2.8rem;
            margin-bottom: 0.5rem;
            text-shadow: 
                0 4px 15px rgba(0, 0, 0, 0.5),
                0 0 30px rgba(102, 126, 234, 0.4);
            animation: 
                logoFloat 4s ease-in-out infinite,
                logoGlow 3s ease-in-out infinite alternate;
            transform-style: preserve-3d;
        }
        
        @keyframes logoFloat {
            0%, 100% { transform: translateY(0) rotateY(0deg) translateZ(0); }
            50% { transform: translateY(-8px) rotateY(5deg) translateZ(10px); }
        }
        
        @keyframes logoGlow {
            from { 
                text-shadow: 0 4px 15px rgba(0, 0, 0, 0.5), 0 0 30px rgba(102, 126, 234, 0.4);
                filter: brightness(1);
            }
            to { 
                text-shadow: 0 6px 25px rgba(0, 0, 0, 0.6), 0 0 50px rgba(118, 75, 162, 0.6);
                filter: brightness(1.2);
            }
        }
        
        /* Enhanced Title */
        .sidebar-title {
            font-size: 1.8rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 0 3px 15px rgba(0, 0, 0, 0.4);
            background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: titleShimmer 6s ease-in-out infinite;
        }
        
        @keyframes titleShimmer {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .sidebar-subtitle {
            font-size: 0.9rem;
            opacity: 0.9;
            margin-top: 0.5rem;
            animation: subtitlePulse 4s ease-in-out infinite alternate;
        }
        
        @keyframes subtitlePulse {
            from { opacity: 0.8; }
            to { opacity: 1; }
        }
        
        /* Enhanced 3D User Profile */
        .user-profile {
            background: linear-gradient(135deg, 
                rgba(255,255,255,0.18) 0%, 
                rgba(255,255,255,0.08) 50%,
                rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255,255,255,0.25);
            padding: 2rem 1.5rem;
            border-radius: 20px;
            margin: 2rem 0.8rem 1.5rem 0.8rem;
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.3),
                0 8px 20px rgba(102, 126, 234, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.4);
            animation: profileFloat 6s ease-in-out infinite;
            transform-style: preserve-3d;
        }
        
        @keyframes profileFloat {
            0%, 100% { transform: translateY(0) rotateX(0deg); }
            50% { transform: translateY(-5px) rotateX(2deg); }
        }
        
        /* Enhanced 3D Avatar */
        .user-avatar {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            background-size: 200% 200%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.8rem;
            margin: 0 auto 1.5rem auto;
            box-shadow: 
                0 10px 25px rgba(0, 0, 0, 0.4),
                0 5px 15px rgba(102, 126, 234, 0.3);
            animation: 
                avatarSpin 10s linear infinite,
                avatarGradient 8s ease infinite,
                avatarFloat 4s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }
        
        .user-avatar::before {
            content: '';
            position: absolute;
            top: -2px; left: -2px; right: -2px; bottom: -2px;
            background: linear-gradient(45deg, 
                transparent, 
                rgba(255, 255, 255, 0.6), 
                transparent);
            border-radius: 50%;
            animation: avatarRing 6s linear infinite;
            z-index: -1;
        }
        
        @keyframes avatarSpin {
            0% { transform: rotateY(0deg); }
            100% { transform: rotateY(360deg); }
        }
        
        @keyframes avatarGradient {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        @keyframes avatarFloat {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-3px) scale(1.05); }
        }
        
        @keyframes avatarRing {
            0% { transform: rotate(0deg); opacity: 0.6; }
            50% { transform: rotate(180deg); opacity: 1; }
            100% { transform: rotate(360deg); opacity: 0.6; }
        }
        
        /* Enhanced User Info */
        .user-name {
            font-weight: 700;
            color: #ffffff;
            text-align: center;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            animation: nameGlow 5s ease-in-out infinite alternate;
        }
        
        @keyframes nameGlow {
            from { text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3); }
            to { text-shadow: 0 4px 20px rgba(102, 126, 234, 0.4); }
        }
        
        .user-role {
            font-size: 0.9rem;
            color: #b3b3ff;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 500;
            animation: roleShine 4s ease-in-out infinite alternate;
        }
        
        @keyframes roleShine {
            from { color: #b3b3ff; }
            to { color: #e0e0ff; }
        }
        
        /* Enhanced Navigation Section */
        .nav-section {
            margin: 2.5rem 0.8rem 2rem 0.8rem;
            animation: sectionSlideIn 1s ease-out 0.5s both;
        }
        
        @keyframes sectionSlideIn {
            from { opacity: 0; transform: translateX(-30px) translateZ(-20px); }
            to { opacity: 1; transform: translateX(0) translateZ(0); }
        }
        
        .nav-section-title {
            color: #a0a0ff;
            font-size: 0.8rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 1.5rem;
            padding-left: 1.5rem;
            position: relative;
            animation: titleGlow 4s ease-in-out infinite alternate;
        }
        
        .nav-section-title::before {
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            width: 4px;
            height: 18px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 3px;
            transform: translateY(-50%);
            animation: accentPulse 3s ease-in-out infinite alternate;
            box-shadow: 0 0 15px rgba(102, 126, 234, 0.4);
        }
        
        @keyframes titleGlow {
            from { color: #a0a0ff; text-shadow: none; }
            to { color: #d0d0ff; text-shadow: 0 0 10px rgba(160, 160, 255, 0.5); }
        }
        
        @keyframes accentPulse {
            from { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                box-shadow: 0 0 15px rgba(102, 126, 234, 0.4);
            }
            to { 
                background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
                box-shadow: 0 0 25px rgba(102, 126, 234, 0.7);
            }
        }
        
        /* Enhanced 3D Navigation Buttons */
        .sidebar .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, 
                rgba(255,255,255,0.08) 0%, 
                rgba(255,255,255,0.03) 50%,
                rgba(255,255,255,0.01) 100%);
            backdrop-filter: blur(15px) saturate(180%);
            border: 1px solid rgba(255,255,255,0.15);
            color: #ffffff;
            text-align: left;
            padding: 1.2rem 1.8rem;
            margin: 0.7rem 0;
            border-radius: 15px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            font-weight: 600;
            font-size: 0.95rem;
            position: relative;
            overflow: hidden;
            box-shadow: 
                0 8px 20px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transform-style: preserve-3d;
            animation: buttonFloat 6s ease-in-out infinite;
        }
        
        .sidebar .stButton > button::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(135deg, 
                rgba(102, 126, 234, 0.3) 0%, 
                rgba(118, 75, 162, 0.3) 50%,
                rgba(240, 147, 251, 0.3) 100%);
            transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 0;
        }
        
        .sidebar .stButton > button::after {
            content: '';
            position: absolute;
            top: -2px; left: -2px; right: -2px; bottom: -2px;
            background: linear-gradient(45deg, 
                transparent,
                rgba(255, 255, 255, 0.3),
                transparent 30%);
            border-radius: 17px;
            animation: buttonShimmer 8s linear infinite;
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: -1;
        }
        
        @keyframes buttonFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-2px); }
        }
        
        @keyframes buttonShimmer {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(100%) rotate(45deg); }
        }
        
        .sidebar .stButton > button:hover {
            background: linear-gradient(135deg, 
                rgba(102, 126, 234, 0.25) 0%, 
                rgba(118, 75, 162, 0.25) 50%,
                rgba(240, 147, 251, 0.25) 100%);
            border-color: rgba(102, 126, 234, 0.5);
            transform: translateX(8px) translateZ(15px) rotateY(5deg);
            box-shadow: 
                0 15px 35px rgba(102, 126, 234, 0.4),
                0 8px 20px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            color: #ffffff;
        }
        
        .sidebar .stButton > button:hover::before {
            left: 0;
        }
        
        .sidebar .stButton > button:hover::after {
            opacity: 1;
        }
        
        .sidebar .stButton > button:active {
            transform: translateX(4px) translateZ(8px) rotateY(2deg) scale(0.98);
        }
        
        /* Enhanced Stats Section */
        .quick-stats {
            background: linear-gradient(135deg, 
                rgba(255,255,255,0.12) 0%, 
                rgba(255,255,255,0.06) 50%,
                rgba(255,255,255,0.04) 100%);
            backdrop-filter: blur(20px) saturate(200%);
            border: 1px solid rgba(255,255,255,0.2);
            padding: 2rem 1.5rem;
            border-radius: 20px;
            margin: 2rem 0.8rem;
            box-shadow: 
                0 15px 35px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            animation: statsFloat 8s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }
        
        .quick-stats::before {
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: radial-gradient(circle at center, 
                rgba(102, 126, 234, 0.1) 0%, 
                transparent 50%);
            animation: statsGlow 12s linear infinite;
            z-index: 0;
        }
        
        @keyframes statsFloat {
            0%, 100% { transform: translateY(0) rotateX(0deg); }
            50% { transform: translateY(-3px) rotateX(1deg); }
        }
        
        @keyframes statsGlow {
            0% { transform: rotate(0deg) scale(0.8); opacity: 0.4; }
            50% { transform: rotate(180deg) scale(1.2); opacity: 0.8; }
            100% { transform: rotate(360deg) scale(0.8); opacity: 0.4; }
        }
        
        /* Enhanced Stat Items */
        .stat-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 1rem 0;
            padding: 0.8rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.15);
            position: relative;
            z-index: 1;
            transition: all 0.3s ease;
        }
        
        .stat-item:hover {
            padding-left: 10px;
            transform: translateX(5px);
            border-bottom-color: rgba(102, 126, 234, 0.4);
        }
        
        .stat-item:last-child {
            border-bottom: none;
        }
        
        .stat-label {
            color: #c0c0ff;
            font-size: 0.9rem;
            font-weight: 500;
            animation: labelGlow 5s ease-in-out infinite alternate;
        }
        
        @keyframes labelGlow {
            from { color: #c0c0ff; }
            to { color: #e0e0ff; }
        }
        
        .stat-value {
            color: #ffffff;
            font-weight: 700;
            font-size: 1rem;
            text-shadow: 0 2px 8px rgba(255, 255, 255, 0.2);
            animation: valueFloat 4s ease-in-out infinite;
        }
        
        @keyframes valueFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-1px); }
        }
        
        /* Enhanced Logout Section */
        .logout-section {
            margin: 2.5rem 0.8rem 1.5rem 0.8rem;
            animation: logoutSlideUp 1s ease-out 0.8s both;
        }
        
        @keyframes logoutSlideUp {
            from { opacity: 0; transform: translateY(30px) translateZ(-20px); }
            to { opacity: 1; transform: translateY(0) translateZ(0); }
        }
        
        .logout-btn {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 50%, #b91c1c 100%) !important;
            background-size: 200% 200% !important;
            border: 1px solid #dc2626 !important;
            color: white !important;
            box-shadow: 
                0 10px 25px rgba(239, 68, 68, 0.5),
                0 5px 15px rgba(220, 38, 38, 0.3) !important;
            position: relative !important;
            overflow: hidden !important;
            animation: logoutPulse 6s ease-in-out infinite !important;
        }
        
        .logout-btn::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
            background: linear-gradient(45deg, 
                transparent,
                rgba(255, 255, 255, 0.2),
                transparent) !important;
            transform: translateX(-100%) !important;
            transition: transform 0.4s ease !important;
        }
        
        @keyframes logoutPulse {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .logout-btn:hover {
            transform: translateY(-3px) translateZ(10px) scale(1.02) !important;
            box-shadow: 
                0 15px 40px rgba(239, 68, 68, 0.7),
                0 8px 25px rgba(220, 38, 38, 0.5) !important;
        }
        
        .logout-btn:hover::before {
            transform: translateX(100%) !important;
        }
        
        /* Enhanced Custom Scrollbar */
        .sidebar .sidebar-content::-webkit-scrollbar {
            width: 8px;
        }
        
        .sidebar .sidebar-content::-webkit-scrollbar-track {
            background: linear-gradient(180deg, 
                rgba(255,255,255,0.1) 0%, 
                rgba(255,255,255,0.05) 100%);
            border-radius: 4px;
        }
        
        .sidebar .sidebar-content::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
            box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
            animation: scrollThumbGlow 4s ease-in-out infinite alternate;
        }
        
        @keyframes scrollThumbGlow {
            from { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
            }
            to { 
                background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
                box-shadow: 0 0 20px rgba(102, 126, 234, 0.8);
            }
        }
        
        .sidebar .sidebar-content::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
            box-shadow: 0 0 25px rgba(102, 126, 234, 0.9);
        }
            border-radius: 3px;
        }
        
        .sidebar .sidebar-content::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar Header
    st.sidebar.markdown(f"""
    <div class="sidebar-header">
        <div class="sidebar-header-content">
            <div class="sidebar-logo">🚀</div>
            <div class="sidebar-title">IMIQ</div>
            <div class="sidebar-subtitle">Intelligent Management Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # User Profile Section
    st.sidebar.markdown(f"""
    <div class="user-profile">
        <div class="user-avatar">👤</div>
        <div class="user-name">{user.get('name', 'User')}</div>
        <div class="user-role">{user.get('role', 'user')} user</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = 'Dashboard'
    
    # Main Navigation - Role-based visibility
    user_role = user.get('role', '').lower()
    
    if user_role == 'admin':
        # Admin sees all navigation items
        st.sidebar.markdown('<div class="nav-section-title">📋 Core Operations</div>', unsafe_allow_html=True)
        
        main_nav_items = [
            ('Dashboard', '📊', 'Overview and key metrics'),
            ('Orders', '📦', 'Manage customer orders'),
            ('Inventory', '📋', 'Product stock management'),
            ('Reports', '📈', 'Business analytics & reports'),
        ]
        
        for page, icon, desc in main_nav_items:
            if st.sidebar.button(f"{icon} {page}", key=f"main_nav_{page}", help=desc):
                st.session_state.selected_page = page
                st.rerun()
    else:
        # Regular users see limited navigation
        st.sidebar.markdown('<div class="nav-section-title">📋 Available Options</div>', unsafe_allow_html=True)
        
        user_nav_items = [
            ('Dashboard', '📊', 'Your orders overview'),
            ('Orders', '📦', 'Your orders only'),
        ]
        
        for page, icon, desc in user_nav_items:
            if st.sidebar.button(f"{icon} {page}", key=f"user_nav_{page}", help=desc):
                st.session_state.selected_page = page
                st.rerun()

    # Admin Navigation (if admin user)
    if user.get('role', '').lower() == 'admin':
        st.sidebar.markdown('<div class="nav-section-title">⚙️ Administration</div>', unsafe_allow_html=True)
        
        admin_nav_items = [
            ('Business Analytics', '📊', 'Advanced business intelligence & KPIs'),
            ('Shipments', '🚚', 'Shipping & logistics management'),
            ('Performance', '📈', 'Team performance metrics'),
            ('Settings', '⚙️', 'System configuration'),
        ]
        
        for page, icon, desc in admin_nav_items:
            if st.sidebar.button(f"{icon} {page}", key=f"admin_nav_{page}", help=desc):
                st.session_state.selected_page = page
                st.rerun()
    
    # Quick Actions
    st.sidebar.markdown('<div class="nav-section-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
    
    quick_col1, quick_col2 = st.sidebar.columns(2)
    with quick_col1:
        if st.button("➕ Order", key="quick_new_order", help="Create new order"):
            st.session_state.selected_page = 'Orders'
            st.session_state.show_new_order = True
            st.rerun()
    
    with quick_col2:
        if st.button("📋 Stock", key="quick_stock_check", help="Check inventory"):
            st.session_state.selected_page = 'Inventory'
            st.rerun()
    
    # System Statistics (for admin)
    if user.get('role', '').lower() == 'admin':
        try:
            orders_df = services['orders'].get_all_orders()
            inventory_df = services['inventory'].get_all_inventory()
            
            total_orders = len(orders_df) if not orders_df.empty else 0
            total_products = len(inventory_df) if not inventory_df.empty else 0
            low_stock = len(services['inventory'].get_low_stock_alerts()) if not inventory_df.empty else 0
            
            # Calculate today's orders
            today_orders = 0
            if not orders_df.empty and 'timestamp' in orders_df.columns:
                today = pd.Timestamp.now().date()
                orders_df['order_date'] = pd.to_datetime(orders_df['timestamp']).dt.date
                today_orders = len(orders_df[orders_df['order_date'] == today])
            
            st.sidebar.markdown("""
            <div class="nav-section-title">📊 System Overview</div>
            <div class="quick-stats">
                <div class="stat-item">
                    <span class="stat-label">Today's Orders:</span>
                    <span class="stat-value">""" + str(today_orders) + """</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Total Orders:</span>
                    <span class="stat-value">""" + str(total_orders) + """</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Products:</span>
                    <span class="stat-value">""" + str(total_products) + """</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Low Stock:</span>
                    <span class="stat-value" style="color: """ + ('#ef4444' if low_stock > 0 else '#10b981') + """;">""" + str(low_stock) + """</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.sidebar.error("⚠️ Stats unavailable")
    
    # Admin Settings Section - Only for admin users
    if user.get('role', '').lower() == 'admin':
        st.sidebar.markdown('<div class="nav-section-title">⚙️ Admin Settings</div>', unsafe_allow_html=True)
        
        # Admin revenue visibility toggle
        admin_mode = st.sidebar.toggle(
            "💰 Show Revenue Metrics",
            value=st.session_state.get('admin_mode', True),
            key="admin_mode_toggle",
            help="Toggle to show/hide revenue and amount related metrics throughout the application"
        )
        
        # Store admin mode in session state
        st.session_state['admin_mode'] = admin_mode
        
        if admin_mode:
            st.sidebar.success("✅ Revenue Visible")
        else:
            st.sidebar.info("🔒 Revenue Hidden")
    else:
        # For regular users, always hide revenue metrics
        st.session_state['admin_mode'] = False
    
    # Logout Section
    st.sidebar.markdown('<div class="nav-section-title">🔐 Session</div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Logout", key="logout_btn", help="Sign out securely"):
        logout()
        st.rerun()


def render_horizontal_menu_bar(services, user):
    """Render professional horizontal menu bar with organized sections"""
    
    # Menu bar CSS
    st.markdown("""
    <style>
        .menu-bar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 0;
            margin: -1rem -1rem 2rem -1rem;
            border-radius: 0 0 15px 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .menu-bar::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .menu-container {
            position: relative;
            z-index: 2;
            padding: 1rem 2rem;
        }
        
        .menu-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        
        .menu-title {
            color: white;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .user-info {
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .menu-sections {
            display: flex;
            flex-wrap: wrap;
            gap: 2rem;
            align-items: center;
        }
        
        .menu-section {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }
        
        .section-title {
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.25rem;
        }
        
        .menu-items {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }
        
        .menu-item {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: pointer;
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        
        .menu-item:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .menu-item.active {
            background: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.4);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        
        .quick-actions {
            display: flex;
            gap: 0.75rem;
            margin-left: auto;
        }
        
        .action-btn {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-size: 0.8rem;
            font-weight: 600;
            transition: all 0.3s ease;
            cursor: pointer;
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .action-btn:hover {
            background: rgba(255, 255, 255, 0.25);
            transform: scale(1.05);
        }
        
        @media (max-width: 768px) {
            .menu-container {
                padding: 1rem;
            }
            
            .menu-header {
                flex-direction: column;
                gap: 0.5rem;
                text-align: center;
            }
            
            .menu-sections {
                justify-content: center;
                gap: 1rem;
            }
            
            .menu-section {
                min-width: auto;
            }
            
            .quick-actions {
                margin-left: 0;
                justify-content: center;
                margin-top: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = 'Dashboard'
    
    current_page = st.session_state.get('selected_page', 'Dashboard')
    
    # Menu bar HTML
    menu_html = f"""
    <div class="menu-bar">
        <div class="menu-container">
            <div class="menu-header">
                <div class="menu-title">
                    🚀 IMIQ Platform
                </div>
                <div class="user-info">
                    👤 {user.get('name', 'User')} ({user.get('role', 'user').title()})
                </div>
            </div>
            
            <div class="menu-sections">
                <div class="menu-section">
                    <div class="section-title">📊 Business Analytics</div>
                    <div class="menu-items">
                        <div class="menu-item {'active' if current_page == 'Dashboard' else ''}" onclick="selectPage('Dashboard')">
                            📊 Dashboard
                        </div>
                        <div class="menu-item {'active' if current_page == 'Reports' else ''}" onclick="selectPage('Reports')">
                            📈 Reports
                        </div>
    """
    
    # Add Analytics for admin users
    if user.get('role', '').lower() == 'admin':
        menu_html += f"""
                        <div class="menu-item {'active' if current_page == 'Business Analytics' else ''}" onclick="selectPage('Business Analytics')">
                            📊 Business Analytics
                        </div>
        """
    
    menu_html += """
                    </div>
                </div>
                
                <div class="menu-section">
                    <div class="section-title">🛒 Operations</div>
                    <div class="menu-items">
    """
    
    menu_html += f"""
                        <div class="menu-item {'active' if current_page == 'Orders' else ''}" onclick="selectPage('Orders')">
                            📦 Orders
                        </div>
                        <div class="menu-item {'active' if current_page == 'Inventory' else ''}" onclick="selectPage('Inventory')">
                            📋 Inventory
                        </div>
    """
    
    # Add admin operations
    if user.get('role', '').lower() == 'admin':
        menu_html += f"""
                        <div class="menu-item {'active' if current_page == 'Shipments' else ''}" onclick="selectPage('Shipments')">
                            🚚 Shipments
                        </div>
        """
    
    menu_html += """
                    </div>
                </div>
    """
    
    # Add admin section
    if user.get('role', '').lower() == 'admin':
        menu_html += f"""
                <div class="menu-section">
                    <div class="section-title">⚙️ Management</div>
                    <div class="menu-items">
                        <div class="menu-item {'active' if current_page == 'Performance' else ''}" onclick="selectPage('Performance')">
                            📈 Performance
                        </div>
                        <div class="menu-item {'active' if current_page == 'Settings' else ''}" onclick="selectPage('Settings')">
                            ⚙️ Settings
                        </div>
                    </div>
                </div>
        """
    
    # Quick actions
    menu_html += """
                <div class="quick-actions">
                    <div class="action-btn" onclick="quickAction('new_order')">
                        ➕ New Order
                    </div>
                    <div class="action-btn" onclick="quickAction('stock_check')">
                        📋 Stock Check
                    </div>
                    <div class="action-btn" onclick="logout()">
                        🚪 Logout
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function selectPage(page) {
            window.parent.postMessage({type: 'selectPage', page: page}, '*');
        }
        
        function quickAction(action) {
            window.parent.postMessage({type: 'quickAction', action: action}, '*');
        }
        
        function logout() {
            window.parent.postMessage({type: 'logout'}, '*');
        }
    </script>
    """
    
    st.markdown(menu_html, unsafe_allow_html=True)
    
    # Handle menu interactions with columns for better UX
    st.markdown("### 🎛️ Navigation")
    
    # Create interactive navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    nav_items = [
        ('Dashboard', '📊', col1),
        ('Orders', '📦', col2), 
        ('Inventory', '📋', col3),
        ('Reports', '📈', col4)
    ]
    
    # Add admin items if admin user
    admin_items = []
    if user.get('role', '').lower() == 'admin':
        admin_items = [
            ('Business Analytics', '📊'),
            ('Shipments', '🚚'),
            ('Performance', '📈'),
            ('Settings', '⚙️')
        ]
    
    # Main navigation buttons
    for page, icon, col in nav_items:
        with col:
            if st.button(f"{icon} {page}", key=f"nav_btn_{page}", width='stretch'):
                st.session_state.selected_page = page
                st.rerun()
    
    # Admin navigation section
    if admin_items:
        st.markdown("### ⚙️ Admin Tools")
        admin_cols = st.columns(len(admin_items))
        
        for i, (page, icon) in enumerate(admin_items):
            with admin_cols[i]:
                if st.button(f"{icon} {page}", key=f"admin_btn_{page}", width='stretch'):
                    st.session_state.selected_page = page
                    st.rerun()
    
    # Quick Actions section
    st.markdown("### ⚡ Quick Actions")
    quick_col1, quick_col2, quick_col3 = st.columns(3)
    
    with quick_col1:
        if st.button("➕ New Order", key="quick_new_order", width='stretch'):
            st.session_state.selected_page = 'Orders'
            st.session_state.show_new_order = True
            st.rerun()
    
    with quick_col2:
        if st.button("📋 Stock Check", key="quick_stock_check", width='stretch'):
            st.session_state.selected_page = 'Inventory'
            st.rerun()
    
    with quick_col3:
        if st.button("🚪 Logout", key="quick_logout", width='stretch'):
            logout()
            st.rerun()


def render_enhanced_sidebar(services, user):
    """Render enhanced sidebar with modern navigation and user info"""
    
    # Custom CSS for enhanced sidebar
    st.sidebar.markdown("""
    <style>
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem 1rem;
            margin: -1rem -1rem 2rem -1rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .sidebar-user-info {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .nav-section-title {
            color: #64748b;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin: 1.5rem 0 0.5rem 0;
            padding-left: 0.5rem;
        }
        
        .sidebar .stButton > button {
            width: 100%;
            border: none;
            background: transparent;
            text-align: left;
            padding: 0.75rem 1rem;
            margin: 0.25rem 0;
            border-radius: 8px;
            transition: all 0.3s ease;
            color: #475569;
            font-weight: 500;
        }
        
        .sidebar .stButton > button:hover {
            background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
            color: #667eea;
            transform: translateX(4px);
        }
        
        .logout-btn {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
            color: white !important;
            margin-top: 2rem !important;
        }
        
        .logout-btn:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
        }
        
        .system-stats {
            background: rgba(255,255,255,0.05);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .stat-row {
            display: flex;
            justify-content: space-between;
            margin: 0.5rem 0;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar Header
    st.sidebar.markdown(f"""
    <div class="sidebar-header">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">🚀</div>
        <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.25rem;">IMIQ</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">Intelligent Management</div>
    </div>
    """, unsafe_allow_html=True)
    
    # User Info Section
    st.sidebar.markdown(f"""
    <div class="sidebar-user-info">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; margin-right: 0.75rem;">
                👤
            </div>
            <div>
                <div style="font-weight: 600; color: white;">{user.get('name', 'User')}</div>
                <div style="font-size: 0.8rem; opacity: 0.8;">{user.get('role', 'user').title()}</div>
            </div>
        </div>
        <div style="font-size: 0.75rem; opacity: 0.7; word-break: break-all;">{user.get('email', '')}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for selected page
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = 'Dashboard'
    
    # Main Navigation
    st.sidebar.markdown('<div class="nav-section-title">📋 MAIN MENU</div>', unsafe_allow_html=True)
    
    nav_items = [
        ('Dashboard', '📊', 'Dashboard overview and key metrics'),
        ('Orders', '📦', 'Manage and track orders'),
        ('Inventory', '📋', 'Product inventory management'),
        ('Reports', '📈', 'Generate business reports'),
    ]
    
    for page, icon, desc in nav_items:
        if st.sidebar.button(f"{icon} {page}", key=f"nav_{page}", help=desc):
            st.session_state.selected_page = page
            st.rerun()
    
    # Admin-only sections
    if user.get('role', '').lower() == 'admin':
        st.sidebar.markdown('<div class="nav-section-title">⚙️ ADMIN TOOLS</div>', unsafe_allow_html=True)
        
        admin_items = [
            ('Business Analytics', '📊', 'Advanced business analytics'),
            ('Shipments', '🚚', 'Shipping and logistics'),
            ('Performance', '📈', 'Team and business performance'),
            ('Settings', '⚙️', 'System configuration'),
        ]
        
        for page, icon, desc in admin_items:
            if st.sidebar.button(f"{icon} {page}", key=f"admin_{page}", help=desc):
                st.session_state.selected_page = page
                st.rerun()
    
    # Quick Actions
    st.sidebar.markdown('<div class="nav-section-title">⚡ QUICK ACTIONS</div>', unsafe_allow_html=True)
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("➕ New", key="quick_order", help="Create a new order"):
            st.session_state.selected_page = 'Orders'
            st.session_state.show_new_order = True
            st.rerun()
    
    with col2:
        if st.button("📋 Stock", key="quick_stock", help="Check inventory levels"):
            st.session_state.selected_page = 'Inventory'
            st.rerun()
    
    # System Stats (for admin)
    if user.get('role', '').lower() == 'admin':
        st.sidebar.markdown('<div class="nav-section-title">📊 SYSTEM STATUS</div>', unsafe_allow_html=True)
        
        try:
            # Get system stats
            orders_df = services['orders'].get_all_orders()
            inventory_df = services['inventory'].get_all_inventory()
            
            total_orders = len(orders_df) if not orders_df.empty else 0
            total_products = len(inventory_df) if not inventory_df.empty else 0
            low_stock = len(services['inventory'].get_low_stock_alerts()) if not inventory_df.empty else 0
            
            st.sidebar.markdown(f"""
            <div class="system-stats">
                <div class="stat-row">
                    <span style="color: #64748b;">Orders:</span>
                    <span style="color: #10b981; font-weight: 600;">{total_orders}</span>
                </div>
                <div class="stat-row">
                    <span style="color: #64748b;">Products:</span>
                    <span style="color: #3b82f6; font-weight: 600;">{total_products}</span>
                </div>
                <div class="stat-row">
                    <span style="color: #64748b;">Low Stock:</span>
                    <span style="color: {'#ef4444' if low_stock > 0 else '#10b981'}; font-weight: 600;">{low_stock}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.sidebar.error("⚠️ Stats unavailable")
    
    st.sidebar.markdown("---")
    
    # Logout button
    if st.sidebar.button("🚪 Logout", key="logout_btn", help="Sign out of your account"):
        logout()
        st.rerun()


def render_date_filters(key_prefix="date_filter"):
    """Render enhanced date filter with Today default and apply button control"""
    from datetime import datetime, timedelta
    import streamlit as st
    import pandas as pd
    
    # Initialize session state for default Today filter
    if f"{key_prefix}_initialized" not in st.session_state:
        st.session_state[f"{key_prefix}_initialized"] = True
        st.session_state[f"{key_prefix}_default_applied"] = False
    
    # Date filter options
    filter_options = {
        "Today": "📅 Today",
        "Yesterday": "📅 Yesterday", 
        "Last 3 days": "📅 Last 3 days",
        "Last 7 days": "📅 Last 7 days",
        "Last 30 days": "📅 Last 30 days",
        "Last month": "📅 Last month",
        "Custom range": "📅 Custom range"
    }
    
    # Enhanced date filter UI
    st.markdown("""
    <div class="date-filter-container" style="
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    ">
    <div style="font-weight: 600; color: #374151; margin-bottom: 1.5rem; display: flex; align-items: center; font-size: 1.1rem;">
        <span style="margin-right: 0.75rem;">🗓️</span>
        Date Filters
    </div>
    """, unsafe_allow_html=True)
    
    # Better column layout - put Apply button next to dropdown
    col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1])
    
    with col1:
        selected_filter = st.selectbox(
            "Select time period:",
            options=list(filter_options.keys()),
            format_func=lambda x: filter_options[x],
            key=f"{key_prefix}_select",
            index=0  # Default to "Today"
        )
    
    # Compact Apply Filter button - aligned with dropdown
    with col2:
        st.markdown("<div style='margin-top: 1.9rem;'></div>", unsafe_allow_html=True)  # Align with dropdown
        apply_filter = st.button(
            "🔍 Apply Filter",
            key=f"{key_prefix}_apply",
            width='stretch',
            type="primary"
        )
    
    # Calculate date ranges
    today = datetime.now().date()
    start_date = end_date = None
    
    if selected_filter == "Today":
        start_date = end_date = today
    elif selected_filter == "Yesterday":
        start_date = end_date = today - timedelta(days=1)
    elif selected_filter == "Last 3 days":
        start_date = today - timedelta(days=2)
        end_date = today
    elif selected_filter == "Last 7 days":
        start_date = today - timedelta(days=6)
        end_date = today
    elif selected_filter == "Last 30 days":
        start_date = today - timedelta(days=29)
        end_date = today
    elif selected_filter == "Last month":
        if today.month == 1:
            last_month = today.replace(year=today.year-1, month=12, day=1)
            last_day = today.replace(year=today.year-1, month=12, day=31)
        else:
            last_month = today.replace(month=today.month-1, day=1)
            import calendar
            last_day = today.replace(month=today.month-1, 
                                   day=calendar.monthrange(today.year, today.month-1)[1])
        start_date = last_month
        end_date = last_day
    elif selected_filter == "Custom range":
        with col3:
            start_date = st.date_input("Start Date:", value=today - timedelta(days=7), key=f"{key_prefix}_start")
        with col4:
            end_date = st.date_input("End Date:", value=today, key=f"{key_prefix}_end")
    else:
        # Show current date range
        with col3:
            st.markdown(f"**From:** {start_date}")
        with col4:
            st.markdown(f"**To:** {end_date}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Default load Today's orders on first visit or when Today is selected
    if (not st.session_state[f"{key_prefix}_default_applied"] and selected_filter == "Today") or (selected_filter == "Today" and not apply_filter):
        st.session_state[f"{key_prefix}_default_applied"] = True
        return start_date, end_date, selected_filter
    
    # Only apply filter when button is clicked for non-Today filters
    if apply_filter or selected_filter == "Today":
        return start_date, end_date, selected_filter
    
    # For other filters, return the calculated dates but indicate no filtering applied yet
    return start_date, end_date, selected_filter


def filter_dataframe_by_date(df, start_date, end_date, date_column='timestamp'):
    """Filter dataframe by date range with enhanced timezone handling"""
    import pandas as pd
    from datetime import datetime
    import pytz
    
    if df.empty or start_date is None or end_date is None:
        return df
    
    try:
        # Auto-detect date columns if primary doesn't exist
        possible_date_columns = ['timestamp', 'date', 'order_date', 'created_at', 'Date', 'Order Date']
        actual_date_column = None
        
        # First try the specified column
        if date_column in df.columns:
            actual_date_column = date_column
        else:
            # Try to find alternative date columns
            for col in possible_date_columns:
                if col in df.columns:
                    actual_date_column = col
                    break
        
        # If no date column found, return original dataframe
        if actual_date_column is None:
            st.warning(f"No date column found. Available columns: {list(df.columns)}")
            return df
        
        # Convert dates to datetime if they aren't already - with UTC handling
        if not pd.api.types.is_datetime64_any_dtype(df[actual_date_column]):
            df[actual_date_column] = pd.to_datetime(df[actual_date_column], errors='coerce', utc=True)
        
        # Ensure consistent timezone handling
        if df[actual_date_column].dt.tz is None:
            # If no timezone, assume UTC
            df[actual_date_column] = df[actual_date_column].dt.tz_localize('UTC')
        
        # Convert filter dates to timezone-aware datetime objects matching data timezone
        data_tz = df[actual_date_column].dt.tz if df[actual_date_column].dt.tz else pytz.UTC
        
        # Convert filter dates
        start_datetime = pd.to_datetime(start_date)
        end_datetime = pd.to_datetime(end_date) + pd.Timedelta(hours=23, minutes=59, seconds=59)
        
        # Make them timezone-aware to match data
        if start_datetime.tz is None:
            start_datetime = start_datetime.tz_localize(data_tz)
        if end_datetime.tz is None:
            end_datetime = end_datetime.tz_localize(data_tz)
        
        # Filter dataframe
        mask = (df[actual_date_column] >= start_datetime) & (df[actual_date_column] <= end_datetime)
        filtered_df = df[mask]
        
        # Debug info
        if len(filtered_df) == 0:
            st.info(f"No records found for {start_date} to {end_date} in column '{actual_date_column}'. Total records: {len(df)}")
        else:
            st.success(f"Found {len(filtered_df)} records for {start_date} to {end_date}")
        
        return filtered_df
        
    except Exception as e:
        st.error(f"Date filtering error: {e}")
        return df


def logout():
    """Handle user logout"""
    # Clear all session state
    keys_to_clear = ['authenticated', 'user', 'selected_page', 'show_new_order']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    
    # Clear session persistence parameters
    params_to_clear = ['session', 'user_email']
    for param in params_to_clear:
        if param in st.query_params:
            del st.query_params[param]