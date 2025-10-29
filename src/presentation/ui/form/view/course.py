import streamlit as st
import requests
import pandas as pd
from src.presentation.ui import api_base

def view_course():
    st.title("View course details")
    
    with st.form("view_form", clear_on_submit=True):
        course_id = st.text_input("Course ID")
        submit = st.form_submit_button("View")
    
    if submit:
        if not course_id:
            st.error("Course ID is required.")
        else:
            try:
                url = api_base.rstrip("/") + f"/courses/{course_id}"
                resp = requests.get(url, timeout=10)
                try:
                    data = resp.json()
                    st.info(f"Response JSON: {data}")
                except ValueError:
                    st.error(f"Invalid JSON response (status {resp.status_code})")
                    st.write(resp.text)
                else:
                    if resp.status_code == 200 or resp.status_code == 201:
                        # Expecting structure like { "course": {...} }
                        if isinstance(data, dict) and "course" in data:
                            st.success("Course retrieved successfully")
                            st.subheader("📊 Course Details")
                            st.markdown("---")
                            st.dataframe(pd.json_normalize(data["course"]))
                        else:
                            st.error(f"Course not found (status {resp.status_code})")
                            st.json(data)
                    else:
                        st.error(f"Request failed with status {resp.status_code}")
                        st.json(data)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {e}")