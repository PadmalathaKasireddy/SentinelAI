"""
Module 2: Scam SMS detection — TF-IDF + Logistic Regression.
"""

import re
from typing import Any

from utils.model_loader import ensure_models, load_sms_bundle
from utils.text_features import URGENCY_WORDS, FINANCIAL_WORDS, clean_text, sms_heuristic_features
from utils.threat_levels import score_to_threat_level


def _highlight_terms(text: str) -> list[str]:
    """Find suspicious words present in the message."""
    lower = text.lower()
    found = []
    for w in URGENCY_WORDS + FINANCIAL_WORDS:
        if w in lower:
            found.append(w)
    if re.search(r"http[s]?://|bit\.ly|tinyurl", lower):
        found.append("suspicious_link")
    return list(set(found))


def predict_sms(text: str) -> dict[str, Any]:
    ensure_models()
    vec, clf = load_sms_bundle()
    cleaned = clean_text(text)
    X = vec.transform([cleaned])
    proba = clf.predict_proba(X)[0]
    scam_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])
    label = "Scam" if scam_prob >= 0.5 else "Legitimate"
    heuristics = sms_heuristic_features(text)

    return {
        "text": text,
        "prediction": label,
        "threat_level": score_to_threat_level(scam_prob),
        "scam_probability": round(scam_prob, 4),
        "confidence": round(max(scam_prob, 1 - scam_prob), 4),
        "highlighted_terms": _highlight_terms(text),
        "heuristic_features": heuristics,
        "explanation": [
            f"Urgency indicators: {heuristics['urgency_count']}",
            f"Financial terms: {heuristics['financial_count']}",
            f"Contains link pattern: {'Yes' if heuristics['has_link'] else 'No'}",
        ],
    }
