import streamlit as st
import json

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
            self.selected_type = st.selectbox("Type", ["All"] + types, index=0 if self.selected_type == "All" else None)

        lengths = sorted(set(
            p['length'] for p in self.packages
            if self.selected_type == "All" or p['type'] == self.selected_type
        ))
        with col2:
            self.selected_length = st.selectbox("Length", ["All"] + lengths, index=0 if self.selected_length == "All" else None)

        hands = sorted(set(
            p['hand'] for p in self.packages
            if (self.selected_type == "All" or p['type'] == self.selected_type) and
               (self.selected_length == "All" or p['length'] == self.selected_length)
        ))
        with col3:
            self.selected_hand = st.selectbox("Hand", ["All"] + hands, index=0 if self.selected_hand == "All" else None)

        sides = sorted(set(
            p['side'] for p in self.packages
            if (self.selected_type == "All" or p['type'] == self.selected_type) and
               (self.selected_length == "All" or p['length'] == self.selected_length) and
               (self.selected_hand == "All" or p['hand'] == self.selected_hand)
        ))
        with col4:
            self.selected_side = st.selectbox("Side", ["All"] + sides, index=0 if self.selected_side == "All" else None)

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

        # Display cards in rows of 4
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
                if st.button("Click twice to show more!", use_container_width=True):
                    st.session_state.show_all = True
                    st.session_state.show_more_clicked = True
                    st.stop()
            else:
                st.markdown(
                    '<div style="color: #a83254; font-weight: bold; margin-top: 8px; text-align: center;">Click twice to show more</div>',
                    unsafe_allow_html=True,
                )
        else:
            self.reset_show_more_clicked()

    @staticmethod
    def render_card(pkg):
        st.markdown(
            f"""
            <div style="
                border: 2px solid #d1495b;
                border-radius: 15px;
                padding: 15px;
                margin-bottom: 20px;
                background: #ffffff;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                height: 100%;
            ">
                <h3 style="color: #a83254; margin-top:0;">{pkg['name']}</h3>
                <p style="color:#333;"><b>Type:</b> {pkg['type']}</p>
                <p style="color:#333;"><b>Length:</b> {pkg['length']}</p>
                <p style="color:#333;"><b>Hand:</b> {pkg['hand']}</p>
                <p style="color:#333;"><b>Side:</b> {pkg['side']}</p>
                <p style="color:#555; white-space: pre-wrap;">{pkg['description']}</p>
                <p style="color:#000;"><b>Price:</b> {pkg['price']} BDT</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main(): 
    st.set_page_config(page_title="Packages - rafiya.ai", layout="wide")
    st.title("🎁 Packages")

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
