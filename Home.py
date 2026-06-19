import streamlit as st
from utils.theme import inject_global_theme, render_header, CONFIG
from utils.utils import AgenticAI, FAQHandler

class RafiyaAIApp:
    def __init__(self):
        self.faq_data, self.personal_context, self.api_key = self.load_configuration()
        self.faq_handler = FAQHandler(self.faq_data)
        self.agentic_ai = AgenticAI(
            api_key=self.api_key,
            context={"faq": self.faq_data, "personal": self.personal_context}
        )

    def load_configuration(self):
        faq_data = st.secrets.get("faq", {}).get("questions", [])
        personal_data = st.secrets.get("personal", {}).get("data", {})
        api_key = st.secrets.get("genai", {}).get("api_key", "")
        return faq_data, personal_data, api_key

    def process_user_query(self, query: str) -> str:
        faq_q, faq_a = self.faq_handler.find_similar_question(query)
        if faq_a:
            return f"🔍 **FAQ Match:** *{faq_q}*\n\n{faq_a}"
        return self.agentic_ai.generate_response(query)

    def run(self):
        inject_global_theme("Home", "🌿")
        render_header("Rafiya’s Henna Art", "Tradition in Every Stroke, Intelligence in Every Answer!")

        # High-End Navigation Deck
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button("📦 Explore Bridal & Event Packages", use_container_width=True):
                st.switch_page("pages/1_📦_Packages.py")
        with nav_col2:
            if st.button("💡 Browse Helpful Knowledge Base", use_container_width=True):
                st.switch_page("pages/2_💡_FAQs.py")
        
        st.divider()
        st.subheader("💬 Chat with The Henna Whisperer")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Chat Stream Component Builder
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(f"""<div style="background:{CONFIG['user_bg']}; border-left:4px solid {CONFIG['user_border']}; color:{CONFIG['user_text']}; padding:14px; border-radius:10px; font-size:15px; box-shadow:0 2px 4px {CONFIG['card_shadow']};">{chat['user']}</div>""", unsafe_allow_html=True)
            with st.chat_message("assistant"):
                st.markdown(f"""<div style="background:{CONFIG['bot_bg']}; border-left:4px solid {CONFIG['bot_border']}; color:{CONFIG['bot_text']}; padding:14px; border-radius:10px; font-size:15px; box-shadow:0 2px 4px {CONFIG['card_shadow']};">{chat['bot']}</div>""", unsafe_allow_html=True)

        user_query = st.chat_input("Ask me anything about organic henna, packages, or booking...")

        if user_query:
            with st.chat_message("user"):
                st.markdown(f"""<div style="background:{CONFIG['user_bg']}; border-left:4px solid {CONFIG['user_border']}; color:{CONFIG['user_text']}; padding:14px; border-radius:10px;">{user_query}</div>""", unsafe_allow_html=True)
            
            with st.spinner("💭 Mixing organic mehendi paste..."):
                reply = self.process_user_query(user_query)
            
            with st.chat_message("assistant"):
                st.markdown(f"""<div style="background:{CONFIG['bot_bg']}; border-left:4px solid {CONFIG['bot_border']}; color:{CONFIG['bot_text']}; padding:14px; border-radius:10px;">{reply}</div>""", unsafe_allow_html=True)
            
            st.session_state.chat_history.append({"user": user_query, "bot": reply})
            st.rerun()

        if st.session_state.chat_history:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("♻️ Reset Conversion Session", use_container_width=True):
                st.session_state.chat_history = []
                self.agentic_ai.configure_ai()
                st.rerun()

if __name__ == "__main__":
    RafiyaAIApp().run()
