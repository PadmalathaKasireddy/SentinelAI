"""Reusable UI blocks for prediction panels."""

import streamlit as st

from frontend.components.charts import gauge_confidence
from frontend.components.styles import threat_badge


def show_prediction_card(result: dict, prob_key: str = "confidence") -> None:
    level = result.get("threat_level", result.get("risk_level", "N/A"))
    conf = result.get(prob_key, result.get("confidence", 0))
    if prob_key == "risk_score" and isinstance(conf, (int, float)):
        conf = float(conf)  # already 0-1 for phishing
    elif isinstance(conf, (int, float)) and conf > 1:
        conf = float(conf) / 100.0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Prediction", result.get("prediction", "—"))
    with col2:
        st.markdown(f"**Threat Level**  \n{threat_badge(level)}", unsafe_allow_html=True)
    with col3:
        st.metric("Confidence", f"{conf:.1%}" if isinstance(conf, float) and conf <= 1 else conf)

    st.plotly_chart(gauge_confidence(float(conf) if float(conf) <= 1 else float(conf) / 100), use_container_width=True)

    if result.get("explanation"):
        st.subheader("Explanation")
        for line in result["explanation"]:
            st.markdown(f"- {line}")


def show_explainability(xai: dict | None) -> None:
    if not xai:
        return
    st.subheader("Explainable AI")
    if xai.get("contributions"):
        for c in xai["contributions"]:
            st.progress(min(abs(c["impact"]), 1.0), text=f"{c['feature']}: {c['impact']:.4f}")
    if xai.get("weights"):
        for w in xai["weights"]:
            color = "🔴" if w["weight"] > 0 else "🟢"
            st.markdown(f"{color} **{w['term']}** ({w['weight']:+.3f})")
