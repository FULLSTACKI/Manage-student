import streamlit as st
import requests
from src.config import API_BASE
from src.presentation.ui.utils import authenticated_request

def deleted_student(student_id: str):
    try:
        url = API_BASE.rstrip("/") + f"/students/{student_id}"
        resp = authenticated_request("DELETE",url, timeout=10)
        resp.raise_for_status()
        try:
            data = resp.json()
        except ValueError:
            st.error(f"Invalid JSON response (status {resp.status_code})")
            st.write(resp.text)
        else:
            if resp.status_code == 200:
                # Expecting structure like { "student": {...} }
                if isinstance(data, dict) and data.get("success"):
                    st.session_state.search_student = None 
                    st.session_state.success_msg = data.get("message")
                    st.session_state.toast_msg = "💾 Đã lưu thông tin vào lịch sử xóa."
                    st.rerun()
                else:
                    st.error(f"Student not found (status {resp.status_code})")
                    st.json(data)
            else:
                st.error(f"Request failed with status {resp.status_code}")
                st.json(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        
def deleted_course(course_id: str):
    try:
        url = API_BASE.rstrip("/") + f"/courses/{course_id}"
        resp = authenticated_request("DELETE",url, timeout=10)
        resp.raise_for_status()
        try:
            data = resp.json()
        except ValueError:
            st.error(f"Invalid JSON response (status {resp.status_code})")
            st.write(resp.text)
        else:
            if resp.status_code == 200:
                # Expecting structure like { "course": {...} }
                if isinstance(data, dict) and data.get("success"):
                    st.session_state.search_course = None 
                    st.session_state.success_msg = data.get("message")
                    st.session_state.toast_msg = "💾 Đã lưu thông tin vào lịch sử xóa."
                    st.rerun()
                else:
                    st.error(f"course not found (status {resp.status_code})")
                    st.json(data)
            else:
                st.error(f"Request failed with status {resp.status_code}")
                st.json(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")