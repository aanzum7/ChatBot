"""
Model Context Protocol (MCP) Knowledge Server for Rafiya's Henna Art.

Indexes studio packages, 2026 training courses, products, booking policies,
and aftercare FAQs into discrete semantic memory cards. Exposes functions
for Gemini tool calling and a standard JSON-RPC 2.0 stdio protocol handler.
"""
from __future__ import annotations

import json
import re
import sys
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional, Set, Tuple

from services.logger import get_logger

logger = get_logger(__name__)

STOPWORDS: Set[str] = {
    "a", "about", "an", "and", "are", "as", "at", "be", "by", "can", "could",
    "do", "does", "for", "from", "how", "i", "in", "is", "it", "me", "my",
    "of", "on", "or", "tell", "the", "to", "was", "what", "when", "where",
    "which", "who", "why", "with", "would", "you", "your", "please", "koto",
    "dam", "ki", "hobe"
}

def _tokenize(text: str) -> List[str]:
    """Extract lowercase alphanumeric tokens."""
    return re.findall(r"\b\w+\b", text.lower())

def _significant_tokens(text: str) -> Set[str]:
    """Extract non-stopword tokens."""
    tokens = _tokenize(text)
    meaningful = {w for w in tokens if w not in STOPWORDS}
    return meaningful if meaningful else set(tokens)


class MCPKnowledgeBase:
    """
    Structured Memory & MCP Tool provider for Rafiya's Henna Art.
    """

    def __init__(self, personal_data: Dict[str, Any], faq_data: List[Dict[str, Any]]):
        self.personal = personal_data or {}
        self.raw_faq = faq_data or []
        self.packages: List[Dict[str, Any]] = self.personal.get("packages", [])
        self.course_info: Dict[str, Any] = self.personal.get("course", {})
        self.products: Dict[str, Any] = self.personal.get("products", {})
        self.contacts: Dict[str, Any] = self.personal.get("contacts", {})

        self.memory_cards: Dict[str, Dict[str, Any]] = {}
        self._build_memory_index()

    def _build_memory_index(self):
        """Indexes all studio context into semantic memory cards."""

        # 1. Studio Overview Card
        overview_text = (
            "Rafiya's Henna Art is a premier atelier based in Azimpur, Dhaka, Bangladesh, "
            "specializing in fine bridal, semi-bridal, and contemporary non-bridal henna designs. "
            "Artist: Rafiya. All henna used is 100% organic, chemical-free, and halal.\n"
            "Direct Booking Channels:\n"
            "- WhatsApp: +8801323278403 (wa.me/8801323278403)\n"
            "- Messenger: m.me/Rafiya.HennaArt\n"
            "- Email: rafiyashennaart@gmail.com\n"
            "- Instagram: @rafiyas_henna_art\n"
            "Home service is available within Dhaka city (service charges depend on location)."
        )
        self.memory_cards["overview"] = {
            "title": "Studio Overview & Artist Rafiya",
            "keywords": {"studio", "rafiya", "henna", "mehendi", "about", "artist", "location", "azimpur", "dhaka"},
            "content": overview_text,
        }

        # 2. Packages Catalog Card
        bridal_pkgs = [p for p in self.packages if "bridal" in p.get("type", "").lower() and "non-bridal" not in p.get("type", "").lower()]
        non_bridal_pkgs = [p for p in self.packages if "non-bridal" in p.get("type", "").lower()]

        b_lines = [f"- {p['name']} ({p.get('length', '')}): {p.get('price')} BDT — {p.get('description', '')}" for p in bridal_pkgs]
        nb_lines = [f"- {p['name']} ({p.get('length', '')}): {p.get('price')} BDT — {p.get('description', '')}" for p in non_bridal_pkgs]

        packages_text = (
            "=== BRIDAL HENNA PACKAGES ===\n" + "\n".join(b_lines) + "\n\n"
            "=== NON-BRIDAL / PARTY HENNA PACKAGES ===\n" + "\n".join(nb_lines) + "\n\n"
            "All bridal packages cover both hands, both sides. Non-bridal rates are per hand, per side."
        )
        self.memory_cards["packages"] = {
            "title": "Bridal & Non-Bridal Henna Packages Catalog",
            "keywords": {"package", "packages", "price", "rate", "cost", "bridal", "non-bridal", "party", "pricing", "elbow", "wrist", "mandala", "arabic"},
            "content": packages_text,
        }

        # 3. Academy Courses & Training Card
        c_list = self.course_info.get("courses", [])
        c_lines = []
        for c in c_list:
            c_lines.append(
                f"Course: {c.get('title')}\n"
                f"- Duration: {c.get('total_classes')} intensive classes (Seats: Strictly limited to 5 students per batch)\n"
                f"- Eligibility: {c.get('eligibility')} | Outcome: {c.get('outcome')}\n"
                f"- Formats: Offline Studio (Azimpur, Dhaka) & Live Online (Google Meet)\n"
                f"- Syllabus:\n{c.get('learning')}\n"
            )

        combo = self.course_info.get("combo_offer", {})
        materials = self.course_info.get("materials", {})
        exam = self.course_info.get("exam", {})

        courses_text = (
            f"Title: {self.course_info.get('title', 'Rafiya Henna Course')}\n"
            f"Note: {self.course_info.get('note', '')}\n\n"
            + "\n".join(c_lines)
            + f"\nCombo Offer: {combo.get('details', 'Enroll in both courses together')} -> Special combo discount available!\n"
            + f"Materials: {materials.get('offline', '')}\n"
            + f"Exam & Certification: {exam.get('details', '')}\n"
            + "IMPORTANT ON SCHEDULE & TUITION: Active batch schedules, daily class timings, and current tuition fees vary by season and seat capacity. Direct visitors to message artist Rafiya directly via WhatsApp (wa.me/8801323278403) or Messenger (m.me/Rafiya.HennaArt) to check if admissions are currently open and confirm exact tuition details."
        )
        self.memory_cards["courses"] = {
            "title": "Henna Academy Courses & Training Plans",
            "keywords": {"course", "courses", "class", "training", "learn", "academy", "fee", "tuition", "schedule", "certificate", "combo", "discount"},
            "content": courses_text,
        }

        # 4. Products Card (Organic Cones)
        items = self.products.get("items", [])
        p_lines = [f"- {it.get('name')}: {it.get('description')} (MRP: {it.get('mrp')} BDT)" for it in items]
        products_text = (
            "Organic Cones & Products:\n"
            + "\n".join(p_lines)
            + "\nHandmade with 100% natural henna leaves and premium essential oils (eucalyptus/lavender/cajeput). Halal and completely chemical-free."
        )
        self.memory_cards["products"] = {
            "title": "Organic Henna Cones & Studio Products",
            "keywords": {"cone", "cones", "product", "products", "organic", "halal", "natural", "chemical", "oil", "buy"},
            "content": products_text,
        }

        # 5. Home Service & Booking Policy
        booking_text = (
            "Home Service & Appointment Policy:\n"
            "- Home service is provided across Dhaka city only. Service charge varies by specific area (confirm by messaging exact location).\n"
            "- Bridal booking: Recommended at least 1 week in advance.\n"
            "- Booking confirmation: Direct chat on WhatsApp (+8801323278403) or Facebook Messenger."
        )
        self.memory_cards["booking"] = {
            "title": "Home Service & Booking Guidelines",
            "keywords": {"home", "service", "booking", "book", "dhaka", "appointment", "reserve", "advance", "area", "charge"},
            "content": booking_text,
        }

        # 6. Aftercare & Stain Darkening
        aftercare_text = (
            "Stain Darkening & Henna Care Routine:\n"
            "1. Leave the henna paste on for 6 to 8 hours (or overnight for brides).\n"
            "2. Dab with lemon juice and sugar mixture once dry to keep paste attached.\n"
            "3. DO NOT wash with water! Scrape off the dried paste gently.\n"
            "4. Avoid contact with water for the first 24 hours.\n"
            "5. Apply natural coconut oil or mustard oil before showering to protect the stain.\n"
            "6. The stain oxidizes and achieves its deepest, darkest mahogany shade within 24-48 hours."
        )
        self.memory_cards["aftercare"] = {
            "title": "Henna Aftercare & Rich Stain Preservation Guide",
            "keywords": {"aftercare", "stain", "dark", "care", "color", "darken", "water", "oil", "lemon", "sugar", "wash", "mahogany"},
            "content": aftercare_text,
        }

    def search_knowledge_base(self, query: str, max_results: int = 2) -> str:
        """Search memory cards and FAQs for matching information."""
        if not query:
            return self.memory_cards["overview"]["content"]

        tokens = _significant_tokens(query)
        scored: List[Tuple[float, str, str]] = []

        # 1. Score Memory Cards
        for key, card in self.memory_cards.items():
            kws = card["keywords"]
            overlap = len(tokens.intersection(kws))
            ratio = SequenceMatcher(None, query.lower(), card["title"].lower()).ratio()
            score = (overlap * 2.5) + (ratio * 1.5)

            # Check if any token exists inside content
            content_lower = card["content"].lower()
            containment = sum(0.5 for t in tokens if t in content_lower)
            score += containment

            if score > 0.8:
                scored.append((score, card["title"], card["content"]))

        # 2. Score FAQs
        for faq in self.raw_faq:
            q_str = str(faq.get("question", ""))
            a_str = str(faq.get("answer", ""))
            seq_ratio = SequenceMatcher(None, query.lower(), q_str.lower()).ratio()
            q_tokens = _significant_tokens(q_str)
            intersection = len(tokens.intersection(q_tokens))
            faq_score = (intersection * 2.2) + (seq_ratio * 2.0)

            if faq_score > 1.2:
                scored.append((faq_score, f"FAQ: {q_str}", a_str))

        if not scored:
            return self.memory_cards["overview"]["content"]

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:max_results]
        return "\n\n".join([f"=== {title} ===\n{content}" for _, title, content in top])

    def get_package_details(self, category_or_name: str) -> str:
        """Retrieve details about specific henna packages or categories."""
        cat_lower = category_or_name.lower().strip()
        matched = []

        for p in self.packages:
            p_name = p.get("name", "").lower()
            p_type = p.get("type", "").lower()
            if cat_lower in p_name or cat_lower in p_type or p_name in cat_lower:
                matched.append(
                    f"• {p['name']} ({p.get('type')}) - {p.get('length')}, {p.get('hand')} ({p.get('side')}): {p.get('price')} BDT\n"
                    f"  Details: {p.get('description')}"
                )

        if matched:
            return "Found Packages:\n" + "\n".join(matched[:8])

        # Fallback to general packages card
        return self.memory_cards["packages"]["content"]

    def get_course_details(self, course_name: str = "") -> str:
        """Retrieve 2026 henna training course details, fees, and syllabus."""
        return self.memory_cards["courses"]["content"]

    def get_studio_faq(self, question_or_topic: str) -> str:
        """Search verified studio FAQs."""
        if not question_or_topic or not self.raw_faq:
            return self.memory_cards["aftercare"]["content"]

        tokens = _significant_tokens(question_or_topic)
        best_faq = None
        best_score = 0.0

        for faq in self.raw_faq:
            q = str(faq.get("question", ""))
            q_tokens = _significant_tokens(q)
            overlap = len(tokens.intersection(q_tokens)) / max(len(tokens), 1)
            ratio = SequenceMatcher(None, question_or_topic.lower(), q.lower()).ratio()
            score = (overlap * 0.6) + (ratio * 0.4)
            if score > best_score:
                best_score = score
                best_faq = faq

        if best_faq and best_score >= 0.40:
            return f"Q: {best_faq.get('question')}\nA: {best_faq.get('answer')}"

        return self.search_knowledge_base(question_or_topic, max_results=1)

    def get_tools_manifest(self) -> List[Dict[str, Any]]:
        """Return MCP standard JSON-RPC tools list manifest."""
        return [
            {
                "name": "search_knowledge_base",
                "description": "Search Rafiya's Henna Art knowledge base for details on studio rates, artist background, location, home service, and policies.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query about packages, courses, care, or booking."}
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "get_package_details",
                "description": "Lookup specific bridal or non-bridal henna packages, prices in BDT, lengths, and design coverage.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category_or_name": {"type": "string", "description": "Package name or category ('bridal', 'non-bridal', 'mandala', 'elbow', etc.)"}
                    },
                    "required": ["category_or_name"],
                },
            },
            {
                "name": "get_course_details",
                "description": "Lookup henna training academy courses (Basic to Advance, Advance to Pro), fees, online/offline schedules, and 10% combo discount.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "course_name": {"type": "string", "description": "Optional course name or inquiry"}
                    },
                },
            },
            {
                "name": "get_studio_faq",
                "description": "Lookup verified studio FAQs regarding home service in Dhaka, aftercare, dark stains, and booking.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question_or_topic": {"type": "string", "description": "FAQ topic or question"}
                    },
                    "required": ["question_or_topic"],
                },
            },
        ]


class MCPServer:
    """
    Model Context Protocol (MCP) Server for Rafiya's Henna Art.
    Exposes callable Python methods for Gemini tools=[...] and handles JSON-RPC 2.0 stdio.
    """

    def __init__(self, personal_data: Dict[str, Any], faq_data: List[Dict[str, Any]]):
        self.kb = MCPKnowledgeBase(personal_data=personal_data, faq_data=faq_data)

    def search_knowledge_base(self, query: str) -> str:
        """Search verified studio knowledge for packages, courses, booking, or aftercare."""
        return self.kb.search_knowledge_base(query=query)

    def get_package_details(self, category_or_name: str) -> str:
        """Lookup bridal or non-bridal package rates, lengths, and coverage."""
        return self.kb.get_package_details(category_or_name=category_or_name)

    def get_course_details(self, course_name: str = "") -> str:
        """Lookup 2026 henna training academy courses, syllabus, and fees."""
        return self.kb.get_course_details(course_name=course_name)

    def get_studio_faq(self, question_or_topic: str) -> str:
        """Lookup verified studio FAQs and aftercare tips."""
        return self.kb.get_studio_faq(question_or_topic=question_or_topic)

    def get_python_tools(self) -> List[Any]:
        """Return list of Python callable functions for Google Gemini tools parameter."""
        return [
            self.search_knowledge_base,
            self.get_package_details,
            self.get_course_details,
            self.get_studio_faq,
        ]

    def handle_jsonrpc(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle standard JSON-RPC 2.0 requests per MCP specification."""
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "rafiya-henna-mcp-server", "version": "1.0.0"},
                    "capabilities": {"tools": {}},
                },
            }
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": self.kb.get_tools_manifest()},
            }
        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})
            if tool_name == "search_knowledge_base":
                res = self.search_knowledge_base(query=str(args.get("query", "")))
            elif tool_name == "get_package_details":
                res = self.get_package_details(category_or_name=str(args.get("category_or_name", "")))
            elif tool_name == "get_course_details":
                res = self.get_course_details(course_name=str(args.get("course_name", "")))
            elif tool_name == "get_studio_faq":
                res = self.get_studio_faq(question_or_topic=str(args.get("question_or_topic", "")))
            else:
                res = self.search_knowledge_base(query=str(args))

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": res}]},
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"},
            }


def create_mcp_server(personal_data: Dict[str, Any], faq_data: List[Dict[str, Any]]) -> MCPServer:
    """Factory helper to instantiate an MCPServer."""
    return MCPServer(personal_data=personal_data, faq_data=faq_data)
