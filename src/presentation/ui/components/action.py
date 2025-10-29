import streamlit as st
import requests
from src.presentation.ui import api_base
from datetime import datetime

def deleted(student_id: str):
    try:
        url = api_base.rstrip("/") + f"/student/{student_id}"
        resp = requests.delete(url, timeout=10)
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
                    data["student"].update({
                        "action_time": datetime.now(),
                        "action": "Xóa"
                    })
                    deleted_student_data = data["student"]
                    if deleted_student_data:
                        st.session_state.history.append(deleted_student_data)
                    st.session_state.search_student = None 
                    st.session_state.success_msg = f"Đã xóa thành công sinh viên ID: {student_id}"
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