import streamlit as st 
import requests 
from src.presentation.ui.config import API_BASE
import json
from src.presentation.ui.utils import authenticated_request

def _get_history():
    try:
        url = API_BASE.rstrip("/") + "/students/history"
        response = authenticated_request("GET",url, timeout=10)
        if response.status_code == 404:
            return []
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return []

def history_student():
    st.session_state.history_list = _get_history()
    st.subheader("📜 Lịch sử Thay đổi Sinh viên")

    if not st.session_state.history_list:
        st.info("Chưa có lịch sử thay đổi cho sinh viên này.")
    else:
        for entry in st.session_state.history_list:
            with st.container(border=True):
                col1, col2 = st.columns([3, 2])
                with col1:
                    st.markdown(f"**👤 Người thực hiện:** `{entry.get("user_email") or 'N/A'}`")
                with col2:
                    st.caption(f"🗓️ {entry.get("change_at")}")

                st.markdown(f"**⚡ Hành động:** `{entry.get("action")}`")
                st.divider()

                # --- 2. "Diff" (So sánh) new_val và old_val ---
                st.markdown("**Thay đổi chi tiết:**")
                
                try:
                    # Dùng `or '{}'` để xử lý an toàn nếu value là None
                    old_data = json.loads(entry.get("old_val") or '{}')
                    new_data = json.loads(entry.get("new_val") or '{}')
                except json.JSONDecodeError:
                    st.error("Lỗi: Không thể đọc dữ liệu lịch sử (JSON hỏng).")
                    continue

                all_keys = set(old_data.keys()) | set(new_data.keys())
                
                if not all_keys:
                    st.caption("Không có thay đổi dữ liệu chi tiết được ghi lại.")
                else:
                    c1, c2, c3 = st.columns([1, 2, 2])
                    c1.markdown("**Trường**")
                    c2.markdown("**Giá trị cũ**")
                    c3.markdown("**Giá trị mới**")

                    for key in sorted(list(all_keys)):
                        old_val = old_data.get(key)
                        new_val = new_data.get(key)
                        
                        if old_val != new_val:
                            c1_diff, c2_diff, c3_diff = st.columns([1, 2, 2])
                            with c1_diff:
                                st.code(key, language="plaintext")
                            with c2_diff:
                                st.error(f"{old_val}")
                            with c3_diff:
                                st.success(f"{new_val}")
                
                # --- 3. Hiển thị "Toàn bộ thuộc tính" (snapshot) trong expander ---
                if entry.get("detail"):
                    with st.expander("Xem toàn bộ thông tin tại thời điểm này"):
                        student = entry.get("detail") # Đây là một object studentOut
                        
                        # Tái sử dụng layout "nén" từ trước
                        st.caption(f"**ID:** {student.get("student_id") or 'N/A'} | **Khoa:** {student.get("departments") or 'N/A'}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**🚻 Giới tính:** {student.get("sex") or 'N/A'}")
                            st.markdown(f"**🎂 Tuổi:** {student.get("age") or 'N/A'}")
                            st.markdown(f"**🗓️ Ngày sinh:** {student.get("birthday") or 'N/A'}")
                            st.markdown(f"**🌍 Nơi sinh:** {student.get("birthplace") or 'N/A'}")
                        with col2:
                            st.markdown(f"**👥 Dân tộc:** {student.get("ethnicity") or 'N/A'}")
                            st.markdown(f"**🧘 Tôn giáo:** {student.get("religion") or 'N/A'}")
                            st.markdown(f"**📱 Điện thoại:** {student.get("phone") or 'N/A'}")
                            st.markdown(f"**📧 Email:** {student.get("email") or 'N/A'}")

                        st.markdown(f"**🏠 Địa chỉ:** {student.get("address") or 'N/A'}")
                        
                        col3, col4 = st.columns(2)
                        with col3:
                            st.markdown(f"**💳 CCCD:** `{student.get("id_card") or 'N/A'}`")
                        with col4:
                            st.markdown(f"**Ngày cấp:** {student.get("issue_date") or 'N/A'}")
                        st.caption(f"**Nơi cấp:** {student.get("issue_place") or 'N/A'}")
