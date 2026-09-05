from __future__ import annotations

import urllib.parse
from typing import Any, Dict, List
import streamlit as st


def _clean_html(html_str: str) -> str:
    """
    Strips leading/trailing whitespace from each line and joins with single space.
    This guarantees no empty lines (\\n\\n) or 4-space indented blocks exist,
    preventing Markdown parsers from breaking out and leaking raw HTML tags.
    """
    return " ".join(line.strip() for line in html_str.strip().splitlines() if line.strip())


def _format_learning_html(raw_text: str) -> str:
    """Formats syllabus bullet points as clean inline HTML without newlines."""
    if not raw_text:
        return ""
    lines = [line.strip() for line in str(raw_text).strip().splitlines() if line.strip()]
    formatted = []
    for line in lines:
        if "What You" in line or line.startswith("🌸"):
            formatted.append(f"<div style='font-weight: 700; color: #F8FAFC; margin-bottom: 8px;'>{line}</div>")
        else:
            bullet = "" if line.startswith("•") else "• "
            formatted.append(f"<div style='margin-bottom: 4px; color: #CBD5E1;'>{bullet}{line}</div>")
    return "".join(formatted)


def _format_info_html(raw_text: str) -> str:
    """Formats materials and assessment text as clean inline HTML without newlines."""
    if not raw_text:
        return ""
    lines = [line.strip() for line in str(raw_text).strip().splitlines() if line.strip()]
    formatted = []
    for line in lines:
        if line.startswith("Provided in class:") or line.startswith("Final Exam"):
            formatted.append(f"<div style='font-weight: 600; color: #F1F5F9; margin-bottom: 4px;'>{line}</div>")
        elif line.startswith("Note:"):
            formatted.append(f"<div style='font-size: 11.5px; color: #C5A059; margin-top: 6px;'>ℹ️ {line}</div>")
        else:
            formatted.append(f"<div style='margin-bottom: 2px; color: #94A3B8;'>{line}</div>")
    return "".join(formatted)


def render_course_view(course_data: Dict[str, Any]):
    """Renders visual cards for Henna Academy courses, syllabus, and enrollment."""
    st.markdown("### 🎓 Henna Academy & Professional Training")
    st.markdown(
        "<p style='font-size:13.5px; color:#94A3B8; margin-top:-6px;'>"
        "Master the fine art of henna from foundational strokes to full bridal symmetry. "
        "Earn from home with verified professional skills."
        "</p>",
        unsafe_allow_html=True,
    )

    courses = course_data.get("courses", [])
    combo = course_data.get("combo_offer", {})

    # Combo Offer Banner
    if combo:
        combo_card = f"""
        <div style="background: linear-gradient(135deg, rgba(197, 160, 89, 0.15), rgba(16, 185, 129, 0.1)); 
                    border: 1px solid #C5A059; border-radius: 12px; padding: 16px 20px; margin-bottom: 24px; 
                    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="background: #C5A059; color: #0A0D14; font-size: 10px; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-transform: uppercase;">
                    Special Combo Offer
                </span>
                <h4 style="margin: 6px 0 2px 0; color: #F8FAFC; font-size: 16px;">{combo.get('details', 'Enroll in Both Courses Together')}</h4>
                <p style="margin: 0; font-size: 12px; color: #94A3B8;">Master both non-bridal and bridal henna artistry and save instantly!</p>
            </div>
            <div style="font-family: 'Marcellus', serif; font-size: 24px; color: #10B981; font-weight: 700;">
                {combo.get('discount', '10%')} OFF
            </div>
        </div>
        """
        st.markdown(_clean_html(combo_card), unsafe_allow_html=True)

    # Render Individual Courses
    for idx, course in enumerate(courses):
        col_info, col_fee = st.columns([3, 2])

        with col_info:
            learning_content = _format_learning_html(course.get('learning', ''))
            card_info = f"""
            <div style="background: #121620; border: 1px solid #2C323F; border-radius: 12px; padding: 24px; height: 100%;">
                <span style="background: rgba(197, 160, 89, 0.15); color: #C5A059; font-size: 10px; font-weight: 700; padding: 4px 10px; border-radius: 4px; text-transform: uppercase;">
                    Level {idx + 1}
                </span>
                <h3 style="margin-top: 10px; color: #FFFFFF; font-size: 20px;">{course.get('title')}</h3>
                <div style="font-size: 12px; color: #64748B; margin-bottom: 12px;">
                    ⏳ <b>{course.get('total_classes')} Intensive Classes</b> • 👥 Batch Size: <b>5 Students Only</b>
                </div>
                <div style="font-size: 12px; color: #94A3B8; margin-bottom: 14px;">
                    🎯 <b>Outcome:</b> {course.get('outcome')}<br>
                    👥 <b>Eligibility:</b> {course.get('eligibility')}
                </div>
                <hr style="border-color: rgba(255,255,255,0.05); margin: 12px 0;">
                <div style="font-size: 12.5px; color: #CBD5E1; line-height: 1.6;">
                    {learning_content}
                </div>
            </div>
            """
            st.markdown(_clean_html(card_info), unsafe_allow_html=True)

        with col_fee:
            course_title = course.get('title', 'Henna Course')
            inquiry_title = "Basic to Advance" if "Basic" in course_title else "Advance to Professional"
            encoded_title = urllib.parse.quote(inquiry_title)
            card_fee = f"""
            <div style="background: #121620; border: 1px solid #C5A059; border-radius: 12px; padding: 24px; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="color: #C5A059; margin-top: 0; font-size: 15px; text-transform: uppercase; letter-spacing: 0.05em;">
                        Admissions & Batches
                    </h4>
                    <div style="background: rgba(255,255,255,0.02); border-radius: 8px; padding: 14px; margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.05);">
                        <div style="font-size: 12px; color: #F1F5F9; line-height: 1.6;">
                            📍 <b>In-Person Studio (Azimpur, Dhaka)</b><br>
                            Hands-on practical guidance with direct instructor feedback.
                        </div>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); border-radius: 8px; padding: 14px; margin-bottom: 14px; border: 1px solid rgba(255,255,255,0.05);">
                        <div style="font-size: 12px; color: #F1F5F9; line-height: 1.6;">
                            🌐 <b>Live Online (Google Meet)</b><br>
                            Real-time interactive video training for distant learners.
                        </div>
                    </div>
                    <div style="background: rgba(197, 160, 89, 0.08); border-left: 3px solid #C5A059; padding: 10px 14px; border-radius: 4px;">
                        <span style="font-size: 12px; color: #F1E7D0; line-height: 1.5; display: block;">
                            💬 <b>Schedule & Tuition:</b> Batch timings and active tuition fees are updated per term. Please contact artist Rafiya directly to check current seat availability.
                        </span>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 18px;">
                    <a href="https://wa.me/8801323278403?text=Assalamu%20Alaikum,%20I%20want%20to%20know%20about%20the%20active%20schedule%20and%20tuition%20for%20{encoded_title}" target="_blank" style="text-decoration: none;">
                        <div style="background: #C5A059; color: #0A0D14; text-align: center; padding: 11px; border-radius: 6px; font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em;">
                            📱 Inquire on WhatsApp
                        </div>
                    </a>
                    <a href="https://m.me/Rafiya.HennaArt" target="_blank" style="text-decoration: none;">
                        <div style="background: rgba(0, 132, 255, 0.12); border: 1px solid rgba(0, 132, 255, 0.3); color: #0084FF; text-align: center; padding: 10px; border-radius: 6px; font-weight: 600; font-size: 12px;">
                            💬 Message on Facebook
                        </div>
                    </a>
                </div>
            </div>
            """
            st.markdown(_clean_html(card_fee), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

    # Materials & Certification
    materials = course_data.get("materials", {})
    exam = course_data.get("exam", {})

    col_mat, col_cert = st.columns(2)
    with col_mat:
        mat_content = _format_info_html(materials.get('offline', 'Practice cones, paper, and guides provided during offline classes.'))
        card_mat = f"""
        <div style="background: #121620; border: 1px solid #2C323F; border-radius: 10px; padding: 18px; height: 100%;">
            <h4 style="color: #F8FAFC; margin-top: 0; font-size: 15px;">📦 Practice Materials</h4>
            <div style="font-size: 12px; color: #94A3B8; line-height: 1.6;">
                {mat_content}
            </div>
        </div>
        """
        st.markdown(_clean_html(card_mat), unsafe_allow_html=True)

    with col_cert:
        cert_content = _format_info_html(exam.get('details', 'Final assessment with formal certification upon successful completion.'))
        card_cert = f"""
        <div style="background: #121620; border: 1px solid #2C323F; border-radius: 10px; padding: 18px; height: 100%;">
            <h4 style="color: #F8FAFC; margin-top: 0; font-size: 15px;">📜 Certification & Assessment</h4>
            <div style="font-size: 12px; color: #94A3B8; line-height: 1.6;">
                {cert_content}
            </div>
        </div>
        """
        st.markdown(_clean_html(card_cert), unsafe_allow_html=True)

