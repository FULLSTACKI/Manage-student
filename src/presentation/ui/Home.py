from src.presentation.ui.components import footer
import streamlit as st 

def main():
    st.set_page_config(page_title="Student Management App", page_icon=":school:", layout="wide")
    with st.container():
        st.title("👨‍🎓 Student Management")
        st.markdown("---")
        st.markdown("Chào mừng đến với ứng dụng quản lý học sinh.")

    with st.container():
        st.write("Đây là nội dung của trang chủ.")
        
    if st.button("Đi đến Trang Quản lý"):
        st.switch_page("pages/2_⚙️_Management.py")
    
    if st.button("Đi đến Trang Phân Tích Data"):
        st.switch_page("pages/1_📈_Dashboard.py")

    footer()

if __name__ == "__main__":
    main()