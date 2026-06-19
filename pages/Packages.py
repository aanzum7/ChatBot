import streamlit as st
from utils.theme import inject_global_theme, render_header, CONFIG

class SocialPackageShowcase:
    def __init__(self, packages):
        self.packages = packages
        if "visible_packages_count" not in st.session_state:
            st.session_state.visible_packages_count = 4

    def render_filters(self):
        # Premium Modern Filter Bar
        st.markdown(f"<p style='color:{CONFIG['accent_rose_gold']}; font-weight:700; margin-bottom:2px;'>⚙️ FILTER COLLECTION</p>", unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
        
        with col1:
            types = sorted(list(set(p['type'] for p in self.packages)))
            sel_type = st.selectbox("Category", ["All"] + types)
        filtered = [p for p in self.packages if sel_type == "All" or p['type'] == sel_type]
        
        with col2:
            lengths = sorted(list(set(p['length'] for p in filtered)))
            sel_length = st.selectbox("Length", ["All"] + lengths)
        filtered = [p for p in filtered if sel_length == "All" or p['length'] == sel_length]
        
        with col3:
            hands = sorted(list(set(p['hand'] for p in filtered)))
            sel_hand = st.selectbox("Hands", ["All"] + hands)
        filtered = [p for p in filtered if sel_hand == "All" or p['hand'] == sel_hand]
        
        with col4:
            sides = sorted(list(set(p['side'] for p in filtered)))
            sel_side = st.selectbox("Side", ["All"] + sides)
        filtered = [p for p in filtered if sel_side == "All" or p['side'] == sel_side]
        
        with col5:
            prices = [p['price'] for p in filtered]
            min_p, max_p = (min(prices), max(prices)) if prices else (0, 0)
            if min_p == max_p:
                st.number_input("Budget Cap (BDT)", value=max_p, disabled=True)
                sel_price = max_p
            else:
                sel_price = st.slider("Budget Cap (BDT)", int(min_p), int(max_p), int(max_p))

        current_sig = f"{sel_type}-{sel_length}-{sel_hand}-{sel_side}-{sel_price}"
        if st.session_state.get("last_filter_sig") != current_sig:
            st.session_state.visible_packages_count = 4
            st.session_state.last_filter_sig = current_sig

        return [p for p in filtered if p['price'] <= sel_price]

    def display_grid(self, matched_packages):
        if not matched_packages:
            st.warning("No design drops found matching current active filters.")
            return

        visible_pool = matched_packages[:st.session_state.visible_packages_count]

        # Fluid social catalog layout format (4 Columns)
        for idx in range(0, len(visible_pool), 4):
            row_items = visible_pool[idx:idx+4]
            cols = st.columns(4)
            for col, item in zip(cols, row_items):
                with col:
                    st.markdown(f"""
                    <div style="border: 1px solid {CONFIG['border_color']}; border-radius: 20px; padding: 20px; 
                         background: {CONFIG['card_bg']}; display: flex; flex-direction: column; 
                         justify-content: space-between; height: 380px; margin-bottom: 20px;
                         box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: transform 0.3s ease;">
                        <div>
                            <span style="background: rgba(214,175,55,0.1); color: {CONFIG['accent_rose_gold']}; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 20px; text-transform: uppercase;">
                                {item['type']}
                            </span>
                            <h3 style="margin-top: 14px; margin-bottom: 8px; font-size: 18px;">{item['name']}</h3>
                            <div style="font-size:12px; color: #9CA3AF; margin: 4px 0;">📏 {item['length']} • ✋ {item['hand']} ({item['side']})</div>
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

        if len(matched_packages) > st.session_state.visible_packages_count:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✨ LOAD MORE PACKAGES", use_container_width=True):
                st.session_state.visible_packages_count += 4
                st.rerun()

def main():
    inject_global_theme("Collections", "📦")
    if st.button("← RETURN TO LOUNGE"):
        st.switch_page("Home.py")
        
    render_header("Artistic Collections", "Curated Luxury Bridal & Event Packages")

    packages = st.secrets.get("personal", {}).get("data", {}).get("packages", [])
    if not packages:
        st.info("No package vectors available.")
        return

    engine = SocialPackageShowcase(packages)
    engine.display_grid(engine.render_filters())

if __name__ == "__main__":
    main()
