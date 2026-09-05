from __future__ import annotations

from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple

from config.settings import FAQ_SIMILARITY_THRESHOLD

class FAQHandler:
    """Fuzzy matching engine for studio FAQs."""

    def __init__(self, faq_list: List[Dict]):
        self.faq_list = faq_list or []
        self.faq_cache: Dict[str, Tuple[Optional[str], Optional[str]]] = {}

    def find_similar_question(
        self, user_input: str, threshold: float = FAQ_SIMILARITY_THRESHOLD
    ) -> Tuple[Optional[str], Optional[str]]:
        cleaned_input = user_input.strip().lower()

        if cleaned_input in self.faq_cache:
            return self.faq_cache[cleaned_input]

        best_q, best_a, highest = None, None, 0.0
        for faq in self.faq_list:
            sim = SequenceMatcher(None, cleaned_input, faq["question"].lower()).ratio()
            if sim > highest:
                highest, best_q, best_a = sim, faq["question"], faq["answer"]

        if highest >= threshold:
            self.faq_cache[cleaned_input] = (best_q, best_a)
            return best_q, best_a

        return None, None
