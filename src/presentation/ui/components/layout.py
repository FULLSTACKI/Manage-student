import streamlit as st
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
    
def _get_students(payload):
    try:
        url = api_base.rstrip("/") + "/student/list"
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return None

def table_detail_student():
    data_col = _get_columns()
    
    st.subheader(data_col["display_name"])
    
    if not data_col or "columns" not in data_col:
        st.error("❌ Không thể tải danh sách cột từ API. Vui lòng kiểm tra lại backend.")
        st.stop() 
        
    map_col = {col["label"]: col for col in data_col["columns"]}
    map_label_to_key = {col["label"]: col["key"] for col in data_col["columns"]}

    # --- Session State init ---
    if "selected_columns" not in st.session_state:
        st.session_state.selected_columns = list(map_col.keys())
    if "selected_departments" not in st.session_state:
        st.session_state.selected_departments = ["All"]
    if "selected_courses" not in st.session_state:
        st.session_state.selected_courses = ["All"]

    # --- Giao diện ---
    col1, col2, col3 = st.columns([3, 1, 1])

    # 🔹 Chọn cột hiển thị
    with col1:
        selection = st.multiselect(
            "Select columns to display:",
            list(map_col.keys()),
            default=st.session_state.selected_columns
        )

    # 🔹 Nếu chưa chọn cột thì dừng
    if not selection:
        st.warning("Please select at least one column.")
        return

    # 🔹 Lấy danh sách filter từ API
    list_col = [map_label_to_key[col] for col in selection]
    data_filter = _get_filters(list_col)

    # 🔹 Chuẩn bị ánh xạ khoa và môn học
    map_dept = {d["name"]: d for d in data_filter["departments"]}
    map_course = {c["name"]: c for c in data_filter["courses"]}

    # --- Filter khoa ---
    with col3:
        if "departments" in data_filter:
            dept = st.multiselect(
                "🏫 Department",
                ["All"] + list(map_dept.keys()),
                default=st.session_state.selected_departments,
                key="selected_departments"
            )

    # --- Filter môn học ---
    with col2:
        if "courses" in data_filter:
            course = st.multiselect(
                "📘 Course",
                ["All"] + list(map_course.keys()),
                default=st.session_state.selected_courses,
                key="selected_courses"
            )

    # --- Tạo payload API ---
    payload = {
        "columns": list_col
    }

    if "All" not in st.session_state.selected_departments:
        payload["department_id"] = [map_dept[d]["id"] for d in st.session_state.selected_departments]

    if "All" not in st.session_state.selected_courses:
        payload["course_id"] = [map_course[c]["id"] for c in st.session_state.selected_courses]

    # --- Gọi API ---
    data_student = _get_students(payload)
    
    # --- Mapping lại label cho bảng ---
    mapped_students = [
        {col["label"]: student.get(col["key"], None) for col in data_col["columns"]}
        for student in data_student
    ]
    
    # --- Hiển thị bảng ---
    st.table(mapped_students)