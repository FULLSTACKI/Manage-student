import streamlit as st 
from src.presentation.ui.form import *
from src.presentation.ui.components import *

# -- init session_state search_student --
if "search_student" not in st.session_state:
    st.session_state.search_student = None
if "history" not in st.session_state:
    st.session_state.history = []

def manage_ui():
    st.set_page_config(page_title="Student Management", page_icon=":school:", layout="wide")
    with st.container():
        st.title("👨‍🎓 Student Management")
        st.markdown("---")
    
    tab_student, tab_course, tab_score = st.tabs(["🎓 Sinh viên", "📚 Khóa học", "📝 Điểm số"])
    
    with tab_student.container(border=True):
        column_s1, column_s2, column_s3 = st.columns([1, 1, 1])
        
        with column_s1:
            view_student()
            success = st.session_state.pop("success_msg", None)
            toast = st.session_state.pop("toast_msg", None)
            if success and toast:
                st.success(success)
                st.toast(toast)
            
        with column_s3: 
            st.subheader("📜 Lịch sử thay đổi")

            if not st.session_state.history:
                st.info("Chưa có thay đổi nào được ghi lại.")
            else:
                st.caption("Hiển thị các thay đổi gần đây nhất:")
                for data in reversed(st.session_state.history):
                    action = data.get("action")
                    action_time = data.get("action_time")
                    with st.container(border=True):
                        history_col1, history_col2 = st.columns([4,1])
                        with history_col1.container(vertical_alignment="center", height="stretch"): 
                            st.markdown(f"**{action.upper()}** - **{data.get('student_name', 'N/A')}** (ID: {data.get('student_id', 'N/A')})")
                            details = []
                            if 'departments' in data:
                                details.append(f"Khoa: {data['departments']}")
                            if 'email' in data:
                                details.append(f"Email: {data['email']}")
                            if 'birthday' in data:
                                details.append(f"Ngày sinh: {data['birthday']}")
                            if "action_time" in data:
                                details.append(f"Thời gian: `{action_time.strftime('%Y-%m-%d %H:%M:%S')}`")
                                
                            st.caption(" | ".join(details))
                        with history_col2.container(height="stretch", vertical_alignment="center"):
                            if st.button("Chi tiết",type="tertiary",use_container_width=True, key=f"{action}_{data.get("student_id")}"):
                                st.warning("Xem chi tiết...")
                            
        with column_s2:
            upload_student()
            success = st.session_state.pop("upload_success_msg", None)
            toast = st.session_state.pop("upload_toast_msg", None)
            if success and toast:
                st.success(success)
                st.toast(toast)
            
        with st.expander("Xem Danh sách thông tin Sinh viên", expanded=True):
            table_detail_student()

    # Bạn có thể tiếp tục thiết kế cho tab_course và tab_score theo cách tương tự
    with tab_course:
        st.write("Chức năng quản lý khóa học...")

    with tab_score:
        st.write("Chức năng quản lý điểm...")

if __name__ == "__main__":
    manage_ui()