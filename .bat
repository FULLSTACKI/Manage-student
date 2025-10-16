@echo off
ECHO Starting FastAPI server on port 8000...
REM --port 8000: Chỉ định rõ cổng cho FastAPI
start "FastAPI Server" cmd /k "python -m uvicorn src.presentation.api.main:app --reload"

ECHO Starting Streamlit UI on port 8501...
REM --server.port 8501: Chỉ định rõ cổng cho Streamlit
start "Streamlit UI" cmd /k "streamlit run src/presentation/ui/form_dashboard.py"