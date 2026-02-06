@echo off
cd /d "%~dp0"
echo Starting Recipe Intelligence API on http://127.0.0.1:8001
echo If port 8001 is in use, set RECIPE_API_BASE in the Streamlit terminal and use: python -m uvicorn src.api:app --reload --host 127.0.0.1 --port 8002
python -m uvicorn src.api:app --reload --host 127.0.0.1 --port 8001
