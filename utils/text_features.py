"""
Text feature helpers for SMS and fake news modules.
"""

import re
from typing import Any

# Urgency / scam indicators in SMS
URGENCY_WORDS = [
    "urgent", "immediately", "act now", "limited", "expire", "winner",
    "congratulations", "free", "claim", "verify", "suspended", "locked",
]

FINANCIAL_WORDS = [
    "bank", "account", "credit", "debit", "payment", "transfer", "refund",
    "bitcoin", "crypto", "wallet", "irs", "tax",
]

LINK_PATTERNS = [
    r"http[s]?://",
    r"bit\.ly",
    r"tinyurl",
    r"\.com/",
    r"click here",
]


def count_word_matches(text: str, word_list: list[str]) -> int:
    """Count how many words from list appear in text."""
    lower = text.lower()
    return sum(1 for w in word_list if w in lower)


def has_suspicious_link(text: str) -> int:
    """1 if text contains link-like patterns."""
    lower = text.lower()
    return 1 if any(re.search(p, lower) for p in LINK_PATTERNS) else 0


def sms_heuristic_features(text: str) -> dict[str, Any]:
    """Interpretable SMS scam signals."""
    return {
        "urgency_count": count_word_matches(text, URGENCY_WORDS),
        "financial_count": count_word_matches(text, FINANCIAL_WORDS),
        "has_link": has_suspicious_link(text),
        "message_length": len(text),
        "uppercase_ratio": sum(1 for c in text if c.isupper()) / max(len(text), 1),
        "exclamation_count": text.count("!"),
    }


def clean_text(text: str) -> str:
    """Basic text normalization for NLP."""
    text = text.lower().strip()
    text = re.sub(r"http\S+", " URL ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
