from __future__ import annotations

from typing import Any, Dict, List
import streamlit as st

def render_faq_view(faq_data: List[Dict[str, Any]], products: Dict[str, Any]):
    """Renders categorized studio knowledge cards and default-open FAQ expanders."""
    st.markdown("### 💡 FAQ & Studio Care")
    st.markdown(
        "<p style='font-size:13.5px; color:#94A3B8; margin-top:-6px;'>"
        "Essential knowledge on henna stain preservation, home service policies, and 100% organic cones."
        "</p>",
        unsafe_allow_html=True,
    )

    # Core Knowledge Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div style="background: #121620; border: 1px solid #2C323F; border-radius: 12px; padding: 20px; height: 100%;">
                <div style="font-size: 28px; margin-bottom: 8px;">📍</div>
                <h4 style="margin-top: 0; color: #F8FAFC; font-size: 16px;">Home Service in Dhaka</h4>
                <p style="font-size: 12.5px; color: #94A3B8; line-height: 1.6;">
                    We offer home service across Dhaka city! Service charges are based on your specific location. 
                    Please message your exact area to confirm.
                </p>
                <div style="font-size: 11px; color: #C5A059; font-weight: 600;">
                    ✓ Bridal & Party Available
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div style="background: #121620; border: 1px solid #C5A059; border-radius: 12px; padding: 20px; height: 100%;">
                <div style="font-size: 28px; margin-bottom: 8px;">🌸</div>
                <h4 style="margin-top: 0; color: #C5A059; font-size: 16px;">Dark Mahogany Stain Routine</h4>
                <p style="font-size: 12.5px; color: #94A3B8; line-height: 1.6;">
                    Keep paste on for 6-8 hours. Avoid water for the first 24 hours. 
                    Apply coconut or mustard oil before showering. The stain oxidizes and deepens over 24-48 hours!
                </p>
                <div style="font-size: 11px; color: #10B981; font-weight: 600;">
                    ✓ 100% Organic Oxidation
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        items = products.get("items", [])
        cone_price = items[0].get("mrp", 100.0) if items else 100.0
        st.markdown(
            f"""
            <div style="background: #121620; border: 1px solid #2C323F; border-radius: 12px; padding: 20px; height: 100%;">
                <div style="font-size: 28px; margin-bottom: 8px;">🧴</div>
                <h4 style="margin-top: 0; color: #F8FAFC; font-size: 16px;">100% Organic Henna Cones</h4>
                <p style="font-size: 12.5px; color: #94A3B8; line-height: 1.6;">
                    Handmade using organic Rajasthani henna powder and therapeutic essential oils (eucalyptus/lavender). 
                    No chemicals or PPD.
                </p>
                <div style="font-size: 12px; color: #C5A059; font-weight: 700;">
                    MRP: {cone_price:.2f} BDT / cone
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📁 Frequently Asked Questions")

    # Expanders for FAQ items
    if faq_data:
        categories = sorted(list(set(faq.get("category", "General") for faq in faq_data)))
        for cat in categories:
            cat_faqs = [f for f in faq_data if f.get("category") == cat]
            for faq in cat_faqs:
                with st.expander(f"✨ {faq.get('question')}", expanded=True):
                    st.markdown(faq.get("answer", ""))
    else:
        st.info("No additional FAQs configured.")
