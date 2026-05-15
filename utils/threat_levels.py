"""
Map model probabilities to human-readable threat levels.
"""

from typing import Literal

ThreatLevel = Literal["Safe", "Suspicious", "Dangerous"]


def score_to_threat_level(score: float, invert: bool = False) -> ThreatLevel:
    """
    Convert a 0-1 risk score to Safe / Suspicious / Dangerous.
    invert=False: higher score = more dangerous.
    invert=True: higher score = safer (e.g. legitimacy probability).
    """
    if invert:
        score = 1.0 - score
    if score < 0.33:
        return "Safe"
    if score < 0.66:
        return "Suspicious"
    return "Dangerous"


def threat_color(level: ThreatLevel) -> str:
    """Hex color for UI badges."""
    return {
        "Safe": "#2ed573",
        "Suspicious": "#ffa502",
        "Dangerous": "#ff4757",
    }.get(level, "#8b949e")
