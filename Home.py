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
# Premium Black & Gold Theme Configuration
# ---------------------------
CONFIG = {
    "bg_color": "#0D0F12",          # Premium dark background
    "card_bg": "#161920",           # High-contrast surface cards
    "border_color": "#262B36",      # Clean boundaries
    "text_color": "#F3F4F6",        # Premium white text
    "text_muted": "#9CA3AF",        # Readable labels
    "accent_rose_gold": "#D4AF37",  # Metallic gold accent
    "hover_gold": "#E5C158",        # Active interaction glow
    "user_msg_bg": "#1F3520",       # Dark organic green DM bubble
    "bot_msg_bg": "#231E16"         # Warm amber DM bubble
}

# ---------------------------
# Safe Session State Initialization
# ---------------------------
if "selected_package" not in st.session_state:
    st.session_state.selected_package = None

if "favorites" not in st.session_state or not isinstance(st.session_state.favorites, set):
    st.session_state.favorites = set()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------
# Core Logic Engines
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
# Global CSS Injector
# ---------------------------
def apply_premium_styles():
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

        .stButton>button {{
            background: linear-gradient(135deg, {CONFIG['accent_rose_gold']}, #AA7C11) !important;
            color: #0D0F12 !important;
            border-radius: 25px !important;
            border: none !important;
            padding: 10px 22px !important;
            font-size: 13px !important;
            font-weight: 700 !important;
            text-transform: uppercase;
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
# Visual Component Layout Helpers
# ---------------------------
def display_package_grid(package_list: List[Dict], prefix: str):
    """Displays a responsive 4-column portfolio matrix matching NovelNexus engine."""
    for idx, item in enumerate(package_list):
        if idx % 4 == 0:
            row_items = package_list[idx:idx+4]
            cols = st.columns(4)
            
        col = cols[idx % 4]
        with col:
            is_loved = item['name'] in st.session_state.favorites
            love_icon = "❤️ Loved" if is_loved else "🤍 Love"
            
            st.markdown(f"""
            <div style="border: 1px solid {CONFIG['border_color']}; border-radius: 20px; padding: 20px; 
                 background: {CONFIG['card_bg']}; display: flex; flex-direction: column; 
                 justify-content: space-between; height: 320px; margin-bottom: 10px;
                 box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
                <div>
                    <span style="background: rgba(214,175,55,0.1); color: {CONFIG['accent_rose_gold']}; font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 20px; text-transform: uppercase;">
                        {item['type']}
                    </span>
                    <h3 style="margin-top: 14px; margin-bottom: 4px; font-size: 17px; line-height: 1.2;">{item['name']}</h3>
                    <div style="font-size:11px; color: {CONFIG['text_muted']}; margin-bottom: 8px;">📏 {item['length']} • ✋ {item['hand']}</div>
                    <p style="color: #D1D5DB; font-size: 12.5px; overflow-y: auto; max-height: 90px; line-height: 1.4;">
                        {item['description']}
                    </p>
                </div>
                <div style="border-top: 1px solid {CONFIG['border_color']}; padding-top: 10px; font-weight: 800; color: {CONFIG['accent_rose_gold']}; font-size: 15px;">
                    {item['price']} BDT
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Interactive Action Triggers
            btn_col1, btn_col2 = st.columns([5, 4])
            with btn_col1:
                if st.button("📖 Details", key=f"det_{prefix}_{idx}_{item['name']}", use_container_width=True):
                    st.session_state.selected_package = item
                    st.rerun()
            with btn_col2:
                if st.button(love_icon, key=f"fav_{prefix}_{idx}_{item['name']}", use_container_width=True):
                    if is_loved:
                        st.session_state.favorites.remove(item['name'])
                        st.toast(f"Removed {item['name']} from vault.", icon="🗑️")
                    else:
                        st.session_state.favorites.add(item['name'])
                        st.toast(f"Added {item['name']} to favorites vault!", icon="❤️")
                    st.rerun()

# ---------------------------
# Main Routing Application
# ---------------------------
def main():
    apply_premium_styles()

    # Data Pull Configuration
    faq_data = st.secrets.get("faq", {}).get("questions", [])
    personal_data = st.secrets.get("personal", {}).get("data", {})
    api_key = st.secrets.get("genai", {}).get("api_key", "")
    packages = personal_data.get("packages", [])

    faq_handler = FAQHandler(faq_data)
    agentic_ai = AgenticAI(api_key=api_key, context={"faq": faq_data, "personal": personal_data})

    # --- ROUTE A: DEEP-DIVE DEDICATED VIEW SCREEN ---
    if st.session_state.selected_package:
        pkg = st.session_state.selected_package
        
        if st.button("← Back to Lookbook Marketplace", use_container_width=True):
            st.session_state.selected_package = None
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div style="border: 2px solid {CONFIG['accent_rose_gold']}; border-radius: 20px; padding: 40px; 
                 background: {CONFIG['card_bg']}; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <div style="font-size: 60px; margin-bottom: 10px;">🌿</div>
                <span style="background: rgba(214,175,55,0.1); color: {CONFIG['accent_rose_gold']}; font-size: 12px; font-weight: 700; padding: 6px 14px; border-radius: 20px; text-transform: uppercase;">
                    {pkg['type']}
                </span>
                <h2 style="margin-top: 20px; color: white;">{pkg['name']}</h2>
                <h1 style="color: {CONFIG['accent_rose_gold']}; margin-top: 10px;">{pkg['price']} BDT</h1>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"## Collection Specifications")
            st.markdown(f"**📐 Design Length Extension:** {pkg['length']}")
            st.markdown(f"**✋ Hand Metrics Coverage:** {pkg['hand']} ({pkg['side']})")
            st.markdown("---")
            st.markdown(f"### Artistry Description")
            st.markdown(f"<p style='font-size:16px; line-height:1.6; color:#D1D5DB;'>{pkg['description']}</p>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📅 Live Booking Actions")
            st.markdown(
                "Ready to secure this look? Secure custom slots instantly via direct link messaging:\n\n"
                "[💬 Messenger Support](https://m.me/Rafiya.HennaArt) | "
                "[📱 Contact WhatsApp](https://wa.me/8801323278403) | "
                "[✉️ Direct Mail Inbox](mailto:rafiyashennaart@gmail.com)"
            )
            
    # --- ROUTE B: MAIN MARKETPLACE & CONCIERGE HUD ---
    else:
        # Header Dynamic Social Identity
        st.markdown(f"""
        <div style="text-align: center; margin-top: 15px; margin-bottom: 25px;">
            <div style="display: inline-block; width: 90px; height: 90px; border-radius: 50%; background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); padding: 3px;">
                <div style="width: 100%; height: 100%; border-radius: 50%; background: #161920; display: flex; align-items: center; justify-content: center; font-size: 36px;">🌿</div>
            </div>
            <h1 style="font-size: 2.3rem; margin-top: 10px; margin-bottom: 2px;">Rafiya's Henna Art</h1>
            <p style="color: {CONFIG['accent_rose_gold']}; font-weight: 600; margin-top:0;">@rafiyas_henna_art</p>
        </div>
        """, unsafe_allow_html=True)

        # ---------------------------
        # Section 1: The Favorites Vault Shelf
        # ---------------------------
        if st.session_state.favorites:
            st.markdown(f"## ❤️ Your Saved Favorites Vault ({len(st.session_state.favorites)})")
            saved_items = [p for p in packages if p['name'] in st.session_state.favorites]
            display_package_grid(saved_items, prefix="vault")
            st.markdown("---")

        # ---------------------------
        # Section 2: Lookbook Catalog Filter Engines
        # ---------------------------
        st.markdown("## 📦 Curated Portfolios Collection")
        
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
        with col1:
            types = sorted(list(set(p['type'] for p in packages)))
            sel_type = st.selectbox("Category Filter", ["All"] + types)
        filtered = [p for p in packages if sel_type == "All" or p['type'] == sel_type]
        
        with col2:
            lengths = sorted(list(set(p['length'] for p in filtered)))
            sel_length = st.selectbox("Design Length", ["All"] + lengths)
        filtered = [p for p in filtered if sel_length == "All" or p['length'] == sel_length]
        
        with col3:
            hands = sorted(list(set(p['hand'] for p in filtered)))
            sel_hand = st.selectbox("Hand Count", ["All"] + hands)
        filtered = [p for p in filtered if sel_hand == "All" or p['hand'] == sel_hand]
        
        with col4:
            sides = sorted(list(set(p['side'] for p in filtered)))
            sel_side = st.selectbox("Coverage Side", ["All"] + sides)
        filtered = [p for p in filtered if sel_side == "All" or p['side'] == sel_side]
        
        with col5:
            prices = [p['price'] for p in filtered]
            min_p, max_p = (min(prices), max(prices)) if prices else (0, 0)
            if min_p == max_p:
                st.number_input("Max Budget Limit (BDT)", value=max_p, disabled=True)
                sel_price = max_p
            else:
                sel_price = st.slider("Max Budget Limit (BDT)", int(min_p), int(max_p), int(max_p))

        final_packages = [p for p in filtered if p['price'] <= sel_price]
        
        # Display Core Catalog Shelf
        display_package_grid(final_packages, prefix="catalog")
        st.markdown("---")

        # ---------------------------
        # Section 3: AI Assistant Lounge (Henna Whisperer)
        # ---------------------------
        st.markdown(f"## 💬 DM Assistant: **Henna Whisperer**")
        
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(f"""<div style="background:{CONFIG['user_msg_bg']}; color:{CONFIG['text_color']}; padding:14px; border-radius:16px 16px 2px 16px; font-size:15px; border: 1px solid #2e4d30; max-width: 85%; margin-left: auto;">{chat['user']}</div>""", unsafe_allow_html=True)
            with st.chat_message("assistant"):
                st.markdown(f"""<div style="background:{CONFIG['bot_msg_bg']}; color:{CONFIG['text_color']}; padding:14px; border-radius:16px 16px 16px 2px; font-size:15px; border: 1px solid #4a3b20; max-width: 85%;"><b>Henna Whisperer:</b><br>{chat['bot']}</div>""", unsafe_allow_html=True)

        user_query = st.chat_input("Message Henna Whisperer about portfolio sets, care techniques or styles...")

        if user_query:
            with st.chat_message("user"):
                st.markdown(f"""<div style="background:{CONFIG['user_msg_bg']}; padding:14px; border-radius:16px 16px 2px 16px;">{user_query}</div>""", unsafe_allow_html=True)
            
            with st.spinner("Henna Whisperer is typing..."):
                faq_q, faq_a = faq_handler.find_similar_question(user_query)
                reply = f"🔍 **FAQ Match:** *{faq_q}*\n\n{faq_a}" if faq_a else agentic_ai.generate_response(user_query)
            
            with st.chat_message("assistant"):
                st.markdown(f"""<div style="background:{CONFIG['bot_msg_bg']}; padding:14px; border-radius:16px 16px 16px 2px;">{reply}</div>""", unsafe_allow_html=True)
            
            st.session_state.chat_history.append({"user": user_query, "bot": reply})
            st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑️ Reset DM Conversational Canvas", use_container_width=True):
                st.session_state.chat_history = []
                agentic_ai.configure_ai()
                st.rerun()

        st.markdown("---")

        # ---------------------------
        # Section 4: Help Center Knowledge Base
        # ---------------------------
        st.markdown("## 💡 Knowledge Base Help Center")
        if faq_data:
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

if __name__ == "__main__":
    main()
