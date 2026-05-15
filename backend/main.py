"""
SentinelAI FastAPI backend — lightweight REST API for all detectors.
Run: uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.predictors.deepfake import predict_deepfake
from app.predictors.fake_news import predict_fake_news
from app.predictors.phishing import predict_phishing
from app.predictors.sms import predict_sms
from app.predictors.url_analyzer import analyze_url
from backend.schemas import ChatRequest, PredictionResponse, TextRequest, URLRequest
from chatbot.assistant import chat
from explainability.lime_explainer import explain_text_lime
from explainability.shap_explainer import explain_tree_model
from utils.database import log_scan
from utils.model_loader import ensure_models

app = FastAPI(
    title="SentinelAI API",
    description="AI-Powered Digital Safety Ecosystem",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    """Train/load models once at startup."""
    ensure_models()


@app.get("/")
def root():
    return {"service": "SentinelAI", "status": "online", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/phishing", response_model=PredictionResponse)
def api_phishing(req: URLRequest):
    try:
        result = predict_phishing(req.url)
        bundle = __import__("utils.model_loader", fromlist=["load_phishing_bundle"]).load_phishing_bundle()
        names = bundle["feature_names"]
        vals = [result["feature_values"][n] for n in names]
        xai = explain_tree_model(bundle["model"], names, vals)
        log_scan("phishing", req.url, result["prediction"], result["confidence"], result["threat_level"])
        return PredictionResponse(data=result, explainability=xai)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/sms", response_model=PredictionResponse)
def api_sms(req: TextRequest):
    try:
        result = predict_sms(req.text)
        from utils.model_loader import load_sms_bundle
        vec, clf = load_sms_bundle()

        def proba_fn(texts):
            import numpy as np
            from utils.text_features import clean_text
            X = vec.transform([clean_text(t) for t in texts])
            return clf.predict_proba(X)

        xai = explain_text_lime(proba_fn, req.text)
        log_scan("sms", req.text[:80], result["prediction"], result["confidence"], result["threat_level"])
        return PredictionResponse(data=result, explainability=xai)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/fake-news", response_model=PredictionResponse)
def api_fake_news(req: TextRequest):
    try:
        result = predict_fake_news(req.text)
        log_scan("fake_news", req.text[:80], result["prediction"], result["confidence"], result["threat_level"])
        return PredictionResponse(data=result, explainability={"method": "heuristic", "markers": result.get("sensational_markers")})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/url-analyze", response_model=PredictionResponse)
def api_url_analyze(req: URLRequest):
    try:
        result = analyze_url(req.url)
        return PredictionResponse(data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/deepfake", response_model=PredictionResponse)
def api_deepfake(file: UploadFile = File(...)):
    try:
        content = file.file.read()
        if len(content) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image must be under 5MB")
        result = predict_deepfake(content)
        from utils.model_loader import load_deepfake_bundle
        bundle = load_deepfake_bundle()
        names = bundle["feature_names"]
        vals = [result["image_features"][n] for n in names]
        xai = explain_tree_model(bundle["model"], names, vals)
        log_scan("deepfake", file.filename or "image", result["prediction"], result["confidence"], result["threat_level"])
        return PredictionResponse(data=result, explainability=xai)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        return {"success": True, "data": chat(req.message, req.context)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
