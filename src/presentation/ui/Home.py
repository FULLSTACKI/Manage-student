import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../../"))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import streamlit as st
from src.config import API_BASE
import requests
from src.config.settings import Role
from src.presentation.ui.admin import *
from src.presentation.ui.student.profile import render_student_profile

def manage_departments_ui(): st.title("🏢 Quản lý Khoa")
def manage_scores_ui(): st.title("📊 Quản lý Điểm số")

def student_profile_ui(): st.title("🧑 Hồ sơ Cá nhân")
def register_course_ui(): st.title("✍️ Đăng ký Môn học")
def view_scores_ui(): st.title("📈 Xem Điểm thi")
def view_timetable_ui(): st.title("📅 Xem Thời khóa biểu")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.token = ""
    st.session_state.role = None
    st.session_state.username = ""
    st.session_state.student_id = None
    
def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
    
def sidebar_ui():
    with st.sidebar.container(height="stretch"):
        # --- Phần Header ---
        st.header("🎓 EduManager")
        st.caption(f"Vai trò: **{st.session_state.role.upper()}**")
        
        st.divider()
        
        if st.session_state.role == Role.ADMIN.value:
            # Sử dụng use_container_width=True để nút trông giống menu item hơn
            if st.button("🏠 Dashboard", use_container_width=True, type="tertiary"):
                st.session_state.current_page = "Dashboard"
                
            if st.button("👥 Quản lý Sinh viên", use_container_width=True, type="tertiary"):
                st.session_state.current_page = "Sinh viên"
                
            if st.button("📚 Quản lý Môn học", use_container_width=True, type="tertiary"):
                st.session_state.current_page = "Môn học"
                
            if st.button("📚 Quản lý Điểm", use_container_width=True, type="tertiary"):
                st.session_state.current_page = "Điểm"
                
            if st.button("📚 Quản lý Khoa", use_container_width=True, type="tertiary"):
                st.session_state.current_page = "Khoa"
                
        elif st.session_state.role == "student":
            if st.button("👤 Hồ sơ cá nhân", use_container_width=True):
                st.session_state.current_page = "Hồ sơ"
            if st.button("✍️ Đăng ký môn", use_container_width=True):
                st.session_state.current_page = "Đăng ký môn"
            if st.button("📈 Xem điểm", use_container_width=True):
                st.session_state.current_page = "Xem điểm"
            if st.button("📅 Thời khóa biểu", use_container_width=True):
                st.session_state.current_page = "Thời khóa biểu"

        # --- Phần Footer ---
        st.divider()
        if st.button("🚪 Đăng xuất", key="btn_logout_student", use_container_width=True):
            logout()

def show_login_page():
    st.set_page_config(page_title="Login", layout="centered")
    st.title("🔐 Đăng nhập hệ thống")

    with st.form("login_form"):
        username = st.text_input("Tên đăng nhập")
        password = st.text_input("Mật khẩu", type="password")
        submitted = st.form_submit_button("Đăng nhập")

        if submitted:
            payload={
                "username": username,
                "password": password
            }
            try:
                url = API_BASE.rstrip("/") + "/auth/login"
                resp = requests.post(url, json=payload, timeout=10)
                try:
                    data = resp.json()
                except ValueError:
                    st.error(f"Invalid JSON response (status {resp.status_code})")
                    st.write(resp.text)
                else:
                    if resp.status_code == 200 or resp.status_code == 201:
                        if isinstance(data, dict) and data.get("success", True):
                            st.session_state.logged_in = True
                            st.session_state.token = data.get("access_token")
                            st.session_state.username = data.get("username")
                            st.session_state.student_id = data.get("student_id")
                            st.session_state.role = data.get("role")
                            st.rerun()
                    else:
                        st.error(f"Request failed with status {resp.status_code}")
                        st.json(data)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {e}")

def main():
    if not st.session_state.logged_in:
        show_login_page()
    else:
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Dashboard" if st.session_state.role == Role.ADMIN.value else "Hồ sơ"
        sidebar_ui()
        selected_page = st.session_state.current_page
        if st.session_state.role == Role.ADMIN.value:    
            if selected_page == "Dashboard":
                dashboard_ui()
            elif selected_page == "Sinh viên":
                manage_ui_student()
            elif selected_page == "Môn học":
                manage_course_ui()
            elif selected_page == "Khoa":
                manage_departments_ui()
            elif selected_page == "Điểm":
                manage_scores_ui()
        elif st.session_state.role == Role.STUDENT.value:
            if selected_page == "Hồ sơ":
                render_student_profile(st.session_state.get("student_id"))
            elif selected_page == "Đăng ký môn":
                register_course_ui()
            elif selected_page == "Xem điểm":
                view_scores_ui()
            elif selected_page == "Thời khóa biểu":
                view_timetable_ui()



if __name__ == "__main__":
    main()