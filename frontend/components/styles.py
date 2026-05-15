"""
Custom CSS for dark cybersecurity theme.
Inject once at app startup.
"""

import streamlit as st

from app.config import THEME


def inject_custom_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Inter:wght@400;600;700&display=swap');

        .stApp {{
            background: linear-gradient(160deg, {THEME['background']} 0%, #0a0e14 100%);
            color: {THEME['text']};
            font-family: 'Inter', sans-serif;
        }}

        [data-testid="stSidebar"] {{
            background: {THEME['secondary']};
            border-right: 1px solid #30363d;
        }}

        .sentinel-title {{
            font-size: 1.8rem;
            font-weight: 700;
            color: {THEME['primary']};
            letter-spacing: -0.5px;
        }}

        .sentinel-sub {{
            color: {THEME['muted']};
            font-size: 0.95rem;
        }}

        .kpi-card {{
            background: {THEME['card']};
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        }}

        .kpi-value {{
            font-size: 2rem;
            font-weight: 700;
            color: {THEME['primary']};
            font-family: 'JetBrains Mono', monospace;
        }}

        .kpi-label {{
            color: {THEME['muted']};
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .threat-safe {{ color: {THEME['success']}; font-weight: 600; }}
        .threat-warn {{ color: {THEME['warning']}; font-weight: 600; }}
        .threat-danger {{ color: {THEME['accent']}; font-weight: 600; }}

        div[data-testid="stMetricValue"] {{
            font-family: 'JetBrains Mono', monospace;
        }}

        .stButton>button {{
            background: linear-gradient(90deg, #00b894, {THEME['primary']});
            color: #0e1117;
            border: none;
            font-weight: 600;
            border-radius: 8px;
        }}

        .stButton>button:hover {{
            filter: brightness(1.1);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def threat_badge(level: str) -> str:
    cls = {
        "Safe": "threat-safe",
        "Suspicious": "threat-warn",
        "Dangerous": "threat-danger",
        "Low Risk": "threat-safe",
        "Medium Risk": "threat-warn",
        "High Risk": "threat-danger",
    }.get(level, "sentinel-sub")
    return f'<span class="{cls}">{level}</span>'
