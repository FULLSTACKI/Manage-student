import streamlit as st
import httpx
import asyncio
import requests
from src.presentation.ui import api_base

def footer():
    with st.container():
        st.markdown("---")
        st.markdown("© 2025 Student Management App. All rights reserved.")


def _get_columns():
    try:
        url = api_base.rstrip("/") + "/student/column"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return None

def _get_filters(columns):
    try:
        col = ",".join(columns)
        url = api_base.rstrip("/") + f"/student/filter?columns={col}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return None

def table_detail_student():
    data_col = _get_columns()
    
    if not data_col or "columns" not in data_col:
        st.error("❌ Không thể tải danh sách cột từ API. Vui lòng kiểm tra lại backend.")
        st.stop() 

    map_col = {col["label"]: col for col in data_col["columns"]}
    selection = st.multiselect("Select columns to display:", map_col.keys())
    list_col = [map_col[col].get("key") for col in selection]
    
    if not selection:
        st.warning("Please select at least one column.")
        return
    
    data_filter = _get_filters(list_col)
    filter_params = {}
    if "departments" in data_filter:
        dept = st.selectbox(
            "🏫 Department",
            ["All"] + [d["name"] for d in data_filter["departments"]]
        )
        if dept != "All":
            filter_params["department_name"] = dept

    if "courses" in data_filter:
        course = st.selectbox(
            "📘 Course",
            ["All"] + [c["name"] for c in data_filter["courses"]]
        )
        if course != "All":
            filter_params["course_name"] = course