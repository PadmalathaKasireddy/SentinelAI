# SentinelAI

## An AI-Powered Digital Safety Ecosystem for Real-Time Threat Detection

SentinelAI is a lightweight and deployment-ready AI cybersecurity platform designed to detect and analyze modern digital threats such as phishing URLs, scam SMS messages, fake news, suspicious URLs, and deepfake images in real time.

The platform integrates Machine Learning, Natural Language Processing (NLP), Computer Vision, Explainable AI, and interactive dashboard engineering into a single modular ecosystem.

Built with scalability, usability, and deployment optimization in mind, SentinelAI is suitable for AI/ML portfolios, cybersecurity demonstrations, research projects, and real-world educational applications.

---

# Live Demo

### Streamlit Deployment
[click to view](https://sentinelaigi-garttucruxrazitmpngmud.streamlit.app/)

---

# Problem Statement

The rapid growth of cyber threats such as phishing attacks, scam messages, misinformation, malicious URLs, and AI-generated manipulated media has made it increasingly difficult for internet users to identify harmful digital content.

Traditional security systems are often:
- isolated and single-purpose
- difficult for non-technical users
- lacking explainability
- unable to detect modern AI-generated threats

SentinelAI addresses these limitations by providing an integrated AI-powered digital safety ecosystem capable of analyzing multiple types of cyber threats through a unified dashboard.

---

# Key Features

## Phishing URL Detection

Detects malicious and suspicious URLs using Machine Learning and URL feature engineering.

### Features
- URL length analysis
- HTTPS detection
- suspicious character detection
- IP-based domain analysis
- redirection pattern analysis

### Output
- Safe / Suspicious / Dangerous
- confidence score
- threat explanation

---

## Scam SMS Detection

Analyzes SMS content using NLP techniques to identify scam and phishing messages.

### Features
- urgency keyword detection
- malicious link analysis
- fraud pattern identification
- spam classification

### Output
- scam probability
- confidence score
- highlighted suspicious terms

---

## Fake News Detection

Uses NLP-based text classification to identify misinformation and fake news articles.

### Features
- fake/real classification
- sentiment analysis
- misinformation detection

### Output
- Fake / Real prediction
- confidence score
- prediction explanation

---

## Deepfake Image Detection

Detects manipulated or AI-generated facial images using lightweight Computer Vision models.

### Features
- image upload support
- manipulation detection
- facial inconsistency analysis

### Output
- deepfake probability
- confidence score
- prediction explanation

---

## Suspicious URL Intelligence

Provides rule-based URL threat intelligence and cybersecurity recommendations.

### Features
- malicious keyword analysis
- URL entropy analysis
- suspicious pattern detection
- shortened URL detection

### Output
- risk score (0–100)
- safety recommendations
- threat explanation

---

## Cyber Awareness Chatbot

An offline AI chatbot designed to educate users about cybersecurity threats and digital safety practices.

### Capabilities
- phishing awareness
- cyber threat explanation
- prevention tips
- FAQ assistance

---

# Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| Machine Learning | Scikit-learn |
| NLP | TF-IDF, Logistic Regression, NLTK |
| Computer Vision | OpenCV, MobileNet/EfficientNet-B0 |
| Explainable AI | SHAP, LIME |
| Data Visualization | Plotly |
| Database | SQLite |
| Deployment | Streamlit Cloud, Render |

---

# System Architecture

```text
User Input
   ↓
Threat Analysis Modules
   ↓
Machine Learning / NLP / CV Models
   ↓
Prediction Engine
   ↓
Explainable AI Layer
   ↓
Dashboard Visualization
   ↓
Cyber Awareness Chatbot
```

---

# Project Structure

```text
SentinelAI/
│
├── app/
├── backend/
├── frontend/
├── models/
├── datasets/
├── utils/
├── chatbot/
├── explainability/
├── assets/
├── notebooks/
├── scripts/
├── tests/
├── uploads/
├── requirements.txt
├── Dockerfile
├── README.md
└── .gitignore
```

---

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/PadmalathaKasireddy/SentinelAI.git
cd SentinelAI
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Train Lightweight Demo Models

```bash
python -m scripts.train_all
```

The generated model files are lightweight and optimized for deployment.

---

# Run the Application

## Start Streamlit Dashboard

```bash
streamlit run frontend/app.py
```

Open:

```text
http://localhost:8501
```

---

## Start FastAPI Backend

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

API Documentation:

```text
http://localhost:8000/docs
```

---

# API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| /api/phishing | POST | Phishing URL detection |
| /api/sms | POST | Scam SMS detection |
| /api/fake-news | POST | Fake news detection |
| /api/url-analyze | POST | Suspicious URL analysis |
| /api/deepfake | POST | Deepfake image detection |
| /api/chat | POST | Cyber awareness chatbot |

---

# Example API Request

```bash
curl -X POST http://localhost:8000/api/phishing \
-H "Content-Type: application/json" \
-d "{\"url\": \"http://paypal-verify.tk/login\"}"
```

---

# Explainable AI

SentinelAI integrates Explainable AI techniques using:

- SHAP
- LIME

These modules provide:
- feature importance analysis
- prediction transparency
- confidence visualization
- user-friendly explanations

---

# Dashboard Features

The Streamlit dashboard includes:

- dark cybersecurity theme
- sidebar navigation
- KPI cards
- analytics charts
- real-time predictions
- upload functionality
- confidence indicators
- interactive visualizations
- responsive layout

---

# Deployment

## Streamlit Cloud Deployment

1. Push repository to GitHub
2. Open Streamlit Cloud
3. Select GitHub repository
4. Set main file path:

```text
frontend/app.py
```

5. Deploy application

---

## Render Backend Deployment

### Build Command

```bash
pip install -r requirements.txt && python -m scripts.train_all
```

### Start Command

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

---

# Optimization Strategy

To maintain lightweight deployment and GitHub compatibility:

- lightweight ML models are used
- large datasets are excluded
- model files are compressed
- no GPU dependency required
- deployment optimized for free-tier cloud hosting

---

# Advantages of SentinelAI

- Unified multi-threat detection system
- Real-time cybersecurity analysis
- Explainable AI integration
- Lightweight deployment architecture
- Beginner-friendly implementation
- Interactive dashboard visualization
- Modular and scalable structure

---

# Future Enhancements

Potential future improvements include:

- browser extension integration
- voice deepfake detection
- multilingual threat detection
- real-time social media monitoring
- cloud database integration
- user authentication system
- advanced transformer-based NLP models

---


# License

This project is released under the MIT License.

---

# Author

**Padmalatha Kasireddy**

AI/ML | Cybersecurity | Data Science | Full Stack AI Development

GitHub:
https://github.com/PadmalathaKasireddy
