import streamlit as st

# 🎨 GLOBAL COLOR PALETTE (Mehendi Theme)
BACKGROUND_COLOR = "#f9f7f1"      # Cream background
TEXT_COLOR = "#3b3a36"            # Dark earthy brown
HEADER_COLOR = "#6b8e23"          # Olive green
EXPANDER_BG = "#fdf5e6"           # Light golden
EXPANDER_BORDER = "#b8860b"       # Goldenrod
QUESTION_COLOR = "#2f4f2f"        # Deep green
ANSWER_COLOR = "#5b4636"          # Warm brown

# Set page config
st.set_page_config(page_title="FAQs - Rafiya’s Henna Art", layout="wide")

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
    .streamlit-expanderHeader {{
        background-color: {EXPANDER_BG} !important;
        border-left: 4px solid {EXPANDER_BORDER};
        font-weight: bold;
        color: {HEADER_COLOR} !important;
        border-radius: 6px;
        padding: 6px;
    }}
    .streamlit-expanderContent {{
        background-color: {BACKGROUND_COLOR};
        padding: 10px;
        border-left: 2px solid {EXPANDER_BORDER};
    }}
    .faq-question {{
        color: {QUESTION_COLOR};
        font-weight: 600;
        font-size: 15px;
    }}
    .faq-answer {{
        color: {ANSWER_COLOR};
        font-size: 14px;
        margin-bottom: 12px;
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

# Load FAQ data from Streamlit secrets safely
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
                st.markdown(f"<div class='faq-answer'>{faq['answer']}</div>", unsafe_allow_html=True)
