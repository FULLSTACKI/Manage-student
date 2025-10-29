import streamlit as st
import requests
import pandas as pd
from src.presentation.ui import api_base

def view_score():
    st.title("View student score")

    with st.form("view_form", clear_on_submit=True):
        student_id = st.text_input("Student ID")
        course_id = st.text_input("Course ID")
        submit = st.form_submit_button("View")
    
    if submit:
        if not student_id or not course_id:
            st.error("Student ID and Course ID are required.")
        else:
            try:
                url = api_base.rstrip("/") + f"/scores/student_id={student_id}/course_id={course_id}"
                resp = requests.get(url, timeout=10)
                try:
                    data = resp.json()
                    st.info(f"Response JSON: {data}")
                except ValueError:
                    st.error(f"Invalid JSON response (status {resp.status_code})")
                    st.write(resp.text)
                else:
                    if resp.status_code == 200 or resp.status_code == 201:
                        # Expecting structure like { "score": {...} }
                        if isinstance(data, dict) and "score" in data:
                            st.success("Score retrieved successfully")
                            st.subheader("📊 Score Details")
                            st.markdown("---")
                            st.dataframe(pd.json_normalize(data["score"]))
                        else:
                            st.error(f"Score not found (status {resp.status_code})")
                            st.json(data)
                    else:
                        st.error(f"Request failed with status {resp.status_code}")
                        st.json(data)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {e}")