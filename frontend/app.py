"""
SentinelAI Streamlit Dashboard — main entry point.
Run from project root: streamlit run frontend/app.py
"""

import sys
from pathlib import Path

# Ensure project root on path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from app.config import API_BASE_URL
from frontend.components.styles import inject_custom_css

st.set_page_config(
    page_title="SentinelAI | Digital Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()

PAGES = [
    "Home",
    "URL Detection",
    "Scam SMS",
    "Fake News",
    "Deepfake Detection",
    "Threat Analytics",
    "Cyber Chatbot",
    "About",
]

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None


def sidebar() -> str:
    with st.sidebar:
        st.markdown('<p class="sentinel-title">🛡️ SentinelAI</p>', unsafe_allow_html=True)
        st.markdown('<p class="sentinel-sub">Digital Safety Ecosystem</p>', unsafe_allow_html=True)
        st.divider()
        page = st.radio("Navigation", PAGES, label_visibility="collapsed")
        st.divider()
        st.caption(f"API: `{API_BASE_URL}`")
        use_api = st.toggle("Use FastAPI backend", value=False)
        st.session_state.use_api = use_api
        if st.button("Train / Refresh Models", use_container_width=True):
            with st.spinner("Training lightweight demo models..."):
                from scripts.train_all import train_all_models
                from utils.model_loader import load_phishing_bundle
                load_phishing_bundle.cache_clear()
                train_all_models()
            st.success("Models ready!")
    return page


def page_home():
    st.markdown("## Welcome to SentinelAI")
    st.markdown(
        "Real-time AI-powered threat detection for **phishing URLs**, **scam SMS**, "
        "**fake news**, **deepfake images**, and **suspicious URLs** — with explainable AI."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Modules", "6")
    c2.metric("ML Stack", "sklearn")
    c3.metric("XAI", "SHAP / LIME")
    c4.metric("Deploy", "Cloud Ready")

    st.info("Select a module from the sidebar. Models auto-train on first run (~5 seconds).")

    from utils.database import get_scan_stats
    stats = get_scan_stats()
    st.metric("Total Scans Logged", stats["total_scans"])


def page_url_detection():
    st.header("🔗 Phishing URL Detection")
    url = st.text_input("Enter URL to analyze", placeholder="https://example.com/login")
    col1, col2 = st.columns(2)
    with col1:
        analyze_phish = st.button("Detect Phishing", type="primary", use_container_width=True)
    with col2:
        analyze_intel = st.button("URL Intelligence", use_container_width=True)

    if analyze_phish and url:
        with st.spinner("Analyzing URL..."):
            try:
                if st.session_state.get("use_api"):
                    import httpx
                    r = httpx.post(f"{API_BASE_URL}/api/phishing", json={"url": url}, timeout=30)
                    r.raise_for_status()
                    payload = r.json()
                    result, xai = payload["data"], payload.get("explainability")
                else:
                    from app.predictors.phishing import predict_phishing
                    from explainability.shap_explainer import explain_tree_model
                    from utils.model_loader import load_phishing_bundle
                    result = predict_phishing(url)
                    b = load_phishing_bundle()
                    names = b["feature_names"]
                    vals = [result["feature_values"][n] for n in names]
                    xai = explain_tree_model(b["model"], names, vals)
                st.session_state.last_prediction = {"module": "phishing", **result}
                from utils.database import log_scan
                log_scan("phishing", url, result["prediction"], result["confidence"], result["threat_level"])
                from frontend.components.ui_helpers import show_explainability, show_prediction_card
                show_prediction_card(result, "risk_score")
                show_explainability(xai)
                with st.expander("Feature values"):
                    st.json(result.get("feature_values", {}))
            except Exception as e:
                st.error(f"Error: {e}")

    if analyze_intel and url:
        with st.spinner("Running URL intelligence..."):
            from app.predictors.url_analyzer import analyze_url
            r = analyze_url(url)
            st.metric("Risk Score", f"{r['risk_score']}/100")
            st.markdown(f"**Level:** {r['risk_level']}")
            for rec in r["recommendations"]:
                st.warning(rec)


def page_sms():
    st.header("📱 Scam SMS Detection")
    text = st.text_area("Paste SMS message", height=120)
    if st.button("Analyze SMS", type="primary") and text:
        with st.spinner("Classifying..."):
            try:
                from app.predictors.sms import predict_sms
                from explainability.lime_explainer import explain_text_lime
                from utils.model_loader import load_sms_bundle
                from utils.text_features import clean_text
                result = predict_sms(text)
                vec, clf = load_sms_bundle()

                def proba_fn(texts):
                    X = vec.transform([clean_text(t) for t in texts])
                    return clf.predict_proba(X)

                xai = explain_text_lime(proba_fn, text)
                st.session_state.last_prediction = {"module": "sms", **result}
                from utils.database import log_scan
                log_scan("sms", text[:80], result["prediction"], result["confidence"], result["threat_level"])
                from frontend.components.ui_helpers import show_explainability, show_prediction_card
                show_prediction_card(result, "scam_probability")
                if result.get("highlighted_terms"):
                    st.subheader("Suspicious terms")
                    st.write(", ".join(f"`{t}`" for t in result["highlighted_terms"]))
                show_explainability(xai)
            except Exception as e:
                st.error(f"Error: {e}")


def page_fake_news():
    st.header("📰 Fake News Detection")
    article = st.text_area("Paste article text", height=200)
    if st.button("Analyze Article", type="primary") and article:
        with st.spinner("Analyzing..."):
            try:
                from app.predictors.fake_news import predict_fake_news
                result = predict_fake_news(article)
                st.session_state.last_prediction = {"module": "fake_news", **result}
                from utils.database import log_scan
                log_scan("fake_news", article[:80], result["prediction"], result["confidence"], result["threat_level"])
                from frontend.components.ui_helpers import show_prediction_card
                show_prediction_card(result, "fake_probability")
            except Exception as e:
                st.error(f"Error: {e}")


def page_deepfake():
    st.header("🖼️ Deepfake Image Detection")
    st.caption("Image only — lightweight OpenCV features + RandomForest (no GPU).")
    uploaded = st.file_uploader("Upload image (JPG/PNG, max 5MB)", type=["jpg", "jpeg", "png"])
    if uploaded and st.button("Scan Image", type="primary"):
        data = uploaded.read()
        if len(data) > 5 * 1024 * 1024:
            st.error("File too large.")
        else:
            with st.spinner("Analyzing image..."):
                try:
                    from app.predictors.deepfake import predict_deepfake
                    result = predict_deepfake(data)
                    st.session_state.last_prediction = {"module": "deepfake", **result}
                    from utils.database import log_scan
                    log_scan("deepfake", uploaded.name or "image", result["prediction"], result["confidence"], result["threat_level"])
                    st.image(data, caption="Uploaded", use_container_width=True)
                    from frontend.components.ui_helpers import show_prediction_card
                    show_prediction_card(result, "deepfake_probability")
                except Exception as e:
                    st.error(f"Error: {e}")


def page_analytics():
    st.header("📊 Threat Analytics")
    from utils.database import get_scan_stats
    from frontend.components.charts import bar_module_usage, pie_threat_distribution
    stats = get_scan_stats()
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(pie_threat_distribution(stats["by_threat"]), use_container_width=True)
    with c2:
        st.plotly_chart(bar_module_usage(stats["by_module"]), use_container_width=True)
    st.subheader("Recent scans")
    if stats["recent"]:
        st.dataframe(stats["recent"], use_container_width=True)
    else:
        st.info("Run detections to populate analytics.")


def page_chatbot():
    st.header("💬 Cyber Awareness Chatbot")
    st.caption("Offline rule-based assistant — no API key required.")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Ask about phishing, SMS scams, deepfakes...")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        from chatbot.assistant import chat
        resp = chat(prompt, {"last_prediction": st.session_state.last_prediction})
        reply = resp["reply"]
        if resp.get("tips"):
            reply += "\n\n**Tips:**\n" + "\n".join(f"- {t}" for t in resp["tips"])
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()


def page_about():
    st.header("About SentinelAI")
    st.markdown(
        """
        **SentinelAI** is a lightweight, modular cybersecurity AI ecosystem for academic
        and portfolio use. It combines classical ML, NLP, computer vision heuristics,
        and explainable AI in a Streamlit + FastAPI architecture.

        | Module | Technique |
        |--------|-----------|
        | Phishing URL | RandomForest + URL features |
        | Scam SMS | TF-IDF + Logistic Regression |
        | Fake News | TF-IDF + Logistic Regression |
        | Deepfake | OpenCV features + RandomForest |
        | URL Intel | Rule-based risk scoring |
        | Chatbot | Rule-based FAQ |

        **Repository stays small:** no large weights committed; train locally with sample data.
        """
    )


def main():
    page = sidebar()
    routes = {
        "Home": page_home,
        "URL Detection": page_url_detection,
        "Scam SMS": page_sms,
        "Fake News": page_fake_news,
        "Deepfake Detection": page_deepfake,
        "Threat Analytics": page_analytics,
        "Cyber Chatbot": page_chatbot,
        "About": page_about,
    }
    routes[page]()


# Must run on Streamlit Cloud (script __name__ is not "__main__")
main()
