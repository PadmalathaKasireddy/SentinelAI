"""
Module 3: Fake news detection — lightweight TF-IDF + Logistic Regression.
"""

from typing import Any

from utils.model_loader import ensure_models, load_fake_news_bundle
from utils.text_features import clean_text
from utils.threat_levels import score_to_threat_level

# Heuristic sensationalism markers
SENSATIONAL = ["shocking", "secret", "they don't want", "!!!", "anonymous", "hoax", "miracle"]


def predict_fake_news(text: str) -> dict[str, Any]:
    ensure_models()
    vec, clf = load_fake_news_bundle()
    cleaned = clean_text(text)
    X = vec.transform([cleaned])
    proba = clf.predict_proba(X)[0]
    fake_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])
    label = "Fake" if fake_prob >= 0.5 else "Real"

    sensational_hits = [s for s in SENSATIONAL if s in text.lower()]
    coef = clf.coef_[0]
    vocab = vec.get_feature_names_out()
    top_idx = coef.argsort()[-5:][::-1]
    top_words = [vocab[i] for i in top_idx if coef[i] > 0][:5]

    return {
        "text": text[:500],
        "prediction": label,
        "threat_level": score_to_threat_level(fake_prob),
        "fake_probability": round(fake_prob, 4),
        "confidence": round(max(fake_prob, 1 - fake_prob), 4),
        "sensational_markers": sensational_hits,
        "explanation": [
            f"Model fake probability: {fake_prob:.2%}",
            f"Sensational language detected: {len(sensational_hits)} marker(s)",
            f"Top risk-associated terms (global): {', '.join(top_words) or 'N/A'}",
        ],
    }
