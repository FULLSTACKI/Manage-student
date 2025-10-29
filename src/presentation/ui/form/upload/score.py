import streamlit as st
import requests  
from datetime import datetime
from src.presentation.ui import api_base

def upload_score():
    st.title("Upload student score")

    with st.form("upload_form", clear_on_submit=True):
        student_id = st.text_input("Student ID")
        course_id = st.text_input("Course ID")
        coursework = st.number_input("Coursework grade", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        midterm = st.number_input("Midterm grade", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        final = st.number_input("Final grade", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
        submit = st.form_submit_button("Upload")

    if submit:
        if not student_id or not course_id:
            st.error("Student ID and Course ID are required.")
        else:
            payload = {
                "student_id": student_id,
                "course_id": course_id,
                "coursework_grade": coursework,
                "midterm_grade": midterm,
                "final_grade": final,
            }

            try:
                url = api_base.rstrip("/") + "/scores"
                resp = requests.post(url, json=payload, timeout=10)
                try:
                    data = resp.json()
                    st.info(f"Response JSON: {data}")
                except ValueError:
                    st.error(f"Invalid JSON response (status {resp.status_code})")
                    st.write(resp.text)
                else:
                    if resp.status_code == 200 or resp.status_code == 201:
                        # Expecting structure like { "success": True, "message": "...", "score": {...} }
                        if isinstance(data, dict) and data.get("success", True):
                            st.success(data.get("message", "Score uploaded successfully"))
                            if data.get("score"):
                                st.json(data["score"])
                        else:
                            st.error(data.get("message", f"Upload failed (status {resp.status_code})"))
                            st.json(data)
                    else:
                        st.error(f"Request failed with status {resp.status_code}")
                        st.json(data)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {e}")