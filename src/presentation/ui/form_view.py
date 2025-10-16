import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import streamlit as st
import requests
import pandas as pd

api_base = "http://127.0.0.1:8000"

def view_score():
    st.title("View student score")

    with st.form("view_form"):
        student_id = st.text_input("Student ID")
        course_id = st.text_input("Course ID")
        submit = st.form_submit_button("View")
    
    if submit:
        if not student_id or not course_id:
            st.error("Student ID and Course ID are required.")
        else:
            payload = {
                "student_id": student_id,
                "course_id": course_id
            }

            try:
                url = api_base.rstrip("/") + "/scores"
                resp = requests.get(url, json=payload, timeout=10)
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
                
def view_student():
    st.title("View student details")

    with st.form("view_form"):
        student_id = st.text_input("Student ID")
        submit = st.form_submit_button("View")
    
    if submit:
        if not student_id:
            st.error("Student ID is required.")
        else:
            payload = {
                "id": student_id
            }

            try:
                url = api_base.rstrip("/") + "/get_student"
                resp = requests.post(url, json=payload, timeout=10)
                try:
                    data = resp.json()
                    st.info(f"Response JSON: {data}")
                except ValueError:
                    st.error(f"Invalid JSON response (status {resp.status_code})")
                    st.write(resp.text)
                else:
                    if resp.status_code == 200 or resp.status_code == 201:
                        # Expecting structure like { "student": {...} }
                        if isinstance(data, dict) and "student" in data:
                            st.success("Student retrieved successfully")
                            st.subheader("📊 Student Details")
                            st.markdown("---")
                            st.dataframe(pd.json_normalize(data["student"]))
                        else:
                            st.error(f"Student not found (status {resp.status_code})")
                            st.json(data)
                    else:
                        st.error(f"Request failed with status {resp.status_code}")
                        st.json(data)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {e}")
                
def view_course():
    st.title("View course details")
    
    with st.form("view_form"):
        course_id = st.text_input("Course ID")
        submit = st.form_submit_button("View")
    
    if submit:
        if not course_id:
            st.error("Course ID is required.")
        else:
            payload = {
                "id": course_id
            }

            try:
                url = api_base.rstrip("/") + "/get_course"
                resp = requests.post(url, json=payload, timeout=10)
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