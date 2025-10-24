import streamlit as st 
from src.presentation.ui.form import *
from src.presentation.ui.components import *

if 'students' not in st.session_state:
    st.session_state.students = [
        {'id': 'SV001', 'name': 'Nguyễn Văn An', 'birthday': '2002-01-15', 'email': 'an.nv@email.com'},
        {'id': 'SV002', 'name': 'Trần Thị Bình', 'birthday': '2002-05-20', 'email': 'binh.tt@email.com'}
    ]

def manage_ui():
    st.set_page_config(page_title="Student Management", page_icon=":school:", layout="wide")
    with st.container():
        st.title("👨‍🎓 Student Management")
        st.markdown("---")
    
    tab_student, tab_course, tab_score = st.tabs(["🎓 Sinh viên", "📚 Khóa học", "📝 Điểm số"])
    
    with tab_student.container(border=True):
        column_s1, column_s2, column_s3 = st.columns([3, 3, 1])
        
        with column_s1:
            view_student()
            
        with column_s2:
            st.subheader("📝 Chỉnh sửa")
            st.info("Nhấn nút 'Sửa' ở danh sách để chỉnh sửa thông tin.")
            
        with column_s3:
            if st.button("➕ Thêm"):
                upload_student()
            
        with st.expander("Xem Danh sách thông tin Sinh viên"):
            table_detail_student()

    # Bạn có thể tiếp tục thiết kế cho tab_course và tab_score theo cách tương tự
    with tab_course:
        st.write("Chức năng quản lý khóa học...")

    with tab_score:
        st.write("Chức năng quản lý điểm...")

if __name__ == "__main__":
    manage_ui()