import streamlit as st
import google.generativeai as genai
import langdetect
import logging
from difflib import SequenceMatcher
from typing import Dict, Tuple, Optional, List

# ---------------------------
# Logging Configuration
# ---------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
# Premium Social Media Theme Configuration
# ---------------------------
CONFIG = {
    "bg_color": "#0D0F12",          # Ultra-dark luxury background
    "card_bg": "#161920",           # Sleek surface cards
    "border_color": "#262B36",      # Soft clean boundaries
    "text_color": "#F3F4F6",        # Premium off-white prose text
    "text_muted": "#9CA3AF",        # Readable labels
    "accent_rose_gold": "#D4AF37",  # Metallic gold accent
    "hover_gold": "#E5C158",        # Active interaction glow
    "user_msg_bg": "#1F3520",       # Dark organic green DM bubble
    "bot_msg_bg": "#231E16"         # Warm amber DM bubble
}

# ---------------------------
# Core Logic Engines (utils.py migration)
# ---------------------------
class AgenticAI:
    def __init__(self, api_key: str, context: Dict):
        self.api_key = api_key
        self.context = context
        self.configure_ai()

    def configure_ai(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            generation_config={
                "temperature": 0.1,
                "top_p": 0.9,
                "max_output_tokens": 512,
            },
        )
        self.chat_session = self.model.start_chat()
        logger.info("Gemini AI configured.")

    def generate_response(self, user_input: str) -> str:
        try:
            try:
                input_language = langdetect.detect(user_input)
            except langdetect.lang_detect_exception.LangDetectException:
                input_language = "en"

            prompt = (
                f"FAQ Context: {self.context['faq']}\n"
                f"Personal Context: {self.context['personal']}\n"
                f"User Input: {user_input}\n\n"
                "You are Rafiya, a talented and friendly henna artist 🌿✨. "
                "Respond naturally and warmly, mirroring the user's tone. "
                "Understand queries in Bangla, English, or Banglish, and reply in the same language the user asks in.\n\n"
                "Use the following info dynamically to respond in a **friendly, concise, summary style**:\n"
                "1️⃣ FAQ: Provide answers from the FAQ if relevant.\n"
                "2️⃣ Bridal and Non-Bridal Henna Packages:\n"
                "   - Show short lists with prices and descriptions.\n"
                "   - Always link to full details: 🌿 [Packages](https://rafiyashennaart.streamlit.app/Packages)\n"
                "   - Guide users on how to **book appointments**.\n"
                "3️⃣ Organic Henna & Products:\n"
                "   - Mention availability and details for each product.\n"
                "   - Link for full details: 🌿 [Products](https://sites.google.com/view/rafiyashennaart/products)\n"
                "   - Guide users on how to **purchase products**.\n"
                "4️⃣ Courses & Training:\n"
                "   - Include highlights, learning outcomes, and benefits dynamically.\n"
                "   - Link for full details: 🌿 [Courses & Training](https://sites.google.com/view/rafiyashennaart/courses-training)\n"
                "   - Guide users on how to **enroll**.\n\n"
                "Always keep responses:\n"
                "- Friendly, concise, engaging, and emoji-rich 🌿✨\n"
                "- Include clickable contact options for any action:\n"
                "💬 [Messenger](https://m.me/Rafiya.HennaArt) | "
                "📱 [WhatsApp](https://wa.me/8801323278403) | "
                "✉️ [Email](mailto:rafiyashennaart@gmail.com)\n\n"
                "- Include links to recent work:\n"
                "📘 [Facebook](https://www.facebook.com/share/1CFfRyJ1wY/) | "
                "📸 [Instagram](https://www.instagram.com/rafiyas_henna_art) | "
                "▶️ [YouTube](https://youtube.com/@RafiyasHennaArt)\n\n"
                "Guide the user naturally toward **booking, purchasing, enrolling, or viewing packages**.\n"
                "If a query is not listed in the FAQ or data, politely suggest the closest relevant option with links and action buttons."
            )

            response = self.chat_session.send_message(prompt)
            if response and hasattr(response, "text") and response.text:
                return response.text.strip()
            else:
                self.chat_session = self.model.start_chat()
                retry = self.chat_session.send_message(prompt)
                if retry and hasattr(retry, "text") and retry.text:
                    return retry.text.strip()
                return "🤖 Sorry, I couldn’t generate a response."
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"⚠️ Error: {e}"

class FAQHandler:
    def __init__(self, faq_list: List[Dict]):
        self.faq_list = faq_list

    def find_similar_question(self, user_input: str, threshold: float = 0.65) -> Tuple[Optional[str], Optional[str]]:
        best_q, best_a, highest = None, None, 0
        for faq in self.faq_list:
            sim = SequenceMatcher(None, user_input.lower(), faq['question'].lower()).ratio()
            if sim > highest:
                highest, best_q, best_a = sim, faq['question'], faq['answer']
        if highest >= threshold:
            return best_q, best_a
        return None, None

# ---------------------------
# Global Dynamic CSS Injector
# ---------------------------
def apply_premium_styles():
    st.set_page_config(page_title="Rafiya's Henna Portal", page_icon="🌿", layout="wide")
    st.markdown(f"""
    <style>
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {{
            background-color: {CONFIG['bg_color']} !important;
            color: {CONFIG['text_color']} !important;
            font-family: system-ui, -apple-system, sans-serif;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: {CONFIG['text_color']} !important;
            font-weight: 700 !important;
        }}

        /* Inputs Contrast Fix: Prevents labels or background overlapping */
        div[data-baseweb="select"] > div {{
            border: 1px solid {CONFIG['border_color']} !important;
            border-radius: 12px !important;
            background-color: {CONFIG['card_bg']} !important;
        }}
        div[data-baseweb="select"] span, div[data-baseweb="select"] div {{
            color: {CONFIG['text_color']} !important;
        }}
        [data-testid="stWidgetLabel"] p {{
            color: {CONFIG['text_muted']} !important;
            font-size: 13px !important;
            font-weight: 600 !important;
        }}

        /* Premium Social Lookbook Buttons */
        .stButton>button {{
            background: linear-gradient(135deg, {CONFIG['accent_rose_gold']}, #AA7C11) !important;
            color: #0D0F12 !important;
            border-radius: 25px !important;
            border: none !important;
            padding: 10px 22px !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            transition: all 0.2s ease-in-out !important;
        }}
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(212, 175, 55, 0.35) !important;
            color: #0D0F12 !important;
        }}
        
        .stSlider [role="slider"] {{ background-color: {CONFIG['accent_rose_gold']} !important; }}
        [data-testid="stExpander"] {{
            background-color: {CONFIG['card_bg']} !important;
            border: 1px solid {CONFIG['border_color']} !important;
            border-radius: 14px !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# ---------------------------
# Main App Execution Architecture
# ---------------------------
def main():
    apply_premium_styles()

    # Core Configurations Pull
    faq_data = st.secrets.get("faq", {}).get("questions", [])
    personal_data = st.secrets.get("personal", {}).get("data", {})
    api_key = st.secrets.get("genai", {}).get("api_key", "")
    packages = personal_data.get("packages", [])

    # Instantiate logic tools
    faq_handler = FAQHandler(faq_data)
    agentic_ai = AgenticAI(api_key=api_key, context={"faq": faq_data, "personal": personal_data})

    # Header Instagram Profile Badge
    st.markdown(f"""
    <div style="text-align: center; margin-top: 15px; margin-bottom: 5px;">
        <div style="display: inline-block; width: 90px; height: 90px; border-radius: 50%; background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); padding: 3px;">
            <div style="width: 100%; height: 100%; border-radius: 50%; background: #161920; display: flex; align-items: center; justify-content: center; font-size: 36px;">🌿</div>
        </div>
        <h1 style="font-size: 2.2rem; margin-top: 10px; margin-bottom: 2px;">Rafiya's Henna Art</h1>
        <p style="color: {CONFIG['accent_rose_gold']}; font-weight: 600; margin-top:0; margin-bottom: 25px;">@rafiyas_henna_art</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------
    # Navigation Dashboard Setup via Tabs
    # ---------------------------
    tab_chat, tab_packages, tab_faqs = st.tabs([
        "💬 CHAT ASSISTANT", 
        "📦 PORTFOLIO LOOKBOOK", 
        "💡 HELP CENTER FAQ"
    ])

    # --- TAB 1: AI ASSISTANT LOUNGE ---
    with tab_chat:
        st.markdown(f"### 💬 Consulting with **Henna Whisperer**", unsafe_allow_html=True)
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(f"""<div style="background:{CONFIG['user_msg_bg']}; color:{CONFIG['text_color']}; padding:14px; border-radius:16px 16px 2px 16px; font-size:15px; border: 1px solid #2e4d30; max-width: 85%; margin-left: auto;">{chat['user']}</div>""", unsafe_allow_html=True)
            with st.chat_message("assistant"):
                st.markdown(f"""<div style="background:{CONFIG['bot_msg_bg']}; color:{CONFIG['text_color']}; padding:14px; border-radius:16px 16px 16px 2px; font-size:15px; border: 1px solid #4a3b20; max-width: 85%;"><b>Henna Whisperer:</b><br>{chat['bot']}</div>""", unsafe_allow_html=True)

        user_query = st.chat_input("Ask Henna Whisperer about custom look designs or booking availability...")

        if user_query:
            with st.chat_message("user"):
                st.markdown(f"""<div style="background:{CONFIG['user_msg_bg']}; padding:14px; border-radius:16px 16px 2px 16px;">{user_query}</div>""", unsafe_allow_html=True)
            
            with st.spinner("Henna Whisperer is selecting design advice..."):
                # Run FAQ check matching logic first, fallback to LLM
                faq_q, faq_a = faq_handler.find_similar_question(user_query)
                reply = f"🔍 **FAQ Match:** *{faq_q}*\n\n{faq_a}" if faq_a else agentic_ai.generate_response(user_query)
            
            with st.chat_message("assistant"):
                st.markdown(f"""<div style="background:{CONFIG['bot_msg_bg']}; padding:14px; border-radius:16px 16px 16px 2px;">{reply}</div>""", unsafe_allow_html=True)
            
            st.session_state.chat_history.append({"user": user_query, "bot": reply})
            st.rerun()

        if st.session_state.chat_history:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️ CLEAR DM HISTORY", use_container_width=True):
                st.session_state.chat_history = []
                agentic_ai.configure_ai()
                st.rerun()

    # --- TAB 2: PORTFOLIO LOOKBOOK ---
    with tab_packages:
        st.markdown("### 📦 Curated Artistic Collections")
        if not packages:
            st.info("No collections loaded.")
        else:
            if "visible_packages_count" not in st.session_state:
                st.session_state.visible_packages_count = 4

            # Dynamic Filter Mechanics Setup
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
            with col1:
                types = sorted(list(set(p['type'] for p in packages)))
                sel_type = st.selectbox("Category Drop", ["All"] + types)
            filtered = [p for p in packages if sel_type == "All" or p['type'] == sel_type]
            
            with col2:
                lengths = sorted(list(set(p['length'] for p in filtered)))
                sel_length = st.selectbox("Design Length", ["All"] + lengths)
            filtered = [p for p in filtered if sel_length == "All" or p['length'] == sel_length]
            
            with col3:
                hands = sorted(list(set(p['hand'] for p in filtered)))
                sel_hand = st.selectbox("Hand Coverage", ["All"] + hands)
            filtered = [p for p in filtered if sel_hand == "All" or p['hand'] == sel_hand]
            
            with col4:
                sides = sorted(list(set(p['side'] for p in filtered)))
                sel_side = st.selectbox("Palm Side", ["All"] + sides)
            filtered = [p for p in filtered if sel_side == "All" or p['side'] == sel_side]
            
            with col5:
                prices = [p['price'] for p in filtered]
                min_p, max_p = (min(prices), max(prices)) if prices else (0, 0)
                if min_p == max_p:
                    st.number_input("Budget Ceiling (BDT)", value=max_p, disabled=True)
                    sel_price = max_p
                else:
                    sel_price = st.slider("Budget Ceiling (BDT)", int(min_p), int(max_p), int(max_p))

            # Auto-reset structural signature counters
            current_sig = f"{sel_type}-{sel_length}-{sel_hand}-{sel_side}-{sel_price}"
            if st.session_state.get("last_filter_sig") != current_sig:
                st.session_state.visible_packages_count = 4
                st.session_state.last_filter_sig = current_sig

            final_packages = [p for p in filtered if p['price'] <= sel_price]
            visible_pool = final_packages[:st.session_state.visible_packages_count]

            # Render Grid Layout Modules (up to 4 per row)
            for idx in range(0, len(visible_pool), 4):
                chunk = visible_pool[idx:idx+4]
                cols = st.columns(4)
                for col, item in zip(cols, chunk):
                    with col:
                        st.markdown(f"""
                        <div style="border: 1px solid {CONFIG['border_color']}; border-radius: 20px; padding: 20px; 
                             background: {CONFIG['card_bg']}; display: flex; flex-direction: column; 
                             justify-content: space-between; height: 380px; margin-bottom: 20px;
                             box-shadow: 0 10px 30px rgba(0,0,0,0.35);">
                            <div>
                                <span style="background: rgba(214,175,55,0.1); color: {CONFIG['accent_rose_gold']}; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; text-transform: uppercase;">
                                    {item['type']}
                                </span>
                                <h3 style="margin-top: 14px; margin-bottom: 8px; font-size: 18px;">{item['name']}</h3>
                                <div style="font-size:12px; color: {CONFIG['text_muted']}; margin: 4px 0;">📏 {item['length']} • ✋ {item['hand']} ({item['side']})</div>
                                <p style="color: #D1D5DB; font-size: 13px; margin-top: 12px; overflow-y: auto; max-height: 120px; line-height: 1.5;">
                                    {item['description']}
                                </p>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid {CONFIG['border_color']}; padding-top: 12px; margin-top: 10px;">
                                <span style="font-size: 11px; color: #6B7280; font-weight:700;">INVESTMENT</span>
                                <span style="color: {CONFIG['accent_rose_gold']}; font-weight: 800; font-size: 16px;">{item['price']} BDT</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

            if len(final_packages) > st.session_state.visible_packages_count:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✨ LOAD MORE PACKAGES", use_container_width=True):
                    st.session_state.visible_packages_count += 4
                    st.rerun()

    # --- TAB 3: KNOWLEDGE BASE PORTAL ---
    with tab_faqs:
        st.markdown("### 💡 Help Center Resources")
        if not faq_data:
            st.info("Knowledge base is currently empty.")
        else:
            categories = sorted(list(set(faq['category'] for faq in faq_data)))
            for cat in categories:
                st.markdown(f"#### 📁 {cat.upper()}")
                cat_faqs = [f for f in faq_data if f['category'] == cat]
                
                for faq in cat_faqs:
                    with st.expander(f"✨ {faq['question']}", expanded=False):
                        st.markdown(f"""
                        <div style="background-color: #1C202A; padding: 16px; border-left: 3px solid {CONFIG['accent_rose_gold']}; 
                                    border-radius: 4px; color: #E5E7EB; font-size: 14.5px; line-height: 1.6;">
                            {faq['answer']}
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
