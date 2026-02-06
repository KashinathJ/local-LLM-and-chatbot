@echo off
cd /d "%~dp0"
echo Starting Streamlit Chatbot. Open http://localhost:8501
python -m streamlit run src/bot.py
