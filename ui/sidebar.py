from __future__ import annotations

import base64
import os
from typing import Any, Dict, Optional
import streamlit as st

from config.settings import AVATAR_PATH, APP_VERSION, APP_SUBTITLE

def _get_image_base64(filepath) -> Optional[str]:
    """Convert local image file to base64 data URI."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/jpeg;base64,{encoded}"
        except Exception:
            return None
    return None

def render_sidebar(personal_data: Optional[Dict[str, Any]] = None, active_model_label: Optional[str] = None):
    """Render high-polish atelier sidebar with concierge booking links and model tag."""
    data = personal_data or {}
    avatar_b64 = _get_image_base64(AVATAR_PATH)
    contacts = data.get("contacts", {})

    with st.sidebar:
        # Avatar Header
        avatar_html = (
            f'<img src="{avatar_b64}" alt="Rafiya Henna Art">'
            if avatar_b64
            else '<div style="font-size: 46px; padding: 16px;">🌿</div>'
        )
        st.markdown(
            f"""
            <div class="sidebar-avatar-container">
                <div class="avatar-wrapper">
                    {avatar_html}
                </div>
                <div class="sidebar-name">Rafiya's Henna Art</div>
                <div class="sidebar-caption">{APP_SUBTITLE}</div>
                <div style="margin-top: 10px; display: inline-flex; align-items: center; gap: 6px; 
                            background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); 
                            padding: 4px 12px; border-radius: 9999px; font-size: 11px; color: #10B981; font-weight: 600;">
                    <span class="pulse-dot"></span>
                    <span>Atelier Online 🌿</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<hr style='margin: 12px 0; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

        # Studio Details Card
        st.markdown(
            f"""
            <div class="sidebar-card">
                <div class="sidebar-item">
                    <span class="sidebar-badge">📍 Location</span>
                    <div class="sidebar-title">Azimpur, Dhaka</div>
                    <div class="sidebar-sub">Private Atelier & Home Service</div>
                </div>
                <div class="sidebar-item" style="margin-top: 10px;">
                    <span class="sidebar-badge seeking">✨ Model</span>
                    <div class="sidebar-title">{active_model_label or "Gemini Multi-Model"}</div>
                    <div class="sidebar-sub">MCP Knowledge Server Active</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Direct Booking & Concierge Links
        st.markdown("### 💬 Direct Concierge")
        wa_url = contacts.get("WhatsApp", "https://wa.me/8801323278403")
        if not wa_url.startswith("http"):
            wa_clean = wa_url.replace("+", "").replace(" ", "").replace("-", "")
            wa_url = f"https://wa.me/{wa_clean}"

        fb_msg = contacts.get("Messenger", "https://m.me/Rafiya.HennaArt")
        email_addr = contacts.get("Email", "rafiyashennaart@gmail.com")

        st.markdown(
            f"""
            <div style="display: flex; flex-direction: column; gap: 8px; margin-bottom: 16px;">
                <a href="{wa_url}" target="_blank" style="text-decoration: none;">
                    <div style="background: rgba(37, 211, 102, 0.12); border: 1px solid rgba(37, 211, 102, 0.35); 
                                color: #25D366; padding: 10px 14px; border-radius: 8px; font-size: 13px; font-weight: 600; 
                                display: flex; align-items: center; gap: 10px; transition: all 0.2s;">
                        <span>📱</span> WhatsApp Booking
                    </div>
                </a>
                <a href="{fb_msg}" target="_blank" style="text-decoration: none;">
                    <div style="background: rgba(0, 132, 255, 0.12); border: 1px solid rgba(0, 132, 255, 0.35); 
                                color: #0084FF; padding: 10px 14px; border-radius: 8px; font-size: 13px; font-weight: 600; 
                                display: flex; align-items: center; gap: 10px;">
                        <span>💬</span> Facebook Messenger
                    </div>
                </a>
                <a href="mailto:{email_addr}" style="text-decoration: none;">
                    <div style="background: rgba(197, 160, 89, 0.12); border: 1px solid rgba(197, 160, 89, 0.35); 
                                color: #C5A059; padding: 10px 14px; border-radius: 8px; font-size: 13px; font-weight: 600; 
                                display: flex; align-items: center; gap: 10px;">
                        <span>✉️</span> Email Studio
                    </div>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Social Follows
        ig_url = contacts.get("Instagram", "https://www.instagram.com/rafiyas_henna_art")
        fb_url = contacts.get("Facebook", "https://www.facebook.com/share/1CFfRyJ1wY/")
        yt_url = contacts.get("YouTube", "https://youtube.com/@RafiyasHennaArt")

        st.markdown(
            f"""
            <div style="font-size: 11px; color: #64748B; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;">
                Follow the Artistry
            </div>
            <div style="display: flex; gap: 12px; font-size: 18px; margin-bottom: 20px;">
                <a href="{ig_url}" target="_blank" title="Instagram" style="text-decoration: none;">📸</a>
                <a href="{fb_url}" target="_blank" title="Facebook" style="text-decoration: none;">🌐</a>
                <a href="{yt_url}" target="_blank" title="YouTube" style="text-decoration: none;">🎥</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="font-size: 10.5px; color: #475569; text-align: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;">
                Rafiya's Henna Art v{APP_VERSION}<br>
                Crafted with Fine Artistry & AI
            </div>
            """,
            unsafe_allow_html=True,
        )
