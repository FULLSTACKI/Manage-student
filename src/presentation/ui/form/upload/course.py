import streamlit as st
import requests 
from src.config import API_BASE
from src.presentation.ui.components.layout import _get_filters
from src.presentation.ui.utils import authenticated_request

# --- HÀM MỚI: UPLOAD_COURSE ---
def upload_course():
    st.subheader("➕ Thêm mới Môn học")

    # --- 1. Lấy dữ liệu cho Selectbox (Khoa) ---
    try:
        data_filter = _get_filters(["departments"])
        departments = data_filter.get("departments", [])
        # Tạo map: Tên Khoa -> ID Khoa
        map_dept_name_to_id = {dept["name"]: dept["id"] for dept in departments}
        department_names = list(map_dept_name_to_id.keys())
    except Exception as e:
        st.error(f"Không thể tải danh sách khoa: {e}")
        department_names = []
        map_dept_name_to_id = {}

    # --- 2. Xử lý giá trị mặc định ---
    # (Để trống cho việc tạo mới)
    start_date_val = None # Hoặc date.today()
    end_date_val = None

    # --- Bắt đầu Form ---
    with st.form("upload_course_form", clear_on_submit=True):
        st.markdown("Nhập thông tin chi tiết cho môn học mới.")
        
        # --- Thiết kế UI 2 cột ---
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 📚 Thông tin Môn học")
            course_id = st.text_input(
                "Mã Môn học *", 
                placeholder="Ví dụ: C001"
            )
            course_name = st.text_input(
                "Tên Môn học *", 
                placeholder="Ví dụ: Lập trình Python"
            )
            credits = st.number_input(
                "Số tín chỉ *", 
                min_value=1, max_value=10, 
                value=3, # Giá trị mặc định
                step=1
            )

        with col2:
            st.markdown("##### 📅 Quản lý & Thời gian")
            department_name = st.selectbox(
                "Khoa quản lý *", 
                options=department_names, 
                index=None, # Để trống, hiển thị placeholder
                placeholder="Chọn khoa..."
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
        submit = st.form_submit_button("Thêm Môn học", use_container_width=True, type="primary")

    # --- 3. Xử lý logic khi Submit ---
    if submit:
        # Validation
        if not course_id or not course_name or not department_name:
            st.error("Mã Môn học, Tên Môn học và Khoa là bắt buộc.")
        else:
            # Lấy ID khoa từ tên khoa đã chọn
            selected_dept_id = map_dept_name_to_id.get(department_name)
            
            payload = {
                "course_id": course_id,
                "course_name": course_name,
                "credits": credits,
                "start_course": str(start_course) if start_course else None,
                "end_course": str(end_course) if end_course else None,
                "department_id": selected_dept_id
            }
            
            try:
                # API Upload Môn học (dùng POST)
                url = f"{API_BASE.rstrip('/')}/courses/upload" 
                resp = authenticated_request("POST", url, json=payload, timeout=10) 
                resp.raise_for_status() # Báo lỗi nếu 4xx/5xx

                data = resp.json()
                
                if (resp.status_code == 200 or resp.status_code == 201) and data.get("success"):
                    # Đặt cờ thành công để hiển thị ở trang chính
                    st.session_state.course_upload_success = data.get("message", "Thêm môn học thành công!")
                    st.rerun() # Đóng dialog (nếu là dialog) và làm mới trang
                else:
                    st.error(data.get("message", f"Thêm môn học thất bại (status {resp.status_code})"))

            except requests.exceptions.HTTPError as e:
                st.error(f"Lỗi HTTP {e.response.status_code}: {e.response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Không thể kết nối tới API: {e}")