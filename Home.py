import streamlit as st
import google.generativeai as genai
import pandas as pd
import langdetect
import logging
import time
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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "user": None,
            "bot": "Assalamu Alaikum! 🌿 I am **Rafiya**. Welcome to my design studio. Let's find your perfect look! 💬"
        }
    ]

# ---------------------------
# Interactive Live Data Pipeline
# ---------------------------
def fetch_live_studio_data():
    """Dynamically streams the latest studio coordinates via Google Sheets CSV endpoints."""
    # Base Sheet ID parsed from user layout architecture
    sheet_id = "1n8b5WCeHAeCrMeM_GhxsUGKmT3CILMnrm8a8yYxWaPU"
    
    # Export GID pointers mapped to respective matrix views
    packages_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    courses_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1815133618"
    products_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1114580373"
    
    try:
        # Stream remote CSV frames into native dictionary array layouts
        df_packages = pd.read_csv(packages_url).fillna("")
        df_courses = pd.read_csv(courses_url).fillna("")
        df_products = pd.read_csv(products_url).fillna("")
        
        packages = df_packages.to_dict(orient="records")
        courses = df_courses.to_dict(orient="records")
        products = df_products.to_dict(orient="records")
        
        return packages, courses, products
    except Exception as e:
        logger.error(f"Pipeline Sync Interrupted: {e}")
        # Elegant structurally empty return arrays to prevent runtime execution faults
        return [], [], []

def run_interactive_pipeline():
    """Renders a premium visual state transition indicating ledger execution."""
    with st.spinner("⚡ Connecting to Studio Cloud Engine..."):
        time.sleep(0.7)
    progress_bar = st.progress(0, text="🔄 Syncing active lookbooks & registries...")
    for percent_complete in range(0, 101, 25):
        time.sleep(0.15)
        progress_bar.progress(percent_complete, text=f"📥 Pulling structural tables... ({percent_complete}%)")
    time.sleep(0.2)
    progress_bar.empty()
    st.toast("Studio ecosystem successfully updated with latest database changes!", icon="✅")

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
                "temperature": 0.2,
                "top_p": 0.85,
                "max_output_tokens": 256,
            },
        )
        self.chat_session = self.model.start_chat()
        logger.info("Gemini AI configured.")

    def generate_response(self, user_input: str) -> str:
        try:
            prompt = (
                f"FAQ Context: {self.context['faq']}\n"
                f"Studio Package Context: {self.context['packages']}\n"
                f"Studio Course Context: {self.context['courses']}\n"
                f"Studio Product Context: {self.context['products']}\n"
                f"User Input: {user_input}\n\n"
                "You are Rafiya, a friendly henna artist 🌿✨. Respond naturally, matching the user's tone. "
                "Reply instantly in whatever language the query uses (Bangla, English, or Banglish).\n\n"
                "CRITICAL: Keep your response short, precise, and directly to the point. No fluff or lengthy introductions. "
                "Use the provided database variables context to instantly summarize prices, programs, or cone availability.\n\n"
                "Always drop short links to secure direct bookings or questions:\n"
                "💬 [Messenger](https://m.me/Rafiya.HennaArt) | 📱 [WhatsApp](https://wa.me/8801323278403)\n\n"
                "If information isn't available in context, provide the closest alternative and guide them to message directly."
            )

            response = self.chat_session.send_message(prompt)
            if response and hasattr(response, "text") and response.text:
                return response.text.strip()
            return "🤖 Couldn’t process statement. Drop a direct note instead!"
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"⚠️ Connection Timeout. Drop a text query directly!"

class FAQHandler:
    def __init__(self, faq_list: List[Dict]):
        self.faq_list = faq_list
        self.faq_cache: Dict[str, Tuple[str, str]] = {}

    def find_similar_question(self, user_input: str, threshold: float = 0.65) -> Tuple[Optional[str], Optional[str]]:
        cleaned_input = user_input.strip().lower()
        if cleaned_input in self.faq_cache:
            return self.faq_cache[cleaned_input]
            
        best_q, best_a, highest = None, None, 0
        for faq in self.faq_list:
            sim = SequenceMatcher(None, cleaned_input, faq['question'].lower()).ratio()
            if sim > highest:
                highest, best_q, best_a = sim, faq['question'], faq['answer']
                
        if highest >= threshold:
            self.faq_cache[cleaned_input] = (best_q, best_a)
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

        /* Canvas Setup */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            background: radial-gradient(circle at top right, #161A24, #0A0D14) !important;
            color: #E2E8F0 !important;
            font-family: 'Montserrat', sans-serif;
        }
        
        h1, h2, h3, h4 {
            font-family: 'Marcellus', serif !important;
            color: #F8FAFC !important;
            font-weight: 400 !important;
        }

        /* Input Controls */
        div[data-baseweb="select"] > div {
            border: 1px solid #2C323F !important;
            border-radius: 8px !important;
            background-color: #121620 !important;
        }
        div[data-baseweb="select"] span, div[data-baseweb="select"] div {
            color: #E2E8F0 !important;
        }

        /* Buttons */
        .stButton>button {
            background: transparent !important;
            color: #C5A059 !important;
            border: 1px solid #C5A059 !important;
            border-radius: 4px !important;
            padding: 8px 20px !important;
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
        
        /* Interactive Atelier Tabs */
        button[data-baseweb="tab"] {
            color: #64748B !important;
            font-family: 'Marcellus', serif !important;
            font-size: 15px !important;
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
    """Displays a responsive portfolio grid separating Bridal vs Non-Bridal styling aesthetics."""
    for idx, item in enumerate(package_list):
        if idx % 4 == 0:
            cols = st.columns(4)
            
        col = cols[idx % 4]
        with col:
            is_loved = item['name'] in st.session_state.favorites
            love_icon = "❤️ Saved" if is_loved else "🤍 Save Look"
            
            is_bridal = "bridal" in str(item.get('type', '')).lower()
            if is_bridal:
                card_style = "border: 1px solid #C5A059; background: linear-gradient(135deg, #181C26, #0A0D14);"
                badge_style = "background: rgba(197, 160, 89, 0.15); color: #C5A059;"
                title_color = "#F1E7D0"
            else:
                card_style = "border: 1px solid #2C323F; background: #121620;"
                badge_style = "background: rgba(148, 163, 184, 0.1); color: #94A3B8;"
                title_color = "#FFFFFF"
            
            st.markdown(f"""
            <div style="border-radius: 12px; padding: 22px; display: flex; flex-direction: column; 
                 justify-content: space-between; height: 340px; margin-bottom: 12px; {card_style}">
                <div>
                    <span style="font-size: 9px; font-weight: 600; padding: 4px 10px; border-radius: 4px; text-transform: uppercase; {badge_style}">
                        {item['type']}
                    </span>
                    <h3 style="margin-top: 16px; margin-bottom: 4px; font-size: 18px; line-height: 1.3; color: {title_color};">{item['name']}</h3>
                    <div style="font-size:11px; color: #64748B; margin-bottom: 12px;">📐 Length: {item['length']} • ✋ {item['hand']}</div>
                    <p style="color: #94A3B8; font-size: 13px; overflow-y: auto; max-height: 95px; line-height: 1.5;">
                        {item['description']}
                    </p>
                </div>
                <div style="border-top: 1px solid rgba(255,255,255,0.05); padding-top: 12px; font-family: 'Marcellus', serif; font-size: 16px; color: #C5A059;">
                    {int(float(item['price'])) if item['price'] else 0} BDT
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
                    else:
                        st.session_state.favorites.add(item['name'])
                    st.rerun()

# ---------------------------
# Main Routing Application
# ---------------------------
def main():
    apply_premium_styles()

    # Read base keys directly from backend secrets to keep operations secure
    api_key = st.secrets.get("genai", {}).get("api_key", "")
    faq_data = st.secrets.get("faq", {}).get("questions", [])

    # Persistent Data Caching in Session State to throttle remote network operations
    if "db_packages" not in st.session_state or "db_courses" not in st.session_state or "db_products" not in st.session_state:
        run_interactive_pipeline()
        pkgs, crs, prds = fetch_live_studio_data()
        st.session_state.db_packages = pkgs
        st.session_state.db_courses = crs
        st.session_state.db_products = prds

    packages = st.session_state.db_packages
    courses = st.session_state.db_courses
    products = st.session_state.db_products

    # Sidebar Pipeline Management System
    with st.sidebar:
        st.markdown("### 🎛️ Studio Administration")
        if st.button("🔄 Sync Studio Records", use_container_width=True):
            run_interactive_pipeline()
            pkgs, crs, prds = fetch_live_studio_data()
            st.session_state.db_packages = pkgs
            st.session_state.db_courses = crs
            st.session_state.db_products = prds
            st.rerun()
        st.markdown("---")
        st.markdown(f"**📊 Ledger Statistics:**\n* Design Items: {len(packages)}\n* Active Courses: {len(courses)}\n* Retained Products: {len(products)}")

    if "faq_handler" not in st.session_state:
        st.session_state.faq_handler = FAQHandler(faq_data)
        
    faq_handler = st.session_state.faq_handler
    agentic_ai = AgenticAI(api_key=api_key, context={"faq": faq_data, "packages": packages, "courses": courses, "products": products})

    # --- ROUTE A: DEEP-DIVE ATELIER SCREEN ---
    if st.session_state.selected_package:
        pkg = st.session_state.selected_package
        
        if st.button("← Return to Lookbook Catalog", use_container_width=True):
            st.session_state.selected_package = None
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            is_bridal = "bridal" in str(pkg.get('type', '')).lower()
            border_clr = "#C5A059" if is_bridal else "#2C323F"
            
            st.markdown(f"""
            <div style="border: 1px solid {border_clr}; border-radius: 12px; padding: 40px; 
                 background: #121620; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
                <div style="font-size: 50px; margin-bottom: 15px;">🌿</div>
                <span style="background: rgba(197,160,89,0.1); color: #C5A059; font-size: 11px; font-weight: 600; padding: 6px 14px; border-radius: 4px; text-transform: uppercase;">
                    {pkg['type']}
                </span>
                <h2 style="margin-top: 24px; color: white; font-size: 28px;">{pkg['name']}</h2>
                <h1 style="color: #C5A059; margin-top: 15px; font-family: 'Marcellus', serif; font-size: 32px;">{int(float(pkg['price'])) if pkg['price'] else 0} BDT</h1>
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
        st.markdown("""
        <div style="text-align: center; margin-top: 20px; margin-bottom: 35px;">
            <div style="display: inline-block; width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg, #C5A059, #8D6E31); padding: 1px; margin-bottom: 10px;">
                <div style="width: 100%; height: 100%; border-radius: 50%; background: #0A0D14; display: flex; align-items: center; justify-content: center; font-size: 28px;">🌿</div>
            </div>
            <h1 style="font-size: 2.6rem; margin: 0; letter-spacing: 0.05em; color: #FFFFFF;">RAFIYA HENNA ART</h1>
            <p style="color: #C5A059; font-weight: 500; font-size: 11px; letter-spacing: 0.35em; text-transform: uppercase; margin-top: 4px; margin-bottom: 0;">Atelier & Design Studio</p>
        </div>
        """, unsafe_allow_html=True)

        tab_chat, tab_packages, tab_faq = st.tabs([
            "💬 Private Studio Lounge", 
            "🎨 Curated Collections", 
            "💡 Studio Knowledge Base"
        ])

        # --- TAB 1: ARTIST CHAT (Lead Interface) ---
        with tab_chat:
            st.markdown(f"### 🌿 Automated Assistant")
            st.markdown("<p style='font-size:13px; color:#64748B; margin-top:-10px;'>Inquire instantly about designs, structural compositions, or preservation details.</p>", unsafe_allow_html=True)
            
            for chat in st.session_state.chat_history:
                if chat['user']:
                    with st.chat_message("user"):
                        st.markdown(f"""<div style="background:#1E293B; color:#F1F5F9; padding:12px 16px; border-radius:12px; font-size:14.5px; border: 1px solid #334155; max-width: 80%; margin-left: auto;">{chat['user']}</div>""", unsafe_allow_html=True)
                
                with st.chat_message("assistant"):
                    st.markdown(f"""<div style="background:#121620; color:#E2E8F0; padding:12px 16px; border-radius:12px; font-size:14.5px; border: 1px solid #C5A059; max-width: 85%;"><b>Henna Whisperer:</b><br>{chat['bot']}</div>""", unsafe_allow_html=True)

            user_query = st.chat_input("Message assistant for direct pricing, design structures, or tips...")

            if user_query:
                with st.chat_message("user"):
                    st.markdown(f"""<div style="background:#1E293B; padding:12px 16px; border-radius:12px;">{user_query}</div>""", unsafe_allow_html=True)
                
                with st.spinner("Weaving insight..."):
                    faq_q, faq_a = faq_handler.find_similar_question(user_query)
                    reply = f"🔍 **Studio FAQ:** *{faq_q}*\n\n{faq_a}" if faq_a else agentic_ai.generate_response(user_query)
                
                with st.chat_message("assistant"):
                    st.markdown(f"""<div style="background:#121620; padding:12px 16px; border-radius:12px; border: 1px solid #C5A059;">{reply}</div>""", unsafe_allow_html=True)
                
                st.session_state.chat_history.append({"user": user_query, "bot": reply})
                st.rerun()

            st.markdown("""
            <div style='background: rgba(148,163,184,0.04); border-radius: 8px; padding: 12px 16px; margin-top: 20px; border: 1px dashed rgba(255,255,255,0.08);'>
                <p style='margin:0; font-size:11.5px; color:#64748B; line-height:1.4;'>
                    ⚠️ <b>Studio Note:</b> Automated details may contain minor variance and are optimized to provide immediate clarity when the artist is away. Please confirm pricing and active slot scheduling directly via personal text link.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # --- TAB 2: PACKAGES, COURSES & PRODUCTS ---
        with tab_packages:
            sub_packages, sub_courses, sub_products = st.tabs([
                "📦 Design Packages", 
                "🎓 Training Programs", 
                "🌿 Organic Products"
            ])
            
            # --- SUB-TAB 1: PACKAGES & LOOKBOOK ---
            with sub_packages:
                if st.session_state.favorites:
                    st.markdown(f"### ❤️ Saved Portfolio Vault ({len(st.session_state.favorites)})")
                    saved_items = [p for p in packages if p['name'] in st.session_state.favorites]
                    display_package_grid(saved_items, prefix="vault")
                    st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

                st.markdown("### 📦 Portfolio Matrix Lookbook")
                col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
                with col1:
                    types = sorted(list(set(str(p['type']) for p in packages))) if packages else []
                    sel_type = st.selectbox("Aesthetic Category", ["All"] + types)
                filtered = [p for p in packages if sel_type == "All" or str(p['type']) == sel_type]
                
                with col2:
                    lengths = sorted(list(set(str(p['length']) for p in filtered))) if filtered else []
                    sel_length = st.selectbox("Design Architecture", ["All"] + lengths)
                filtered = [p for p in filtered if sel_length == "All" or str(p['length']) == sel_length]
                
                with col3:
                    hands = sorted(list(set(str(p['hand']) for p in filtered))) if filtered else []
                    sel_hand = st.selectbox("Coverage Scale", ["All"] + hands)
                filtered = [p for p in filtered if sel_hand == "All" or str(p['hand']) == sel_hand]
                
                with col4:
                    sides = sorted(list(set(str(p['side']) for p in filtered))) if filtered else []
                    sel_surface = st.selectbox("Surface Alignment", ["All"] + sides)
                filtered = [p for p in filtered if sel_surface == "All" or str(p['side']) == sel_surface]
                
                with col5:
                    prices = [float(p['price']) for p in filtered if p['price']]
                    min_p, max_p = (min(prices), max(prices)) if prices else (0.0, 0.0)
                    if min_p == max_p:
                        st.number_input("Budget Threshold (BDT)", value=int(max_p), disabled=True)
                        sel_price = max_p
                    else:
                        sel_price = st.slider("Budget Threshold (BDT)", int(min_p), int(max_p), int(max_p))

                final_packages = [p for p in filtered if p['price'] and float(p['price']) <= sel_price]
                display_package_grid(final_packages, prefix="catalog")

            # --- SUB-TAB 2: TRAINING PROGRAMS ---
            with sub_courses:
                st.markdown("### 🎓 Educational Atelier Workshops")
                for c in courses:
                    with st.expander(f"📖 {c['course_title']} — Starts {c['start_date']}", expanded=True):
                        col_info, col_off, col_on = st.columns(3)
                        with col_info:
                            st.markdown(f"**⏳ Structure:** {int(float(c['total_classes'])) if c['total_classes'] else 0} Intensive Sessions")
                            st.markdown(f"**👥 Group Profile:** {c['eligibility']}")
                            st.markdown(f"**🎯 Career Milestone:** {c['outcome']}")
                        with col_off:
                            st.markdown(f"**📍 In-Person Studio:**")
                            st.markdown(f"* Rate: **{int(float(c['offline_fee'])) if c['offline_fee'] else 0} BDT**")
                            st.markdown(f"* Timeline: {c['offline_days']} ({c['offline_time']})")
                            st.markdown(f"* Hub: {c['offline_location']}")
                        with col_on:
                            st.markdown(f"**🌐 Live Virtual Classroom:**")
                            st.markdown(f"* Rate: **{int(float(c['online_fee'])) if c['online_fee'] else 0} BDT**")
                            st.markdown(f"* Timeline: {c['online_days']} ({c['online_time']})")
                            st.markdown(f"* Engine: {c['online_platform']}")

            # --- SUB-TAB 3: ORGANIC PRODUCTS ---
            with sub_products:
                st.markdown("### 🌿 Handcrafted Stain Materials")
                for prd in products:
                    st.markdown(f"""
                    <div style="border: 1px solid #2C323F; background: #121620; padding: 20px; border-radius: 8px; margin-bottom: 12px;">
                        <h4 style="margin:0 0 4px 0; color: #C5A059;">✨ {prd['product_name']}</h4>
                        <p style="margin:0 0 10px 0; font-size:13px; color:#94A3B8;">{prd['description']}</p>
                        <span style="font-family:'Marcellus', serif; font-size:15px; color:#FFF;">Base Rate: {int(float(prd['mrp'])) if prd['mrp'] else 0} BDT</span>
                    </div>
                    """, unsafe_allow_html=True)

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
