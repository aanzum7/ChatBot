from __future__ import annotations

import streamlit as st

def inject_styles():
    """Injects the high-polish luxury atelier CSS design system."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Marcellus&family=Montserrat:wght@300;400;500;600;700&display=swap');

            /* Global Canvas */
            .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
                background: radial-gradient(circle at top right, #161A24, #0A0D14) !important;
                color: #E2E8F0 !important;
                font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif !important;
            }

            /* Typography */
            h1, h2, h3, h4, .marcellus-font {
                font-family: 'Marcellus', serif !important;
                color: #F8FAFC !important;
                font-weight: 400 !important;
                letter-spacing: 0.02em;
            }

            /* Hero Banner */
            .hero-container {
                background: linear-gradient(135deg, rgba(22, 26, 36, 0.85), rgba(10, 13, 20, 0.95));
                border: 1px solid rgba(197, 160, 89, 0.35);
                border-radius: 16px;
                box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4);
                backdrop-filter: blur(12px);
            }
            .brand-gradient {
                background: linear-gradient(135deg, #F1E7D0 0%, #C5A059 50%, #8D6E31 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-family: 'Marcellus', serif;
            }
            .hero-badge-pill {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 6px 14px;
                background: rgba(197, 160, 89, 0.12);
                border: 1px solid rgba(197, 160, 89, 0.3);
                border-radius: 9999px;
                font-size: 11.5px;
                font-weight: 600;
                color: #C5A059;
                text-transform: uppercase;
                letter-spacing: 0.06em;
            }
            .pulse-dot {
                width: 8px;
                height: 8px;
                background: #10B981;
                border-radius: 50%;
                box-shadow: 0 0 10px #10B981;
                animation: pulse 2s infinite;
            }
            @keyframes pulse {
                0% { opacity: 0.6; transform: scale(0.95); }
                50% { opacity: 1; transform: scale(1.25); }
                100% { opacity: 0.6; transform: scale(0.95); }
            }

            /* Buttons */
            .stButton>button {
                background: transparent !important;
                color: #C5A059 !important;
                border: 1px solid #C5A059 !important;
                border-radius: 6px !important;
                padding: 8px 18px !important;
                font-size: 12px !important;
                font-weight: 600 !important;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                transition: all 0.25s ease-in-out !important;
            }
            .stButton>button:hover {
                transform: translateY(-2px) !important;
                background: #C5A059 !important;
                color: #0A0D14 !important;
                box-shadow: 0 6px 20px rgba(197, 160, 89, 0.25) !important;
            }

            /* Input Controls */
            div[data-baseweb="select"] > div {
                border: 1px solid #2C323F !important;
                border-radius: 8px !important;
                background-color: #121620 !important;
            }
            div[data-baseweb="select"] span, div[data-baseweb="select"] div {
                color: #E2E8F0 !important;
            }
            [data-testid="stWidgetLabel"] p {
                color: #94A3B8 !important;
                font-size: 13px !important;
                font-weight: 500 !important;
            }
            .stSlider [role="slider"] {
                background-color: #C5A059 !important;
                border-color: #C5A059 !important;
            }

            /* Navigation Tabs */
            button[data-baseweb="tab"] {
                color: #64748B !important;
                font-family: 'Marcellus', serif !important;
                font-size: 16px !important;
                letter-spacing: 0.04em;
                padding: 10px 18px !important;
            }
            button[aria-selected="true"] {
                color: #C5A059 !important;
                border-bottom-color: #C5A059 !important;
            }

            /* Expanders */
            [data-testid="stExpander"] {
                background-color: #121620 !important;
                border: 1px solid #2C323F !important;
                border-radius: 10px !important;
                margin-bottom: 12px;
            }

            /* Sidebar Styling */
            .sidebar-avatar-container {
                text-align: center;
                padding: 18px 0 10px 0;
            }
            .avatar-wrapper img {
                width: 96px;
                height: 96px;
                border-radius: 50%;
                border: 2px solid #C5A059;
                object-fit: cover;
                box-shadow: 0 4px 18px rgba(197, 160, 89, 0.25);
            }
            .sidebar-name {
                font-family: 'Marcellus', serif;
                font-size: 20px;
                color: #FFFFFF;
                margin-top: 10px;
                letter-spacing: 0.05em;
            }
            .sidebar-caption {
                color: #C5A059;
                font-size: 10.5px;
                letter-spacing: 0.2em;
                text-transform: uppercase;
                margin-top: 2px;
            }
            .sidebar-card {
                background: #121620;
                border: 1px solid #2C323F;
                border-radius: 10px;
                padding: 14px;
                margin: 12px 0;
            }
            .sidebar-item {
                margin-bottom: 10px;
            }
            .sidebar-item:last-child {
                margin-bottom: 0;
            }
            .sidebar-badge {
                font-size: 9px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                padding: 3px 8px;
                border-radius: 4px;
                background: rgba(197, 160, 89, 0.15);
                color: #C5A059;
            }
            .sidebar-badge.seeking {
                background: rgba(16, 185, 129, 0.15);
                color: #10B981;
            }
            .sidebar-title {
                font-size: 13px;
                font-weight: 600;
                color: #F1F5F9;
                margin-top: 4px;
            }
            .sidebar-sub {
                font-size: 11px;
                color: #94A3B8;
            }

            /* Suggestion Chips - Unified Box Dimensions & Text */
            div[data-testid="stVerticalBlock"]:has(.chip-label) div[data-testid="stHorizontalBlock"] .stButton>button {
                min-height: 52px !important;
                height: 52px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
                white-space: normal !important;
                word-break: normal !important;
                overflow-wrap: break-word !important;
                font-size: 12.5px !important;
                line-height: 1.35 !important;
                padding: 6px 12px !important;
                border-radius: 8px !important;
                border: 1px solid rgba(197, 160, 89, 0.4) !important;
                background: rgba(18, 22, 32, 0.85) !important;
            }
            div[data-testid="stVerticalBlock"]:has(.chip-label) div[data-testid="stHorizontalBlock"] .stButton>button:hover {
                background: #C5A059 !important;
                color: #0A0D14 !important;
                border-color: #C5A059 !important;
                box-shadow: 0 4px 15px rgba(197, 160, 89, 0.3) !important;
            }

            /* Package & Lookbook Card Action Buttons */
            div[data-testid="stColumn"] div[data-testid="stHorizontalBlock"] .stButton>button {
                padding: 8px 10px !important;
                font-size: 11.5px !important;
                font-weight: 600 !important;
                letter-spacing: 0.04em !important;
                white-space: nowrap !important;
                min-height: 38px !important;
                height: 38px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
            }

            /* Luxury Elegant Chat Styling */
            [data-testid="stChatMessage"] {
                background: rgba(18, 22, 32, 0.75) !important;
                backdrop-filter: blur(14px) !important;
                border: 1px solid rgba(197, 160, 89, 0.22) !important;
                border-radius: 14px !important;
                padding: 16px 20px !important;
                margin-bottom: 12px !important;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
                transition: all 0.2s ease !important;
            }
            [data-testid="stChatMessage"]:hover {
                border-color: rgba(197, 160, 89, 0.42) !important;
                box-shadow: 0 6px 24px rgba(197, 160, 89, 0.08) !important;
            }
            [data-testid="stChatMessageContent"] {
                font-size: 14.5px !important;
                line-height: 1.7 !important;
                color: #E2E8F0 !important;
            }
            [data-testid="stChatMessage"] [data-testid="stChatMessageAvatarCustom"],
            [data-testid="stChatMessage"] .stChatMessageAvatar {
                background: #0A0D14 !important;
                border: 1px solid #C5A059 !important;
                border-radius: 50% !important;
            }

            /* Elegant Chat Input Box */
            div[data-testid="stChatInput"] {
                border-radius: 14px !important;
            }
            div[data-testid="stChatInput"] > div {
                background-color: #121620 !important;
                border: 1px solid rgba(197, 160, 89, 0.35) !important;
                border-radius: 14px !important;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
                transition: all 0.25s ease !important;
            }
            div[data-testid="stChatInput"] > div:focus-within {
                border-color: #C5A059 !important;
                box-shadow: 0 0 0 2px rgba(197, 160, 89, 0.2), 0 6px 25px rgba(0, 0, 0, 0.5) !important;
            }
            div[data-testid="stChatInput"] textarea {
                color: #F8FAFC !important;
                font-size: 14px !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
