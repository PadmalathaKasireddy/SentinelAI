"""
Lazy model loading with functools.lru_cache — fast startup on Streamlit Cloud.
"""

from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib

from app.config import MODELS_DIR


def model_path(name: str) -> Path:
    return MODELS_DIR / name


def models_exist() -> bool:
    """Check if demo models have been trained."""
    required = [
        "phishing_model.joblib",
        "sms_model.joblib",
        "sms_vectorizer.joblib",
        "fake_news_model.joblib",
        "fake_news_vectorizer.joblib",
        "deepfake_model.joblib",
    ]
    return all(model_path(f).exists() for f in required)


@lru_cache(maxsize=1)
def load_phishing_bundle() -> dict[str, Any]:
    return joblib.load(model_path("phishing_model.joblib"))


@lru_cache(maxsize=1)
def load_sms_bundle() -> tuple[Any, Any]:
    return (
        joblib.load(model_path("sms_vectorizer.joblib")),
        joblib.load(model_path("sms_model.joblib")),
    )


@lru_cache(maxsize=1)
def load_fake_news_bundle() -> tuple[Any, Any]:
    return (
        joblib.load(model_path("fake_news_vectorizer.joblib")),
        joblib.load(model_path("fake_news_model.joblib")),
    )


@lru_cache(maxsize=1)
def load_deepfake_bundle() -> dict[str, Any]:
    return joblib.load(model_path("deepfake_model.joblib"))


def ensure_models() -> None:
    """Train demo models on first run if missing."""
    if not models_exist():
        from scripts.train_all import train_all_models
        train_all_models()
