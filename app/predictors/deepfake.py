"""
Module 4: Lightweight image deepfake detection (OpenCV features + RandomForest).
Image only — no video processing for deployment efficiency.
"""

from typing import Any

import numpy as np

from utils.image_features import extract_image_features, feature_names, features_to_vector
from utils.model_loader import ensure_models, load_deepfake_bundle
from utils.threat_levels import score_to_threat_level


def predict_deepfake(image_bytes: bytes) -> dict[str, Any]:
    ensure_models()
    bundle = load_deepfake_bundle()
    clf = bundle["model"]
    names = bundle["feature_names"]

    features = extract_image_features(image_bytes)
    X = np.array([features_to_vector(features, names)])
    proba = clf.predict_proba(X)[0]
    df_prob = float(proba[1]) if len(proba) > 1 else float(proba[0])

    notes = []
    if features["laplacian_var"] < 50:
        notes.append("Low sharpness variance — possible smoothing/blending")
    if features["edge_ratio"] > 0.15:
        notes.append("Unusually high edge density")
    if features["color_std"] > 40:
        notes.append("High color channel variance")
    if not notes:
        notes.append("Image statistics within typical range for demo model")

    return {
        "prediction": "Deepfake" if df_prob >= 0.5 else "Authentic",
        "threat_level": score_to_threat_level(df_prob),
        "deepfake_probability": round(df_prob, 4),
        "confidence": round(max(df_prob, 1 - df_prob), 4),
        "image_features": features,
        "explanation": notes,
        "frame_analysis": "Single-image analysis (no video frames processed).",
    }
