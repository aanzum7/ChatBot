from __future__ import annotations

import streamlit as st

from config.settings import APP_TITLE, APP_ICON, APP_SUBTITLE
from services.config import load_studio_configuration, ConfigError
from services.logger import get_logger
from services.agentic_ai import AgenticAI
from services.faq import FAQHandler
from services.mcp_server import create_mcp_server
from services.cache_manager import get_response_cache
from ui.styles import inject_styles
from ui.sidebar import render_sidebar
from ui.chat import render_chat
from ui.catalog_view import render_catalog_view, render_package_detail, render_saved_view
from ui.course_view import render_course_view
from ui.faq_view import render_faq_view

logger = get_logger(__name__)

def build_studio_app():
    """Create and wire up studio dependencies with session persistence."""
    config = load_studio_configuration()
    faq_data = config["faq_data"]
    personal_data = config["personal_data"]
    api_key = config["api_key"]
    packages = config["packages"]
    courses = config["courses"]
    products = config["products"]

    # In-memory FAQ Handler
    if "faq_handler" not in st.session_state:
        st.session_state.faq_handler = FAQHandler(faq_data)

    # MCP Knowledge Server
    mcp_server = create_mcp_server(personal_data=personal_data, faq_data=faq_data)
    response_cache = get_response_cache()

    # Cache AgenticAI instance across reruns to preserve conversation memory
    if "agent" not in st.session_state:
        st.session_state.agent = AgenticAI(
            api_key=api_key,
            context={"faq": faq_data, "personal": personal_data},
            mcp_server=mcp_server,
            cache=response_cache,
        )

    return st.session_state.agent, packages, courses, products, faq_data, personal_data


def render_hero_banner(active_model_label: str):
    """Render compact, luxury atelier glassmorphism hero banner."""
    st.markdown(
        f"""
        <div class="hero-container" style="padding: 22px 28px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="font-family: 'Marcellus', serif; font-size: 2.1rem; color: #FFFFFF; letter-spacing: 0.04em;">
                        <span>RAFIYA</span>
                        <span class="brand-gradient">HENNA ART</span>
                        <span style="font-size: 1.6rem;">🌿</span>
                    </div>
                    <p style="color: #C5A059; font-size: 11px; font-weight: 600; letter-spacing: 0.25em; text-transform: uppercase; margin: 4px 0 0 0;">
                        Atelier & Design Studio • Azimpur, Dhaka
                    </p>
                </div>
                <div class="hero-badge-pill" title="MCP Knowledge Server & Multi-Model Failover Active">
                    <span class="pulse-dot"></span>
                    <span>Atelier Online • {active_model_label} • MCP Agent</span>
                </div>
            </div>
            <p style="font-size: 0.95rem; color: #94A3B8; margin-top: 10px; line-height: 1.6; margin-bottom: 0;">
                Bespoke bridal symmetry, organic hand-crafted cones, and professional academy training. 
                Inquire instantly with our intelligent assistant or reserve dates directly via concierge channels.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Global Atelier Design System
    inject_styles()

    # Session state initialization
    if "selected_package" not in st.session_state:
        st.session_state.selected_package = None

    if "favorites" not in st.session_state or not isinstance(st.session_state.favorites, set):
        st.session_state.favorites = set()

    try:
        agent, packages, courses, products, faq_data, personal_data = build_studio_app()
    except ConfigError as e:
        st.error(f"Configuration error: {e}")
        logger.exception("Failed to start app due to configuration error.")
        st.stop()
    except Exception as e:
        st.error(f"Startup error: {e}")
        logger.exception("Unexpected error during startup.")
        st.stop()

    # Studio Sidebar
    render_sidebar(personal_data=personal_data, active_model_label=agent.active_model_label)

    # Route A: Deep-Dive Look Detail Screen
    if st.session_state.selected_package:
        render_package_detail(st.session_state.selected_package)
    # Route B: Main Studio Navigation
    else:
        render_hero_banner(active_model_label=agent.active_model_label)

        fav_count = len(st.session_state.favorites)
        saved_tab_title = f"❤️ Saved Looks ({fav_count})" if fav_count > 0 else "❤️ Saved Looks"

        tab_chat, tab_packages, tab_saved, tab_courses, tab_faq = st.tabs([
            "💬 Private Studio Lounge",
            "🎨 Curated Collections",
            saved_tab_title,
            "🎓 Academy & Training",
            "💡 FAQ",
        ])

        with tab_chat:
            render_chat(agent=agent)

        with tab_packages:
            render_catalog_view(packages=packages)

        with tab_saved:
            render_saved_view(packages=packages)

        with tab_courses:
            render_course_view(course_data=courses)

        with tab_faq:
            render_faq_view(faq_data=faq_data, products=products)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        logger.exception("Application crashed.")
