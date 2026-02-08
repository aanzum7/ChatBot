import google.generativeai as genai
import langdetect
import logging
from difflib import SequenceMatcher
from typing import Dict, Tuple, Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgenticAI:
    def __init__(self, api_key: str, context: Dict):
        self.api_key = api_key
        self.context = context
        self.configure_ai()

    def configure_ai(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.5-flash-lite",
            generation_config={
                "temperature": 0.1,
                "top_p": 0.9,
                "max_output_tokens": 1024,
            },
        )
        self.chat_session = self.model.start_chat()
        logger.info("Gemini AI configured.")

    def generate_response(self, user_input: str) -> str:
        try:
            # Detect user input language
            try:
                input_language = langdetect.detect(user_input)
            except langdetect.lang_detect_exception.LangDetectException:
                input_language = "en"  # default to English if detection fails

            # Include language-specific guidance if needed
            language_note = ""
            if input_language != "en":
                language_note = f"Respond in {input_language} where possible, but keep it simple and friendly. "
                            
            prompt = (
                f"FAQ Context: {self.context['faq']}\n"
                f"Personal Context: {self.context['personal']}\n"
                f"User Input: {user_input}\n\n"
                "You are Rafiya, a talented and friendly henna artist 🌿✨. "
                "Respond naturally and warmly, mirroring the user's tone. "
                "Understand queries in Bangla, English, or Banglish, and reply in the same language the user asks in.\n\n"
                "Use the following info dynamically to respond in a **friendly, concise, summary style**:\n"
                "1️⃣ FAQ: Provide answers from the FAQ if relevant.\n"
                "2️⃣ Bridal and Non-Bridal Henna Packages:\n"
                "   - Show short lists with prices and descriptions.\n"
                "   - Always link to full details: 🌿 [Packages](https://rafiyashennaart.streamlit.app/Packages)\n"
                "   - Guide users on how to **book appointments**.\n"
                "3️⃣ Organic Henna & Products:\n"
                "   - Mention availability and details for each product.\n"
                "   - Link for full details: 🌿 [Products](https://sites.google.com/view/rafiyashennaart/products)\n"
                "   - Guide users on how to **purchase products**.\n"
                "4️⃣ Courses & Training:\n"
                "   - Include highlights, learning outcomes, and benefits dynamically.\n"
                "   - Link for full details: 🌿 [Courses & Training](https://sites.google.com/view/rafiyashennaart/courses-training)\n"
                "   - Guide users on how to **enroll**.\n\n"
                "Always keep responses:\n"
                "- Friendly, concise, engaging, and emoji-rich 🌿✨\n"
                "- Include clickable contact options for any action:\n"
                "💬 [Messenger](https://m.me/Rafiya.HennaArt) | "
                "📱 [WhatsApp](https://wa.me/8801323278403) | "
                "✉️ [Email](mailto:rafiyashennaart@gmail.com)\n\n"
                "- Include links to recent work:\n"
                "📘 [Facebook](https://www.facebook.com/share/1CFfRyJ1wY/) | "
                "📸 [Instagram](https://www.instagram.com/rafiyas_henna_art) | "
                "▶️ [YouTube](https://youtube.com/@RafiyasHennaArt)\n\n"
                "Guide the user naturally toward **booking, purchasing, enrolling, or viewing packages**.\n"
                "If a query is not listed in the FAQ or data, politely suggest the closest relevant option with links and action buttons."
            )

            # Generate response
            response = self.chat_session.send_message(prompt)
            if response and hasattr(response, "text") and response.text:
                return response.text.strip()
            else:
                # Retry chat session in case of empty response
                self.chat_session = self.model.start_chat()
                retry = self.chat_session.send_message(prompt)
                if retry and hasattr(retry, "text") and retry.text:
                    return retry.text.strip()
                return "🤖 Sorry, I couldn’t generate a response."
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"⚠️ Error: {e}"

class FAQHandler:
    def __init__(self, faq_list: List[Dict]):
        self.faq_list = faq_list

    def find_similar_question(self, user_input: str, threshold: float = 0.65) -> Tuple[Optional[str], Optional[str]]:
        best_q, best_a, highest = None, None, 0
        for faq in self.faq_list:
            sim = SequenceMatcher(None, user_input.lower(), faq['question'].lower()).ratio()
            if sim > highest:
                highest, best_q, best_a = sim, faq['question'], faq['answer']
        if highest >= threshold:
            return best_q, best_a
        return None, None
