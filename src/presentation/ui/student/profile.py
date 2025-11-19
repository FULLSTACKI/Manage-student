import streamlit as st
from src.config import API_BASE
from src.presentation.ui.utils import authenticated_request
import requests

def get_student_profile(student_id: str):
    try:
        url = API_BASE.rstrip("/") + f"/students?student_id={student_id}"
        resp = authenticated_request("GET", url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")

def render_student_profile(student_id: str):
    """Hiển thị thông tin sinh viên dưới dạng hồ sơ (Profile Card)."""
    data = get_student_profile(student_id)
    student = data.get("student") if data else None
    if not student:
        st.warning("Không có thông tin sinh viên để hiển thị.")
        return
    
    st.set_page_config(page_title="Student Profile", page_icon=":school:", layout="wide")
    with st.container():
        st.title("👨‍🎓 Profile")
        st.markdown("---")
    # --- Bắt đầu Container chứa Profile ---
    with st.container(border=True):
        # === PHẦN HEADER: Tên và thông tin định danh chính ===
        col_avatar, col_info = st.columns([1, 5])
        with col_avatar:
            # Hiển thị avatar giả lập dựa trên giới tính
            if student.get("sex") == "Nam":
                st.markdown("# 👨‍🎓")
            elif student.get("sex") == "Nữ":
                st.markdown("# 👩‍🎓")
            else:
                st.markdown("# 🧑‍🎓")
        
        with col_info:
            st.markdown(f"### {student.get('student_name')}")
            st.caption(f"🆔 **ID:** `{student.get('student_id')}`  |  🏢 **Khoa:** {student.get('departments')}")

        st.divider()

        # === PHẦN 1: THÔNG TIN CÁ NHÂN CƠ BẢN ===
        st.markdown("#### 👤 Thông tin cá nhân")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"**🎂 Ngày sinh:** \n{student.get('birthday')}")
        with c2:
             st.markdown(f"**🔞 Tuổi:** \n{student.get('age')}")
        with c3:
            st.markdown(f"**🚻 Giới tính:** \n{student.get('sex')}")
        with c4:
             st.markdown(f"**👥 Dân tộc:** \n{student.get('ethnicity')}")

        c5, c6 = st.columns([1, 3]) # Cột birthplace và religion
        with c5:
             st.markdown(f"**🛐 Tôn giáo:** \n{student.get('religion')}")
        with c6:
             st.markdown(f"**🌍 Nơi sinh:** \n{student.get('birthplace')}")

        # === PHẦN 2: THÔNG TIN LIÊN HỆ ===
        st.write("") # Tạo khoảng trống nhỏ
        st.markdown("#### 📞 Thông tin liên hệ")
        c_contact1, c_contact2 = st.columns(2)
        with c_contact1:
            st.markdown(f"📧 **Email:** {student.get('email')}")
        with c_contact2:
            st.markdown(f"📱 **SĐT:** {student.get('phone')}")
        
        st.markdown(f"🏠 **Địa chỉ:** {student.get('address')}")

        # === PHẦN 3: THÔNG TIN PHÁP LÝ (CCCD) ===
        st.write("")
        with st.expander("💳 Xem thông tin CCCD/CMND"):
            ec1, ec2, ec3 = st.columns([2, 1, 2])
            with ec1:
                 st.markdown(f"**Số CCCD:** \n`{student.get('id_card')}`")
            with ec2:
                 st.markdown(f"**Ngày cấp:** \n{student.get('issue_date')}")
            with ec3:
                 st.markdown(f"**Nơi cấp:** \n{student.get('issue_place')}")

        # === PHẦN 4: HỌC VỤ (Tùy chọn hiển thị) ===
        # Nếu danh sách khóa học quá dài, nên để trong expander
        courses = student.get('courses', None)
        if courses and courses != "---":
            st.write("")
            st.markdown("#### 📚 Khóa học đã đăng ký")
            st.info(courses)