import streamlit as st
from src.presentation.ui.utils import authenticated_request
from ..update.course import update_course
import requests
from src.presentation.ui.config import API_BASE

def view_course():
    st.subheader("📊 Thông tin Môn học")
    
    # Khởi tạo session state
    if "search_course" not in st.session_state:
        st.session_state.search_course = None

    with st.form("course_view_form", clear_on_submit=True):
        col_search1, col_search2 = st.columns([3,1])
        with col_search1:
            course_id = st.text_input("Tìm kiếm theo mã Môn học (VD: C001):")
        with col_search2:
            st.write("") # Thêm để căn chỉnh nút
            st.write("")
            submit = st.form_submit_button("🔍 Tìm")
    
    if submit:
        if not course_id:
            st.error("Mã Môn học là bắt buộc.")
            st.session_state.search_course = None
        else:
            try:
                # Sửa URL: Dùng /courses/{id} (chuẩn REST) thay vì query param
                url = f"{API_BASE.rstrip('/')}/courses/{course_id}" 
                resp = authenticated_request("GET", url, timeout=10)
                
                # Bắt lỗi 4xx/5xx (ví dụ 404 Not Found)
                resp.raise_for_status() 
                
                try:
                    data = resp.json()
                except ValueError:
                    st.error(f"Phản hồi không phải JSON hợp lệ (status {resp.status_code})")
                    st.write(resp.text)
                else:
                    # Kiểm tra response trả về (đã bỏ check 200/201 vì raise_for_status đã xử lý)
                    if isinstance(data, dict) and data.get("success"):
                        # Sửa "student" thành "course"
                        st.session_state.search_course = data 
                        st.success(data.get("message", "Lấy thông tin thành công!"))
                    else:
                        st.error(data.get("message", "Không tìm thấy môn học."))
                        st.session_state.search_course = None
                        
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    st.error(f"Không tìm thấy môn học với mã: {course_id}")
                else:
                    st.error(f"Lỗi HTTP: {e}")
                st.session_state.search_course = None
            except requests.exceptions.RequestException as e:
                st.error(f"Không thể kết nối tới API: {e}")

    # --- Hiển thị thông tin Môn học nếu tìm thấy ---
    if st.session_state.get("search_course") is not None:
        course_info = st.session_state.get("search_course")
        course = course_info.get("course", {}) # Lấy object course
        
        st.markdown("---")
        with st.container(border=True):
            # --- Dòng 1: Tên, ID, Khoa ---
            st.markdown(f"### 📚 **{course.get('course_name', 'N/A')}**")
            st.caption(f"**Mã MH:** {course.get('course_id', 'N/A')} | **Khoa:** {course.get('department_name', 'N/A')}")
            
            st.divider()

            # --- Dòng 2: Thông tin chi tiết ---
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**🎓 Tín chỉ:** {course.get('credits', 'N/A')}")
            with col2:
                st.markdown(f"**Bắt đầu:** {course.get('start_date', 'N/A')}")
            with col3:
                st.markdown(f"**Kết thúc:** {course.get('end_date', 'N/A')}")
                
            st.markdown(f"**🧑‍🏫 Giảng viên:** {course.get('teacher_name', 'N/A')}")

            st.divider()
            
            # --- Dòng 3: Nút bấm ---
            button_col1, button_col2 = st.columns(2)
            with button_col2:
                if st.button("Sửa", key=f"edit_{course.get('course_id')}", use_container_width=True):
                    update_course(old_course=course) # Gọi hàm sửa
            with button_col1:
                if st.button("Xóa", key=f"delete_{course.get('course_id')}", type="primary", use_container_width=True):
                    deleted_course(course_id=course.get("course_id")) # Gọi hàm xóa
    else:
        st.info("Chưa có tìm kiếm môn học nào!")