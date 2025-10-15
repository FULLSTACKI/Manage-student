@echo off
start cmd /k "uvicorn src.app.api.main:app --reload"
start cmd /k "streamlit run src/app/ui/form_dashboard.py"