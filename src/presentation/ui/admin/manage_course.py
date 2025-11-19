import streamlit as st
from src.presentation.ui.form import view_course, upload_course

# --- Khởi tạo session state cho Môn học ---
if "search_course" not in st.session_state:
    st.session_state.search_course = None
if "course_history_list" not in st.session_state:
    st.session_state.course_history_list = []
# (Các key message riêng biệt để tránh xung đột với Student)
if "course_upload_success" not in st.session_state:
    st.session_state.course_upload_success = None
if "course_update_success" not in st.session_state:
    st.session_state.course_update_success = None
if "course_delete_success" not in st.session_state:
    st.session_state.course_delete_success = None


def manage_course_ui():
    st.set_page_config(page_title="Course Management", page_icon="📚", layout="wide")
    with st.container():
        st.title("📚 Quản lý Môn học")
        st.markdown("---")

        # --- Xử lý thông báo (gom về một chỗ ở đầu) ---
        # Kiểm tra thông báo từ nghiệp vụ Thêm
        upload_msg = st.session_state.pop("course_upload_success", None)
        if upload_msg:
            st.success(upload_msg)
            st.toast("Môn học đã được tạo!")

        # Kiểm tra thông báo từ nghiệp vụ Sửa
        update_msg = st.session_state.pop("course_update_success", None)
        if update_msg:
            st.success(update_msg)
            st.toast("Môn học đã được cập nhật!")
            
        # Kiểm tra thông báo từ nghiệp vụ Xóa
        delete_msg = st.session_state.pop("course_delete_success", None)
        if delete_msg:
            st.success(delete_msg)
            st.toast("Môn học đã được xóa.")

        # --- Sử dụng TABS thay vì COLUMNS ---
        tab_upload, tab_view = st.tabs([
            "➕ Thêm mới Môn học",
            "🔍 Tìm kiếm & Cập nhật",
            # "📜 Lịch sử Thay đổi"
        ])

        # Tab 1: Form Thêm mới
        with tab_upload:
            upload_course()

        # Tab 2: Form Tìm kiếm, Sửa, Xóa
        with tab_view:
            view_course()

        # # Tab 3: Form Lịch sử
        # with tab_history:
        #     history_course()

        # # --- Bảng danh sách (Giữ nguyên ở dưới) ---
        # st.divider()
        # with st.expander("Xem Toàn bộ Danh sách Môn học", expanded=True):
        #     table_detail_course()