@echo off
start "FastAPI Server" cmd /k "python -m uvicorn src.presentation.api.main:app --reload"
start "Streamlit UI" cmd /k "python -m streamlit run src/presentation/ui/Home.py"