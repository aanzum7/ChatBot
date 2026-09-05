"""
Autonomous Multi-Model Gemini Agent for Rafiya's Henna Art.
Features:
- MCP Knowledge Server integration with autonomous function calling.
- Automatic failover across 14 Gemini models on 429 quota exhaustion.
- True token streaming for Streamlit (st.write_stream).
- Semantic caching integration for instant 0-token responses.
- Silent exception recovery with studio-themed fallbacks.
"""
from __future__ import annotations

import json
import time
import warnings
from typing import Any, Dict, Generator, List, Optional

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*google.generativeai.*")

import google.generativeai as genai
from google.ai import generativelanguage as glm
from google.api_core import exceptions as google_exceptions

from config.settings import (
    DEFAULT_GEMINI_MODEL,
    GEMINI_FALLBACK_MODELS,
    GENERATION_CONFIG,
    MODEL_QUOTA_COOLDOWN_SECONDS,
    SUGGESTION_CHIPS,
)
from services.cache_manager import SemanticResponseCache, get_response_cache
from services.logger import get_logger
from services.mcp_server import MCPServer, create_mcp_server
from services.rate_limiter import get_funky_glitch_response

logger = get_logger(__name__)


def format_model_label(model_name: str) -> str:
    """Format technical model string into a clean UI label."""
    cleaned = model_name.replace("models/", "")
    parts = cleaned.split("-")
    return " ".join(
        p.capitalize() if not any(c.isdigit() for c in p) else p for p in parts
    )


class AgenticAI:
    """
    State-of-the-art AI Assistant for Rafiya's Henna Art.
    """

    def __init__(
        self,
        api_key: str,
        context: Dict[str, Any],
        mcp_server: Optional[MCPServer] = None,
        cache: Optional[SemanticResponseCache] = None,
    ):
        self.api_key = api_key
        self.context = context

        # 1. MCP Server instance
        if mcp_server:
            self.mcp_server = mcp_server
        else:
            personal = context.get("personal", {})
            faqs = context.get("faq", [])
            self.mcp_server = create_mcp_server(personal, faqs)

        # 2. Semantic Response Cache
        if cache:
            self.cache = cache
        else:
            self.cache = get_response_cache()
            self.cache.preseed(
                faq_data=context.get("faq", []),
                suggestion_chips=SUGGESTION_CHIPS,
                personal_data=context.get("personal", {}),
            )

        # 3. System Instruction
        self.system_instruction = self._format_lean_instruction()

        # 4. Candidate Model Pool
        pool: List[str] = []
        if DEFAULT_GEMINI_MODEL:
            pool.append(DEFAULT_GEMINI_MODEL)
        for m in GEMINI_FALLBACK_MODELS:
            if m not in pool:
                pool.append(m)

        self.model_pool: List[str] = pool
        self._active_model_name: str = pool[0] if pool else DEFAULT_GEMINI_MODEL
        self._session_model: Optional[str] = None
        self._exhausted_models: Dict[str, float] = {}  # model -> cooldown expiration

        self.model: Optional[genai.GenerativeModel] = None
        self.chat_session = None

        self._configure_ai()

    def _format_lean_instruction(self) -> str:
        """
        Artisanal, topic-specific system instruction for Rafiya's Henna Art.
        Empowers dynamic, knowledgeable, and personalized responses using MCP studio tools.
        """
        return (
            "You are Rafiya, a celebrated professional henna artist and mentor based at your private studio in Azimpur, Dhaka 🌿✨.\n"
            "You are conversing with guests in your private digital design lounge. You speak warmly, artistically, and authoritatively "
            "as a passionate artisan who cares deeply about symmetry, natural stains, and bespoke bridal aesthetics.\n\n"

            "=== ARTISTIC PERSONA & VOICE ===\n"
            "- Tone: Warm, poised, elegant, and attentive — like a master artist consulting a bride in a luxury atelier.\n"
            "- Perspective: First person ('I', 'my studio', 'my students', 'our bespoke organic cones').\n"
            "- Language: Naturally bilingual. Reply in the language and script the client uses — English, Bangla (বাংলা), or Banglish.\n"
            "- Avoid generic, repetitive responses. Give fresh, thoughtful, topic-specific insights tailored to what the client actually asks.\n"
            "- Provide structured, visually readable answers with clean markdown formatting, bullets, and highlighting.\n\n"

            "=== TOPIC-SPECIFIC CONSULTATION GUIDELINES ===\n"
            "1. BRIDAL INQUIRIES:\n"
            "   - Discuss aesthetic styles: Classic symmetric Mandala (timeless, spiritual center), intricate Gorgeous bridal (negative space, dense florals), and flowing Arabic (modern, diagonal elegance).\n"
            "   - Explain coverage tiers: Wrist length, Midway forearm, or Elbow length for both hands and feet.\n"
            "   - Call `get_package_details` or `search_knowledge_base` to retrieve exact verified names and rates (e.g. Mandala Bridal at 1500 BDT, Midway Gorgeous at 2000 BDT, Royal Bridal, etc.).\n"
            "   - Offer styling suggestions based on their wedding outfit or event type (e.g. Holud, Mehendi night, Wedding reception).\n\n"

            "2. NON-BRIDAL & PARTY HENNA:\n"
            "   - Recommend chic party choices: delicate one-side chains, finger mandalas, floral kolki, or back-hand grids starting at accessible rates.\n"
            "   - Perfect for Eid, family weddings, sangeet, or bridesmaid groups.\n\n"

            "3. HENNA ACADEMY & COURSES:\n"
            "   - Explain the skill journey: Level 1 (Basic to Advance) builds cone grip, steady pressure control, clean lines, jhumka, and mandala mastery. Level 2 (Advance to Pro) unlocks bridal cutwork, shading, negative space, mirror work, and miniature motifs.\n"
            "   - Mention both Azimpur In-Person studio (strictly 5 students max) and Live Online (Google Meet) formats, plus the 10% combo discount.\n"
            "   - Note that term schedules and active fees are confirmed directly via direct inquiry.\n\n"

            "4. 100% ORGANIC CONES & STAIN SCIENCE:\n"
            "   - Emphasize zero chemicals, zero PPD, and 100% halal ingredients. Handcrafted with Rajasthani triple-filtered henna powder and essential oils (cajeput/lavender/eucalyptus) for 100 BDT/cone.\n"
            "   - Share authentic aftercare: keep paste 6-8 hours, apply lemon-sugar sealant, never wash with soap/water on day one, apply mustard/coconut oil before baths, let stain oxidize naturally to deep mahogany over 24-48 hours.\n\n"

            "5. HOME SERVICE & BOOKING IN DHAKA:\n"
            "   - Available across all Dhaka neighborhoods (Gulshan, Banani, Dhanmondi, Uttara, Mirpur, Old Dhaka, etc.).\n"
            "   - Service charge depends on travel distance from Azimpur studio. Recommend booking 1-2 weeks in advance.\n\n"

            "=== CALL TO ACTION & CONTACT ===\n"
            "- When booking, exact dates, custom coverage, or orders are discussed, naturally guide them to direct concierge links:\n"
            "  💬 [WhatsApp Concierge](https://wa.me/8801323278403) | 📱 [Facebook Messenger](https://m.me/Rafiya.HennaArt)\n"
            "- Do NOT paste the exact same boilerplate contact disclaimer on every single sentence. Keep the conversation natural, inspiring, and helpful."
        )

    def _dispatch_tool_call(self, tool_name: str, args: Dict[str, Any]) -> str:
        """Route tool call from Gemini to the MCP Knowledge Server."""
        logger.debug(f"Agentic Tool Execution: {tool_name} with args: {args}")
        try:
            if tool_name == "get_package_details":
                cat = str(args.get("category_or_name", ""))
                return self.mcp_server.get_package_details(category_or_name=cat)
            elif tool_name == "get_course_details":
                name = str(args.get("course_name", ""))
                return self.mcp_server.get_course_details(course_name=name)
            elif tool_name == "get_studio_faq":
                q = str(args.get("question_or_topic", ""))
                return self.mcp_server.get_studio_faq(question_or_topic=q)
            elif tool_name == "search_knowledge_base":
                query = str(args.get("query", ""))
                return self.mcp_server.search_knowledge_base(query=query)
            else:
                return self.mcp_server.search_knowledge_base(query=str(args))
        except Exception as e:
            logger.debug(f"Error executing MCP tool '{tool_name}': {e}")
            return f"Error retrieving studio details: {e}"

    def _init_chat(self, model_name: str, history: Optional[List] = None) -> bool:
        """Initialize chat session on model with MCP tools."""
        try:
            tools = self.mcp_server.get_python_tools() if self.mcp_server else None
            self.model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=GENERATION_CONFIG,
                system_instruction=self.system_instruction,
                tools=tools,
            )
            self.chat_session = self.model.start_chat(history=history or [])
            self._session_model = model_name
            logger.debug(f"Initialized Gemini chat on '{model_name}' with MCP tools.")
            return True
        except Exception as e:
            logger.debug(f"Model '{model_name}' tool setup: {e}. Attempting tool-less fallback...")
            try:
                self.model = genai.GenerativeModel(
                    model_name=model_name,
                    generation_config=GENERATION_CONFIG,
                    system_instruction=self.system_instruction,
                )
                self.chat_session = self.model.start_chat(history=history or [])
                self._session_model = model_name
                return True
            except Exception as e2:
                logger.debug(f"Fallback init failed on '{model_name}': {e2}")
                self.model = None
                self.chat_session = None
                self._session_model = None
                return False

    def _configure_ai(self):
        """Initial configuration using the top available model."""
        try:
            if self.api_key:
                genai.configure(api_key=self.api_key)
            candidates = self.get_candidate_models()
            configured = False
            for cand in candidates:
                if self._init_chat(cand):
                    self._active_model_name = cand
                    configured = True
                    break

            if not configured:
                self._init_chat(DEFAULT_GEMINI_MODEL)
                self._active_model_name = DEFAULT_GEMINI_MODEL

            logger.debug(f"Studio AI initialized with model: {self._active_model_name}")
        except Exception as e:
            logger.exception(f"Failed to configure Gemini AI: {e}")

    @property
    def active_model_name(self) -> str:
        return self._active_model_name

    @property
    def active_model_label(self) -> str:
        return format_model_label(self._active_model_name)

    def reset(self):
        """Reset chat session history."""
        logger.debug("Resetting studio chat session.")
        if self.model:
            self.chat_session = self.model.start_chat(history=[])

    def _is_quota_or_recoverable_error(self, e: Exception) -> bool:
        """Check if exception is a 429 quota or recoverable rate limit error."""
        if isinstance(
            e,
            (
                google_exceptions.ResourceExhausted,
                google_exceptions.TooManyRequests,
                google_exceptions.DeadlineExceeded,
                google_exceptions.ServiceUnavailable,
                google_exceptions.NotFound,
                google_exceptions.InternalServerError,
            ),
        ):
            return True

        err_str = str(e).lower()
        markers = [
            "429", "503", "504", "404", "resource_exhausted",
            "resourceexhausted", "quota exceeded", "rate limit",
            "quota", "deadline expired", "exceeded your current quota",
            "no longer available", "overloaded",
        ]
        return any(m in err_str for m in markers)

    def get_candidate_models(self) -> List[str]:
        """Return candidate models respecting cooldowns."""
        now = time.time()
        self._exhausted_models = {
            m: exp for m, exp in self._exhausted_models.items() if exp > now
        }

        available: List[str] = []
        cooling_down: List[str] = []

        if self._active_model_name in self.model_pool:
            if self._active_model_name in self._exhausted_models:
                cooling_down.append(self._active_model_name)
            else:
                available.append(self._active_model_name)

        for m in self.model_pool:
            if m not in available and m not in cooling_down:
                if m in self._exhausted_models:
                    cooling_down.append(m)
                else:
                    available.append(m)

        return available if available else cooling_down

    def stream_response(self, user_input: str) -> Generator[str, None, None]:
        """
        Yield streaming text chunks for st.write_stream().
        Fast paths through semantic cache. If not cached, runs autonomous MCP tool
        calling and transparently fails over to alternative Gemini models on 429 quota limits.
        """
        # 1. Semantic Cache check (Instant, 0 API tokens)
        cached_result = self.cache.get(user_input)
        if cached_result:
            cached_text, score = cached_result
            logger.debug(f"Serving query from semantic cache (similarity: {score:.2f})")
            for chunk in self.cache.stream_cached_response(cached_text):
                yield chunk
            return

        candidate_models = self.get_candidate_models()
        prior_history = list(self.chat_session.history) if self.chat_session else []

        collected_chunks: List[str] = []

        for model_candidate in candidate_models:
            if (
                self._session_model != model_candidate
                or not self.chat_session
                or not self.model
            ):
                initialized = self._init_chat(model_candidate, history=prior_history)
                if not initialized:
                    self._exhausted_models[model_candidate] = (
                        time.time() + MODEL_QUOTA_COOLDOWN_SECONDS
                    )
                    continue

            yielded_any = False
            try:
                logger.debug(f"Generating studio response on '{model_candidate}'...")
                response = self.chat_session.send_message(user_input, stream=True)

                pending_fn_call = None
                for chunk in response:
                    if not chunk.candidates:
                        continue
                    parts = chunk.candidates[0].content.parts
                    for p in parts:
                        if p.function_call:
                            pending_fn_call = p.function_call
                        elif p.text:
                            yielded_any = True
                            collected_chunks.append(p.text)
                            yield p.text

                # Handle MCP Tool Call if requested by Gemini
                if pending_fn_call:
                    fn_name = pending_fn_call.name
                    fn_args = dict(pending_fn_call.args)
                    tool_result = self._dispatch_tool_call(fn_name, fn_args)

                    fn_part = glm.Part(
                        function_response=glm.FunctionResponse(
                            name=fn_name,
                            response={"result": tool_result},
                        )
                    )
                    stream_res = self.chat_session.send_message(fn_part, stream=True)
                    for final_chunk in stream_res:
                        if final_chunk and hasattr(final_chunk, "text") and final_chunk.text:
                            yielded_any = True
                            collected_chunks.append(final_chunk.text)
                            yield final_chunk.text

                if not yielded_any:
                    fallback_text = (
                        "I would be delighted to guide you! Whether you are exploring bridal looks (Mandala, Gorgeous, Arabic), "
                        "arranging home service in Dhaka, joining our Henna Academy, or ordering fresh organic cones — "
                        "feel free to ask or connect directly on [WhatsApp](https://wa.me/8801323278403) or [Messenger](https://m.me/Rafiya.HennaArt) 🌿✨."
                    )
                    yield fallback_text
                    return

                # Successfully completed turn -> cache result
                self._active_model_name = model_candidate
                full_text = "".join(collected_chunks)
                if full_text:
                    self.cache.set(user_input, full_text)
                return

            except Exception as e:
                if yielded_any:
                    logger.debug(f"Stream interrupted mid-generation on '{model_candidate}': {e}")
                    yield "\n\n*(Feel free to message directly on [WhatsApp](https://wa.me/8801323278403) for bespoke bookings!)*"
                    return

                if self._is_quota_or_recoverable_error(e):
                    self._exhausted_models[model_candidate] = (
                        time.time() + MODEL_QUOTA_COOLDOWN_SECONDS
                    )
                    logger.debug(
                        f"Model '{model_candidate}' hit quota. Failing over to next Gemini model..."
                    )
                    continue
                else:
                    logger.debug(f"Error on '{model_candidate}': {e}")
                    continue

        logger.warning("All candidate models exhausted.")
        yield get_funky_glitch_response()

    def generate_response(self, user_input: str) -> str:
        """Synchronous response generation."""
        return "".join(list(self.stream_response(user_input)))
