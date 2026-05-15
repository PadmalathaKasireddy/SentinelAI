"""Basic tests for SentinelAI predictors."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.train_all import train_all_models


def setup_module():
    train_all_models()


def test_phishing_safe_url():
    from app.predictors.phishing import predict_phishing
    r = predict_phishing("https://www.python.org")
    assert "prediction" in r
    assert "confidence" in r


def test_phishing_risky_url():
    from app.predictors.phishing import predict_phishing
    r = predict_phishing("http://192.168.1.1/paypal-verify.tk/login")
    assert r["risk_score"] >= 0


def test_sms_legitimate():
    from app.predictors.sms import predict_sms
    r = predict_sms("See you at lunch tomorrow.")
    assert r["prediction"] in ("Scam", "Legitimate")


def test_fake_news():
    from app.predictors.fake_news import predict_fake_news
    r = predict_fake_news("City council approved the park budget after review.")
    assert r["prediction"] in ("Fake", "Real")


def test_url_analyzer():
    from app.predictors.url_analyzer import analyze_url
    r = analyze_url("https://example.com")
    assert 0 <= r["risk_score"] <= 100


def test_chatbot():
    from chatbot.assistant import chat
    r = chat("What is phishing?")
    assert "reply" in r
    assert r["source"] == "rule_based"
