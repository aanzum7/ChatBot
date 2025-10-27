import streamlit as st

# 🎨 GLOBAL COLOR PALETTE (Mehendi Theme)
BACKGROUND_COLOR = "#f9f7f1"      # Cream background
TEXT_COLOR = "#3b3a36"            # Dark earthy brown
HEADER_COLOR = "#6b8e23"          # Olive green
CARD_BORDER = "#b8860b"           # Goldenrod
CARD_BG = "#ffffff"                # White for contrast
CARD_SHADOW = "rgba(0,0,0,0.08)"  # Soft shadow
PRICE_COLOR = "#2f4f2f"           # Deep green
DESC_COLOR = "#5b4636"            # Warm brown
BUTTON_HOVER_COLOR = "#a07400"    # Darker gold hover
SLIDER_GRADIENT_ACTIVE = f"linear-gradient(to right, {CARD_BORDER}, {BUTTON_HOVER_COLOR})"

# ---------- FILTER CLASS ----------
class PackageFilter:
    def __init__(self, packages):
        self.packages = packages
        self.selected_type = "All"
        self.selected_length = "All"
        self.selected_hand = "All"
        self.selected_side = "All"
        self.selected_price = 0

    def render_filters(self):
        types = sorted(set(p['type'] for p in self.packages))
        col1, col2, col3, col4, col5 = st.columns([1,1,1,1,2])

        with col1:
            self.selected_type = st.selectbox("Type", ["All"] + types)

        lengths = sorted(set(
            p['length'] for p in self.packages
            if self.selected_type == "All" or p['type'] == self.selected_type
        ))
        with col2:
            self.selected_length = st.selectbox("Length", ["All"] + lengths)

        hands = sorted(set(
            p['hand'] for p in self.packages
            if (self.selected_type == "All" or p['type'] == self.selected_type) and
               (self.selected_length == "All" or p['length'] == self.selected_length)
        ))
        with col3:
            self.selected_hand = st.selectbox("Hand", ["All"] + hands)

        sides = sorted(set(
            p['side'] for p in self.packages
            if (self.selected_type == "All" or p['type'] == self.selected_type) and
               (self.selected_length == "All" or p['length'] == self.selected_length) and
               (self.selected_hand == "All" or p['hand'] == self.selected_hand)
        ))
        with col4:
            self.selected_side = st.selectbox("Side", ["All"] + sides)

        price_filtered = [
            p['price'] for p in self.packages
            if (self.selected_type == "All" or p['type'] == self.selected_type) and
               (self.selected_length == "All" or p['length'] == self.selected_length) and
               (self.selected_hand == "All" or p['hand'] == self.selected_hand) and
               (self.selected_side == "All" or p['side'] == self.selected_side)
        ]
        min_price, max_price = (min(price_filtered), max(price_filtered)) if price_filtered else (0, 0)

        with col5:
            if min_price == max_price:
                self.selected_price = st.number_input(
                    "Max Price (BDT)", value=max_price, disabled=True)
            else:
                self.selected_price = st.slider(
                    "Max Price (BDT)", min_price, max_price, max_price)

    def get_filter_tuple(self):
        return (self.selected_type, self.selected_length, self.selected_hand, self.selected_side, self.selected_price)

    def apply_filters(self):
        filtered = [
            p for p in self.packages
            if (self.selected_type == "All" or p['type'] == self.selected_type) and
               (self.selected_length == "All" or p['length'] == self.selected_length) and
               (self.selected_hand == "All" or p['hand'] == self.selected_hand) and
               (self.selected_side == "All" or p['side'] == self.selected_side) and
               p['price'] <= self.selected_price
        ]
        return filtered

# ---------- DISPLAY CLASS ----------
class PackageDisplay:
    def __init__(self, filtered_packages):
        self.filtered = filtered_packages
        if "show_all" not in st.session_state:
            st.session_state.show_all = False
        if "show_more_clicked" not in st.session_state:
            st.session_state.show_more_clicked = False

    def reset_show_more_clicked(self):
        st.session_state.show_more_clicked = False

    def display_cards(self):
        display_data = self.filtered if st.session_state.show_all else self.filtered[:4]

        # Display cards in rows of up to 4
        for i in range(0, len(display_data), 4):
            row_cards = display_data[i:i+4]
            cols = st.columns(len(row_cards))
            for col, pkg in zip(cols, row_cards):
                with col:
                    self.render_card(pkg)

    def show_more_button(self):
        total_filtered = len(self.filtered)
        if not st.session_state.show_all and total_filtered > 4:
            if not st.session_state.show_more_clicked:
                if st.button("🌿 Show More Packages (Click Twice)", use_container_width=True):
                    st.session_state.show_all = True
                    st.session_state.show_more_clicked = True
                    st.stop()
            else:
                st.markdown(
                    f'<div style="color: {HEADER_COLOR}; font-weight: bold; margin-top: 8px; text-align: center;">Click again to expand more packages</div>',
                    unsafe_allow_html=True,
                )
        else:
            self.reset_show_more_clicked()

    @staticmethod
    def render_card(pkg):
        st.markdown(
            f"""
            <div style="
                border: 2px solid {CARD_BORDER};
                border-radius: 15px;
                padding: 15px;
                margin-bottom: 20px;
                background: {CARD_BG};
                box-shadow: 0 4px 12px {CARD_SHADOW};
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                height: 400px; /* fixed height for all cards */
            ">
                <div style="overflow: hidden; flex-grow: 1;">
                    <h3 style="color: {HEADER_COLOR}; margin-top:0; margin-bottom: 8px; line-height: 1.2;">{pkg['name']}</h3>
                    <p style="color:{TEXT_COLOR}; margin:2px 0;"><b>Type:</b> {pkg['type']}</p>
                    <p style="color:{TEXT_COLOR}; margin:2px 0;"><b>Length:</b> {pkg['length']}</p>
                    <p style="color:{TEXT_COLOR}; margin:2px 0;"><b>Hand:</b> {pkg['hand']}</p>
                    <p style="color:{TEXT_COLOR}; margin:2px 0;"><b>Side:</b> {pkg['side']}</p>
                    <p style="color:{DESC_COLOR}; white-space: pre-wrap; overflow-y: auto; max-height: 150px; margin-top: 8px;">{pkg['description']}</p>
                </div>
                <p style="color:{PRICE_COLOR}; font-weight:bold; margin-top:10px;"><b>Price:</b> {pkg['price']} BDT</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------- MAIN ----------
def main():
    st.set_page_config(page_title="Packages - Rafiya’s Henna Art", page_icon="https://lh3.googleusercontent.com/sitesv/AAzXCkf-1N6x6wwyDShvokvM-bQgyx7RMwgRPfrY2rbKk5eVsByjS9PhQ3C0XOd9re_f8VFhc0guPTV7cNUbQclM8N3l3CRpvj2b8Vd_pi89-5OJX0ND_P7HJrplzTH7MOUYdauYisHiQrEbXQjlAOCC9BMeDaifdkSnaTkE0zIotl6eXhHMp7SDjiR95jo=w16383", layout="wide")
    st.markdown(f"""
        <style>
        /* 🌿 Global Page Styling */
        body {{
            background-color: {BACKGROUND_COLOR};
            color: {TEXT_COLOR};
            font-family: 'Segoe UI', sans-serif;
        }}
        h1 {{
            color: {HEADER_COLOR};
            text-align:center;
        }}
        hr {{
            border: 1px solid {CARD_BORDER};
        }}

        /* 🌿 Button Styling */
        .stButton>button {{
            background-color: {CARD_BORDER} !important;
            color: white !important;
            border-radius: 8px;
            border: none;
            padding: 8px 16px;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: {BUTTON_HOVER_COLOR} !important;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
            transform: translateY(-1px);
        }}

        /* 🌿 Selectbox Styling */
        div[data-baseweb="select"] > div {{
            border: 2px solid {CARD_BORDER} !important;
            border-radius: 8px !important;
        }}
        div[data-baseweb="select"]:focus-within > div {{
            border-color: {BUTTON_HOVER_COLOR} !important;
            box-shadow: 0 0 6px rgba(184,134,11,0.4);
        }}

        /* 🌿 Slider Track & Thumb */
        .stSlider [role="slider"] {{
            background-color: {CARD_BORDER} !important;
            border: 2px solid white !important;
        }}
        .stSlider [data-baseweb="slider"] > div > div {{
            background: {SLIDER_GRADIENT_ACTIVE} !important;
        }}
        .stSlider [data-baseweb="slider"] > div > div > div {{
            background: {CARD_BORDER} !important;
        }}

        /* 🌿 Slider Number Box Styling */
        .stSlider span[data-baseweb="tag"] {{
            background: black !important;
            color: white !important;
            border-radius: 8px !important;
            border: 2px solid {CARD_BORDER} !important;
            font-weight: bold;
        }}
        .stSlider span[data-baseweb="tag"].active {{
            background: {CARD_BORDER} !important;
            color: white !important;
        }}
        </style>
        """, unsafe_allow_html=True)

    # Title
    st.markdown("<h1>🌿 Packages 🌿</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{HEADER_COLOR}; font-style:italic;'>Pick the perfect henna package for your special occasion! 📦</p>", unsafe_allow_html=True)
    st.markdown(f"<hr style='border:1px solid {CARD_BORDER};'>", unsafe_allow_html=True)

    # Load packages from Streamlit secrets
    packages = st.secrets["personal"]["data"].get("packages", [])

    if not packages:
        st.info("No packages available.")
        return

    # Instantiate filter class and render filters
    pkg_filter = PackageFilter(packages)
    pkg_filter.render_filters()

    # Reset show_all on filter changes
    current_filter = pkg_filter.get_filter_tuple()
    if "last_filter" not in st.session_state:
        st.session_state.last_filter = None

    if st.session_state.last_filter != current_filter:
        st.session_state.show_all = False
        st.session_state.last_filter = current_filter
        st.session_state.show_more_clicked = False

    # Apply filters
    filtered = pkg_filter.apply_filters()

    if not filtered:
        st.warning("No packages match your filters.")
        return

    # Instantiate display class and show packages
    pkg_display = PackageDisplay(filtered)
    pkg_display.display_cards()
    pkg_display.show_more_button()

if __name__ == "__main__":
    main()
