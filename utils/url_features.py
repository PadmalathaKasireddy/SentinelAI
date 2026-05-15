"""
URL feature extraction for phishing and suspicious URL analysis.
Beginner-friendly: each function extracts one interpretable signal.
"""

import math
import re
from typing import Any
from urllib.parse import urlparse

import tldextract

# Keywords often seen in malicious URLs
MALICIOUS_KEYWORDS = [
    "login", "verify", "secure", "account", "update", "banking",
    "password", "confirm", "wallet", "crypto", "free", "winner",
    "urgent", "suspend", "click", "bit.ly", "tinyurl",
]

SUSPICIOUS_SYMBOLS = ["@", "%", "#", "\\", "..", "--"]


def _safe_parse(url: str) -> urlparse:
    """Normalize URL before parsing."""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return urlparse(url)


def url_length(url: str) -> int:
    """Total character count of the URL."""
    return len(url.strip())


def has_https(url: str) -> int:
    """1 if HTTPS, 0 otherwise."""
    parsed = _safe_parse(url)
    return 1 if parsed.scheme == "https" else 0


def count_suspicious_symbols(url: str) -> int:
    """Count suspicious symbols in the URL string."""
    return sum(url.count(sym) for sym in SUSPICIOUS_SYMBOLS)


def count_subdomains(url: str) -> int:
    """Number of subdomain parts (excluding www)."""
    ext = tldextract.extract(url)
    if not ext.subdomain:
        return 0
    parts = [p for p in ext.subdomain.split(".") if p.lower() != "www"]
    return len(parts)


def has_ip_domain(url: str) -> int:
    """1 if hostname looks like an IP address."""
    parsed = _safe_parse(url)
    host = parsed.netloc.split(":")[0]
    ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    return 1 if re.match(ip_pattern, host) else 0


def url_entropy(url: str) -> float:
    """
    Shannon entropy of the URL string.
    High entropy can indicate obfuscation.
    """
    if not url:
        return 0.0
    freq: dict[str, int] = {}
    for char in url:
        freq[char] = freq.get(char, 0) + 1
    length = len(url)
    entropy = 0.0
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return round(entropy, 4)


def count_malicious_keywords(url: str) -> int:
    """Count how many known malicious keywords appear."""
    lower = url.lower()
    return sum(1 for kw in MALICIOUS_KEYWORDS if kw in lower)


def has_redirect_pattern(url: str) -> int:
    """Detect common redirect / URL-shortener patterns."""
    patterns = [r"url=", r"redirect", r"goto=", r"link=", r"//", r"\.tk\b", r"\.ml\b"]
    lower = url.lower()
    return 1 if any(re.search(p, lower) for p in patterns) else 0


def digit_ratio(url: str) -> float:
    """Ratio of digits to total length."""
    if not url:
        return 0.0
    digits = sum(c.isdigit() for c in url)
    return round(digits / len(url), 4)


def special_char_ratio(url: str) -> float:
    """Ratio of non-alphanumeric characters."""
    if not url:
        return 0.0
    special = sum(not c.isalnum() for c in url)
    return round(special / len(url), 4)


def mock_domain_age_days(url: str) -> int:
    """
    Mock domain age based on TLD heuristics (demo when WHOIS unavailable).
    Suspicious TLDs get low age; .edu/.gov get high age.
    """
    ext = tldextract.extract(url)
    tld = (ext.suffix or "").lower()
    risky_tlds = {"tk", "ml", "ga", "cf", "gq", "xyz", "top", "work"}
    trusted = {"edu", "gov", "org"}
    if tld in risky_tlds:
        return 30
    if tld in trusted:
        return 3650
    return 400


def extract_phishing_features(url: str) -> dict[str, Any]:
    """Full feature vector for phishing URL model."""
    return {
        "url_length": url_length(url),
        "has_https": has_https(url),
        "suspicious_symbols": count_suspicious_symbols(url),
        "subdomain_count": count_subdomains(url),
        "has_ip_domain": has_ip_domain(url),
        "entropy": url_entropy(url),
        "malicious_keywords": count_malicious_keywords(url),
        "redirect_pattern": has_redirect_pattern(url),
        "digit_ratio": digit_ratio(url),
        "special_char_ratio": special_char_ratio(url),
        "domain_age_days": mock_domain_age_days(url),
    }


def features_to_vector(features: dict[str, Any], feature_names: list[str]) -> list[float]:
    """Convert feature dict to ordered list for sklearn."""
    return [float(features[name]) for name in feature_names]


PHISHING_FEATURE_NAMES = list(extract_phishing_features("https://example.com").keys())
