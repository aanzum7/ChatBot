import streamlit as st

# 🎨 GLOBAL COLOR PALETTE (Mehendi Theme)
BACKGROUND_COLOR = "#f9f7f1"      # Cream background
TEXT_COLOR = "#3b3a36"            # Dark earthy brown
HEADER_COLOR = "#6b8e23"          # Olive green
EXPANDER_BG = "#fff8dc"           # Light golden (like packages)
EXPANDER_BORDER = "#b8860b"       # Goldenrod
QUESTION_BG = "#f0e6d2"           # Soft beige for questions
QUESTION_COLOR = "#2f4f2f"        # Deep green (matches price color)
ANSWER_BG = "#fffdf5"             # Lighter cream for answers
ANSWER_COLOR = "#5b4636"          # Warm brown
CARD_SHADOW = "rgba(0,0,0,0.08)"  # Soft shadow
BUTTON_HOVER_COLOR = "#a07400"    # Darker gold hover for interactive elements

# Set page config
st.set_page_config(
    page_title="FAQs - Rafiya’s Henna Art",
    page_icon="logo/rafiya.jpg",
    layout="wide"
)

# Inject CSS for theme
st.markdown(f"""
    <style>
    body {{
        background-color: {BACKGROUND_COLOR};
        color: {TEXT_COLOR};
        font-family: 'Segoe UI', sans-serif;
    }}
    h1, h2, h3 {{
        color: {HEADER_COLOR};
    }}
    /* Expander styling */
    .streamlit-expanderHeader {{
        background-color: {EXPANDER_BG} !important;
        border-left: 4px solid {EXPANDER_BORDER};
        font-weight: bold;
        color: {HEADER_COLOR} !important;
        border-radius: 8px;
        padding: 10px 12px;
        margin-bottom: 6px;
        box-shadow: 0 2px 6px {CARD_SHADOW};
        transition: all 0.2s ease-in-out;
    }}
    .streamlit-expanderHeader:hover {{
        background-color: {BUTTON_HOVER_COLOR} !important;
        color: white !important;
    }}
    .streamlit-expanderContent {{
        background-color: {BACKGROUND_COLOR};
        padding: 12px 18px;
        border-left: 2px solid {EXPANDER_BORDER};
        border-radius: 0 8px 8px 0;
        margin-bottom: 14px;
    }}
    /* FAQ Question Card */
    .faq-question {{
        background-color: {QUESTION_BG};
        color: {QUESTION_COLOR};
        font-weight: 600;
        font-size: 15px;
        padding: 10px 14px;
        border-left: 3px solid {EXPANDER_BORDER};
        border-radius: 6px;
        margin-bottom: 6px;
        box-shadow: 0 1px 4px {CARD_SHADOW};
    }}
    /* FAQ Answer Card */
    .faq-answer {{
        background-color: {ANSWER_BG};
        color: {ANSWER_COLOR};
        font-size: 14px;
        padding: 10px 14px;
        border-radius: 6px;
        box-shadow: 0 1px 4px {CARD_SHADOW};
        margin-bottom: 12px;
        white-space: pre-wrap;
    }}
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown(
    f"<h1 style='text-align:center;'>🌿 Frequently Asked Questions 🌿</h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<p style='text-align:center; color:{HEADER_COLOR}; font-style:italic;'>Everything you need to know about Rafiya’s Henna Art! 💡</p>",
    unsafe_allow_html=True
)
st.divider()

# Load FAQ data
faq_data = st.secrets.get("faq", {}).get("questions", [])
if not faq_data:
    st.info("No FAQ data available.")
else:
    # Extract unique categories
    categories = sorted(set(faq['category'] for faq in faq_data))

    # Render FAQs grouped by category
    for category in categories:
        with st.expander(category, expanded=False):
            cat_faqs = [f for f in faq_data if f['category'] == category]
            for faq in cat_faqs:
                st.markdown(f"<div class='faq-question'>❓ {faq['question']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='faq-answer'>💬 {faq['answer']}</div>", unsafe_allow_html=True)
