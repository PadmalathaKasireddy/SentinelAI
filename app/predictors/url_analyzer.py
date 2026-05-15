"""
Module 5: Suspicious URL intelligence analyzer (rule + feature scoring).
"""

from typing import Any

from utils.url_features import (
    MALICIOUS_KEYWORDS,
    extract_phishing_features,
    url_entropy,
)


def analyze_url(url: str) -> dict[str, Any]:
    """Risk score 0-100 with recommendations — no ML required."""
    features = extract_phishing_features(url)
    score = 0.0
    reasons = []
    recommendations = []

    if not features["has_https"]:
        score += 15
        reasons.append("Missing HTTPS")
        recommendations.append("Avoid entering credentials on non-HTTPS sites")

    if features["has_ip_domain"]:
        score += 25
        reasons.append("IP-based domain detected")

    if features["malicious_keywords"] > 0:
        score += 10 * min(features["malicious_keywords"], 3)
        reasons.append("Malicious keyword patterns found")

    if features["entropy"] > 4.5:
        score += 10
        reasons.append("High URL entropy (possible obfuscation)")

    if features["url_length"] > 75:
        score += 10
        reasons.append("Unusually long URL")

    if features["redirect_pattern"]:
        score += 15
        reasons.append("Redirect or shortener pattern detected")

    if features["subdomain_count"] > 2:
        score += 10
        reasons.append("Excessive subdomains")

    score = min(100.0, score)
    if score < 30:
        level = "Low Risk"
    elif score < 60:
        level = "Medium Risk"
    else:
        level = "High Risk"

    if score >= 40:
        recommendations.append("Do not click — verify domain via official channels")
    else:
        recommendations.append("Still verify sender and domain before sharing data")

    return {
        "url": url,
        "risk_score": round(score, 2),
        "risk_level": level,
        "entropy": url_entropy(url),
        "features": features,
        "explanation": reasons or ["No major structural risks detected"],
        "recommendations": recommendations,
        "keywords_checked": MALICIOUS_KEYWORDS[:8],
    }
