import streamlit as st
from utils.utils import AgenticAI, FAQHandler

# 🎨 GLOBAL COLOR PALETTE (Mehendi Theme)
BACKGROUND_COLOR = "#f9f7f1"       # Cream background
TEXT_COLOR = "#3b3a36"             # Dark earthy brown
HEADER_COLOR = "#6b8e23"           # Olive green
BUTTON_COLOR = "#b8860b"            # Goldenrod
BUTTON_HOVER_COLOR = "#a07400"      # Darker gold
USER_CHAT_BG = "#e6f2e1"           # Soft mehendi green
USER_BORDER_COLOR = "#6b8e23"       # Olive green border
USER_TEXT_COLOR = "#2f4f2f"         # Dark green for user text
ASSISTANT_CHAT_BG = "#fdf5e6"       # Light gold
ASSISTANT_BORDER_COLOR = "#b8860b"  # Goldenrod border
ASSISTANT_TEXT_COLOR = "#5b4636"    # Warm brown

class RafiyaAIApp:
    def __init__(self):
        self.faq_data, self.personal_context, self.api_key = self.load_configuration()
        self.faq_handler = FAQHandler(self.faq_data)
        self.agentic_ai = AgenticAI(
            api_key=self.api_key,
            context={"faq": self.faq_data, "personal": self.personal_context}
        )

    def load_configuration(self):
        faq_data = st.secrets["faq"]["questions"]
        personal_data = st.secrets["personal"]["data"]
        api_key = st.secrets["genai"]["api_key"]
        return faq_data, personal_data, api_key

    def process_user_query(self, query: str) -> str:
        faq_q, faq_a = self.faq_handler.find_similar_question(query)
        if faq_a:
            return f"🔍 **FAQ Match:** *{faq_q}*\n\n{faq_a}"
        return self.agentic_ai.generate_response(query)

    def run(self):
        st.set_page_config(page_title="Rafiya's Henna Art", layout="wide")

        # Inject global theme styles
        st.markdown(f"""
            <style>
            body {{
                background: {BACKGROUND_COLOR};
                color: {TEXT_COLOR};
                font-family: 'Segoe UI', sans-serif;
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: {HEADER_COLOR};
            }}
            .stButton>button {{
                background-color: {BUTTON_COLOR} !important;
                color: white !important;
                border-radius: 8px;
                border: none;
                padding: 10px 18px;
                font-size: 16px;
                font-weight: bold;
                transition: all 0.3s ease;
            }}
            .stButton>button:hover {{
                background-color: {BUTTON_HOVER_COLOR} !important;
                box-shadow: 0px 3px 12px rgba(0,0,0,0.2);
                transform: translateY(-1px);
            }}
            .chat-box {{
                padding: 14px;
                border-radius: 10px;
                margin-bottom: 10px;
                box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
                font-size: 15px;
                line-height: 1.5;
            }}
            .assistant {{
                background: {ASSISTANT_CHAT_BG};
                border-left: 4px solid {ASSISTANT_BORDER_COLOR};
                color: {ASSISTANT_TEXT_COLOR};
            }}
            .user {{
                background: {USER_CHAT_BG};
                border-left: 4px solid {USER_BORDER_COLOR};
                color: {USER_TEXT_COLOR};
            }}
            </style>
        """, unsafe_allow_html=True)

        # App name & tagline
        st.markdown(f"<h1 style='text-align:center;'>🌿 Rafiya’s Henna Art 🌿</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; color:{HEADER_COLOR}; font-style:italic;'>Tradition in Every Stroke, Intelligence in Every Answer! ✨</p>", unsafe_allow_html=True)
        st.divider()

        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💡 View FAQs", use_container_width=True):
                st.switch_page("pages/FAQs.py")
        with col2:
            if st.button("📦 View Packages", use_container_width=True):
                st.switch_page("pages/Packages.py")
        st.divider()

        # Chat section
        st.subheader("💬 Chat with The Henna Whisperer")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(f"<div class='chat-box user'>{chat['user']}</div>", unsafe_allow_html=True)
            with st.chat_message("assistant"):
                st.markdown(f"<div class='chat-box assistant'>{chat['bot']}</div>", unsafe_allow_html=True)

        user_query = st.chat_input("🌿 Ask me anything about henna, packages, or booking...")

        if user_query:
            with st.chat_message("user"):
                st.markdown(f"<div class='chat-box user'>{user_query}</div>", unsafe_allow_html=True)
            with st.spinner("💭 Mixing henna paste..."):
                reply = self.process_user_query(user_query)
            with st.chat_message("assistant"):
                st.markdown(f"<div class='chat-box assistant'>{reply}</div>", unsafe_allow_html=True)
            st.session_state.chat_history.append({"user": user_query, "bot": reply})

        if st.session_state.chat_history:
            if st.button("♻️ Start Over", use_container_width=True):
                st.session_state.chat_history = []
                self.agentic_ai.configure_ai()
                st.rerun()


if __name__ == "__main__":
    RafiyaAIApp().run()
