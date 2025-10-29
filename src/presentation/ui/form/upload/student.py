import streamlit as st
import requests  
from datetime import datetime
from src.presentation.ui import api_base
from src.presentation.ui.components.layout import _get_filters
                    
def upload_student():
    st.subheader("Thêm Sinh viên mới")
    data_filter = _get_filters(["departments"])
    departments = data_filter["departments"]
    map_dept = {dept["name"]: dept for dept in departments}
    with st.form("upload_form", clear_on_submit=True):
        id = st.text_input("Student ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
        birthday = st.text_input("Birthday", placeholder="YYYY-MM-DD")
        sex = st.selectbox("Sex", options=["M", "F", "Unknown"], index=2)
        department = st.selectbox("Department", options=map_dept.keys())
        submit = st.form_submit_button("Upload", width="stretch", type="tertiary")
    
    if submit:
        if not id or not name or not email or not birthday:
            st.error("Student ID, Name, Email and birthday are required.")
        else:
            payload = {
                "id": id,
                "name": name,
                "email": email,
                "birthday": birthday,
                "sex":  sex,
                "department_id": map_dept[department]["id"]
            }
            try:
                url = api_base.rstrip("/") + "/student/upload"
                resp = requests.post(url, json=payload, timeout=10)
                try:
                    data = resp.json()
                except ValueError:
                    st.error(f"Invalid JSON response (status {resp.status_code})")
                    st.write(resp.text)
                else:
                    if resp.status_code == 200 or resp.status_code == 201:
                        # Expecting structure like { "success": True, "message": "...", "score": {...} }
                        if isinstance(data, dict) and data.get("success", True):
                            data["student"].update({
                                "action_time": datetime.now(),
                                "action": "Thêm"
                            })
                            upload_student = data["student"]
                            if upload_student: 
                                st.session_state.history.append(upload_student)
                            st.session_state.upload_success_msg = f"Đã thêm thành công sinh viên ID: {upload_student.get("student_id")}"
                            st.session_state.upload_toast_msg = "💾 Đã lưu thông tin vào lịch sử."
                            st.rerun()
                        else:
                            st.error(data.get("message", f"Upload failed (status {resp.status_code})"))
                            st.json(data)
                    else:
                        st.error(f"Request failed with status {resp.status_code}")
                        st.json(data)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {e}")

