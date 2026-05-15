@echo off
cd /d "%~dp0"
python -m scripts.train_all
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
