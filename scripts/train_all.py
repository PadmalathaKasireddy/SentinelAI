"""
Train all lightweight demo models from sample CSV datasets.
Run: python -m scripts.train_all
Models saved to models/ (small joblib files, gitignored).
"""

import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import DATASETS_DIR, MODELS_DIR
from utils.image_features import feature_names
from utils.text_features import clean_text
from utils.url_features import PHISHING_FEATURE_NAMES, extract_phishing_features


def train_phishing() -> None:
    """RandomForest on URL features — lightweight, interpretable."""
    df = pd.read_csv(DATASETS_DIR / "sample_phishing_urls.csv")
    X = np.array([
        [extract_phishing_features(u)[k] for k in PHISHING_FEATURE_NAMES]
        for u in df["url"]
    ])
    y = df["label"].values
    clf = RandomForestClassifier(n_estimators=50, max_depth=8, random_state=42)
    clf.fit(X, y)
    bundle = {"model": clf, "feature_names": PHISHING_FEATURE_NAMES}
    joblib.dump(bundle, MODELS_DIR / "phishing_model.joblib")
    print("[OK] Phishing model saved.")


def train_sms() -> None:
    """TF-IDF + Logistic Regression for scam SMS."""
    df = pd.read_csv(DATASETS_DIR / "sample_sms.csv")
    texts = [clean_text(t) for t in df["text"]]
    y = df["label"].values
    vec = TfidfVectorizer(max_features=500, ngram_range=(1, 2), stop_words="english")
    X = vec.fit_transform(texts)
    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(X, y)
    joblib.dump(vec, MODELS_DIR / "sms_vectorizer.joblib")
    joblib.dump(clf, MODELS_DIR / "sms_model.joblib")
    print("[OK] SMS model saved.")


def train_fake_news() -> None:
    """TF-IDF + Logistic Regression for fake news (lightweight vs BERT)."""
    df = pd.read_csv(DATASETS_DIR / "sample_fake_news.csv")
    texts = [clean_text(t) for t in df["text"]]
    y = df["label"].values
    vec = TfidfVectorizer(max_features=800, ngram_range=(1, 2), stop_words="english")
    X = vec.fit_transform(texts)
    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(X, y)
    joblib.dump(vec, MODELS_DIR / "fake_news_vectorizer.joblib")
    joblib.dump(clf, MODELS_DIR / "fake_news_model.joblib")
    print("[OK] Fake news model saved.")


def train_deepfake() -> None:
    """
  Synthetic demo data from image feature heuristics.
  In production, replace with real labeled face datasets.
  """
    names = feature_names()
    # Synthetic: "deepfake-like" = high edge + low laplacian variance pattern
    rng = np.random.RandomState(42)
    n = 80
    X_real = rng.randn(n, len(names)) * 0.5 + np.array([400, 400, 1.0, 120, 25, 0.08, 6.5, 128])
    X_fake = X_real + rng.randn(n, len(names)) * 2
    X_fake[:, 3] *= 0.3  # lower laplacian_var
    X_fake[:, 5] *= 1.5  # higher edge_ratio
    X = np.vstack([X_real, X_fake])
    y = np.array([0] * n + [1] * n)
    clf = RandomForestClassifier(n_estimators=30, max_depth=6, random_state=42)
    clf.fit(X, y)
    bundle = {"model": clf, "feature_names": names}
    joblib.dump(bundle, MODELS_DIR / "deepfake_model.joblib")
    print("[OK] Deepfake model saved (synthetic demo).")


def train_all_models() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    train_phishing()
    train_sms()
    train_fake_news()
    train_deepfake()
    print("All models trained successfully.")


if __name__ == "__main__":
    train_all_models()
