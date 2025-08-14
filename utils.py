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
            model_name="gemini-2.0-flash",
            generation_config={
                "temperature": 0.5,
                "top_p": 0.9,
                "max_output_tokens": 512,
            },
        )
        self.chat_session = self.model.start_chat()
        logger.info("Gemini AI configured.")

    def generate_response(self, user_input: str) -> str:
        try:
            try:
                input_language = langdetect.detect(user_input)
            except langdetect.lang_detect_exception.LangDetectException:
                input_language = "unknown"
            prompt = (
                f"FAQ Context: {self.context['faq']}\n"
                f"Personal Context: {self.context['personal']}\n"
                f"User Input: {user_input}\n\n"
                "You are Rafiya's henna artist, speaking in her voice. "
                "Respond simply, warmly, and conversationally in English, matching the tone of the user's input, "
                f"which is in {input_language}. "
                "When relevant, briefly mention the available packages or services in a clear, well-formatted list including their prices, "
                "and reference the page: (https://Packages)"
                "Use friendly emojis to make the conversation lively.\n\n"
                "For contact, show short clickable buttons with icons:\n"
                "💬 [Messenger](https://m.me/Messenger) | "
                "📱 [WhatsApp](https://wa.me/WhatsApp) | "
                "✉️ [Email](mailto:Email)\n\n"
                "For recent work, provide button-style links with icons:\n"
                "📘 [Facebook](https://facebook.com/YourPage) | "
                "📸 [Instagram](https://instagram.com/YourPage) | "
                "▶️ [YouTube](https://youtube.com/YourChannel)"
            )

            response = self.chat_session.send_message(prompt)
            if response and hasattr(response, "text") and response.text:
                return response.text.strip()
            else:
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
