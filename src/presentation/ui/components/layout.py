import streamlit as st
import requests
from src.config import API_BASE
from src.presentation.ui.utils import authenticated_request

def footer():
    with st.container():
        st.markdown("---")
        st.markdown("© 2025 Student Management App. All rights reserved.")


def _get_columns():
    try:
        url = API_BASE.rstrip("/") + "/students/column"
        response = authenticated_request("GET",url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return None

def _get_filters(columns):
    try:
        col = ",".join(columns)
        url = API_BASE.rstrip("/") + f"/students/filter?columns={col}"
        response = authenticated_request("GET",url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return None
    
def _get_students(payload):
    try:
        url = API_BASE.rstrip("/") + "/students/list"
        response = authenticated_request("POST",url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return None

def table_detail_student():
    data_col = _get_columns()
    
    st.subheader(data_col["display_name"])
    col1, col2, col3 = st.columns([2,1,1])
    
    if not data_col or "columns" not in data_col:
        st.error("❌ Không thể tải danh sách cột từ API. Vui lòng kiểm tra lại backend.")
        st.stop() 
        
        
    map_col = {col["label"]: col for col in data_col["columns"]}
    map_label_to_key = {col["label"]: col["key"] for col in data_col["columns"]}

    # --- Session State init ---
    if "selected_columns" not in st.session_state:
        st.session_state.selected_columns = [col["label"] for col in data_col["columns"] if col["key"] not in ["departments", "courses"]]
    if "selected_departments" not in st.session_state:
        st.session_state.selected_departments = ["All"]
    if "selected_courses" not in st.session_state:
        st.session_state.selected_courses = ["All"]

    # 🔹 Chọn cột hiển thị
    with col1.container(): 
        selection = st.multiselect(
            "Select columns to display:",
            list(map_col.keys()),
            default=st.session_state.selected_columns,
            key="selected_columns"
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

    with col3.container():
        dept_options = ["All"] + list(map_dept.keys())

        # Đảm bảo giá trị mặc định hợp lệ
        valid_defaults = [d for d in st.session_state.selected_departments if d in dept_options]
        if not valid_defaults:
            valid_defaults = ["All"]

        dept = st.multiselect(
            "🏫 Department",
            dept_options,
            default=valid_defaults,
            key="selected_departments",
        )

    with col2.container():
        course_options = ["All"] + list(map_course.keys())

        valid_courses = [c for c in st.session_state.selected_courses if c in course_options]
        if not valid_courses:
            valid_courses = ["All"]

        course = st.multiselect(
            "📘 Course",
            course_options,
            default=valid_courses,
            key="selected_courses"
        )
        
    # --- Tạo payload API ---
    payload = {
        "columns": list_col
    }
    
    if "All" not in st.session_state.selected_courses:
        payload["course_id"] = [map_course[c]["id"] for c in st.session_state.selected_courses]
    if "All" not in st.session_state.selected_departments:
        payload["department_id"] = [map_dept[d]["id"] for d in st.session_state.selected_departments]
        
    # --- Reset filters khi bỏ chọn cột ---
    # Nếu người dùng bỏ chọn cột "Khoa", reset lại filter khoa về ["All"]
    if "Khoa" not in selection and st.session_state.get("selected_departments", None) != ["All"]:
        st.session_state.selected_departments = ["All"]

    # Nếu người dùng bỏ chọn cột "Môn", reset lại filter môn về ["All"]
    if "Môn" not in selection and st.session_state.get("selected_courses", None) != ["All"]:
        st.session_state.selected_courses = ["All"]
    
    # --- Gọi API ---
    data_student = _get_students(payload)
    # --- Mapping lại label cho bảng ---
    mapped_students = [
        {col["label"]: student.get(col["key"], None) for col in data_col["columns"] if col["label"] in selection}
        for student in data_student
    ]

    st.table(mapped_students)
    