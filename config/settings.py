from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Tuple

# Base Directories & Asset Paths
BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_DIR = BASE_DIR / "logo"
SECRETS_PATH = BASE_DIR / ".streamlit" / "secrets.toml"
AVATAR_PATH = LOGO_DIR / "rafiya.jpg"

# Application Metadata
APP_TITLE = "Rafiya's Henna Art — Atelier & Studio"
APP_SUBTITLE = "Fine Bridal & Organic Henna Artistry • Dhaka"
APP_VERSION = "2.0.0"
APP_ICON = "🌿"
AUTHOR = "Rafiya"

# AI Service Defaults (Tuned for responsive, accurate studio guidance)
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"

# Comprehensive pool of Gemini models for automatic quota failover
GEMINI_FALLBACK_MODELS: List[str] = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3-flash-preview",
    "gemini-3.8-flash",
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-3.1-pro-preview",
    "gemini-pro-latest",
    "gemini-2.5-pro",
]

# Cooldown duration (seconds) before retrying a model that hit quota limits
MODEL_QUOTA_COOLDOWN_SECONDS = 600

# Rate Limiting & Abuse Prevention (Single chat / device protection)
MIN_REQUEST_INTERVAL_SECONDS = 2.0   # 2-second debounce between rapid queries
MAX_REQUESTS_PER_MINUTE = 8          # Max 8 queries per rolling minute
MAX_SESSION_REQUESTS = 40            # Max 40 queries per session

# Semantic & Similar Asking Cache Settings
CACHE_SIMILARITY_THRESHOLD = 0.88    # High precision: exact/near-exact queries use cache, fresh queries go to Gemini
CACHE_MAX_ENTRIES = 300              # Maximum LRU cache capacity

GENERATION_CONFIG = {
    "temperature": 0.55,             # Balanced creativity and authentic studio tonality
    "top_p": 0.90,
    "max_output_tokens": 650,        # Generous room for rich topic advice, styling tips, and breakdowns
}

# FAQ Engine Settings
FAQ_SIMILARITY_THRESHOLD = 0.70

CATEGORY_ICONS: Dict[str, str] = {
    "General": "🌿",
    "Booking": "📅",
    "Bridal": "👑",
    "Non-Bridal": "✨",
    "Courses": "🎓",
    "Products": "🧴",
    "Aftercare": "🌸",
}

SUGGESTION_CHIPS: List[Tuple[str, str]] = [
    ("👑 Bridal Lookbook", "Can you guide me through your bridal henna packages, styles (Mandala, Gorgeous, Arabic), and rates?"),
    ("✨ Party & Non-Bridal", "What are your most popular party and non-bridal henna designs for upcoming events?"),
    ("🎓 Academy Syllabus", "How does the academy training progress from foundational strokes to full bridal mastery?"),
    ("🧴 100% Organic Cones", "What ingredients are used in your handmade organic cones and how do I order them?"),
    ("📍 Dhaka Home Service", "Do you offer home service across Dhaka and how are travel charges calculated?"),
    ("🌸 Deep Mahogany Stain", "What is your recommended aftercare routine to get the deepest, darkest henna stain?"),
]

