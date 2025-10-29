import streamlit as st
import requests  
from datetime import datetime
from src.presentation.ui import api_base

def upload_course():
    st.title("Upload course info")
    
    with st.form("upload_form", clear_on_submit=True):
        id = st.text_input("Course ID")
        name = st.text_input("Course Name")
        credits = st.number_input("Credits", min_value=1, max_value=5, value=3, step=1)
        start_date = st.text_input("Start date", placeholder="YYYY-MM-DD")
        department_id = st.text_input("Department ID")
        submit = st.form_submit_button("Upload")
    
    if submit:
        if not id or not name or not credits or not start_date:
            st.error("Course ID, Course Name, start date and credits are required.")
        else:
            payload = {
                "id": id,
                "name": name,
                "credits": credits,
                'start_course': start_date,
                "department_id": department_id
            }

            try:
                url = api_base.rstrip("/") + "/courses"
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
                            st.success(data.get("message", "Course uploaded successfully"))
                            if data.get("course"):
                                st.json(data["course"])
                        else:
                            st.error(data.get("message", f"Upload failed (status {resp.status_code})"))
                            st.json(data)
                    else:
                        st.error(f"Request failed with status {resp.status_code}")
                        st.json(data)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {e}")