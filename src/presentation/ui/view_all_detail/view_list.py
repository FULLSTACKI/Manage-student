import os
import streamlit as st
import requests  
from dotenv import load_dotenv

load_dotenv()
api_base = os.getenv("API_BASE")

def view_all_student_detail():
    try:
        url = api_base.rstrip("/") + "/students"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        st.table(resp.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
    