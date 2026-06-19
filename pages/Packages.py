import streamlit as st
from utils.theme import inject_global_theme, render_header, CONFIG

class PackageShowcaseEngine:
    def __init__(self, packages):
        self.packages = packages
        if "visible_packages_count" not in st.session_state:
            st.session_state.visible_packages_count = 4

    def render_filters(self):
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])
        
        with col1:
            types = sorted(list(set(p['type'] for p in self.packages)))
            sel_type = st.selectbox("Style Type", ["All"] + types)
            
        filtered = [p for p in self.packages if sel_type == "All" or p['type'] == sel_type]
        
        with col2:
            lengths = sorted(list(set(p['length'] for p in filtered)))
            sel_length = st.selectbox("Extension", ["All"] + lengths)
            
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
                st.number_input("Max Budget (BDT)", value=max_p, disabled=True)
                sel_price = max_p
            else:
                sel_price = st.slider("Max Budget (BDT)", int(min_p), int(max_p), int(max_p))

        # Dynamic structural signature state management
        current_sig = f"{sel_type}-{sel_length}-{sel_hand}-{sel_side}-{sel_price}"
        if st.session_state.get("last_filter_sig") != current_sig:
            st.session_state.visible_packages_count = 4
            st.session_state.last_filter_sig = current_sig

        return [p for p in filtered if p['price'] <= sel_price]

    def display_grid(self, matched_packages):
        if not matched_packages:
            st.warning("No artistry packages match your chosen layout configurations.")
            return

        visible_pool = matched_packages[:st.session_state.visible_packages_count]

        # Renders standard 4-column balanced card matrices
        for idx in range(0, len(visible_pool), 4):
            row_items = visible_pool[idx:idx+4]
            cols = st.columns(4)
            for col, item in zip(cols, row_items):
                with col:
                    st.markdown(f"""
                    <div style="border:2px solid {CONFIG['accent_gold']}; border-radius:12px; padding:16px; 
                         background:{CONFIG['card_bg']}; box-shadow:0 4px 10px {CONFIG['card_shadow']}; 
                         display:flex; flex-direction:column; justify-content:space-between; height:390px; margin-bottom:16px;">
                        <div>
                            <h3 style="margin-top:0; margin-bottom:8px; font-size:17px; line-height:1.2;">{item['name']}</h3>
                            <div style="font-size:12px; margin:2px 0;"><b>🏷️ Style:</b> {item['type']}</div>
                            <div style="font-size:12px; margin:2px 0;"><b>📏 Length:</b> {item['length']}</div>
                            <div style="font-size:12px; margin:2px 0;"><b>✋ Scope:</b> {item['hand']} ({item['side']})</div>
                            <p style="color:{CONFIG['bot_text']}; font-size:12px; margin-top:8px; overflow-y:auto; max-height:140px; line-height:1.4;">{item['description']}</p>
                        </div>
                        <div style="color:{CONFIG['user_text']}; font-weight:bold; font-size:15px; border-top:1px dashed #DDD; padding-top:6px; margin-top:6px;">
                            Price: {item['price']} BDT
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        if len(matched_packages) > st.session_state.visible_packages_count:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🌿 Expand Additional Packages", use_container_width=True):
                st.session_state.visible_packages_count += 4
                st.rerun()

def main():
    inject_global_theme("Packages", "📦")
    if st.button("← Back to Lounge Home"):
        st.switch_page("Home.py")
        
    render_header("Artistry Portfolios", "Pick the perfect henna package for your special occasion!")

    packages = st.secrets.get("personal", {}).get("data", {}).get("packages", [])
    if not packages:
        st.info("No package listings found in configuration secrets.")
        return

    engine = PackageShowcaseEngine(packages)
    engine.display_grid(engine.render_filters())

if __name__ == "__main__":
    main()
