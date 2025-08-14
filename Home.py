import streamlit as st
from utils import AgenticAI, FAQHandler

class RafiyaAIApp:
    def __init__(self):
        self.faq_data, self.personal_context, self.api_key = self.load_configuration()
        self.faq_handler = FAQHandler(self.faq_data)
        self.agentic_ai = AgenticAI(
            api_key=self.api_key,
            context={"faq": self.faq_data, "personal": self.personal_context}
        )

    def load_configuration(self):
        """
        Load FAQ, personal data, and API key from Streamlit secrets.
        """
        faq_data = st.secrets["faq"]["questions"]
        personal_data = st.secrets["personal"]["data"]
        api_key = st.secrets["genai"]["api_key"]
        return faq_data, personal_data, api_key

    def process_user_query(self, query: str) -> str:
        """
        First check FAQ similarity; fallback to AI generation.
        """
        faq_q, faq_a = self.faq_handler.find_similar_question(query)
        if faq_a:
            return f"🔍 **FAQ Match:** *{faq_q}*\n\n{faq_a}"
        return self.agentic_ai.generate_response(query)

    def run(self):
        st.set_page_config(page_title="rafiya.ai", layout="wide")

        st.markdown("<h1 style='text-align:center;'>rafiya.ai</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray;'>Your personal AI assistant for henna art & bookings.</p>", unsafe_allow_html=True)
        st.divider()

        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💡 View FAQs", use_container_width=True):
                st.switch_page("pages/FAQ.py")
        with col2:
            if st.button("📦 View Packages", use_container_width=True):
                st.switch_page("pages/Packages.py")
        st.divider()

        # Chat section
        st.subheader("💬 Chat with rafiya.ai")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(chat["user"])
            with st.chat_message("assistant"):
                st.markdown(chat["bot"])

        user_query = st.chat_input("Ask me anything about art, packages, or booking...")

        if user_query:
            with st.chat_message("user"):
                st.markdown(user_query)
            with st.spinner("Thinking... 🤔"):
                reply = self.process_user_query(user_query)
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.chat_history.append({"user": user_query, "bot": reply})

        if st.session_state.chat_history:
            if st.button("♻️ Start Over", use_container_width=True):
                st.session_state.chat_history = []
                self.agentic_ai.configure_ai()
                st.rerun()


if __name__ == "__main__":
    RafiyaAIApp().run()
