import streamlit as st
import requests
from src.presentation.ui.config import API_BASE
from ..update.student import update_student
from src.presentation.ui.components import deleted_student
from src.presentation.ui.utils import authenticated_request

def view_student():
    st.subheader("📊 Thông tin Sinh viên")
    with st.form("view_form", clear_on_submit=True):
        col_search1, col_search2 = st.columns([3,1])
        with col_search1:
            student_id = st.text_input("Tìm kiếm theo mã số Sinh viên:")
        with col_search2.container(vertical_alignment='center', height='stretch', horizontal_alignment='center'):
            submit = st.form_submit_button("🔍")
    
    if submit:
        if not student_id:
            st.error("Student ID is required.")
            st.session_state.search_student = None
        else:
            try:
                url = API_BASE.rstrip("/") + f"/students?student_id={student_id}"
                resp = authenticated_request("GET", url, timeout=10)
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
        student_info = st.session_state.get("search_student")
        student = student_info.get("student", {})
        with st.container(border=True,horizontal_alignment="center", vertical_alignment="center", height="stretch"):
            # --- Dòng 1: Tên, ID, Khoa ---
            st.markdown(f"### 🧑‍🎓 **{student.get('student_name', 'N/A')}**")
            st.caption(f"**ID:** {student.get('student_id', 'N/A')} | **Khoa:** {student.get('departments', 'N/A')}")
            
            st.divider()

            # --- Dòng 2: Thông tin cá nhân (chia 2 cột) ---
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**🚻 Giới tính:** {student.get('sex', 'N/A')}")
                st.markdown(f"**🎂 Tuổi:** {student.get('age', 'N/A')}") # Thay thế st.metric
                st.markdown(f"**🗓️ Ngày sinh:** {student.get('birthday', 'N/A')}")
                st.markdown(f"**🌍 Nơi sinh:** {student.get('birthplace', 'N/A')}")
            with col2:
                st.markdown(f"**👥 Dân tộc:** {student.get('ethnicity', 'N/A')}")
                st.markdown(f"**🧘 Tôn giáo:** {student.get('religion', 'N/A')}")
                st.markdown(f"**📱 Điện thoại:** {student.get('phone', 'N/A')}")
                st.markdown(f"**📧 Email:** {student.get('email', 'N/A')}")

            # --- Dòng 3: Địa chỉ ---
            st.markdown(f"**🏠 Địa chỉ:** {student.get('address', 'N/A')}")

            st.divider() # Ngăn cách

            # --- Dòng 4: Thông tin CCCD (chia 2 cột) ---
            col3, col4 = st.columns(2)
            with col3:
                st.markdown(f"**💳 CCCD:** `{student.get('id_card', 'N/A')}`")
            with col4:
                st.markdown(f"**Ngày cấp:** {student.get('issue_date', 'N/A')}")
            
            # Nơi cấp cho xuống caption để tiết kiệm không gian
            st.caption(f"**Nơi cấp:** {student.get('issue_place', 'N/A')}")

            st.divider()
            button_col1, button_col2 = st.columns(2)
            with button_col2.container(width="stretch"):
                if st.button("Sửa", key=f"edit_{student.get('student_id')}", use_container_width=True):
                    update_student(old_student=student)
            with button_col1.container(width="stretch"):
                if st.button("Xóa", key=f"delete_{student.get('student_id')}", type="primary", use_container_width=True):
                    deleted_student(student_id=student.get("student_id"))
    else:
        st.info("Chưa có tìm kiếm sinh viên nào!")