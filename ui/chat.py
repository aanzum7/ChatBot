from __future__ import annotations

from datetime import datetime
import uuid
from typing import Any, Dict, List, Optional
import streamlit as st

from config.settings import SUGGESTION_CHIPS, AVATAR_PATH
from services.agentic_ai import AgenticAI
from services.logger import get_logger
from services.rate_limiter import get_rate_limiter, get_funky_glitch_response

logger = get_logger(__name__)


def _get_client_id() -> str:
    """Generate or retrieve client device/session identifier for anti-abuse."""
    if "_client_device_id" not in st.session_state:
        st.session_state._client_device_id = str(uuid.uuid4())

    try:
        ctx = getattr(st, "context", None)
        if ctx and hasattr(ctx, "headers"):
            headers = ctx.headers
            fwd = headers.get("x-forwarded-for") or headers.get("remote-addr")
            if fwd:
                return fwd.split(",")[0].strip()
    except Exception:
        pass

    return st.session_state._client_device_id


def _ensure_session_state() -> None:
    """Ensure session state variables exist without initial placeholder message."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    else:
        # Strip legacy default placeholder message if lingering in active browser session
        st.session_state.chat_history = [
            m for m in st.session_state.chat_history
            if not (m.get("user") is None and "Assalamu Alaikum" in str(m.get("bot", "")))
        ]
    if "queued_prompt" not in st.session_state:
        st.session_state.queued_prompt = None


def render_chat(agent: AgenticAI) -> None:
    """
    Render private studio lounge chat with streaming, prompt chips, and rate limits in descending time style.
    """
    _ensure_session_state()
    limiter = get_rate_limiter()
    client_id = _get_client_id()

    st.markdown("### 💬 Private Studio Lounge")
    st.markdown(
        "<p style='font-size:13px; color:#64748B; margin-top:-8px;'>"
        "Inquire instantly about bespoke bridal packages, 2026 courses, organic cones, or stain aftercare."
        "</p>",
        unsafe_allow_html=True,
    )

    # 1. Quick suggestion prompt chips with shortened label
    st.markdown(
        """
        <div class="chip-label">
            <span>✨</span> Popular Inquiries
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 3-column balanced grid ensures full text visibility and unified dimensions
    for row_idx in range(0, len(SUGGESTION_CHIPS), 3):
        row_chips = SUGGESTION_CHIPS[row_idx : row_idx + 3]
        chip_cols = st.columns(3)
        for col_idx, (label, prompt_text) in enumerate(row_chips):
            chip_num = row_idx + col_idx
            with chip_cols[col_idx]:
                if st.button(label, key=f"chip_{chip_num}", use_container_width=True):
                    st.session_state.queued_prompt = prompt_text
                    st.rerun()

    st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

    # 2. Determine User Query
    user_query = st.chat_input("Ask about bridal packages, henna designs, academy training, or stain tips...")

    if st.session_state.queued_prompt:
        user_query = st.session_state.queued_prompt
        st.session_state.queued_prompt = None

    # 3. Descending Timeline Indicator
    if st.session_state.chat_history or user_query:
        st.markdown(
            "<div style='display: flex; justify-content: space-between; align-items: center; margin: 14px 0 12px 0;'>"
            "<span style='font-size: 11px; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;'>Studio Inquiries</span>"
            "<span style='font-size: 10.5px; color: #C5A059; background: rgba(197, 160, 89, 0.08); border: 1px solid rgba(197, 160, 89, 0.2); padding: 2px 8px; border-radius: 4px;'>↓ Newest First</span>"
            "</div>",
            unsafe_allow_html=True,
        )

    # 4. Upper-side slot for the newest incoming message
    active_turn_slot = st.container()
    new_entry_added = False

    if user_query:
        now_time = datetime.now().strftime("%I:%M %p")
        with active_turn_slot:
            with st.chat_message("user", avatar="✨"):
                st.markdown(
                    f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;'>"
                    f"<span style='font-weight:600; font-size:13px; color:#F1F5F9;'>You</span>"
                    f"<span style='font-size:11px; color:#64748B;'>{now_time}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(user_query)

            # Rate limiter check
            is_allowed, limit_msg = limiter.check_rate_limit(client_id)

            if not is_allowed and limit_msg:
                with st.chat_message("assistant", avatar="🌿"):
                    st.markdown(
                        f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;'>"
                        f"<span style='font-weight:600; font-size:13px; color:#C5A059;'>Rafiya • Studio Concierge</span>"
                        f"<span style='font-size:11px; color:#64748B;'>{now_time}</span>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                    st.markdown(limit_msg)
                st.session_state.chat_history.insert(0, {"user": user_query, "bot": limit_msg, "time": now_time})
            else:
                with st.chat_message("assistant", avatar="🌿"):
                    st.markdown(
                        f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;'>"
                        f"<span style='font-weight:600; font-size:13px; color:#C5A059;'>Rafiya • Studio Concierge</span>"
                        f"<span style='font-size:11px; color:#64748B;'>{now_time}</span>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                    try:
                        bot_reply = st.write_stream(agent.stream_response(user_query))
                    except Exception as e:
                        logger.error(f"Chat generation error: {e}")
                        fallback = get_funky_glitch_response()
                        st.markdown(fallback)
                        bot_reply = fallback

                st.session_state.chat_history.insert(0, {"user": user_query, "bot": bot_reply, "time": now_time})
        new_entry_added = True

    # 5. Render Prior Conversation History in Descending Order (Newest to Oldest)
    past_messages = st.session_state.chat_history[1:] if new_entry_added else st.session_state.chat_history

    if past_messages:
        for chat in past_messages:
            t = chat.get("time", "")
            if chat.get("user"):
                with st.chat_message("user", avatar="✨"):
                    if t:
                        st.markdown(
                            f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;'>"
                            f"<span style='font-weight:600; font-size:13px; color:#F1F5F9;'>You</span>"
                            f"<span style='font-size:11px; color:#64748B;'>{t}</span>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                    st.markdown(chat["user"])

            if chat.get("bot"):
                with st.chat_message("assistant", avatar="🌿"):
                    if t:
                        st.markdown(
                            f"<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;'>"
                            f"<span style='font-weight:600; font-size:13px; color:#C5A059;'>Rafiya • Studio Concierge</span>"
                            f"<span style='font-size:11px; color:#64748B;'>{t}</span>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                    st.markdown(chat["bot"])

    # 6. Studio Advisory Note & Feedback/Reset Controls
    if st.session_state.chat_history:
        st.markdown(
            """
            <div style='background: rgba(148,163,184,0.04); border-radius: 8px; padding: 12px 16px; margin-top: 24px; border: 1px dashed rgba(255,255,255,0.08);'>
                <p style='margin:0; font-size:11.5px; color:#64748B; line-height:1.4;'>
                    ⚠️ <b>Studio Note:</b> Automated assistant estimates are tailored to provide immediate clarity. 
                    Please confirm final date availability, travel details, and bespoke bridal customizations directly via 
                    <a href="https://wa.me/8801323278403" target="_blank" style="color: #C5A059;">WhatsApp</a> or 
                    <a href="https://m.me/Rafiya.HennaArt" target="_blank" style="color: #C5A059;">Messenger</a>.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
        col_like, col_dislike = st.columns(2)
        with col_like:
            if st.button("👍 Helpful Look", key="btn_chat_like", use_container_width=True):
                st.toast("Thank you! Glad to help craft your perfect look! 🌿", icon="✨")
        with col_dislike:
            if st.button("👎 Needs Detail", key="btn_chat_dislike", use_container_width=True):
                st.toast("Feedback noted. Feel free to ask more specific questions! 💬", icon="📝")

        if st.button("🗑️ Reset Lounge Workspace", key="btn_reset_chat", use_container_width=True):
            limiter.reset_client(client_id)
            st.session_state.chat_history = []
            st.session_state.queued_prompt = None
            agent.reset()
            st.rerun()

