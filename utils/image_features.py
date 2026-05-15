"""
Lightweight image features for deepfake detection (no heavy CNN weights in repo).
Uses OpenCV statistics — fast on CPU, small model size.
"""

from typing import Any

import cv2
import numpy as np


def extract_image_features(image_bytes: bytes) -> dict[str, float]:
    """
    Handcrafted features: blur, color variance, edge density.
    Suitable for training a small RandomForest demo model.
    """
    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image. Use JPG or PNG.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    # Laplacian variance — manipulated images often differ in sharpness
    lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())

    # Color channel statistics
    b, g, r = cv2.split(img)
    color_std = float(np.std([np.std(r), np.std(g), np.std(b)]))

    # Edge density via Canny
    edges = cv2.Canny(gray, 100, 200)
    edge_ratio = float(np.count_nonzero(edges) / max(h * w, 1))

    # Histogram spread
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
    hist = hist / (hist.sum() + 1e-8)
    hist_entropy = float(-np.sum(hist * np.log2(hist + 1e-10)))

    return {
        "width": float(w),
        "height": float(h),
        "aspect_ratio": round(w / max(h, 1), 4),
        "laplacian_var": lap_var,
        "color_std": color_std,
        "edge_ratio": edge_ratio,
        "hist_entropy": hist_entropy,
        "mean_brightness": float(np.mean(gray)),
    }


IMAGE_FEATURE_NAMES = list(extract_image_features.__doc__ and [])  # placeholder


def feature_names() -> list[str]:
    """Ordered feature keys (computed from dummy if needed)."""
    # Use a 1x1 white pixel encoded minimally — fallback static list
    return [
        "width", "height", "aspect_ratio", "laplacian_var",
        "color_std", "edge_ratio", "hist_entropy", "mean_brightness",
    ]


def features_to_vector(features: dict[str, Any], names: list[str]) -> list[float]:
    return [float(features[n]) for n in names]
