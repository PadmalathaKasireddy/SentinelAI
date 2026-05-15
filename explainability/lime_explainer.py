"""
LIME text explanations for SMS / fake news (sparse TF-IDF).
"""

from typing import Any, Callable


def explain_text_lime(
    predict_fn: Callable,
    text: str,
    num_features: int = 6,
) -> dict[str, Any]:
    """
    Explain text classification with LIME.
    predict_fn: callable(list[str]) -> array of probabilities shape (n, 2)
    """
    try:
        from lime.lime_text import LimeTextExplainer
        explainer = LimeTextExplainer(class_names=["legit", "risk"])
        exp = explainer.explain_instance(
            text,
            predict_fn,
            num_features=num_features,
            top_labels=1,
        )
        label = exp.top_labels[0]
        weights = exp.as_list(label=label)
        return {
            "method": "LIME",
            "label": int(label),
            "weights": [{"term": t, "weight": round(w, 4)} for t, w in weights],
        }
    except Exception as e:
        return {"method": "unavailable", "weights": [], "note": str(e)}
