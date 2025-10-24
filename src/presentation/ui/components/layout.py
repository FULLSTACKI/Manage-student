import streamlit as st
import requests
from src.presentation.ui import api_base

def footer():
    with st.container():
        st.markdown("---")
        st.markdown("© 2025 Student Management App. All rights reserved.")

def table_detail_student():
    # --- Load columns structure
    try:
        url = api_base.rstrip("/") + "/students/columns"
        resp = requests.get(url=url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"⚠️ Failed to fetch column config: {e}")
        return
    
    # st.subheader(view_config.get("display_name"))
    # columns = view_config.get("columns")
    
    # map_col = {
    #     col["label"]: col for col in columns
    # } 
    
    # selected = st.multiselect("Select columns to display:", map_col.keys(), default=map_col.keys()[:5])
    # selected_cols = map_col[selected]["key"]
    
    # if not selected_cols:
    #     st.warning("Please select at least one column to display.")
    #     return

    # # --- Get filter metadata dynamically
    # filter_params = {}
    # try:
    #     filters_resp = requests.get(
    #         f"{api_base}/students/filters",
    #         params={"columns": ",".join(selected_cols)}
    #     )
    #     filters_resp.raise_for_status()
    #     filters = filters_resp.json()

    #     if "departments" in filters:
    #         dept = st.selectbox(
    #             "🏫 Department",
    #             ["All"] + [d["name"] for d in filters["departments"]]
    #         )
    #         if dept != "All":
    #             filter_params["department_name"] = dept

    #     if "courses" in filters:
    #         course = st.selectbox(
    #             "📘 Course",
    #             ["All"] + [c["name"] for c in filters["courses"]]
    #         )
    #         if course != "All":
    #             filter_params["course_name"] = course

    # except Exception as e:
    #     st.warning(f"Could not load filters: {e}")

    # --- Fetch student data
    # try:
    #     resp = requests.get(
    #         f"{api_base}/student/list",
    #         params={"columns": ",".join(selected_cols), **filter_params}
    #     )
    #     resp.raise_for_status()
    #     data = resp.json()
    #     if not data:
    #         st.info("No students found.")
    #         return

    #     df = pd.DataFrame(data)
    #     st.dataframe(df, use_container_width=True)
    # except Exception as e:
    #     st.error(f"❌ Failed to load student data: {e}")
if __name__ == "__main__":
    data = table_detail_student()
    st.info(data)