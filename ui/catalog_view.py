from __future__ import annotations

from typing import Any, Dict, List, Optional
import streamlit as st

def display_package_grid(package_list: List[Dict[str, Any]], prefix: str):
    """Displays a responsive portfolio grid separating Bridal vs Non-Bridal aesthetics."""
    if not package_list:
        st.info("No henna packages matched your selected filter criteria.")
        return

    # 3-column grid gives ample card width so all details and button texts show completely
    for idx, item in enumerate(package_list):
        if idx % 3 == 0:
            cols = st.columns(3)

        col = cols[idx % 3]
        with col:
            is_loved = item["name"] in st.session_state.favorites
            love_icon = "❤️ Saved" if is_loved else "🤍 Save Look"

            is_bridal = "bridal" in item.get("type", "").lower() and "non-bridal" not in item.get("type", "").lower()
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

            st.markdown(
                f"""
                <div style="border-radius: 12px; padding: 22px; display: flex; flex-direction: column; 
                     justify-content: space-between; height: 330px; margin-bottom: 12px; {card_style}">
                    <div>
                        <span style="font-size: 9px; font-weight: 600; padding: 4px 10px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.05em; {badge_style}">
                            {item.get('type', 'Custom')}
                        </span>
                        <h3 style="margin-top: 14px; margin-bottom: 4px; font-size: 17px; line-height: 1.3; color: {title_color};">{item['name']}</h3>
                        <div style="font-size:11px; color: #64748B; margin-bottom: 10px;">📐 {item.get('length', 'Full')} • ✋ {item.get('hand', 'Both Hands')}</div>
                        <p style="color: #94A3B8; font-size: 12.5px; overflow-y: auto; max-height: 85px; line-height: 1.5;">
                            {item.get('description', '')}
                        </p>
                    </div>
                    <div style="border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px; font-family: 'Marcellus', serif; font-size: 16px; color: #C5A059;">
                        {item.get('price', 0)} BDT
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("📖 View Look", key=f"det_{prefix}_{idx}_{item['name']}", use_container_width=True):
                    st.session_state.selected_package = item
                    st.rerun()
            with btn_col2:
                if st.button(love_icon, key=f"fav_{prefix}_{idx}_{item['name']}", use_container_width=True):
                    if is_loved:
                        st.session_state.favorites.remove(item["name"])
                        st.toast(f"Removed {item['name']} from lookbook.", icon="🗑️")
                    else:
                        st.session_state.favorites.add(item["name"])
                        st.toast(f"Saved {item['name']} to lookbook!", icon="❤️")
                    st.rerun()


def render_saved_view(packages: List[Dict[str, Any]]):
    """Renders the dedicated Saved Portfolio Vault tab."""
    st.markdown("### ❤️ Saved Portfolio Vault")
    st.markdown(
        "<p style='font-size:13.5px; color:#94A3B8; margin-top:-6px;'>"
        "Your private curated lookbook of favorite designs. Save designs to keep them here for quick review or booking."
        "</p>",
        unsafe_allow_html=True,
    )

    if st.session_state.favorites:
        saved_items = [p for p in packages if p["name"] in st.session_state.favorites]
        display_package_grid(saved_items, prefix="vault")
    else:
        st.info(
            "✨ Your lookbook vault is currently empty!\n\n"
            "Browse through the **Curated Collections** tab and click **'🤍 Save Look'** on any package to save it here."
        )


def render_catalog_view(packages: List[Dict[str, Any]]):
    """Renders the complete packages lookbook catalog with filter matrix."""
    st.markdown("### 📦 Portfolio Matrix Lookbook")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])

    with col1:
        types = sorted(list(set(p.get("type", "General") for p in packages)))
        sel_type = st.selectbox("Aesthetic Category", ["All"] + types)
    filtered = [p for p in packages if sel_type == "All" or p.get("type") == sel_type]

    with col2:
        lengths = sorted(list(set(p.get("length", "") for p in filtered if p.get("length"))))
        sel_length = st.selectbox("Design Architecture", ["All"] + lengths)
    filtered = [p for p in filtered if sel_length == "All" or p.get("length") == sel_length]

    with col3:
        hands = sorted(list(set(p.get("hand", "") for p in filtered if p.get("hand"))))
        sel_hand = st.selectbox("Coverage Scale", ["All"] + hands)
    filtered = [p for p in filtered if sel_hand == "All" or p.get("hand") == sel_hand]

    with col4:
        sides = sorted(list(set(p.get("side", "") for p in filtered if p.get("side"))))
        sel_surface = st.selectbox("Surface Alignment", ["All"] + sides)
    filtered = [p for p in filtered if sel_surface == "All" or p.get("side") == sel_surface]

    with col5:
        prices = [int(p.get("price", 0)) for p in filtered if isinstance(p.get("price"), (int, float))]
        min_p, max_p = (min(prices), max(prices)) if prices else (0, 0)
        if min_p == max_p:
            st.number_input("Budget Threshold (BDT)", value=max_p, disabled=True)
            sel_price = max_p
        else:
            sel_price = st.slider("Budget Threshold (BDT)", int(min_p), int(max_p), int(max_p))

    final_packages = [p for p in filtered if int(p.get("price", 0)) <= sel_price]
    display_package_grid(final_packages, prefix="catalog")


def render_package_detail(pkg: Dict[str, Any]):
    """Renders full deep-dive design specs and direct booking for a selected look."""
    if st.button("← Return to Lookbook Catalog", use_container_width=True):
        st.session_state.selected_package = None
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])

    with col1:
        is_bridal = "bridal" in pkg.get("type", "").lower() and "non-bridal" not in pkg.get("type", "").lower()
        border_clr = "#C5A059" if is_bridal else "#2C323F"

        st.markdown(
            f"""
            <div style="border: 1px solid {border_clr}; border-radius: 12px; padding: 36px 24px; 
                 background: #121620; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
                <div style="font-size: 52px; margin-bottom: 12px;">🌿</div>
                <span style="background: rgba(197,160,89,0.15); color: #C5A059; font-size: 11px; font-weight: 600; padding: 6px 14px; border-radius: 4px; text-transform: uppercase;">
                    {pkg.get('type', 'Custom')}
                </span>
                <h2 style="margin-top: 20px; color: white; font-size: 26px;">{pkg['name']}</h2>
                <h1 style="color: #C5A059; margin-top: 15px; font-family: 'Marcellus', serif; font-size: 32px;">{pkg.get('price')} BDT</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(f"## Design Specifications")
        st.markdown(f"**📐 Artistry Length Extension:** {pkg.get('length', 'Custom')}")
        st.markdown(f"**✋ Coverage Scale:** {pkg.get('hand', 'Both Hands')} ({pkg.get('side', 'Both Sides')})")
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
        st.markdown(f"### Collection Narrative")
        st.markdown(f"<p style='font-size:15px; line-height:1.7; color:#94A3B8;'>{pkg.get('description', '')}</p>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📅 Live Consultation & Booking")
        st.markdown(
            "Reserve this look for your special occasion. Direct booking channels:\n\n"
            "[💬 Chat on Messenger](https://m.me/Rafiya.HennaArt) | "
            "[📱 WhatsApp Concierge](https://wa.me/8801323278403) | "
            "[✉️ Direct Email Studio](mailto:rafiyashennaart@gmail.com)"
        )
