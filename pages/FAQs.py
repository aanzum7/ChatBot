import streamlit as st
from utils.theme import inject_global_theme, render_header, CONFIG

def main():
    inject_global_theme("Help Center", "💡")
    if st.button("← RETURN TO LOUNGE"):
        st.switch_page("Home.py")
        
    render_header("Knowledge Base", "Instant answers from your digital assistant Henna Whisperer")

    faq_data = st.secrets.get("faq", {}).get("questions", [])
    if not faq_data:
        st.info("Knowledge Base is empty.")
        return

    categories = sorted(list(set(faq['category'] for faq in faq_data)))

    for cat in categories:
        st.markdown(f"### 📁 {cat.upper()}")
        cat_faqs = [f for f in faq_data if f['category'] == cat]
        
        for faq in cat_faqs:
            with st.expander(f"✨ {faq['question']}", expanded=False):
                st.markdown(f"""
                <div style="background-color: #1C202A; padding: 16px; border-left: 3px solid {CONFIG['accent_rose_gold']}; 
                            border-radius: 4px; color: #E5E7EB; font-size: 14.5px; line-height: 1.6;">
                    {faq['answer']}
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
