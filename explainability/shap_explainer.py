"""
Lightweight SHAP explanations for tabular URL / image feature models.
"""

from typing import Any

import numpy as np


def explain_tree_model(
    model,
    feature_names: list[str],
    feature_values: list[float],
    max_display: int = 8,
) -> dict[str, Any]:
    """
    SHAP TreeExplainer for RandomForest — small feature sets only.
    Falls back to feature importances if SHAP fails.
    """
    try:
        import shap
        X = np.array([feature_values])
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)
        # Binary classifier may return list of arrays
        if isinstance(shap_values, list):
            vals = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
        else:
            vals = shap_values[0]
        pairs = sorted(
            zip(feature_names, vals.tolist()),
            key=lambda x: abs(x[1]),
            reverse=True,
        )[:max_display]
        return {
            "method": "SHAP",
            "contributions": [{"feature": f, "impact": round(v, 4)} for f, v in pairs],
        }
    except Exception as e:
        imp = getattr(model, "feature_importances_", None)
        if imp is not None:
            pairs = sorted(zip(feature_names, imp.tolist()), key=lambda x: -x[1])[:max_display]
            return {
                "method": "feature_importance_fallback",
                "contributions": [{"feature": f, "impact": round(v, 4)} for f, v in pairs],
                "note": str(e),
            }
        return {"method": "unavailable", "contributions": [], "note": str(e)}
