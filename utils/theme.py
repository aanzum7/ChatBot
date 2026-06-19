import streamlit as st

CONFIG = {
    "bg_color": "#0D0F12",          # Ultra dark premium backdrop
    "card_bg": "#161920",           # Sleek surface contrast color
    "border_color": "#262B36",      # Soft structure dividers
    "text_color": "#F3F4F6",        # Crisp off-white text
    "header_olive": "#88B04B",      # Vibrant organic mehendi green
    "accent_rose_gold": "#D4AF37",  # Premium metallic gold 
    "hover_glow": "#E5C158",        # Active interaction state
    "user_msg_bg": "#1F3520",       # Dark olive chat bubble
    "bot_msg_bg": "#231E16"         # Warm amber chat bubble
}

def inject_global_theme(page_title: str, page_icon: str):
    st.set_page_config(
        page_title=f"{page_title} | Rafiya's Henna",
        page_icon=page_icon,
        layout="wide"
    )
    
    st.markdown(f"""
    <style>
        /* Document Canvas Base Styling */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {{
            background-color: {CONFIG['bg_color']} !important;
            color: {CONFIG['text_color']} !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        
        h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] h1 {{
            color: {CONFIG['text_color']} !important;
            font-weight: 700 !important;
            letter-spacing: -0.025em;
        }}

        /* Premium Social Media Gradient Buttons */
        .stButton>button {{
            background: linear-gradient(135deg, {CONFIG['accent_rose_gold']}, #AA7C11) !important;
            color: #0D0F12 !important;
            border-radius: 25px !important;
            border: none !important;
            padding: 12px 24px !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2) !important;
        }}
        .stButton>button:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
            color: #0D0F12 !important;
        }}
        
        /* Dropdowns & Selection Fields */
        div[data-baseweb="select"] > div {{
            border: 1px solid {CONFIG['border_color']} !important;
            border-radius: 12px !important;
            background-color: {CONFIG['card_bg']} !important;
            color: {CONFIG['text_color']} !important;
        }}

        /* Native Streamlit Expander Remodelling */
        [data-testid="stExpander"] {{
            background-color: {CONFIG['card_bg']} !important;
            border: 1px solid {CONFIG['border_color']} !important;
            border-radius: 14px !important;
            overflow: hidden;
            margin-bottom: 12px !important;
        }}
    </style>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: str):
    st.markdown(f"""
        <div style="text-align:center; padding: 20px 0;">
            <h1 style="font-size: 2.8rem; margin-bottom: 6px; background: linear-gradient(to right, #FFFFFF, {CONFIG['accent_rose_gold']}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {title}
            </h1>
            <p style="color: #9CA3AF; font-size:16px; letter-spacing: 0.02em;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
