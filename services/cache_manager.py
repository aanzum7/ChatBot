"""
Semantic and normalized response caching for Rafiya's Henna Art.
Eliminates redundant Gemini API calls, saving tokens and accelerating common queries.
"""
from __future__ import annotations

from collections import OrderedDict
from difflib import SequenceMatcher
import re
import threading
import time
from typing import Any, Dict, Generator, List, Optional, Set, Tuple

from config.settings import CACHE_SIMILARITY_THRESHOLD, CACHE_MAX_ENTRIES

STOPWORDS: Set[str] = {
    "a", "about", "an", "and", "are", "as", "at", "be", "by", "can", "could",
    "do", "does", "for", "from", "how", "i", "in", "is", "it", "me", "my",
    "of", "on", "or", "please", "tell", "the", "to", "was", "what", "when",
    "where", "which", "who", "why", "with", "would", "you", "your", "koto",
    "dam", "ki"
}

def normalize_text(text: str) -> str:
    """Lowercase, strip non-alphanumeric chars, and collapse whitespace."""
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    return re.sub(r"\s+", " ", cleaned).strip()

def _stem(word: str) -> str:
    """Lightweight suffix stripping."""
    w = word.lower()
    for suffix in ("ing", "tion", "tions", "ies", "es", "s", "ed"):
        if len(w) > len(suffix) + 3 and w.endswith(suffix):
            return w[:-len(suffix)]
    return w

def extract_keywords(text: str) -> Set[str]:
    """Extract non-stopword stemmed tokens."""
    tokens = normalize_text(text).split()
    stems = {_stem(t) for t in tokens if t not in STOPWORDS}
    return stems if stems else {_stem(t) for t in tokens}


class SemanticResponseCache:
    """
    Thread-safe semantic response cache with LRU eviction, exact match fast-path,
    and fuzzy token-similarity matching.
    """

    def __init__(
        self,
        max_size: int = CACHE_MAX_ENTRIES,
        similarity_threshold: float = CACHE_SIMILARITY_THRESHOLD,
    ):
        self.max_size = max_size
        self.similarity_threshold = similarity_threshold
        self._lock = threading.Lock()
        self._cache: OrderedDict[str, str] = OrderedDict()
        self._keywords_index: Dict[str, Set[str]] = {}

    def get(self, query: str) -> Optional[Tuple[str, float]]:
        """
        Check cache for exact or semantically similar query.
        Returns (cached_response, score) if found, else None.
        """
        norm_query = normalize_text(query)
        if not norm_query:
            return None

        with self._lock:
            # 1. Exact normalized match (O(1))
            if norm_query in self._cache:
                self._cache.move_to_end(norm_query)
                return self._cache[norm_query], 1.0

            # 2. Semantic token similarity
            query_kws = extract_keywords(norm_query)
            if not query_kws:
                return None

            best_match: Optional[str] = None
            best_score = 0.0

            for cached_norm, response_text in self._cache.items():
                cached_kws = self._keywords_index.get(cached_norm, set())
                if not cached_kws:
                    continue

                # Token Jaccard similarity on stemmed keywords
                intersection = query_kws.intersection(cached_kws)
                union = query_kws.union(cached_kws)
                jaccard = len(intersection) / len(union) if union else 0.0

                # Overlap ratio relative to smaller set
                min_kws = min(len(query_kws), len(cached_kws))
                overlap_ratio = len(intersection) / min_kws if min_kws > 0 else 0.0

                # Token sequence similarity on sorted stemmed keywords
                q_token_str = " ".join(sorted(query_kws))
                c_token_str = " ".join(sorted(cached_kws))
                token_seq = SequenceMatcher(None, q_token_str, c_token_str).ratio()

                # Full normalized text sequence similarity
                full_seq = SequenceMatcher(None, norm_query, cached_norm).ratio()

                # Substring containment bonus
                sub_score = 0.0
                if len(norm_query) >= 10 and norm_query in cached_norm:
                    sub_score = 0.85
                elif len(cached_norm) >= 10 and cached_norm in norm_query:
                    sub_score = 0.85

                combined_score = max(
                    jaccard,
                    (overlap_ratio * 0.70 + token_seq * 0.30) if len(intersection) > 0 else 0.0,
                    full_seq * 0.90 if len(intersection) > 0 else 0.0,
                    sub_score,
                )

                if combined_score > best_score:
                    best_score = combined_score
                    best_match = response_text

            if best_match and best_score >= self.similarity_threshold:
                return best_match, best_score

        return None

    def set(self, query: str, response_text: str):
        """Commit query response pair to cache with LRU eviction."""
        norm_query = normalize_text(query)
        if not norm_query or not response_text:
            return

        with self._lock:
            if norm_query in self._cache:
                self._cache.move_to_end(norm_query)
            else:
                if len(self._cache) >= self.max_size:
                    oldest_key, _ = self._cache.popitem(last=False)
                    self._keywords_index.pop(oldest_key, None)

            self._cache[norm_query] = response_text
            self._keywords_index[norm_query] = extract_keywords(norm_query)

    def stream_cached_response(self, cached_text: str) -> Generator[str, None, None]:
        """Yield cached text in natural word-sized chunks for st.write_stream."""
        words = cached_text.split(" ")
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
            time.sleep(0.015)

    def preseed(
        self,
        faq_data: List[Dict[str, Any]],
        suggestion_chips: List[Tuple[str, str]],
        personal_data: Dict[str, Any],
    ):
        """Pre-populate cache with verified studio FAQs and chip prompts."""
        # 1. Preseed FAQs with clean verified content
        for faq in faq_data:
            q = faq.get("question", "")
            a = faq.get("answer", "")
            if q and a:
                self.set(q, a)

        # 2. Preseed Home Service
        self.set(
            "Do you provide home service in Dhaka?",
            "🌿 **Home Service in Dhaka:**\n\n"
            "Yes! We offer home service within Dhaka city. A service charge applies depending on your specific area. "
            "Please message us your exact location on [WhatsApp](https://wa.me/8801323278403) or [Messenger](https://m.me/Rafiya.HennaArt) to confirm.",
        )

        # 3. Preseed Organic Cones
        self.set(
            "Are your henna cones organic and what is the price?",
            "🧴 **Organic Henna Cones:**\n\n"
            "Our cones are 100% organic, halal, and hand-crafted using pure henna powder and essential oils (eucalyptus/cajeput/lavender). "
            "Completely free of chemicals or PPD. Price: **100 BDT per cone**. Message us to order fresh batches!",
        )

        # 4. Preseed Aftercare
        self.set(
            "How can I get the darkest stain?",
            "🌸 **Aftercare & Dark Stain Tips:**\n\n"
            "1. Keep paste on for 6-8 hours (or overnight for brides).\n"
            "2. Apply lemon-sugar sealant while wet.\n"
            "3. DO NOT wash with water! Scrape off the dried crust.\n"
            "4. Avoid water for the first 24 hours.\n"
            "5. Apply coconut or mustard oil before bathing. Stain deepens over 24-48 hours!",
        )


_global_cache: Optional[SemanticResponseCache] = None

def get_response_cache() -> SemanticResponseCache:
    """Return singleton response cache."""
    global _global_cache
    if _global_cache is None:
        _global_cache = SemanticResponseCache()
    return _global_cache
