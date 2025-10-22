import streamlit as st
import httpx
import time
import asyncio
from src.presentation.ui import footer, api_base

async def get_analytic_view():
    try:
        url = api_base.rstrip("/") + "/analytics_view"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        st.error(f"Failed to connect to API: {e}")
        return None

async def get_overview():
    try:
        url = api_base.rstrip("/") + "/overview"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        st.error(f"Failed to connect to API: {e}")
        return None

async def _post_query(req: dict):
    try:
        url = api_base.rstrip("/") + "/analytic_post"
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=req, timeout=60)
            return resp.json()
    except httpx.RequestError as e:
        st.error(f"Failed to connect to API: {e}")
        
async def _load_all():
    return await asyncio.gather(
        get_analytic_view(),
        get_overview()
    )

@st.cache_data
def post_query(req: dict):
    return asyncio.run(_post_query(req))

@st.cache_data
def load_all_data():
    return asyncio.run(_load_all())


def Search(analytics_views):
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
            data = post_query(request_body)
            st.table(data)
            

def Home(data_kpi, data_top3_student):
    if data_kpi:
        # KPI quan trọng nhất
        total_student = data_kpi.get("total_student")
        total_course = data_kpi.get("total_course")
        avg_gpa = data_kpi.get("avg_gpa")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng số Sinh viên:", total_student)
        col2.metric("Tổng số Khóa học:", total_course)
        col3.metric("Điểm TB toàn trường:", avg_gpa)

        st.markdown("---")
    
    
    st.subheader("📊 Bảng Xếp Hạng Sinh Viên Toàn Trường")

    top1, top2, top3 = st.columns(3)
    student1 = data_top3_student[0]
    student2 = data_top3_student[1]
    student3 = data_top3_student[2]

    # --- Component 1: Profile Sinh viên thứ nhất ---
    with top1:
        with st.container(border=True, gap="medium"):
            st.subheader(f"🥇 {student1['student_name']}")
            st.metric("Điểm GPA", student1["gpa"])
            
            with st.container(border=True):
                st.write(f"**🆔 Mã SV:** {student1['student_id']}")
                st.write(f"**🏫 Khoa:** {student1['department_name']}")
                st.write(f"**🎂 Sinh nhật:** {student1['birthday']}")

    # --- Component 2: Profile Sinh viên thứ hai ---
    with top2:
        with st.container(border=True, gap="medium"):
            st.subheader(f"🥈 {student2['student_name']}")
            st.metric("Điểm GPA", student2["gpa"])

            with st.container(border=True):
                st.write(f"**🆔 Mã SV:** {student2['student_id']}")
                st.write(f"**🏫 Khoa:** {student2['department_name']}")
                st.write(f"**🎂 Sinh nhật:** {student2['birthday']}")

    # --- Component 3: Profile Sinh viên thứ ba ---
    with top3:
        with st.container(border=True, gap="medium"):
            st.subheader(f"🥉 {student3['student_name']}")
            st.metric("Điểm GPA", student3['gpa'])
            
            with st.container(border=True):
                st.write(f"**🆔 Mã SV:** {student3['student_id']}")
                st.write(f"**🏫 Khoa:** {student3['department_name']}")
                st.write(f"**🎂 Sinh nhật:** {student3['birthday']}")


    st.markdown("---")

    # # Hàng 2: Các biểu đồ chính
    # st.header(" Phân tích và xu hướng")
    # chart1, chart2 = st.columns(2)
    # with chart1:
    #     st.markdown("#### Số sinh viên theo ngành")
    #     student_by_department = pd.merge(student_df, department_df, on="department_id", suffixes=('_student','_department'))
    #     total_student_by_department = student_by_department.groupby("name_department").agg({"student_id":"count"})
    #     st.bar_chart(total_student_by_department)

    # with chart2:
    #     st.markdown("#### Điểm trung bình theo khóa học")
    #     student_by_department = pd.merge(student_df, department_df, on="department_id", suffixes=('_student','_department'))
    #     department_by_score = pd.merge(student_by_department, score_df, on="student_id")
    #     department_by_gpa = department_by_score.groupby('name_department').agg({"gpa": 'mean'})
    #     st.bar_chart(department_by_gpa)
        
    # st.markdown("---")



def dashboard_ui():
    st.set_page_config(
        page_title="Tổng quan",
        page_icon="🎓",
        layout="wide"
    )
    with st.container():
        st.title("📊 Dashboard Tổng quan")
        st.markdown("---")
    start = time.perf_counter()
    data_analytic, data_overview = load_all_data()
    data_kpi = data_overview.get("kpi")
    data_top3 = data_overview.get("top3_student")
    with st.expander("🔍 Mở rộng phân tích dữ liệu"):
        Search(data_analytic)
    st.markdown("---")
    Home(data_kpi,data_top3)
    end = time.perf_counter()
    st.text(f"Thời gian test: {end-start:.6f} giây")

    if st.button("Về Trang Chủ"):
        st.switch_page("Home.py")
        
    footer()

if __name__ == "__main__":
    dashboard_ui()
