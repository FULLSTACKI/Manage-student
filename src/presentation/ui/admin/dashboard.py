import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from src.presentation.ui.components import footer
from src.presentation.ui.utils.api_helper import authenticated_request
from src.presentation.ui.config import API_BASE
from PIL import Image

# --- Khởi tạo session state ---
if "file_to_download" not in st.session_state:
    st.session_state.file_to_download = None
if "data_analytic" not in st.session_state:
    st.session_state.data_analytic = None
if "chart_path" not in st.session_state:
    st.session_state.chart_path = None
if "chart_name" not in st.session_state:
    st.session_state.chart_name = None
if "data_insight" not in st.session_state:
    st.session_state.data_insight = None

def get_analytic_view():
    try:
        url = API_BASE.rstrip("/") + "/overview/table_analytic"
        response = authenticated_request("GET",url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return None

def get_overview():
    try:
        url = API_BASE.rstrip("/") + "/overview"
        response = authenticated_request("GET",url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return None
    
@st.cache_data
def _post_query(req: dict):
    try:
        url = API_BASE.rstrip("/") + "/overview/analytic"
        resp = authenticated_request("POST",url, json=req, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return None

def _export(req: dict):
    with st.spinner(f"Đang tạo file {req.get("type")}, vui lòng chờ..."):
        try:
            url = API_BASE.rstrip("/") + "/overview/export"
            resp = authenticated_request("POST", url,json=req, timeout=30)
            resp.raise_for_status() # Ném lỗi nếu (4xx, 5xx)
            if "Content-Disposition" in resp.headers:
                disp = resp.headers['Content-Disposition']
                # Trích xuất filename="..."
                fn_part = [part for part in disp.split(';') if part.strip().startswith('filename=')]
                if fn_part:
                    filename = fn_part[0].split('=')[1].strip('"')
            # 3. Lưu nội dung (bytes) và tên file vào session state
            st.session_state.file_to_download = {
                "data": resp.content,
                "filename": filename,
                "mime": resp.headers.get('Content-Disposition')
            }
            st.success("Tạo file thành công! Nhấn nút 'Tải về' bên dưới.")
        except requests.exceptions.HTTPError as e:
            st.error(f"Lỗi API ({e.response.status_code}): {e.response.text}")
        except Exception as e:
            st.error(f"Lỗi: {e}")

def Search(analytics_views):
    if not analytics_views:
        st.error("Không thể tải cấu hình phân tích từ backend.")
    else:
        # Giả sử chúng ta chỉ làm việc với view đầu tiên
        view_config = analytics_views[0]
        
        # --- XÂY DỰNG CÁC SELECTBOX PHỤ THUỘC ---
        st.subheader(view_config.get("display_name"))
        
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
        # 4. Lọc và hiển thị chart type 
        allowed_chart_type = view_config["chart_type"]
        selected_chart_type = st.selectbox(
            "4. Chọn loại biểu đồ:",
            options=allowed_chart_type
        )
        #5. Hiện thị lựa chọn format export data 
        selected_export_type = st.selectbox(
            "5. Chọn loại file trích xuất",
            options=view_config.get("export_type")
        )
        if st.button("Tạo báo cáo"):
            st.session_state.file_to_download = None
            reports = {
                "dimension": selected_dimension["key"],
                "metric": selected_metric_key["key"],
                "agg": selected_aggregation,
                "chart_type": selected_chart_type,
                "type": selected_export_type
            }
            _export(reports)
            if st.session_state.file_to_download:
                file_info = st.session_state.file_to_download
                st.download_button(
                    label=f"📥 Tải về {file_info['filename']}",
                    data=file_info['data'],
                    file_name=file_info['filename'],
                    mime=file_info['mime']
                )

def Overview(data_kpi, data_top3_student):
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
    request_student_by_dept = {
        "dimension": "department",
        "metric": "student",
        "agg":  "count"
    }
    chart_student_by_dept = _post_query(request_student_by_dept)
    df_student_by_dept = pd.DataFrame(chart_student_by_dept)
    request_gpa_by_dept = {
        "dimension": "department",
        "metric": "gpa",
        "agg":  "avg"
    }
    chart_gpa_by_dept = _post_query(request_gpa_by_dept)
    df_gpa_by_dept = pd.DataFrame(chart_gpa_by_dept)
    # Hàng 2: Các biểu đồ chính
    st.header("📊 Phân tích và xu hướng")
    
    with st.container(horizontal_alignment="center", border=True):
        st.markdown("#### Số sinh viên theo ngành")
        fig = px.bar(
            df_student_by_dept, 
            x="department", 
            y="student", 
            text="student", # 👈 Thêm nhãn dữ liệu lên cột
            color="department" # 👈 Tự động thêm màu
        )

        # Tùy chỉnh thêm
        fig.update_layout(xaxis_title="Tên Khoa", yaxis_title="Số học sinh")
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside') # Định dạng số

        # Hiển thị bằng Streamlit
        st.plotly_chart(fig, use_container_width=True)

    with st.container(horizontal_alignment="center", border=True):
        st.markdown("#### Điểm trung bình theo khóa học")
        fig = px.bar(
            df_gpa_by_dept, 
            x="department", 
            y="gpa", 
            text="gpa", # 👈 Thêm nhãn dữ liệu lên cột
            color="department" # 👈 Tự động thêm màu
        )

        # Tùy chỉnh thêm
        fig.update_layout(xaxis_title="Tên Khoa", yaxis_title="Điểm GPA")
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside') # Định dạng số

        # Hiển thị bằng Streamlit
        st.plotly_chart(fig, use_container_width=True)



def dashboard_ui():
    st.set_page_config(
        page_title="Tổng quan",
        page_icon="🎓",
        layout="wide"
    )
    with st.container():
        st.title("📊 Dashboard Tổng quan")
        st.markdown("---")

    data_analytic = get_analytic_view()
    data_overview = get_overview()
    data_kpi = data_overview.get("kpi")
    data_top3 = data_overview.get("top3_student")
    with st.expander("🔍 Mở rộng phân tích dữ liệu", expanded=True):
        Search(data_analytic)
    st.divider()
    Overview(data_kpi,data_top3)

    footer()

