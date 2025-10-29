import streamlit as st
import requests
from src.presentation.ui import api_base
from ..update.student import update_student
from src.presentation.ui.components import deleted

def view_student():
    st.subheader("Danh sách Sinh viên")
    with st.form("view_form", clear_on_submit=True):
        student_id = st.text_input("Tìm kiếm theo mã số Sinh viên:")
        submit = st.form_submit_button("Tìm kiếm")
    
    if submit:
        if not student_id:
            st.error("Student ID is required.")
            st.session_state.search_student = None
        else:
            try:
                url = api_base.rstrip("/") + f"/student?student_id={student_id}"
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                try:
                    data = resp.json()
                except ValueError:
                    st.error(f"Invalid JSON response (status {resp.status_code})")
                    st.write(resp.text)
                else:
                    if resp.status_code == 200 or resp.status_code == 201:
                        # Expecting structure like { "student": {...} }
                        if isinstance(data, dict) and "student" in data:
                            st.session_state.search_student = data
                            st.success(data.get("message"))
                        else:
                            st.error(f"Student not found (status {resp.status_code})")
                            st.json(data)
                            st.session_state.search_student = None
                    else:
                        st.error(f"Request failed with status {resp.status_code}")
                        st.json(data)
                        st.session_state.search_student = None
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {e}")

    if st.session_state.get("search_student") is not None:
        st.markdown("---")
        st.subheader("📊 Thông tin Sinh viên")
        student_info = st.session_state.get("search_student")
        student = student_info.get("student", {})
        with st.container(border=True,horizontal_alignment="center", vertical_alignment="center", height="stretch"):
            st.markdown(f"### 🧑‍🎓 **{student.get('student_name', 'N/A')}**") 
            st.write(f"**ID:** {student.get('student_id', 'N/A')} | **Khoa:** {student.get('departments', 'N/A')}")
            st.write("")
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                st.metric("🎂 Tuổi", student.get('age', 'N/A'))
            with sub_col2:
                st.markdown(f"**🚻 Giới tính:** {student.get('sex', 'N/A')}")
            st.write("**Thông tin liên lạc:**")
            st.caption(f"""
                📧 **Email:** {student.get('email', 'N/A')} | 🎂 **Ngày sinh:** {student.get('birthday', 'N/A')}
            """)
            st.divider()
            button_col1, button_col2 = st.columns(2)
            with button_col2.container(width="stretch"):
                if st.button("Sửa", key=f"edit_{student.get('student_id')}", use_container_width=True):
                    update_student(old_student=student)
            with button_col1.container(width="stretch"):
                if st.button("Xóa", key=f"delete_{student.get('student_id')}", type="primary", use_container_width=True):
                    deleted(student_id=student.get("student_id"))
    else:
        st.info("Chưa có tìm kiếm sinh viên nào!")