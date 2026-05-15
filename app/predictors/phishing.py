"""
Module 1: Phishing URL detection using RandomForest on URL features.
"""

from typing import Any

import numpy as np

from utils.model_loader import ensure_models, load_phishing_bundle
from utils.threat_levels import score_to_threat_level
from utils.url_features import extract_phishing_features


def predict_phishing(url: str) -> dict[str, Any]:
    ensure_models()
    bundle = load_phishing_bundle()
    clf = bundle["model"]
    names = bundle["feature_names"]

    features = extract_phishing_features(url)
    X = np.array([[features[k] for k in names]])
    proba = clf.predict_proba(X)[0]
    # class 1 = phishing
    risk = float(proba[1]) if len(proba) > 1 else float(proba[0])
    pred_label = "Dangerous" if risk >= 0.66 else ("Suspicious" if risk >= 0.33 else "Safe")

    # Rule-based explanation from top signals
    explanations = []
    if not features["has_https"]:
        explanations.append("URL does not use HTTPS")
    if features["has_ip_domain"]:
        explanations.append("Hostname appears to be an IP address")
    if features["malicious_keywords"] > 0:
        explanations.append(f"Contains {features['malicious_keywords']} suspicious keyword(s)")
    if features["suspicious_symbols"] > 2:
        explanations.append("High count of suspicious symbols")
    if features["domain_age_days"] < 90:
        explanations.append("Domain age appears very young (heuristic)")
    if not explanations:
        explanations.append("No major red flags in URL structure")

    importances = dict(zip(names, clf.feature_importances_.tolist()))
    top_features = sorted(importances.items(), key=lambda x: -x[1])[:5]

    return {
        "url": url,
        "prediction": pred_label,
        "threat_level": score_to_threat_level(risk),
        "confidence": round(max(risk, 1 - risk), 4),
        "risk_score": round(risk, 4),
        "feature_values": features,
        "explanation": explanations,
        "top_features": top_features,
    }
