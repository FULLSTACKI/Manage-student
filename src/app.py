import streamlit as st
from src1.app.ui import form_upload, form_view


st.set_page_config(page_title="Student Management App", page_icon=":school:", layout="wide")
st.title("👨‍🎓 Student Management Dashboard")
st.markdown("---")
st.markdown("Chào mừng đến với ứng dụng quản lý học sinh. Vui lòng chọn tab để bắt đầu.")
st.sidebar.title("Menu")
st.sidebar.markdown("---")
PAGES = {
    "📊 Quản lý Điểm": "manage_scores",
    "👥 Quản lý Sinh viên": "manage_students",
    "📚 Quản lý Khóa học": "manage_courses"
}
selection = st.sidebar.selectbox("Chọn trang:", list(PAGES.keys()), index=0)
page_key = PAGES[selection]

if page_key == "manage_scores":
    page = st.tabs(["📤 Tải điểm", "📖 Xem điểm"])

    with page[0]:
        form_upload.upload_score()

    with page[1]:
        form_view.view_score()
elif page_key == "manage_students":
    page = st.tabs(["📤 Tải sinh viên", "📖 Xem sinh viên"])

    with page[0]:
        form_upload.upload_student()

    with page[1]:
        form_view.view_student()
elif page_key == "manage_courses":
    page = st.tabs(["📤 Tải khóa học", "📖 Xem khóa học"])
    with page[0]:
        form_upload.upload_course()
    with page[1]:
        form_view.view_course()

st.markdown("---")
st.markdown("© 2025 Student Management App. All rights reserved.")
