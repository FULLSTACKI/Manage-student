import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
from pathlib import Path
from PIL import Image
import requests

PATH = Path(__file__).parent.parent.parent / "data/seed"
api_base = "http://localhost:8000"

st.set_page_config(
    page_title="Tổng quan",
    page_icon="🎓",
    layout="wide"
)

def compute_gpa(coursework: float, midterm: float, final: float) -> float:
    """
    Tính điểm GPA theo công thức: 20% coursework, 30% midterm, 50% final.
    """
    return round(0.2 * coursework + 0.3 * midterm + 0.5 * final, 2)

student_df = pd.read_csv(PATH / "students.csv")
course_df = pd.read_csv(PATH / "courses.csv")
score_df = pd.read_csv(PATH / "scores.csv")
registration_df = pd.read_csv(PATH / "registrations.csv")
department_df = pd.read_csv(PATH / "departments.csv")



st.title("📊 Dashboard Tổng quan")
st.markdown("---")

@st.cache_data
def get_analytic_view():
    try:
        url = api_base.rstrip("/") + "/analytics_view"
        response = requests.get(url, timeout=10)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        
def Search():
    analytics_views = get_analytic_view()
    if not analytics_views:
        st.error("Không thể tải cấu hình phân tích từ backend.")
    else:
        # Giả sử chúng ta chỉ làm việc với view đầu tiên
        view_config = analytics_views[0]
        
        # --- XÂY DỰNG CÁC SELECTBOX PHỤ THUỘC ---
        st.header("Tùy chọn phân tích")
        
        # 1. Selectbox cho Dimension (Cột X)
        # Tạo map từ display name sang key để dễ xử lý
        dimension_map = {item["display"]: item for item in view_config['dimensions']}
        selected_dim_display = st.selectbox(
            "1. Chọn chiều phân tích (trục X):",
            options=dimension_map.keys()
        )
        selected_dimension = dimension_map[selected_dim_display]

        # 2. Lọc và hiển thị Selectbox cho Metric (Cột Y)
        valid_metric_keys = selected_dimension['valid_metrics']
        
        metric_map = {item['key']: item for item in view_config['metrics']}
        # Lọc ra các metric hợp lệ từ danh sách metrics chung
        available_metrics = []
        for key in valid_metric_keys:
            available_metrics.append(metric_map[key])

        
        metric_display_map = {item['display']: item for item in available_metrics}
        selected_metric_display = st.selectbox(
            "2. Chọn chỉ số để đo lường (trục Y):",
            options=metric_display_map.keys()
        )
        selected_metric_key = metric_display_map[selected_metric_display]
        
        # 3. Lọc và hiển thị Selectbox cho Aggregation
        allowed_aggregations = selected_metric_key['allowed_agg']
        selected_aggregation = st.selectbox(
            "3. Chọn phương thức tính:",
            options=allowed_aggregations
        )
        
        # --- Gửi request và hiển thị kết quả ---
        if st.button("Thực hiện phân tích"):
            request_body = {
                "dimension": selected_dimension['key'],
                "metric": selected_metric_key['key'],
                "agg": selected_aggregation
            }
            st.info(request_body)
            try:
                url = api_base.rstrip("/") + "/analytic_post"
                resp = requests.post(url, json=request_body, timeout=60)
                try:
                    data = resp.json()
                    st.info(f"Response JSON: {data}")
                except ValueError:
                    st.error(f"Invalid JSON response (status {resp.status_code})")
                    st.write(resp.text)
                else:
                    if resp.status_code == 200 or resp.status_code == 201:
                        if isinstance(data, list):
                            st.table(data)
                        else:
                            st.error("output không đúng định dạng")
                    else:
                        st.error(f"Request failed with status {resp.status_code}")
                        st.json(data)
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to API: {e}")

def Home():
    
    
    
    # KPI quan trọng nhất
    total_student = student_df["student_id"].count()
    total_course = course_df["course_id"].count()
    score_df["gpa"] = compute_gpa(score_df["coursework_grade"], score_df["midterm_grade"], score_df["final_grade"])
    avg_all = round(np.average(score_df["gpa"]), 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("Tổng số Sinh viên:", total_student)
    col2.metric("Tổng số Khóa học:", total_course)
    col3.metric("Điểm TB toàn trường:", avg_all)

    st.markdown("---")

    # Student by TOP GPA [BAR CHART]
    top_gpa = score_df.sort_values(by="gpa", ascending=False).head(3)
    table1 = pd.merge(department_df, student_df, on="department_id", suffixes=("_department", "_student"))
    table2 = pd.merge(table1, top_gpa, on= "student_id")
    top_3_students_by_gpa = table2[["student_id", "name_student", "name_department", "email", "birthday", "sex", "gpa"]]
    st.subheader("📊 Bảng Xếp Hạng Sinh Viên Toàn Trường")

    top1, top2, top3 = st.columns(3)
    student1 = top_3_students_by_gpa.iloc[0]
    student2 = top_3_students_by_gpa.iloc[1]
    student3 = top_3_students_by_gpa.iloc[2]

    # --- Component 1: Profile Sinh viên thứ nhất ---
    with top1:
        st.subheader(f"🥇 {student1['name_student']}")
        st.metric("Điểm GPA", f"{student1['gpa']:.2f}")
        
        with st.container(border=True):
            st.write(f"**🆔 Mã SV:** {student1['student_id']}")
            st.write(f"**🏫 Khoa:** {student1['name_department']}")
            st.write(f"**📧 Email:** {student1['email']}")
            st.write(f"**🎂 Sinh nhật:** {student1['birthday']}")

    # --- Component 2: Profile Sinh viên thứ hai ---
    with top2:
        st.subheader(f"🥈 {student2['name_student']}")
        st.metric("Điểm GPA", f"{student2['gpa']:.2f}")

        with st.container(border=True):
            st.write(f"**🆔 Mã SV:** {student2['student_id']}")
            st.write(f"**🏫 Khoa:** {student2['name_department']}")
            st.write(f"**📧 Email:** {student2['email']}")
            st.write(f"**🎂 Sinh nhật:** {student2['birthday']}")

    # --- Component 3: Profile Sinh viên thứ ba ---
    with top3:
        st.subheader(f"🥉 {student3['name_student']}")
        st.metric("Điểm GPA", f"{student3['gpa']:.2f}")
        
        with st.container(border=True):
            st.write(f"**🆔 Mã SV:** {student3['student_id']}")
            st.write(f"**🏫 Khoa:** {student3['name_department']}")
            st.write(f"**📧 Email:** {student3['email']}")
            st.write(f"**🎂 Sinh nhật:** {student3['birthday']}")


    st.markdown("---")

    # Hàng 2: Các biểu đồ chính
    st.header(" Phân tích và xu hướng")
    chart1, chart2 = st.columns(2)
    with chart1:
        st.markdown("#### Số sinh viên theo ngành")
        student_by_department = pd.merge(student_df, department_df, on="department_id", suffixes=('_student','_department'))
        total_student_by_department = student_by_department.groupby("name_department").agg({"student_id":"count"})
        st.bar_chart(total_student_by_department)

    with chart2:
        st.markdown("#### Điểm trung bình theo khóa học")
        student_by_department = pd.merge(student_df, department_df, on="department_id", suffixes=('_student','_department'))
        department_by_score = pd.merge(student_by_department, score_df, on="student_id")
        department_by_gpa = department_by_score.groupby('name_department').agg({"gpa": 'mean'})
        st.bar_chart(department_by_gpa)
        
    st.markdown("---")

if __name__ == "__main__":
    Search() 
