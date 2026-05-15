"""
Module 6: Offline rule-based cybersecurity chatbot (no paid APIs).
Optional OpenAI hook via env var for future extension.
"""

import os
import re
from typing import Any

# FAQ knowledge base — lightweight, expandable
KNOWLEDGE = {
    "phishing": (
        "Phishing tricks you into revealing credentials via fake emails or sites. "
        "Check the URL, look for HTTPS, and never click urgent login links."
    ),
    "sms": (
        "Smishing is scam SMS. Watch for urgency, prizes, and shortened links. "
        "Banks rarely ask you to click links in texts."
    ),
    "fake news": (
        "Fake news spreads misinformation. Verify sources, check author credentials, "
        "and cross-reference with trusted outlets."
    ),
    "deepfake": (
        "Deepfakes use AI to alter faces in images/video. Look for unnatural blinking, "
        "lighting mismatches, and blurry face boundaries."
    ),
    "password": (
        "Use unique passwords, a password manager, and enable multi-factor authentication (MFA)."
    ),
    "malware": (
        "Malware includes viruses and ransomware. Keep software updated, avoid unknown downloads, "
        "and scan attachments."
    ),
    "default": (
        "I'm SentinelAI Assistant. Ask about phishing, SMS scams, fake news, deepfakes, "
        "passwords, or malware. I can also explain your scan results."
    ),
}

INTENT_PATTERNS = [
    (r"phish|url|link|website", "phishing"),
    (r"sms|text message|smish", "sms"),
    (r"fake news|misinformation|article", "fake news"),
    (r"deepfake|fake image|manipulated", "deepfake"),
    (r"password|mfa|2fa|credential", "password"),
    (r"malware|virus|ransomware", "malware"),
    (r"prevent|protect|tips|safe", "default"),
]


def _match_intent(message: str) -> str:
    lower = message.lower()
    for pattern, key in INTENT_PATTERNS:
        if re.search(pattern, lower):
            return key
    return "default"


def chat(message: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Return chatbot reply. context may include last_prediction from dashboard.
    """
    # Optional OpenAI — only if key set (not required)
    api_key = os.getenv("OPENAI_API_KEY", "")
    if api_key:
        return {
            "reply": (
                "[OpenAI placeholder] Set up openai client in production. "
                f"Your question: {message[:100]}"
            ),
            "source": "openai_placeholder",
        }

    intent = _match_intent(message)
    reply = KNOWLEDGE.get(intent, KNOWLEDGE["default"])

    if context and context.get("last_prediction"):
        lp = context["last_prediction"]
        reply += (
            f"\n\nRegarding your last scan ({lp.get('module', 'unknown')}): "
            f"result was **{lp.get('prediction')}** with confidence {lp.get('confidence', 'N/A')}."
        )

    tips = [
        "Enable MFA on all important accounts.",
        "Verify URLs before entering passwords.",
        "Be skeptical of urgent financial messages.",
    ]
    return {
        "reply": reply,
        "intent": intent,
        "tips": tips,
        "source": "rule_based",
    }
