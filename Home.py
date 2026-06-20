import streamlit as st
import google.generativeai as genai
import langdetect
import logging
import pandas as pd
import requests
import time
import io
import os
from difflib import SequenceMatcher
from typing import Dict, Tuple, Optional, List

# ---------------------------
# Logging Configuration
# ---------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
# Core Constants & GSheet Path
# ---------------------------
SHEET_ID = "1n8b5WCeHAeCrMeM_GhxsUGKmT3CILMnrm8a8yYxWaPU"
# Export endpoints targeting distinct structural workspace tabs
PACKAGES_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
COURSES_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=courses"
PRODUCTS_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&sheet=products"

CSV_PATH_PACKAGES = "data_packages.csv"
CSV_PATH_COURSES = "data_courses.csv"
CSV_PATH_PRODUCTS = "data_products.csv"

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
# Interactive Data Sync Pipeline
# ---------------------------
def sync_live_sheets_pipeline():
    """Downloads remote cloud sheets data interactively streaming structural logs directly onto the layout."""
    status_box = st.empty()
    progress_bar = st.progress(0)
    
    with status_box.container():
        st.markdown("### 🔄 Triggering Studio Sync Pipeline...")
        st.caption("Establishing connections to the master ledger architecture...")
    
    try:
        # Step 1: Packages Extraction
        time.sleep(0.4)
        progress_bar.progress(25)
        with status_box.container():
            st.markdown("### 📥 Pulling Curated Collections Lookbook...")
            st.caption("Downloading package rates matrix tables...")
        df_pkg = pd.read_csv(PACKAGES_CSV_URL)
        df_pkg.to_csv(CSV_PATH_PACKAGES, index=False)

        # Step 2: Courses Extraction
        time.sleep(0.4)
        progress_bar.progress(55)
        with status_box.container():
            st.markdown("### 📥 Syncing Academy Training Schedules...")
            st.caption("Parsing course syllabus, parameters and dates blocks...")
        try:
            df_crs = pd.read_csv(COURSES_CSV_URL)
        except Exception:
            # Fallback mock template framework generation if tab name lacks default binding matching gid sequence
            df_crs = pd.DataFrame(columns=["course_title","start_date","total_classes","eligibility","outcome","offline_fee","online_fee"])
        df_crs.to_csv(CSV_PATH_COURSES, index=False)

        # Step 3: Products Extraction
        time.sleep(0.4)
        progress_bar.progress(85)
        with status_box.container():
            st.markdown("### 📥 Loading Organic Inventory Cones Matrix...")
            st.caption("Verifying Halal materials and pricing parameters...")
        try:
            df_prd = pd.read_csv(PRODUCTS_CSV_URL)
        except Exception:
            df_prd = pd.DataFrame(columns=["product_name","description","mrp","details"])
        df_prd.to_csv(CSV_PATH_PRODUCTS, index=False)

        # Finished Pipeline Execution Sequence
        time.sleep(0.3)
        progress_bar.progress(100)
        status_box.success("🎉 Studio Pipeline Sync Complete! All data stored locally as pristine CSV files.")
        time.sleep(0.8)
        status_box.empty()
        progress_bar.empty()
    except Exception as error:
        status_box.error(f"❌ Critical Pipeline Disruption: {error}")
        progress_bar.empty()

def read_local_csv_safely(file_path: str) -> pd.DataFrame:
    """Helper layout logic to return data or mock dataframe framework if absent."""
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

# ---------------------------
# Core AI Prompt Engineering Matrix
# ---------------------------
class AgenticAI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.configure_ai()

    def configure_ai(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            generation_config={
                "temperature": 0.15,
                "top_p": 0.85,
                "max_output_tokens": 256,
            },
        )
        self.chat_session = self.model.start_chat()

    def generate_response(self, user_input: str, csv_context: str) -> str:
        try:
            prompt = (
                f"DATABASE CSV FILES CONTEXT RECORD LOGS:\n{csv_context}\n\n"
                f"User Query: {user_input}\n\n"
                "You are Rafiya, a creative and friendly henna artist 🌿✨. "
                "Respond accurately and naturally matching the user's input language tone. "
                "CRITICAL DIRECTION: Rely exclusively on the CSV context provided above to derive answers. "
                "Keep your response extremely short, concise, and focused to a summary style. Avoid introductions or conversational fluff. "
                "Always point users to direct contact pipelines when unsure:\n"
                "💬 [Messenger](https://m.me/Rafiya.HennaArt) | 📱 [WhatsApp](https://wa.me/8801323278403)"
            )
            response = self.chat_session.send_message(prompt)
            return response.text.strip() if response and hasattr(response, "text") else "🤖 Studio offline. Drop a text query via WhatsApp!"
        except Exception as e:
            logger.error(f"Error parsing text output: {e}")
            return "🤖 Unable to compile response loop. Connect directly via messenger link!"

# ---------------------------
# Production-Safe Premium CSS Injector
# ---------------------------
def apply_premium_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Marcellus&family=Montserrat:wght@400;500;600&display=swap');
        .stApp { background: radial-gradient(circle at top right, #161A24, #0A0D14) !important; color: #E2E8F0 !important; font-family: 'Montserrat', sans-serif; }
        h1, h2, h3, h4 { font-family: 'Marcellus', serif !important; color: #F8FAFC !important; font-weight: 400 !important; }
        div[data-baseweb="select"] > div { border: 1px solid #2C323F !important; border-radius: 8px !important; background-color: #121620 !important; }
        div[data-baseweb="select"] span, div[data-baseweb="select"] div { color: #E2E8F0 !important; }
        .stButton>button { background: transparent !important; color: #C5A059 !important; border: 1px solid #C5A059 !important; border-radius: 4px !important; padding: 8px 20px !important; font-size: 12px !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.1em; transition: all 0.3s ease !important; }
        .stButton>button:hover { transform: translateY(-1px) !important; background: #C5A059 !important; color: #0A0D14 !important; box-shadow: 0 4px 15px rgba(197, 160, 89, 0.2) !important; }
        .stSlider [role="slider"] { background-color: #C5A059 !important; }
        button[data-baseweb="tab"] { color: #64748B !important; font-family: 'Marcellus', serif !important; font-size: 15px !important; letter-spacing: 0.05em; }
        button[aria-selected="true"] { color: #C5A059 !important; border-bottom-color: #C5A059 !important; }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------
# Visual Component Layout Helpers
# ---------------------------
def display_package_grid(package_list: List[Dict], prefix: str):
    """Displays a responsive portfolio matrix distinguishing Bridal vs Daily collections."""
    for idx, item in enumerate(package_list):
        if idx % 4 == 0:
            cols = st.columns(4)
        col = cols[idx % 4]
        with col:
            is_loved = item['name'] in st.session_state.favorites
            love_icon = "❤️ Saved" if is_loved else "🤍 Save Look"
            is_bridal = "bridal" in str(item.get('type', '')).lower()
            
            card_style = "border: 1px solid #C5A059; background: linear-gradient(135deg, #181C26, #0A0D14);" if is_bridal else "border: 1px solid #2C323F; background: #121620;"
            badge_style = "background: rgba(197, 160, 89, 0.15); color: #C5A059;" if is_bridal else "background: rgba(148, 163, 184, 0.1); color: #94A3B8;"
            
            st.markdown(f"""
            <div style="border-radius: 12px; padding: 22px; display: flex; flex-direction: column; justify-content: space-between; height: 340px; margin-bottom: 12px; {card_style}">
                <div>
                    <span style="font-size: 9px; font-weight: 600; padding: 4px 10px; border-radius: 4px; text-transform: uppercase; {badge_style}">
                        {item['type']}
                    </span>
                    <h3 style="margin-top: 16px; margin-bottom: 4px; font-size: 18px; line-height: 1.3;">{item['name']}</h3>
                    <div style="font-size:11px; color: #64748B; margin-bottom: 12px;">📐 {item['length']} • ✋ {item['hand']}</div>
                    <p style="color: #94A3B8; font-size: 13px; overflow-y: auto; max-height: 95px; line-height: 1.5;">{item['description']}</p>
                </div>
                <div style="font-family: 'Marcellus', serif; font-size: 16px; color: #C5A059;">{item['price']} BDT</div>
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
    api_key = st.secrets.get("genai", {}).get("api_key", "")
    
    # Run pipeline automatically to generate CSV files if they don't exist yet
    if not os.path.exists(CSV_PATH_PACKAGES):
        sync_live_sheets_pipeline()

    # Load data from local optimized CSV structures
    df_p = read_local_csv_safely(CSV_PATH_PACKAGES)
    df_c = read_local_csv_safely(CSV_PATH_COURSES)
    df_r = read_local_csv_safely(CSV_PATH_PRODUCTS)
    
    packages_list = df_p.to_dict(orient="records") if not df_p.empty else []

    # Compile compressed text context arrays to optimize runtime token usage
    context_str = f"PACKAGES METRIC:\n{df_p.to_string(index=False)}\n\nCOURSES SCHEDULE:\n{df_c.to_string(index=False)}\n\nPRODUCTS LEDGER:\n{df_r.to_string(index=False)}"
    agentic_ai = AgenticAI(api_key=api_key)

    # Sidebar Pipeline Automation Controls
    with st.sidebar:
        st.markdown("### 🛠️ Data Infrastructure")
        st.caption("Synchronize operational ledgers with your live Google Sheets workspace.")
        if st.button("🔄 Sync Live Database", use_container_width=True):
            sync_live_sheets_pipeline()
            st.rerun()

    # Deep-dive screen overlay checks
    if st.session_state.selected_package:
        pkg = st.session_state.selected_package
        if st.button("← Return to Lookbook Catalog", use_container_width=True):
            st.session_state.selected_package = None
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div style="border: 1px solid #C5A059; border-radius: 12px; padding: 40px; background: #121620; text-align: center;">
                <div style="font-size: 50px; margin-bottom: 15px;">🌿</div>
                <h2 style="color: white; font-size: 28px;">{pkg['name']}</h2>
                <h1 style="color: #C5A059; margin-top: 15px; font-size: 32px;">{pkg['price']} BDT</h1>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"## Design Architecture Specifications")
            st.write(f"**📐 Extent Dimensions:** {pkg['length']} | **✋ Surface Distribution:** {pkg['hand']} ({pkg['side']})")
            st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
            st.write(pkg['description'])
            st.markdown("---")
            st.markdown("[💬 Book on Messenger](https://m.me/Rafiya.HennaArt) \| [📱 Consult on WhatsApp](https://wa.me/8801323278403)")
            
    else:
        # Editorial Luxury Branding Banner
        st.markdown("""
        <div style="text-align: center; margin-top: 20px; margin-bottom: 35px;">
            <h1 style="font-size: 2.6rem; margin: 0; letter-spacing: 0.05em; color: #FFFFFF;">RAFIYA HENNA ART</h1>
            <p style="color: #C5A059; font-weight: 500; font-size: 11px; letter-spacing: 0.35em; text-transform: uppercase; margin-top: 4px; margin-bottom: 0;">Atelier & Design Studio</p>
        </div>
        """, unsafe_allow_html=True)

        # Tab Navigation Architecture Sequences
        tab_chat, tab_packages, tab_courses, tab_products = st.tabs([
            "💬 Private Studio Lounge", 
            "🎨 Curated Collections", 
            "🎓 Studio Academy",
            "🌿 Handcrafted Inventory"
        ])

        # --- TAB 1: INTERACTIVE LLM CHAT ASSISTANT ---
        with tab_chat:
            st.markdown(f"### 🌿 Automated Assistant")
            for chat in st.session_state.chat_history:
                if chat['user']:
                    with st.chat_message("user"):
                        st.markdown(f"""<div style="background:#1E293B; color:#F1F5F9; padding:12px 16px; border-radius:12px; font-size:14.5px; border: 1px solid #334155; max-width: 80%; margin-left: auto;">{chat['user']}</div>""", unsafe_allow_html=True)
                with st.chat_message("assistant"):
                    st.markdown(f"""<div style="background:#121620; color:#E2E8F0; padding:12px 16px; border-radius:12px; font-size:14.5px; border: 1px solid #C5A059; max-width: 85%;"><b>Henna Whisperer:</b><br>{chat['bot']}</div>""", unsafe_allow_html=True)

            user_query = st.chat_input("Ask Henna Whisperer about custom catalog tracks or processing metrics...")
            if user_query:
                with st.chat_message("user"):
                    st.markdown(f"""<div style="background:#1E293B; padding:12px 16px; border-radius:12px;">{user_query}</div>""", unsafe_allow_html=True)
                with st.spinner("Weaving insight logs..."):
                    reply = agentic_ai.generate_response(user_query, context_str)
                with st.chat_message("assistant"):
                    st.markdown(f"""<div style="background:#121620; padding:12px 16px; border-radius:12px; border: 1px solid #C5A059;">{reply}</div>""", unsafe_allow_html=True)
                st.session_state.chat_history.append({"user": user_query, "bot": reply})
                st.rerun()

            st.markdown("<p style='font-size:11px; color:#64748B; margin-top:20px;'>⚠️ <b>Disclaimer:</b> Automated details are pulled directly from local CSV snapshots to assist while offline. Confirm final values with the team before scheduling.</p>", unsafe_allow_html=True)

        # --- TAB 2: PORTFOLIO COLLECTIONS CATALOG ---
        with tab_packages:
            if st.session_state.favorites:
                st.markdown(f"### ❤️ Saved Portfolio Vault ({len(st.session_state.favorites)})")
                saved_items = [p for p in packages_list if p['name'] in st.session_state.favorites]
                display_package_grid(saved_items, prefix="vault")
                st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

            st.markdown("### 📦 Collections Lookbook")
            if packages_list:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    types = sorted(list(set(str(p['type']) for p in packages_list)))
                    sel_type = st.selectbox("Aesthetic Category", ["All"] + types)
                filtered = [p for p in packages_list if sel_type == "All" or str(p['type']) == sel_type]
                
                with col2:
                    lengths = sorted(list(set(str(p['length']) for p in filtered)))
                    sel_length = st.selectbox("Design Extension", ["All"] + lengths)
                filtered = [p for p in filtered if sel_length == "All" or str(p['length']) == sel_length]
                
                with col3:
                    hands = sorted(list(set(str(p['hand']) for p in filtered)))
                    sel_hand = st.selectbox("Hand Count Scale", ["All"] + hands)
                filtered = [p for p in filtered if sel_hand == "All" or str(p['hand']) == sel_hand]
                
                with col4:
                    prices = [float(p['price']) for p in filtered if str(p['price']).isdigit()]
                    max_p = max(prices) if prices else 10000.0
                    sel_price = st.slider("Budget Threshold (BDT)", 0, int(max_p), int(max_p))

                final_packages = [p for p in filtered if str(p['price']).isdigit() and float(p['price']) <= sel_price]
                display_package_grid(final_packages, prefix="catalog")
            else:
                st.info("No package logs found. Trigger a data synchronization pipeline loop via the sidebar.")

        # --- TAB 3: STUDIO ACADEMY TRAINING PATHS ---
        with tab_courses:
            st.markdown("### 🎓 Training Program Masterplan")
            if not df_c.empty:
                for _, row in df_c.iterrows():
                    with st.expander(f"✨ Course: {row.get('course_title', 'Bespoke Track')}", expanded=True):
                        col_l, col_r = st.columns(2)
                        with col_l:
                            st.markdown(f"**📅 Commencement:** {row.get('start_date', 'N/A')}")
                            st.markdown(f"**⏳ Instructional Duration:** {row.get('total_classes', '6')} Sessions")
                            st.markdown(f"**🎯 Target Eligibility:** {row.get('eligibility', 'All Profiles')}")
                        with col_r:
                            st.markdown(f"**🏛️ Atelier Track Fee:** {row.get('offline_fee', 'N/A')} BDT")
                            st.markdown(f"**🌐 Virtual Live Stream Fee:** {row.get('online_fee', 'N/A')} BDT")
                        st.markdown(f"**🔮 Core Focus Outcomes:** *{row.get('outcome', '')}*")
            else:
                st.info("No active course tracking data extracted yet.")

        # --- TAB 4: HANDCRAFTED APPARATUS INVENTORY ---
        with tab_products:
            st.markdown("### 🌿 Raw Organic Botanical Materials")
            if not df_r.empty:
                for _, row in df_r.iterrows():
                    st.markdown(f"""
                    <div style='border: 1px solid #2C323F; padding: 20px; border-radius: 8px; background: #121620; margin-bottom: 12px;'>
                        <h4 style='margin:0; color:#C5A059;'>{row.get('product_name', 'Henna Cone')}</h4>
                        <p style='font-size:13px; color:#94A3B8; margin: 8px 0;'>{row.get('description', '')}</p>
                        <span style='font-weight:600; color:white;'>🏷️ Retail Rate: {row.get('mrp', '0')} BDT</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No physical retail items indexed.")

if __name__ == "__main__":
    main()
