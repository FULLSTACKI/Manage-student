import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
import requests

api_base = "http://localhost:8000"  

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
                url = api_base.rstrip("/") + "/upload_score"
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

def upload_student():
    st.title("Upload student info")
    
    with st.form("upload_form", clear_on_submit=True):
        id = st.text_input("Student ID")
        name = st.text_input("Name")
        email = st.text_input("Email")
        birthday = st.text_input("Birthday", placeholder="YYYY-MM-DD")
        sex = st.selectbox("Sex", options=["M", "F", "Unknown"], index=2)
        submit = st.form_submit_button("Upload")

    if submit:
        if not id or not name or not email or not birthday:
            st.error("Student ID, Name, Email and birthday are required.")
        else:
            payload = {
                "id": id,
                "name": name,
                "email": email,
                "birthday": birthday,
                "sex":  sex,
            }
            st.info(f"Payload: {payload}")

            try:
                url = api_base.rstrip("/") + "/upload_student"
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

def upload_course():
    st.title("Upload course info")
    
    with st.form("upload_form", clear_on_submit=True):
        id = st.text_input("Course ID")
        name = st.text_input("Course Name")
        credits = st.number_input("Credits", min_value=1, max_value=5, value=3, step=1)
        start_date = st.text_input("Start date", placeholder="YYYY-MM-DD")
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
            }

            try:
                url = api_base.rstrip("/") + "/upload_course"
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