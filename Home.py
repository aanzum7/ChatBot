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
# TOML Fallback Backup Pipeline
# ---------------------------
def get_toml_backup_data():
    """Parses structural fallback layout arrays directly from secrets TOML."""
    personal_data = st.secrets.get("personal", {}).get("data", {})
    
    toml_packages = personal_data.get("packages", [])
    toml_courses = personal_data.get("course", {}).get("courses", [])
    toml_products = personal_data.get("products", {}).get("items", [])
    
    packages = []
    for p in toml_packages:
        packages.append({
            "type": p.get("type", ""),
            "name": p.get("name", ""),
            "length": p.get("length", ""),
            "hand": p.get("hand", ""),
            "side": p.get("side", ""),
            "price": p.get("price", 0),
            "description": p.get("description", "")
        })

    courses = []
    for c in toml_courses:
        courses.append({
            "course_title": c.get("title", ""),
            "start_date": c.get("start_date", ""),
            "total_classes": c.get("total_classes", 0),
            "eligibility": c.get("eligibility", ""),
            "outcome": c.get("outcome", ""),
            "offline_fee": 5000 if "Basic" in c.get("title", "") else 6000,
            "offline_days": "Sunday, Tuesday, Thursday",
            "offline_time": "11:00 AM – 1:00 PM",
            "offline_location": "Mohammadpur, Dhaka",
            "online_fee": 4500 if "Basic" in c.get("title", "") else 5500,
            "online_days": "Saturday, Monday, Wednesday",
            "online_time": "11:00 AM – 1:00 PM",
            "online_platform": "Google Meet"
        })
        
    products = []
    for prd in toml_products:
        products.append({
            "product_name": prd.get("name", "Organic Henna Cone"),
            "description": prd.get("description", "100% Organic & Halal Materials"),
            "mrp": prd.get("mrp", 100.0),
            "details": prd.get("details", "")
        })

    return packages, courses, products

# ---------------------------
# Live Spreadsheet Synchronizer
# ---------------------------
def fetch_live_studio_data():
    """Streams data rows straight from live Google Sheets with runtime TOML fallbacks."""
    sheet_id = "1n8b5WCeHAeCrMeM_GhxsUGKmT3CILMnrm8a8yYxWaPU"
    packages_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    courses_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1815133618"
    products_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1114580373"
    
    try:
        df_packages = pd.read_csv(packages_url)
        if not df_packages.empty and ("name" in df_packages.columns or df_packages.shape[1] > 1):
            df_courses = pd.read_csv(courses_url)
            df_products = pd.read_csv(products_url)
            
            return (
                df_packages.fillna("").to_dict(orient="records"),
                df_courses.fillna("").to_dict(orient="records"),
                df_products.fillna("").to_dict(orient="records")
            )
    except Exception as e:
        logger.warning(f"Spreadsheet stream interrupted. Transitioning to local TOML profiles: {e}")
        
    return get_toml_backup_data()

def run_interactive_pipeline():
    """Renders fractional sync visual updates relative to specific database records."""
    status_text = st.empty()
    progress_bar = st.empty()
    
    status_text.markdown("<p style='color:#C5A059; font-size:13px; text-align:center; font-weight:500; letter-spacing:0.1em;'>🔄 INITIALIZING SOURCE PIPELINES: PULLING PACKAGES...</p>", unsafe_allow_html=True)
    progress_bar.progress(33)
    time.sleep(0.3)
    
    status_text.markdown("<p style='color:#C5A059; font-size:13px; text-align:center; font-weight:500; letter-spacing:0.1em;'>🔄 INITIALIZING SOURCE PIPELINES: STREAMING TRAINING SCHEMAS...</p>", unsafe_allow_html=True)
    progress_bar.progress(66)
    time.sleep(0.3)
    
    status_text.markdown("<p style='color:#C5A059; font-size:13px; text-align:center; font-weight:500; letter-spacing:0.1em;'>🔄 INITIALIZING SOURCE PIPELINES: SYNCING RETAIL PRODUCTS...</p>", unsafe_allow_html=True)
    progress_bar.progress(100)
    time.sleep(0.2)
        
    status_text.empty()
    progress_bar.empty()
    st.toast("Ecosystem coordinates successfully refreshed!", icon="✅")

# ---------------------------
# Production-Safe Premium CSS Injector
# ---------------------------
def apply_premium_styles():
    st.set_page_config(page_title="Rafiya's Henna Portal", page_icon="🌿", layout="wide")
    
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Marcellus&family=Montserrat:wght@400;500;600&display=swap');

        /* Complete Full Width Grid Adjustments */
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stSidebarCollapsedControl"] { display: none !important; }
        .stAppViewMain [data-testid="stVerticalBlock"] { max-width: 100% !important; padding-left: 2% !important; padding-right: 2% !important; }

        /* Canvas Setup */
        .stApp, [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at top right, #161A24, #0A0D14) !important;
            color: #E2E8F0 !important;
            font-family: 'Montserrat', sans-serif;
        }
        
        h1, h2, h3, h4 {
            font-family: 'Marcellus', serif !important;
            color: #F8FAFC !important;
            font-weight: 400 !important;
        }

        /* Filter Controls */
        div[data-baseweb="select"] > div {
            border: 1px solid #2C323F !important;
            border-radius: 8px !important;
            background-color: #121620 !important;
        }
        div[data-baseweb="select"] span, div[data-baseweb="select"] div {
            color: #E2E8F0 !important;
        }

        /* Action Buttons */
        .stButton>button {
            background: transparent !important;
            color: #C5A059 !important;
            border: 1px solid #C5A059 !important;
            border-radius: 4px !important;
            padding: 8px 20px !important;
            font-size: 11px !important;
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
        
        .stProgress > div > div > div > div { background-color: #C5A059 !important; }
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
            is_loved = item.get('name', '') in st.session_state.favorites
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
                        {item.get('type', 'Custom')}
                    </span>
                    <h3 style="margin-top: 16px; margin-bottom: 4px; font-size: 17px; line-height: 1.3; color: {title_color};">{item.get('name', 'Henna Look')}</h3>
                    <div style="font-size:11px; color: #64748B; margin-bottom: 12px;">📐 Length: {item.get('length', '-')} • ✋ {item.get('hand', '-')}</div>
                    <p style="color: #94A3B8; font-size: 12.5px; overflow-y: auto; max-height: 95px; line-height: 1.5;">
                        {item.get('description', '')}
                    </p>
                </div>
                <div style="border-top: 1px solid rgba(255,255,255,0.05); padding-top: 12px; font-family: 'Marcellus', serif; font-size: 15px; color: #C5A059;">
                    {int(float(item['price'])) if item.get('price') else 0} BDT
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns([5, 4])
            with btn_col1:
                if st.button("📖 View", key=f"det_{prefix}_{idx}_{item.get('name','')}", use_container_width=True):
                    st.session_state.selected_package = item
                    st.rerun()
            with btn_col2:
                if st.button(love_icon, key=f"fav_{prefix}_{idx}_{item.get('name','')}", use_container_width=True):
                    if is_loved:
                        st.session_state.favorites.remove(item['name'])
                    else:
                        st.session_state.favorites.add(item['name'])
                    st.rerun()

# ---------------------------
# Core Dialog Engines
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
            generation_config={"temperature": 0.2, "top_p": 0.85, "max_output_tokens": 256},
        )
        self.chat_session = self.model.start_chat()

    def generate_response(self, user_input: str) -> str:
        try:
            prompt = (
                f"FAQ Context: {self.context['faq']}\n"
                f"Package Context: {self.context['packages']}\n"
                f"User Input: {user_input}\n\n"
                "You are Rafiya, a friendly henna artist. Keep your response short, clean, and directly to the point. No fluff.\n\n"
                "💬 [Messenger](https://m.me/Rafiya.HennaArt) | 📱 [WhatsApp](https://wa.me/8801323278403)\n\n"
            )
            response = self.chat_session.send_message(prompt)
            return response.text.strip() if response else "🤖 Message WhatsApp or Messenger directly for instant custom quotes!"
        except Exception:
            return "⚠️ Connection Timeout. Drop a text query directly!"

class FAQHandler:
    def __init__(self, faq_list: List[Dict]):
        self.faq_list = faq_list
        self.faq_cache: Dict[str, Tuple[str, str]] = {}

    def find_similar_question(self, user_input: str, threshold: float = 0.65) -> Tuple[Optional[str], Optional[str]]:
        cleaned_input = user_input.strip().lower()
        if cleaned_input in self.faq_cache:
            return self.faq_cache[cleaned_input]
        for faq in self.faq_list:
            if SequenceMatcher(None, cleaned_input, faq['question'].lower()).ratio() >= threshold:
                self.faq_cache[cleaned_input] = (faq['question'], faq['answer'])
                return faq['question'], faq['answer']
        return None, None

# ---------------------------
# Main Routing Application
# ---------------------------
def main():
    apply_premium_styles()

    api_key = st.secrets.get("genai", {}).get("api_key", "")
    faq_data = st.secrets.get("faq", {}).get("questions", [])

    if "db_packages" not in st.session_state or "db_courses" not in st.session_state or "db_products" not in st.session_state:
        run_interactive_pipeline()
        pkgs, crs, prds = fetch_live_studio_data()
        st.session_state.db_packages = pkgs
        st.session_state.db_courses = crs
        st.session_state.db_products = prds

    packages = st.session_state.db_packages
    courses = st.session_state.db_courses
    products = st.session_state.db_products

    if "faq_handler" not in st.session_state:
        st.session_state.faq_handler = FAQHandler(faq_data)
        
    faq_handler = st.session_state.faq_handler
    agentic_ai = AgenticAI(api_key=api_key, context={"faq": faq_data, "packages": packages, "courses": courses, "products": products})

    # --- ROUTE A: DETAIL LOOK COMPOSITION ---
    if st.session_state.selected_package:
        pkg = st.session_state.selected_package
        if st.button("← Return to Collections Marketplace", use_container_width=True):
            st.session_state.selected_package = None
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            is_bridal = "bridal" in str(pkg.get('type', '')).lower()
            border_clr = "#C5A059" if is_bridal else "#2C323F"
            st.markdown(f"""
            <div style="border: 1px solid {border_clr}; border-radius: 12px; padding: 40px; background: #121620; text-align: center;">
                <div style="font-size: 50px; margin-bottom: 15px;">🌿</div>
                <span style="background: rgba(197,160,89,0.1); color: #C5A059; font-size: 11px; font-weight: 600; padding: 6px 14px; border-radius: 4px; text-transform: uppercase;">{pkg.get('type','Custom')}</span>
                <h2 style="margin-top: 24px; color: white; font-size: 28px;">{pkg.get('name','Look')}</h2>
                <h1 style="color: #C5A059; margin-top: 15px; font-family: 'Marcellus', serif; font-size: 32px;">{int(float(pkg['price'])) if pkg.get('price') else 0} BDT</h1>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("## Design Specifications")
            st.markdown(f"**📐 Artistry Length Extension:** {pkg.get('length', '-')}")
            st.markdown(f"**✋ Coverage Scale:** {pkg.get('hand', '-')} ({pkg.get('side', '-')})")
            st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
            st.markdown("### Collection Narrative")
            st.markdown(f"<p style='font-size:15px; line-height:1.7; color:#94A3B8;'>{pkg.get('description','')}</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📅 Live Consultation & Booking")
            st.markdown("[💬 Chat on Messenger](https://m.me/Rafiya.HennaArt) | [📱 WhatsApp Concierge](https://wa.me/8801323278403)")
            
    # --- ROUTE B: MAIN MARKETPLACE HOME ---
    else:
        col_hdr, col_sync = st.columns([8, 2])
        with col_hdr:
            st.markdown("""
            <div style="margin-top: 10px; margin-bottom: 25px;">
                <h1 style="font-size: 2.5rem; margin: 0; letter-spacing: 0.05em; color: #FFFFFF;">RAFIYA HENNA ART</h1>
                <p style="color: #C5A059; font-weight: 500; font-size: 11px; letter-spacing: 0.35em; text-transform: uppercase; margin-top: 4px; margin-bottom: 0;">Atelier & Design Studio</p>
            </div>
            """, unsafe_allow_html=True)
        with col_sync:
            st.markdown("<div style='margin-top:18px;'></div>", unsafe_allow_html=True)
            if st.button("🔄 Sync Ledger", use_container_width=True):
                run_interactive_pipeline()
                pkgs, crs, prds = fetch_live_studio_data()
                st.session_state.db_packages = pkgs
                st.session_state.db_courses = crs
                st.session_state.db_products = prds
                st.rerun()

        tab_chat, tab_packages, tab_courses, tab_products, tab_faq = st.tabs([
            "💬 Private Studio Lounge", "📦 Design Packages", "🎓 Training Programs", "🌿 Organic Products", "💡 Studio Knowledge Base"
        ])

        # --- TAB 1: ARTIST CHAT ---
        with tab_chat:
            st.markdown("### 🌿 Automated Assistant")
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

            st.markdown("<div style='background:rgba(148,163,184,0.04); border-radius:8px; padding:12px 16px; margin-top:20px; border:1px dashed rgba(255,255,255,0.08);'><p style='margin:0; font-size:11.5px; color:#64748B; line-height:1.4;'>⚠️ <b>Studio Note:</b> Automated details may contain minor variance and are optimized to provide immediate clarity when the artist is away. Please confirm pricing and active slot scheduling directly via personal text link.</p></div>", unsafe_allow_html=True)

        # --- TAB 2: DESIGN PACKAGES ---
        with tab_packages:
            if st.session_state.favorites:
                st.markdown(f"### ❤️ Saved Portfolio Vault ({len(st.session_state.favorites)})")
                saved_items = [p for p in packages if p.get('name') in st.session_state.favorites]
                display_package_grid(saved_items, prefix="vault")
                st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

            st.markdown("### 📦 Curated Portfolio Lookbook")
            st.markdown("<p style='font-size:13px; color:#64748B; margin-top:-10px;'>Filter our signature aesthetic sets by length, scale, alignment, or budget parameters.</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
            with col1:
                types = sorted(list(set(str(p.get('type', '')) for p in packages))) if packages else []
                sel_type = st.selectbox("Aesthetic Category", ["All"] + types)
            filtered = [p for p in packages if sel_type == "All" or str(p.get('type', '')) == sel_type]
            with col2:
                lengths = sorted(list(set(str(p.get('length', '')) for p in filtered))) if filtered else []
                sel_length = st.selectbox("Design Architecture", ["All"] + lengths)
            filtered = [p for p in filtered if sel_length == "All" or str(p.get('length', '')) == sel_length]
            with col3:
                hands = sorted(list(set(str(p.get('hand', '')) for p in filtered))) if filtered else []
                sel_hand = st.selectbox("Coverage Scale", ["All"] + hands)
            filtered = [p for p in filtered if sel_hand == "All" or str(p.get('hand', '')) == sel_hand]
            with col4:
                sides = sorted(list(set(str(p.get('side', '')) for p in filtered))) if filtered else []
                sel_surface = st.selectbox("Surface Alignment", ["All"] + sides)
            filtered = [p for p in filtered if sel_surface == "All" or str(p.get('side', '')) == sel_surface]
            with col5:
                prices = [float(p['price']) for p in filtered if p.get('price')]
                min_p, max_p = (min(prices), max(prices)) if prices else (0.0, 0.0)
                sel_price = st.slider("Budget Threshold (BDT)", int(min_p), int(max_p), int(max_p)) if min_p != max_p else max_p

            final_packages = [p for p in filtered if p.get('price') and float(p['price']) <= sel_price]
            display_package_grid(final_packages, prefix="catalog")

        # --- TAB 3: TRAINING PROGRAMS ---
        with tab_courses:
            st.markdown("### 🎓 Educational Atelier Workshops")
            st.markdown("<p style='font-size:13px; color:#64748B; margin-top:-10px;'>Develop professional skill tracks with intensive virtual or in-person mentorship options.</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            if courses:
                for c in courses:
                    with st.expander(f"📖 {c.get('course_title', 'Workshop')} — Sessions Start: {c.get('start_date','-')}", expanded=True):
                        col_info, col_off, col_on = st.columns(3)
                        with col_info:
                            st.markdown(f"**⏳ Structure:** {int(float(c['total_classes'])) if c.get('total_classes') else 0} Intensive Sessions\n\n**👥 Group Profile:** {c.get('eligibility','-')}\n\n**🎯 Career Milestone:** {c.get('outcome','-')}")
                        with col_off:
                            st.markdown(f"**📍 In-Person Studio classes:**\n\n* Rate: **{int(float(c['offline_fee'])) if c['offline_fee'] else 0} BDT**\n* Timeline: {c.get('offline_days','-')} ({c.get('offline_time','-')})\n* Hub: {c.get('offline_location','-')}")
                        with col_on:
                            st.markdown(f"**🌐 Live Virtual Classroom:**\n\n* Rate: **{int(float(c['online_fee'])) if c['online_fee'] else 0} BDT**\n* Timeline: {c.get('online_days','-')} ({c.get('online_time','-')})\n* Engine: {c.get('online_platform','-')}")
            else:
                st.info("No active training workshops registered in the database.")

        # --- TAB 4: ORGANIC PRODUCTS ---
        with tab_products:
            st.markdown("### 🌿 Handcrafted Stain Materials")
            st.markdown("<p style='font-size:13px; color:#64748B; margin-top:-10px;'>Shop chemical-free, premium cones formulated exclusively with 100% natural, halal ingredients.</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            if products:
                for prd in products:
                    st.markdown(f'<div style="border: 1px solid #2C323F; background: #121620; padding: 22px; border-radius: 12px; margin-bottom: 12px;"><h4 style="margin:0 0 4px 0; color: #C5A059; font-size:18px;">✨ {prd.get("product_name", "Handcrafted Cone")}</h4><p style="margin:0 0 12px 0; font-size:13px; color:#94A3B8;">{prd.get("description","")}</p><span style="font-family:\'Marcellus\', serif; font-size:15px; color:#FFF;">Base Rate: {int(float(prd["mrp"])) if prd.get("mrp") else 0} BDT</span></div>', unsafe_allow_html=True)
            else:
                st.info("No retail products available in the collection at this time.")

        # --- TAB 5: FAQ KNOWLEDGE BASE ---
        with tab_faq:
            st.markdown("### 💡 Studio Learning & Care Knowledge Base")
            st.markdown("<p style='font-size:13px; color:#64748B; margin-top:-10px;'>Review comprehensive details regarding operational home services and essential scheduling parameters.</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            if faq_data:
                for cat in sorted(list(set(faq['category'] for faq in faq_data))):
                    st.markdown(f"#### 📁 {cat.upper()}")
                    for faq in [f for f in faq_data if f['category'] == cat]:
                        with st.expander(f"✨ {faq['question']}", expanded=False):
                            st.markdown(f'<div style="background-color: #0A0D14; padding: 18px; border-left: 2px solid #C5A059; border-radius: 4px; color: #94A3B8; font-size: 14px; line-height: 1.7;">{faq["answer"]}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
