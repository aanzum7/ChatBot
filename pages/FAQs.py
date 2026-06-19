import streamlit as st
from utils.theme import inject_global_theme, render_header, CONFIG

def main():
    inject_global_theme("FAQs", "💡")
    if st.button("← Back to Lounge Home"):
        st.switch_page("Home.py")
        
    render_header("Frequently Asked Questions", "Everything you need to know about Rafiya’s Henna Art!")

    faq_data = st.secrets.get("faq", {}).get("questions", [])
    if not faq_data:
        st.info("No query arrays have been initialized inside secrets.")
        return

    # Sort and group entries dynamically by their category keys
    categories = sorted(list(set(faq['category'] for faq in faq_data)))

    for cat in categories:
        st.markdown(f"<h3 style='margin-top:18px; border-bottom:2px solid {CONFIG['accent_gold']}; padding-bottom:2px;'>📂 {cat}</h3>", unsafe_allow_html=True)
        cat_faqs = [f for f in faq_data if f['category'] == cat]
        
        for faq in cat_faqs:
            with st.expander(f"❓ {faq['question']}", expanded=False):
                st.markdown(f"""
                <div style="background-color: {CONFIG['bot_bg']}; padding: 14px; 
                            border-left: 4px solid {CONFIG['accent_gold']}; border-radius: 6px; color: {CONFIG['bot_text']}; font-size:14.5px; line-height:1.5;">
                    <b>Response:</b><br>{faq['answer']}
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
