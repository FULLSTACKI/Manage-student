import streamlit as st
import requests  
from datetime import datetime
from src.presentation.ui import api_base
from src.presentation.ui.components.layout import _get_filters

@st.dialog("Chỉnh sửa Thông tin Sinh viên", width="medium")
def update_student(old_student=None):
    data_filter = _get_filters(["departments"])
    departments = data_filter["departments"]
    map_dept = {dept["name"]: dept for dept in departments}
    with st.form("update_form"):
        # 1. Logic cho Department
        department_names = list(map_dept.keys())
        current_dept_name = old_student.get("departments", "") # Lấy tên khoa hiện tại
        try:
            # Tìm vị trí (index) của khoa hiện tại trong danh sách
            dept_index = department_names.index(current_dept_name) 
        except ValueError:
            dept_index = 0 # Mặc định là 0 nếu không tìm thấy

        # 2. Logic cho Sex
        sex_options = ["M", "F", "Unknown"]
        current_sex = old_student.get("sex", "Unknown")
        try:
            sex_index = sex_options.index(current_sex)
        except ValueError:
            sex_index = 2 # Mặc định là "Unknown"
            
        # --- Tạo các Tab ---
        tab1, tab2, tab3 = st.tabs([
            "🎓 Thông tin chính", 
            "👤 Thông tin cá nhân", 
            "💳 Liên hệ & CCCD"
        ])

        # --- Tab 1: Thông tin chính ---
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                id = st.text_input("Mã Sinh viên", value=old_student.get("student_id", ""), disabled=True)
            with col2:
                name = st.text_input("Họ và Tên", value=old_student.get("student_name", ""))
            
            col3, col4 = st.columns(2)
            with col3:
                email = st.text_input("Email", value=old_student.get("email", ""))
            with col4:
                # Sửa lại: Dùng `index` thay vì `key`
                department = st.selectbox("Khoa", options=department_names, index=dept_index)

        # --- Tab 2: Thông tin cá nhân ---
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                birthday = st.text_input("Ngày sinh", placeholder="YYYY-MM-DD", value=old_student.get("birthday", ""))
            with col2:
                # Sửa lại: Dùng `index` thay vì `key`
                sex = st.selectbox("Giới tính", options=sex_options, index=sex_index)
            
            birthplace = st.text_input("Nơi sinh", value=old_student.get("birthplace", ""))
            
            col3, col4 = st.columns(2)
            with col3:
                ethnicity = st.text_input("Dân tộc", value=old_student.get("ethnicity", ""))
            with col4:
                religion = st.text_input("Tôn giáo", value=old_student.get("religion", ""))

        # --- Tab 3: Thông tin liên hệ và CCCD ---
        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                phone = st.text_input("Điện thoại", value=old_student.get("phone", ""))
            with col2:
                address = st.text_input("Địa chỉ hiện nay", value=old_student.get("address", ""))

            st.divider() # Ngăn cách
            
            col3, col4 = st.columns(2)
            with col3:
                id_card = st.text_input("CCCD/CMND", value=old_student.get("id_card", ""))
            with col4:
                issue_date = st.text_input("Ngày cấp", placeholder="YYYY-MM-DD", value=old_student.get("issue_date", ""))
            
            issue_place = st.text_input("Nơi cấp", value=old_student.get("issue_place", ""))

        # --- Nút Submit ---
        submit = st.form_submit_button("Cập nhật thông tin", use_container_width=True, type="primary")
    
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
                "birthplace": birthplace,
                "address": address,
                "phone": phone,
                "ethnicity": ethnicity,
                "religion": religion,
                "id_card": id_card,
                "issue_date": issue_date,
                "issue_place": issue_place,
                "department_id": map_dept[department]["id"]
            }
            try:
                url = api_base.rstrip("/") + "/student/update"
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
                                "action": "Chỉnh sửa"
                            })
                            edit_student = data["student"]
                            if edit_student: 
                                st.session_state.history.append(edit_student)
                            st.session_state.search_student = None
                            st.session_state.success_msg = f"Đã chỉnh sửa thành công sinh viên ID: {edit_student.get("student_id")}"
                            st.session_state.toast_msg = "💾 Đã lưu thông tin vào lịch sử."
                            st.rerun()
                        else:
                            st.error(data.get("message", f"Upload failed (status {resp.status_code})"))
                            st.json(data)
                    else:
                        st.error(f"Request failed with status {resp.status_code}")
                        st.json(data)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {e}")