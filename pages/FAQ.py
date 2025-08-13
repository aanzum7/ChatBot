import streamlit as st

# Set page config
st.set_page_config(page_title="FAQs - rafiya.ai", layout="wide")
st.title("💡 Frequently Asked Questions")

# Load FAQ data from Streamlit secrets safely
faq_data = st.secrets.get("faq", {}).get("questions", [])
if not faq_data:
    st.info("No FAQ data available.")
else:
    # Extract unique categories
    categories = sorted(set(faq['category'] for faq in faq_data))

    # Render FAQs grouped by category
    for category in categories:
        with st.expander(category):
            cat_faqs = [f for f in faq_data if f['category'] == category]
            for faq in cat_faqs:
                st.markdown(f"**{faq['question']}**  \n{faq['answer']}")
