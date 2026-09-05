"""
Device and session rate limiting for Rafiya's Henna Art.
Prevents API spam and quota exhaustion, paired with warm, studio-themed feedback.
"""
from __future__ import annotations

import random
import time
import threading
from typing import Dict, List, Optional, Tuple

from config.settings import (
    MIN_REQUEST_INTERVAL_SECONDS,
    MAX_REQUESTS_PER_MINUTE,
    MAX_SESSION_REQUESTS,
)

# Studio-themed responses for rate limits
FUNKY_SPEED_RESPONSES: List[str] = [
    "🌿 **Fine art takes a steady hand!** Please pause for just 2 seconds so our studio assistant can process your last question with care. 💬",
    "✨ **Slow and steady!** Intricate henna patterns take patience. Give the assistant 2 seconds before asking again! 🎨",
    "🌸 **Breathe in the eucalyptus!** Our neural cone needs a quick 2-second pause between rapid messages. Try again in just a moment! 🌿",
]

FUNKY_RPM_RESPONSES: List[str] = [
    "👑 **Curiosity is blooming!** You've asked 8 questions in under a minute. Let's pause for 20 seconds so our studio engine can catch up. ✨",
    "🌿 **Studio Refresh!** That is a wonderful flurry of inquiries! Give our assistant 30 seconds to reload the design palette. 💬",
    "🎨 **Pacing the Lookbook!** Even brides take time choosing their favorite motifs. Take 20 seconds to explore our Collections tab above! 💍",
]

FUNKY_SESSION_CAP_RESPONSES: List[str] = [
    "👑 **VIP Consultation Champion!** We've exchanged over 40 questions today! To reserve active dates or customize bespoke packages, please connect directly with Rafiya on [WhatsApp](https://wa.me/8801323278403) or [Messenger](https://m.me/Rafiya.HennaArt)! 📱",
    "🌸 **Studio Bandwidth Reached!** You've completed an extensive studio consultation today! Explore the **Curated Collections** tab or send Rafiya a direct message on WhatsApp (+8801323278403). 🌿",
]

FUNKY_GLITCH_RESPONSES: List[str] = [
    "🌿 **Studio Sabbatical!** Our assistant briefly stepped away to prepare fresh organic henna paste. Please ask your question once more! ✨",
    "🌸 **Design Flourish!** A momentary connection breeze interrupted our flow. Please send your question again! 💬",
    "✨ **Atelier Touch-Up!** Our digital cone had a tiny hiccup. Feel free to re-enter your question—ready when you are! 🌿",
]

def get_funky_glitch_response() -> str:
    """Return a random studio-appropriate response for temporary glitches."""
    return random.choice(FUNKY_GLITCH_RESPONSES)


class RateLimiter:
    """
    Thread-safe sliding-window rate limiter per device/session identifier.
    """

    def __init__(
        self,
        min_interval_seconds: float = MIN_REQUEST_INTERVAL_SECONDS,
        max_requests_per_minute: int = MAX_REQUESTS_PER_MINUTE,
        max_session_requests: int = MAX_SESSION_REQUESTS,
    ):
        self.min_interval = min_interval_seconds
        self.max_rpm = max_requests_per_minute
        self.max_session = max_session_requests

        self._lock = threading.Lock()
        self._request_history: Dict[str, List[float]] = {}
        self._session_totals: Dict[str, int] = {}

    def check_rate_limit(self, client_id: str) -> Tuple[bool, Optional[str]]:
        """
        Check if request is permitted.
        Returns (is_allowed, notice_message).
        """
        now = time.time()

        with self._lock:
            # 1. Total session cap check
            total = self._session_totals.get(client_id, 0)
            if total >= self.max_session:
                return False, random.choice(FUNKY_SESSION_CAP_RESPONSES)

            timestamps = self._request_history.get(client_id, [])

            # Prune timestamps older than 60 seconds
            recent = [t for t in timestamps if now - t < 60.0]

            # 2. Debounce check
            if recent and (now - recent[-1]) < self.min_interval:
                return False, random.choice(FUNKY_SPEED_RESPONSES)

            # 3. Sliding-window RPM check
            if len(recent) >= self.max_rpm:
                return False, random.choice(FUNKY_RPM_RESPONSES)

            # Request accepted: update logs
            recent.append(now)
            self._request_history[client_id] = recent
            self._session_totals[client_id] = total + 1
            return True, None

    def reset_client(self, client_id: str):
        """Reset history for a specific client upon conversation clear."""
        with self._lock:
            self._request_history.pop(client_id, None)
            self._session_totals.pop(client_id, None)


_global_rate_limiter: Optional[RateLimiter] = None

def get_rate_limiter() -> RateLimiter:
    """Return singleton RateLimiter instance."""
    global _global_rate_limiter
    if _global_rate_limiter is None:
        _global_rate_limiter = RateLimiter()
    return _global_rate_limiter
