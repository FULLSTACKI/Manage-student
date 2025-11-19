import streamlit as st 
from src.presentation.ui.form import *
from src.presentation.ui.components import *

# -- init session_state search_student --
if "search_student" not in st.session_state:
    st.session_state.search_student = None
if "history_list" not in st.session_state:
    st.session_state.history_list = []

def manage_ui_student():
    st.set_page_config(page_title="Student Management", page_icon=":school:", layout="wide")
    with st.container():
        st.title("👨‍🎓 Student Management")
        st.markdown("---")
    
        column_s1, column_s2, column_s3= st.columns([2, 2, 2])
        
        with column_s2.container():
            upload_student()
            success = st.session_state.pop("upload_success_msg", None)
            toast = st.session_state.pop("upload_toast_msg", None)
            if success and toast:
                st.success(success)
                st.toast(toast)
            
        with column_s3.container(height=750, border=False): 
            history_student()

        with column_s1.container(border=False):
            view_student()
            success = st.session_state.pop("success_msg", None)
            toast = st.session_state.pop("toast_msg", None)
            if success and toast:
                st.success(success)
                st.toast(toast)         

        st.divider()
        with st.expander("Xem Danh sách thông tin Sinh viên", expanded=True):
            table_detail_student()

if __name__ == "__main__":
    manage_ui_student()