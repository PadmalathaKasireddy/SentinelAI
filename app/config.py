"""
Central configuration for SentinelAI.
Loads settings from environment variables with sensible defaults.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_BASE_URL = os.getenv("API_BASE_URL", f"http://localhost:{API_PORT}")

# Paths
MODELS_DIR = ROOT_DIR / os.getenv("MODELS_DIR", "models")
DATASETS_DIR = ROOT_DIR / "datasets"
ASSETS_DIR = ROOT_DIR / "assets"
UPLOADS_DIR = ROOT_DIR / "uploads"
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "sentinel.db"

# Ensure directories exist
for _dir in (MODELS_DIR, DATASETS_DIR, UPLOADS_DIR, DATA_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# OpenAI (optional)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Threat level thresholds
THREAT_THRESHOLDS = {
    "safe": 0.33,
    "suspicious": 0.66,
    "dangerous": 1.0,
}

# UI theme colors (cybersecurity dark theme)
THEME = {
    "primary": "#00d4aa",
    "secondary": "#1a1f2e",
    "accent": "#ff4757",
    "warning": "#ffa502",
    "success": "#2ed573",
    "background": "#0e1117",
    "card": "#161b22",
    "text": "#e6edf3",
    "muted": "#8b949e",
}
