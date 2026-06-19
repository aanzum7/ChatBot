import streamlit as st

# Central Configuration Context
CONFIG = {
    "bg_color": "#f9f7f1",
    "text_color": "#3b3a36",
    "header_color": "#6b8e23",
    "accent_gold": "#b8860b",
    "hover_gold": "#a07400",
    "user_bg": "#e6f2e1",
    "user_border": "#6b8e23",
    "user_text": "#2f4f2f",
    "bot_bg": "#fdf5e6",
    "bot_border": "#b8860b",
    "bot_text": "#5b4636",
    "card_bg": "#ffffff",
    "card_shadow": "rgba(0,0,0,0.06)"
}

def inject_global_theme(page_title: str, page_icon: str):
    """Sets configuration headers and injects clean semantic markup styles."""
    st.set_page_config(
        page_title=f"{page_title} - Rafiya’s Henna Art",
        page_icon=page_icon,
        layout="wide"
    )
    
    st.markdown(f"""
    <style>
        /* Document Canvas Reset */
        .stApp, [data-testid="stAppViewContainer"] {{
            background-color: {CONFIG['bg_color']};
            color: {CONFIG['text_color']};
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }}
        
        h1, h2, h3, h4, h5, h6, [data-testid="stMarkdownContainer"] h1 {{
            color: {CONFIG['header_color']} !important;
        }}
        
        /* Unified Button Interface */
        .stButton>button {{
            background-color: {CONFIG['accent_gold']} !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 10px 20px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out !important;
        }}
        .stButton>button:hover {{
            background-color: {CONFIG['hover_gold']} !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.12) !important;
            transform: translateY(-1px);
        }}
        
        /* Interactive Input Overrides */
        div[data-baseweb="select"] > div {{
            border: 2px solid {CONFIG['accent_gold']} !important;
            border-radius: 8px !important;
            background-color: white !important;
        }}
        
        .stSlider [role="slider"] {{
            background-color: {CONFIG['accent_gold']} !important;
        }}
        .stSlider [data-baseweb="slider"] > div > div {{
            background: linear-gradient(to right, {CONFIG['accent_gold']}, {CONFIG['hover_gold']}) !important;
        }}
    </style>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: str):
    """Displays localized banner identities."""
    st.markdown(f"""
        <div style="text-align:center; padding: 12px 0;">
            <h1 style="margin-bottom: 2px;">🌿 {title} 🌿</h1>
            <p style="color:{CONFIG['header_color']}; font-style:italic; font-size:16px; margin-top:0;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
