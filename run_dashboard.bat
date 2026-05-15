@echo off
cd /d "%~dp0"
python -m scripts.train_all
streamlit run frontend/app.py
