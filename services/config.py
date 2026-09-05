from __future__ import annotations

import os
from typing import Any, Dict, List, Tuple
import streamlit as st
import toml

from config.settings import SECRETS_PATH
from services.logger import get_logger

logger = get_logger(__name__)

class ConfigError(Exception):
    """Raised when studio configuration or credentials cannot be resolved."""


def _get_secrets_dict() -> Dict[str, Any]:
    """Retrieve full secrets dictionary from st.secrets or local secrets.toml."""
    # 1. Native st.secrets (Streamlit runtime / Cloud deployment)
    try:
        if hasattr(st, "secrets") and len(st.secrets) > 0:
            return {
                k: dict(v) if hasattr(v, "to_dict") or isinstance(v, dict) else v
                for k, v in st.secrets.items()
            }
    except Exception as e:
        logger.debug(f"Unable to read from st.secrets directly: {e}")

    # 2. Local secrets.toml
    if os.path.exists(SECRETS_PATH):
        try:
            return toml.load(str(SECRETS_PATH))
        except Exception as e:
            logger.error(f"Failed to parse {SECRETS_PATH}: {e}")

    return {}


@st.cache_data(show_spinner=False)
def load_studio_configuration() -> Dict[str, Any]:
    """
    Loads API credentials, package catalogs, courses, and FAQs from secrets.
    Cached across reruns for optimal performance.
    """
    secrets_data = _get_secrets_dict()

    # 1. Resolve API Key
    api_key = None
    if "genai" in secrets_data and "api_key" in secrets_data["genai"]:
        api_key = str(secrets_data["genai"]["api_key"]).strip()
    elif "GEMINI_API_KEY" in secrets_data:
        api_key = str(secrets_data["GEMINI_API_KEY"]).strip()
    else:
        for env_var in ("GEMINI_API_KEY", "GENAI_API_KEY"):
            val = os.environ.get(env_var)
            if val:
                api_key = val.strip()
                break

    if not api_key:
        logger.warning("Gemini API key not found in secrets or environment.")

    # 2. Resolve Personal / Studio Data
    personal_data = {}
    if "personal" in secrets_data and "data" in secrets_data["personal"]:
        personal_data = secrets_data["personal"]["data"]
    elif "personal" in secrets_data and isinstance(secrets_data["personal"], dict):
        personal_data = secrets_data["personal"]

    # 3. Resolve FAQs
    faq_data = []
    if "faq" in secrets_data and "questions" in secrets_data["faq"]:
        faq_data = secrets_data["faq"]["questions"]
    elif "faq" in secrets_data and isinstance(secrets_data["faq"], list):
        faq_data = secrets_data["faq"]

    # 4. Resolve Sub-sections
    packages = personal_data.get("packages", [])
    courses = personal_data.get("course", {})
    products = personal_data.get("products", {})
    contacts = personal_data.get("contacts", {})

    logger.debug(
        f"Studio configuration loaded: {len(packages)} packages, "
        f"{len(faq_data)} FAQs, {len(courses.get('courses', []))} courses."
    )

    import json
    result = {
        "api_key": api_key or "",
        "faq_data": faq_data,
        "personal_data": personal_data,
        "packages": packages,
        "courses": courses,
        "products": products,
        "contacts": contacts,
    }
    # Deep convert DynamicInlineTableDict to plain dict/list for pickle safety
    return json.loads(json.dumps(result))
