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
# Global Session State Checks
# ---------------------------
if "selected_package" not in st.session_state:
    st.session_state.selected_package = None

if "favorites" not in st.session_state or not isinstance(st.session_state.favorites, set):
    st.session_state.favorites = set()

# Initialize chat history with a beautifully framed first DM from the Artist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "user": None,
            "bot": "Assalamu Alaikum! 🌿✨ Welcome to my creative sanctuary. I am **Rafiya**, your friendly henna artist. Whether you are seeking a royal bridal transformation, shopping for our handcrafted organic cones, or looking to master the craft in my training courses, I am here to design your vision. <br><br>Tell me what you are dreaming of creating today—in English, Bangla, or Banglish! 💬"
        }
    ]

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
# Production-Safe Premium CSS Injector
# ---------------------------
def apply_premium_styles():
    st.set_page_config(page_title="Rafiya's Henna Portal", page_icon="🌿", layout="wide")
    
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Marcellus&family=Montserrat:wght@400;500;600&display=swap');

        /* Deep Luxurious Canvas Background */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            background: radial-gradient(circle at top right, #161A24, #0A0D14) !important;
            color: #E2E8F0 !important;
            font-family: 'Montserrat', sans-serif;
        }
        
        /* Editorial Typography */
        h1, h2, h3, h4 {
            font-family: 'Marcellus', serif !important;
            color: #F8FAFC !important;
            font-weight: 400 !important;
        }

        /* Deep contrast Dropdowns */
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

        /* Elegant Champagne Minimalist Buttons */
        .stButton>button {
            background: transparent !important;
            color: #C5A059 !important;
            border: 1px solid #C5A059 !important;
            border-radius: 4px !important;
            padding: 8px 20px !important;
            font-family: 'Montserrat', sans-serif;
            font-size: 12px !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            transition: all 0.3s ease !important;
        }
        .stButton>button:hover {
            transform: translateY(-1px) !important;
            background: #C5A059 !important;
            color: #0A0D14 !important;
            box-shadow: 0 4px 15px rgba(197, 160, 89, 0.2) !important;
        }
        
        .stSlider [role="slider"] { background-color: #C5A059 !important; }
        [data-testid="stExpander"] {
            background-color: #121620 !important;
            border: 1px solid #2C323F !important;
            border-radius: 8px !important;
        }
        
        /* Premium Atelier Navigation Tabs */
        button[data-baseweb="tab"] {
            color: #64748B !important;
            font-family: 'Marcellus', serif !important;
            font-size: 16px !important;
            letter-spacing: 0.05em;
        }
        button[aria-selected="true"] {
            color: #C5A059 !important;
            border-bottom-color: #C5A059 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------
# Visual Component Layout Helpers
# ---------------------------
def display_package_grid(package_list: List[Dict], prefix: str):
    """Displays a responsive portfolio grid with distinct styling for Bridal vs Non-Bridal collections."""
    for idx, item in enumerate(package_list):
        if idx % 4 == 0:
            row_items = package_list[idx:idx+4]
            cols = st.columns(4)
            
        col = cols[idx % 4]
        with col:
            is_loved = item['name'] in st.session_state.favorites
            love_icon = "❤️ Saved" if is_loved else "🤍 Save Look"
            
            # Determine card aura style based on Bridal vs Daily classification
            is_bridal = "bridal" in item.get('type', '').lower()
            if is_bridal:
                card_style = """
                    border: 1px solid #C5A059; 
                    background: linear-gradient(135deg, #181C26, #0A0D14);
                    box-shadow: 0 10px 30px rgba(197, 160, 89, 0.08);
                """
                badge_style = "background: rgba(197, 160, 89, 0.15); color: #C5A059; border: 1px solid rgba(197, 160, 89, 0.3);"
                title_color = "#F1E7D0"
            else:
                card_style = """
                    border: 1px solid #2C323F; 
                    background: #121620;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
                """
                badge_style = "background: rgba(148, 163, 184, 0.1); color: #94A3B8;"
                title_color = "#FFFFFF"
            
            st.markdown(f"""
            <div style="border-radius: 12px; padding: 22px; display: flex; flex-direction: column; 
                 justify-content: space-between; height: 340px; margin-bottom: 12px; transition: all 0.3s ease; {card_style}">
                <div>
                    <span style="font-size: 9px; font-weight: 600; padding: 4px 10px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.05em; {badge_style}">
                        {item['type']}
                    </span>
                    <h3 style="margin-top: 16px; margin-bottom: 4px; font-size: 18px; line-height: 1.3; color: {title_color};">{item['name']}</h3>
                    <div style="font-size:11px; color: #64748B; margin-bottom: 12px; font-weight: 500;">📐 {item['length']} • ✋ {item['hand']}</div>
                    <p style="color: #94A3B8; font-size: 13px; overflow-y: auto; max-height: 95px; line-height: 1.5; font-weight: 400;">
                        {item['description']}
                    </p>
                </div>
                <div style="border-top: 1px solid rgba(255,255,255,0.05); padding-top: 12px; font-family: 'Marcellus', serif; font-size: 16px; color: #C5A059; letter-spacing: 0.05em;">
                    {item['price']} BDT
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns([5, 4])
            with btn_col1:
                if st.button("📖 View", key=f"det_{prefix}_{idx}_{item['name']}", use_container_width=True):
                    st.session_state.selected_package = item
                    st.rerun()
            with btn_col2:
                if st.button(love_icon, key=f"fav_{prefix}_{idx}_{item['name']}", use_container_width=True):
                    if is_loved:
                        st.session_state.favorites.remove(item['name'])
                        st.toast(f"Removed {item['name']} from lookbook.", icon="🗑️")
                    else:
                        st.session_state.favorites.add(item['name'])
                        st.toast(f"Saved {item['name']} to your lookbook!", icon="❤️")
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

    # --- ROUTE A: DEEP-DIVE ATELIER SCREEN ---
    if st.session_state.selected_package:
        pkg = st.session_state.selected_package
        
        if st.button("← Return to Lookbook Catalog", use_container_width=True):
            st.session_state.selected_package = None
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            is_bridal = "bridal" in pkg.get('type', '').lower()
            border_clr = "#C5A059" if is_bridal else "#2C323F"
            
            st.markdown(f"""
            <div style="border: 1px solid {border_clr}; border-radius: 12px; padding: 40px; 
                 background: #121620; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
                <div style="font-size: 50px; margin-bottom: 15px;">🌿</div>
                <span style="background: rgba(197,160,89,0.1); color: #C5A059; font-size: 11px; font-weight: 600; padding: 6px 14px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.1em;">
                    {pkg['type']}
                </span>
                <h2 style="margin-top: 24px; color: white; font-size: 28px;">{pkg['name']}</h2>
                <h1 style="color: #C5A059; margin-top: 15px; font-family: 'Marcellus', serif; font-size: 32px;">{pkg['price']} BDT</h1>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"## Design Specifications")
            st.markdown(f"**📐 Artistry Length Extension:** {pkg['length']}")
            st.markdown(f"**✋ Coverage Scale:** {pkg['hand']} ({pkg['side']})")
            st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
            st.markdown(f"### Collection Narrative")
            st.markdown(f"<p style='font-size:15px; line-height:1.7; color:#94A3B8;'>{pkg['description']}</p>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📅 Live Consultation & Booking")
            st.markdown(
                "Ready to transform your vision into fine artistry? Connect directly to reserve bespoke layout times:\n\n"
                "[💬 Chat on Messenger](https://m.me/Rafiya.HennaArt) | "
                "[📱 WhatsApp Concierge](https://wa.me/8801323278403) | "
                "[✉️ Direct Email Studio](mailto:rafiyashennaart@gmail.com)"
            )
            
    # --- ROUTE B: ARTIST PORTAL INTERFACE ---
    else:
        # Luxury Branding Banner
        st.markdown("""
        <div style="text-align: center; margin-top: 20px; margin-bottom: 35px;">
            <div style="display: inline-block; width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #C5A059, #8D6E31); padding: 1px; margin-bottom: 12px;">
                <div style="width: 100%; height: 100%; border-radius: 50%; background: #0A0D14; display: flex; align-items: center; justify-content: center; font-size: 32px;">🌿</div>
            </div>
            <h1 style="font-size: 2.8rem; margin: 0; letter-spacing: 0.05em; color: #FFFFFF;">RAFIYA HENNA ART</h1>
            <p style="color: #C5A059; font-weight: 500; font-size: 12px; letter-spacing: 0.4em; text-transform: uppercase; margin-top: 6px; margin-bottom: 0;">Atelier & Design Studio</p>
        </div>
        """, unsafe_allow_html=True)

        # Tabs Layout Sequence
        tab_chat, tab_packages, tab_faq = st.tabs([
            "💬 Atelier Consult", 
            "🎨 Curated Collections", 
            "💡 Studio Knowledge Base"
        ])

        # --- TAB 1: ARTIST CHAT (Lead Interface) ---
        with tab_chat:
            st.markdown(f"### 🌿 Private Studio Lounge")
            st.write("Inquire dynamically about custom compositions, bridal structural layout adjustments, or stain preservation details.")
            st.markdown("<br>", unsafe_allow_html=True)
            
            for chat in st.session_state.chat_history:
                if chat['user']:
                    with st.chat_message("user"):
                        st.markdown(f"""<div style="background:#1E293B; color:#F1F5F9; padding:14px; border-radius:12px; font-size:14.5px; border: 1px solid #334155; max-width: 80%; margin-left: auto;">{chat['user']}</div>""", unsafe_allow_html=True)
                
                with st.chat_message("assistant"):
                    st.markdown(f"""<div style="background:#121620; color:#E2E8F0; padding:14px; border-radius:12px; font-size:14.5px; border: 1px solid #C5A059; max-width: 85%;"><b>Henna Whisperer:</b><br>{chat['bot']}</div>""", unsafe_allow_html=True)

            user_query = st.chat_input("Ask Henna Whisperer about custom looks, product preservation, or design techniques...")

            if user_query:
                with st.chat_message("user"):
                    st.markdown(f"""<div style="background:#1E293B; padding:14px; border-radius:12px;">{user_query}</div>""", unsafe_allow_html=True)
                
                with st.spinner("Weaving response..."):
                    faq_q, faq_a = faq_handler.find_similar_question(user_query)
                    reply = f"🔍 **Studio FAQ Match:** *{faq_q}*\n\n{faq_a}" if faq_a else agentic_ai.generate_response(user_query)
                
                with st.chat_message("assistant"):
                    st.markdown(f"""<div style="background:#121620; padding:14px; border-radius:12px; border: 1px solid #C5A059;">{reply}</div>""", unsafe_allow_html=True)
                
                st.session_state.chat_history.append({"user": user_query, "bot": reply})
                st.rerun()

            if len(st.session_state.chat_history) > 1:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Reset Consult Canvas", use_container_width=True):
                    del st.session_state.chat_history[1:]
                    agentic_ai.configure_ai()
                    st.rerun()

        # --- TAB 2: PACKAGES & CATALOG ---
        with tab_packages:
            if st.session_state.favorites:
                st.markdown(f"### ❤️ Saved Portfolio Vault ({len(st.session_state.favorites)})")
                saved_items = [p for p in packages if p['name'] in st.session_state.favorites]
                display_package_grid(saved_items, prefix="vault")
                st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

            st.markdown("### 📦 Portfolio Matrix Lookbook")
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
            with col1:
                types = sorted(list(set(p['type'] for p in packages)))
                sel_type = st.selectbox("Aesthetic Category", ["All"] + types)
            filtered = [p for p in packages if sel_type == "All" or p['type'] == sel_type]
            
            with col2:
                lengths = sorted(list(set(p['length'] for p in filtered)))
                sel_length = st.selectbox("Design Architecture", ["All"] + lengths)
            filtered = [p for p in filtered if sel_length == "All" or p['length'] == sel_length]
            
            with col3:
                hands = sorted(list(set(p['hand'] for p in filtered)))
                sel_hand = st.selectbox("Coverage Scale", ["All"] + hands)
            filtered = [p for p in filtered if sel_hand == "All" or p['hand'] == sel_hand]
            
            with col4:
                sides = sorted(list(set(p['side'] for p in filtered)))
                sel_side = st.selectbox("Surface Alignment", ["All"] + sides)
            filtered = [p for p in filtered if sel_side == "All" or p['side'] == sel_side]
            
            with col5:
                prices = [p['price'] for p in filtered]
                min_p, max_p = (min(prices), max(prices)) if prices else (0, 0)
                if min_p == max_p:
                    st.number_input("Budget Threshold (BDT)", value=max_p, disabled=True)
                    sel_price = max_p
                else:
                    sel_price = st.slider("Budget Threshold (BDT)", int(min_p), int(max_p), int(max_p))

            final_packages = [p for p in filtered if p['price'] <= sel_price]
            display_package_grid(final_packages, prefix="catalog")

        # --- TAB 3: FAQ KNOWLEDGE BASE ---
        with tab_faq:
            st.markdown("### 💡 Studio Learning & Care Knowledge Base")
            if faq_data:
                categories = sorted(list(set(faq['category'] for faq in faq_data)))
                for cat in categories:
                    st.markdown(f"#### 📁 {cat.upper()}")
                    cat_faqs = [f for f in faq_data if f['category'] == cat]
                    for faq in cat_faqs:
                        with st.expander(f"✨ {faq['question']}", expanded=False):
                            st.markdown(f"""
                            <div style="background-color: #0A0D14; padding: 18px; border-left: 2px solid #C5A059; 
                                        border-radius: 4px; color: #94A3B8; font-size: 14px; line-height: 1.7;">
                                {faq['answer']}
                            </div>
                            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
