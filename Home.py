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
        inject_global_theme("Lounge", "✨")
        
        # Profile Bio Section (Social Style)
        st.markdown(f"""
        <div style="text-align: center; margin-top: 10px;">
            <div style="display: inline-block; width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); padding: 3px;">
                <div style="width: 100%; height: 100%; border-radius: 50%; background: #222; display: flex; align-items: center; justify-content: center; font-size: 40px;">🌿</div>
            </div>
            <h2 style="margin-top: 12px; margin-bottom: 2px;">Rafiya's Henna Art</h2>
            <p style="color: {CONFIG['accent_rose_gold']}; font-weight: 600; margin-top:0;">@rafiyas_henna_art</p>
        </div>
        """, unsafe_allow_html=True)
        
        render_header("", "Tradition in Every Stroke • Custom Luxury Bridal Experience")

        # Interactive Sticky Navigation Triggers
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button("✨ VIEW LOOKBOOK & PACKAGES", use_container_width=True):
                st.switch_page("pages/1_📦_Packages.py")
        with nav_col2:
            if st.button("💡 HELP CENTER & FAQS", use_container_width=True):
                st.switch_page("pages/2_💡_FAQs.py")
        
        st.divider()
        st.markdown(f"### 💬 Chat with **Henna Whisperer** <small style='color:#6B7280; font-size:12px;'>• AI Concierge</small>", unsafe_allow_html=True)

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Renders Instant messaging platform bubbles
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(f"""<div style="background:{CONFIG['user_msg_bg']}; color:{CONFIG['text_color']}; padding:14px; border-radius:18px 18px 2px 18px; font-size:15px; border: 1px solid #2e4d30; max-width: 85%; margin-left: auto;">{chat['user']}</div>""", unsafe_allow_html=True)
            with st.chat_message("assistant"):
                st.markdown(f"""<div style="background:{CONFIG['bot_msg_bg']}; color:{CONFIG['text_color']}; padding:14px; border-radius:18px 18px 18px 2px; font-size:15px; border: 1px solid #4a3b20; max-width: 85%;"><b>Henna Whisperer:</b><br>{chat['bot']}</div>""", unsafe_allow_html=True)

        user_query = st.chat_input("Message Henna Whisperer...")

        if user_query:
            with st.chat_message("user"):
                st.markdown(f"""<div style="background:{CONFIG['user_msg_bg']}; padding:14px; border-radius:18px 18px 2px 18px;">{user_query}</div>""", unsafe_allow_html=True)
            
            with st.spinner("Henna Whisperer is typing..."):
                reply = self.process_user_query(user_query)
            
            with st.chat_message("assistant"):
                st.markdown(f"""<div style="background:{CONFIG['bot_msg_bg']}; padding:14px; border-radius:18px 18px 18px 2px;">{reply}</div>""", unsafe_allow_html=True)
            
            st.session_state.chat_history.append({"user": user_query, "bot": reply})
            st.rerun()

        if st.session_state.chat_history:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ Clear Direct Messages", use_container_width=True):
                st.session_state.chat_history = []
                self.agentic_ai.configure_ai()
                st.rerun()

if __name__ == "__main__":
    RafiyaAIApp().run()
