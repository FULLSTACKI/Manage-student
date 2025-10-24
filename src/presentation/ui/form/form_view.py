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

def view_student():
    st.subheader("Danh sách Sinh viên")
    with st.form("view_form", clear_on_submit=True):
        student_id = st.text_input("Tìm kiếm theo mã số Sinh viên:")
        submit = st.form_submit_button("Tìm kiếm")
    
    if submit:
        if not student_id:
            st.error("Student ID is required.")
        else:
            try:
                url = api_base.rstrip("/") + f"/students/{student_id}"
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
                try:
                    data = resp.json()
                except ValueError:
                    st.error(f"Invalid JSON response (status {resp.status_code})")
                    st.write(resp.text)
                else:
                    if resp.status_code == 200 or resp.status_code == 201:
                        # Expecting structure like { "student": {...} }
                        if isinstance(data, dict) and "student" in data:
                            st.success("Student retrieved successfully")
                            st.markdown("---")
                            st.subheader("📊 Thông tin Sinh viên")
                            student = data["student"]
                            with st.container(border=True):
                                col_info, col_actions = st.columns([4, 1])
                                with col_info:
                                    st.write(f"**{student.get("name")}** (ID: {student.get("id")})")
                                    st.caption(f"Email: {student.get("email")} | Ngày sinh: {student.get("birthday")}")
                                with col_actions:
                                    st.button("Sửa")
                                    st.button("Xóa")
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