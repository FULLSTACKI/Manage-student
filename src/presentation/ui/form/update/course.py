import streamlit as st
import requests
from src.presentation.ui.config import API_BASE
from src.presentation.ui.components.layout import _get_filters
from src.presentation.ui.utils import authenticated_request

@st.dialog("Chỉnh sửa Thông tin Môn học", width="medium")
def update_course(old_course=None):
    if not old_course:
        st.error("Dữ liệu môn học cũ không được cung cấp.")
        return

    # --- 1. Lấy dữ liệu cho Selectbox (Khoa) ---
    try:
        data_filter = _get_filters(["departments"])
        departments = data_filter.get("departments", [])
        # Tạo map: Tên Khoa -> ID Khoa
        map_dept_name_to_id = {dept["name"]: dept["id"] for dept in departments}
        # Tạo map ngược: ID Khoa -> Tên Khoa
        map_dept_id_to_name = {dept["id"]: dept["name"] for dept in departments}
    except Exception as e:
        st.error(f"Không thể tải danh sách khoa: {e}")
        departments = []
        map_dept_name_to_id = {}
        map_dept_id_to_name = {}

    # --- 2. Xử lý giá trị mặc định cho Selectbox Khoa ---
    department_names = list(map_dept_name_to_id.keys())
    # Giả sử 'old_course' có 'department_id', chúng ta cần tìm 'name' của nó
    current_dept_id = old_course.get("department_id", "")
    current_dept_name = map_dept_id_to_name.get(current_dept_id, "")
    try:
        dept_index = department_names.index(current_dept_name)
    except ValueError:
        dept_index = 0 # Mặc định nếu không tìm thấy

    # --- 3. Xử lý giá trị mặc định cho DateInputs ---
    start_date_val = old_course.get("start_course")
    end_date_val = old_course.get("end_course")

    # --- Bắt đầu Form ---
    with st.form("update_course_form"):
        st.markdown("Cập nhật thông tin chi tiết cho môn học.")
        
        # --- Thiết kế UI 2 cột "khác biệt" ---
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 📚 Thông tin Môn học")
            course_id = st.text_input(
                "Mã Môn học", 
                value=old_course.get("course_id", ""), 
                disabled=True
            )
            course_name = st.text_input(
                "Tên Môn học", 
                value=old_course.get("course_name", "")
            )
            credits = st.number_input(
                "Số tín chỉ", 
                min_value=1, max_value=10, 
                value=old_course.get("credits", 1), 
                step=1
            )

        with col2:
            st.markdown("##### 📅 Quản lý & Thời gian")
            department_name = st.selectbox(
                "Khoa quản lý", 
                options=department_names, 
                index=dept_index
            )
            start_course = st.date_input(
                "Ngày bắt đầu", 
                value=start_date_val
            )
            end_course = st.date_input(
                "Ngày kết thúc", 
                value=end_date_val
            )

        # --- Nút Submit ---
        st.write("") # Thêm khoảng trắng
        submit = st.form_submit_button("Cập nhật Môn học", use_container_width=True, type="primary")

    # --- Xử lý logic khi Submit ---
    if submit:
        # Lấy ID từ 'old_course' vì input bị disabled
        current_id = old_course.get("course_id") 
        
        # Validation
        if not current_id or not course_name or not department_name:
            st.error("Mã Môn học, Tên Môn học và Khoa là bắt buộc.")
        else:
            # Lấy ID khoa từ tên khoa đã chọn
            selected_dept_id = map_dept_name_to_id.get(department_name)
            
            payload = {
                "course_id": current_id,
                "course_name": course_name,
                "credits": credits,
                "start_course": str(start_course) if start_course else None,
                "end_course": str(end_course) if end_course else None,
                "department_id": selected_dept_id
            }
            
            try:
                # API Update Môn học (dùng PUT hoặc PATCH, trỏ đến ID)
                url = f"{API_BASE.rstrip('/')}/courses/{current_id}" 
                # Dùng authenticated_request
                resp = authenticated_request("PUT", url, json=payload, timeout=10) 
                resp.raise_for_status() # Báo lỗi nếu 4xx/5xx

                data = resp.json()
                
                if resp.status_code == 200 and data.get("success"):
                    # Đặt cờ thành công để hiển thị ở trang chính
                    st.session_state.course_update_success = data.get("message", "Cập nhật thành công!")
                    st.rerun() # Đóng dialog và làm mới trang
                else:
                    st.error(data.get("message", f"Cập nhật thất bại (status {resp.status_code})"))

            except requests.exceptions.HTTPError as e:
                st.error(f"Lỗi HTTP {e.response.status_code}: {e.response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Không thể kết nối tới API: {e}")