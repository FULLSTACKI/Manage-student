import streamlit as st
import requests  
from src.config import API_BASE
from src.presentation.ui.components.layout import _get_filters
from src.presentation.ui.utils import authenticated_request
                    
def upload_student():
    st.subheader("Thêm Sinh viên mới")
    data_filter = _get_filters(["departments"])
    departments = data_filter["departments"]
    map_dept = {dept["name"]: dept for dept in departments}
    with st.form("upload_form", clear_on_submit=True, height=600):
        # --- Tạo các Tab để nhóm thông tin ---
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎓 Thông tin chính", 
            "👤 Thông tin cá nhân", 
            "💳 Liên hệ & CCCD", 
            "📁 Nhập từ file"
        ])

        # --- Tab 1: Thông tin quan trọng nhất ---
        with tab1:
            st.markdown("##### Thông tin học vụ (Bắt buộc)")
            
            # Sử dụng cột để xếp các trường ngắn cạnh nhau
            col1, col2 = st.columns(2)
            with col1:
                id = st.text_input("Mã Sinh viên *")
            with col2:
                department = st.selectbox("Khoa *", options=map_dept.keys(), index=None)
            
            name = st.text_input("Họ và Tên *")
            email = st.text_input("Email *")

        # --- Tab 2: Thông tin cá nhân ---
        with tab2:
            st.markdown("##### Thông tin cá nhân & Hộ khẩu")
            
            col1, col2 = st.columns(2)
            with col1:
                birthday = st.text_input("Ngày sinh", placeholder="YYYY-MM-DD")
            with col2:
                sex = st.selectbox("Giới tính", options=["M", "F", "Unknown"], index=2)
            
            birthplace = st.text_input("Nơi sinh")
            
            col3, col4 = st.columns(2)
            with col3:
                ethnicity = st.text_input("Dân tộc", placeholder="Vd: Kinh")
            with col4:
                religion = st.text_input("Tôn giáo", placeholder="Vd: Không")

        # --- Tab 3: Thông tin liên hệ và CCCD ---
        with tab3:
            st.markdown("##### Thông tin liên lạc")
            col1, col2 = st.columns(2)
            with col1:
                address = st.text_input("Địa chỉ hiện nay")
            with col2:
                phone = st.text_input("Điện thoại")

            st.divider() # Ngăn cách 2 nhóm
            
            st.markdown("##### Thông tin CCCD/CMND")
            id_card = st.text_input("CCCD/CMND")
            col3, col4 = st.columns(2)
            with col3:
                issue_date = st.text_input("Ngày cấp", placeholder="YYYY-MM-DD")
            with col4:
                issue_place = st.text_input("Nơi cấp")

        # --- Tab 4: Nhập hàng loạt từ file ---
        with tab4:
            st.info("Tải file .docx theo mẫu. Các thông tin bạn nhập ở các tab trên sẽ được ưu tiên.")
            files = st.file_uploader(
                "Trích xuất thông tin từ file .docx:", 
                type=".docx", 
                accept_multiple_files=True
            )

        with st.container(width="stretch", vertical_alignment="bottom", height="stretch"):
            submit = st.form_submit_button("Thêm Sinh viên", use_container_width=True, type="primary")

    
    if submit:
        if files:
            file_list_for_api = []
            for file in files:
                file_tuple = ("files", (file.name, file.getvalue(), file.type))
                file_list_for_api.append(file_tuple)
            try:
                url = API_BASE.rstrip("/") + "/students/import_file"
                resp = authenticated_request("POST",url, files=file_list_for_api, timeout=10)
                try:
                    data = resp.json()
                except ValueError:
                    st.error(f"Invalid JSON response (status {resp.status_code})")
                    st.write(resp.text)
                else:
                    if resp.status_code == 200 or resp.status_code == 201:
                        # Expecting structure like { "success": True, "message": "...", "score": {...} }
                        if isinstance(data, dict) and data.get("success", True):
                            st.session_state.upload_success_msg = data.get("message")
                            st.session_state.upload_toast_msg = "💾 Đã lưu thông tin vào lịch sử."
                            st.rerun()
                    else:
                        st.error(f"Request failed with status {resp.status_code}")
                        st.json(data)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {e}")          
        elif not (id and name and email and birthday)   :
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
                url = API_BASE.rstrip("/") + "/students/upload"
                resp = authenticated_request("POST",url, json=payload, timeout=10)
                try:
                    data = resp.json()
                except ValueError:
                    st.error(f"Invalid JSON response (status {resp.status_code})")
                    st.write(resp.text)
                else:
                    if resp.status_code == 200 or resp.status_code == 201:
                        # Expecting structure like { "success": True, "message": "...", "score": {...} }
                        if isinstance(data, dict) and data.get("success", True):
                            st.session_state.upload_success_msg = data.get("message")
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

