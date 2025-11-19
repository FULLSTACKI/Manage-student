# 🎓 Hệ thống Quản lý & Phân tích Sinh viên (Student Management & Analytics System)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-green.svg)
![Architecture](https://img.shields.io/badge/Architecture-DDD%2FClean-orange.svg)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-purple.svg)

## 📖 Giới thiệu
Đây là dự án backend quản lý sinh viên được xây dựng dựa trên kiến trúc **Domain-Driven Design (DDD)** và **Clean Architecture**.

Hệ thống không chỉ dừng lại ở việc quản lý thông tin (CRUD) mà còn tích hợp quy trình **Tự động hóa Báo cáo (Automated Reporting Workflow)**. Hệ thống có khả năng tự động vẽ biểu đồ, phân tích dữ liệu và sinh ra nhận xét (insight) bằng trí tuệ nhân tạo (Google Gemini), tất cả được xử lý song song để tối ưu hiệu năng.

## 🚀 Công nghệ sử dụng

* **Core:** Python 3.10+
* **Framework:** FastAPI (Asynchronous Web Framework)
* **Data Analysis:** Pandas, Numpy
* **Visualization:** Seaborn, Matplotlib (xử lý đa luồng tránh blocking)
* **AI Integration:** Google Gemini API (Generative AI)
* **Architecture:** Layered Architecture (UI -> Controller -> Schema -> Application -> Infrastructure)

## ✨ Tính năng nổi bật

### 1. Quản lý Sinh viên (Core Domain)
* Tạo mới sinh viên với validation chặt chẽ (kiểm tra tuổi >= 18).
* Tìm kiếm, cập nhật và xóa thông tin sinh viên.
* Kiểm tra logic nghiệp vụ tại Domain Layer.

### 2. Báo cáo & Phân tích Tự động (Advanced)
Quy trình tạo báo cáo được điều phối tự động (Orchestration):
* **Query:** Tự động phát hiện bảng và truy vấn dữ liệu theo cột động.
* **Visualization:** Vẽ biểu đồ (Bar, Line, Pie...) dựa trên dữ liệu truy vấn.
* **AI Insight:** Sử dụng Google Gemini để đọc dữ liệu và đưa ra nhận xét, dự báo xu hướng.
* **Performance:** Tác vụ Vẽ biểu đồ và AI Insight chạy **song song (Async Parallel)** giúp giảm 50% thời gian chờ.
* **Export:** Xuất kết quả ra các định dạng file (Excel, PDF, CSV...) kèm biểu đồ và nhận xét.

## 🛠️ Cấu trúc Dự án (DDD)

```
doAnCuoiKhoa
├─ .$Bpmn.drawio.bkp
├─ .bat
├─ Bpmn.drawio
├─ requirements.txt
├─ src
│  ├─ application
│  │  ├─ auth
│  │  │  ├─ auth_service.py
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  │     ├─ auth_service.cpython-313.pyc
│  │  │     └─ __init__.cpython-313.pyc
│  │  ├─ dtos
│  │  │  ├─ account_dto.py
│  │  │  ├─ analytic_view_dto.py
│  │  │  ├─ course_dto.py
│  │  │  ├─ department_dto.py
│  │  │  ├─ export_dto.py
│  │  │  ├─ overview_dto.py
│  │  │  ├─ plot_chart_dto.py
│  │  │  ├─ score_dto.py
│  │  │  ├─ student_command_dto.py
│  │  │  ├─ student_history_dto.py
│  │  │  ├─ student_query_dto.py
│  │  │  ├─ token_dto.py
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  │     ├─ account_dto.cpython-313.pyc
│  │  │     ├─ analytic_view_dto.cpython-313.pyc
│  │  │     ├─ course_dto.cpython-313.pyc
│  │  │     ├─ department_dto.cpython-313.pyc
│  │  │     ├─ export_dto.cpython-313.pyc
│  │  │     ├─ overview_dto.cpython-313.pyc
│  │  │     ├─ plot_chart_dto.cpython-313.pyc
│  │  │     ├─ score_dto.cpython-313.pyc
│  │  │     ├─ student_command_dto.cpython-313.pyc
│  │  │     ├─ student_dto.cpython-313.pyc
│  │  │     ├─ student_history_dto.cpython-313.pyc
│  │  │     ├─ student_query_dto.cpython-313.pyc
│  │  │     ├─ token_dto.cpython-313.pyc
│  │  │     └─ __init__.cpython-313.pyc
│  │  ├─ mappers
│  │  └─ services
│  │     ├─ account.py
│  │     ├─ analytic.py
│  │     ├─ course.py
│  │     ├─ department.py
│  │     ├─ overview.py
│  │     ├─ score.py
│  │     ├─ student_command.py
│  │     ├─ student_history.py
│  │     ├─ student_import_file.py
│  │     ├─ student_query.py
│  │     ├─ __init__.py
│  │     └─ __pycache__
│  │        ├─ account.cpython-313.pyc
│  │        ├─ analytic.cpython-313.pyc
│  │        ├─ course.cpython-313.pyc
│  │        ├─ department.cpython-313.pyc
│  │        ├─ overview.cpython-313.pyc
│  │        ├─ score.cpython-313.pyc
│  │        ├─ student.cpython-313.pyc
│  │        ├─ student_command.cpython-313.pyc
│  │        ├─ student_history.cpython-313.pyc
│  │        ├─ student_import_file.cpython-313.pyc
│  │        ├─ student_query.cpython-313.pyc
│  │        └─ __init__.cpython-313.pyc
│  ├─ config
│  │  ├─ paths.py
│  │  ├─ pattern_config.py
│  │  ├─ settings.py
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  │     ├─ api_base.cpython-313.pyc
│  │     ├─ paths.cpython-313.pyc
│  │     ├─ pattern_config.cpython-313.pyc
│  │     ├─ settings.cpython-313.pyc
│  │     └─ __init__.cpython-313.pyc
│  ├─ data
│  │  ├─ backups
│  │  │  ├─ student_score_2025-11-19_16-22-28.db
│  │  │  ├─ student_score_2025-11-19_16-22-38.db
│  │  │  ├─ student_score_2025-11-19_16-22-41.db
│  │  │  ├─ student_score_2025-11-19_16-22-48.db
│  │  │  ├─ student_score_2025-11-19_16-24-18.db
│  │  │  ├─ student_score_2025-11-19_16-24-28.db
│  │  │  ├─ student_score_2025-11-19_16-24-38.db
│  │  │  ├─ student_score_2025-11-19_16-24-46.db
│  │  │  ├─ student_score_2025-11-19_16-25-32.db
│  │  │  └─ student_score_2025-11-19_16-25-40.db
│  │  ├─ backups_data.py
│  │  ├─ charts
│  │  │  ├─ Line Chart_department_by_gpa_at_2025-11-19.png
│  │  │  └─ Pie Chart_department_by_student_at_2025-11-19.png
│  │  ├─ clean_backup.py
│  │  ├─ insight_history.json
│  │  ├─ seed
│  │  │  ├─ account.csv
│  │  │  ├─ classrooms.csv
│  │  │  ├─ courses.csv
│  │  │  ├─ departments.csv
│  │  │  ├─ registrations.csv
│  │  │  ├─ scores.csv
│  │  │  ├─ students.csv
│  │  │  └─ teachers.csv
│  │  ├─ seed_data.py
│  │  └─ __pycache__
│  │     ├─ backups_data.cpython-313.pyc
│  │     ├─ clean_backup.cpython-313.pyc
│  │     ├─ seed_data.cpython-313.pyc
│  │     └─ __init__.cpython-313.pyc
│  ├─ domain
│  │  ├─ entities
│  │  │  ├─ account.py
│  │  │  ├─ classroom.py
│  │  │  ├─ course.py
│  │  │  ├─ cover_letter.py
│  │  │  ├─ department.py
│  │  │  ├─ registration.py
│  │  │  ├─ score.py
│  │  │  ├─ student.py
│  │  │  ├─ teacher.py
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  │     ├─ account.cpython-313.pyc
│  │  │     ├─ classroom.cpython-313.pyc
│  │  │     ├─ course.cpython-313.pyc
│  │  │     ├─ cover_letter.cpython-313.pyc
│  │  │     ├─ department.cpython-313.pyc
│  │  │     ├─ dtos.cpython-313.pyc
│  │  │     ├─ registration.cpython-313.pyc
│  │  │     ├─ score.cpython-313.pyc
│  │  │     ├─ student.cpython-313.pyc
│  │  │     ├─ teacher.cpython-313.pyc
│  │  │     └─ __init__.cpython-313.pyc
│  │  ├─ repositories
│  │  │  ├─ account_repo.py
│  │  │  ├─ analytic_repo.py
│  │  │  ├─ classroom_repo.py
│  │  │  ├─ course_repo.py
│  │  │  ├─ department_repo.py
│  │  │  ├─ export_file.py
│  │  │  ├─ gemini_repo.py
│  │  │  ├─ overview_repo.py
│  │  │  ├─ plot_chart_repo.py
│  │  │  ├─ registration_repo.py
│  │  │  ├─ score_repo.py
│  │  │  ├─ student_command_repo.py
│  │  │  ├─ student_history_repo.py
│  │  │  ├─ student_query_repo.py
│  │  │  ├─ teacher_repo.py
│  │  │  ├─ token_repo.py
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  │     ├─ account_repo.cpython-313.pyc
│  │  │     ├─ analytic_repo.cpython-313.pyc
│  │  │     ├─ course_repo.cpython-313.pyc
│  │  │     ├─ department_repo.cpython-313.pyc
│  │  │     ├─ export_file.cpython-313.pyc
│  │  │     ├─ gemini_repo.cpython-313.pyc
│  │  │     ├─ overview_repo.cpython-313.pyc
│  │  │     ├─ plot_chart_repo.cpython-313.pyc
│  │  │     ├─ registration_repo.cpython-313.pyc
│  │  │     ├─ score_repo.cpython-313.pyc
│  │  │     ├─ student_command_repo.cpython-313.pyc
│  │  │     ├─ student_history_repo.cpython-313.pyc
│  │  │     ├─ student_query_repo.cpython-313.pyc
│  │  │     ├─ student_repo.cpython-313.pyc
│  │  │     ├─ token_repo.cpython-313.pyc
│  │  │     └─ __init__.cpython-313.pyc
│  │  └─ services
│  │     ├─ age_service.py
│  │     ├─ compare_date_service.py
│  │     ├─ end_course.py
│  │     ├─ generate_id.py
│  │     ├─ gpa_service.py
│  │     ├─ hash.py
│  │     ├─ __init__.py
│  │     └─ __pycache__
│  │        ├─ age_service.cpython-313.pyc
│  │        ├─ compare_date_service.cpython-313.pyc
│  │        ├─ end_course.cpython-313.pyc
│  │        ├─ generate_id.cpython-313.pyc
│  │        ├─ gpa_service.cpython-313.pyc
│  │        ├─ hash.cpython-313.pyc
│  │        └─ __init__.cpython-313.pyc
│  ├─ infrastructure
│  │  └─ persistence
│  │     ├─ agent
│  │     │  ├─ gemini_insight.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ gemini_insight.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     ├─ auto
│  │     │  ├─ audit_mixin.py
│  │     │  ├─ build_query.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ audit_mixin.cpython-313.pyc
│  │     │     ├─ build_query.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     ├─ db.py
│  │     ├─ events
│  │     │  ├─ student_event.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ student_event.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     ├─ export
│  │     │  ├─ docx.py
│  │     │  ├─ excel.py
│  │     │  ├─ pdf.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ docx.cpython-313.pyc
│  │     │     ├─ excel.cpython-313.pyc
│  │     │     ├─ pdf.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     ├─ mappers
│  │     │  ├─ analytic_mapper.py
│  │     │  ├─ chart_mapper.py
│  │     │  ├─ course_mapper.py
│  │     │  ├─ department_mapper.py
│  │     │  ├─ registration_mapper.py
│  │     │  ├─ score_mapper.py
│  │     │  ├─ student_history_mapper.py
│  │     │  ├─ student_mapper.py
│  │     │  ├─ student_query_mapper.py
│  │     │  ├─ token_mapper.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ analytic_mapper.cpython-313.pyc
│  │     │     ├─ chart_mapper.cpython-313.pyc
│  │     │     ├─ course_mapper.cpython-313.pyc
│  │     │     ├─ department_mapper.cpython-313.pyc
│  │     │     ├─ registration_mapper.cpython-313.pyc
│  │     │     ├─ score_mapper.cpython-313.pyc
│  │     │     ├─ student_history_mapper.cpython-313.pyc
│  │     │     ├─ student_mapper.cpython-313.pyc
│  │     │     ├─ student_query_mapper.cpython-313.pyc
│  │     │     ├─ token_mapper.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     ├─ models
│  │     │  ├─ account_model.py
│  │     │  ├─ audit_model.py
│  │     │  ├─ classroom_model.py
│  │     │  ├─ course_model.py
│  │     │  ├─ department_model.py
│  │     │  ├─ registration_model.py
│  │     │  ├─ score_model.py
│  │     │  ├─ student_history_model.py
│  │     │  ├─ student_model.py
│  │     │  ├─ teacher_model.py
│  │     │  ├─ token_model.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ account_model.cpython-313.pyc
│  │     │     ├─ audit_model.cpython-313.pyc
│  │     │     ├─ classroom_model.cpython-313.pyc
│  │     │     ├─ course_model.cpython-313.pyc
│  │     │     ├─ department_model.cpython-313.pyc
│  │     │     ├─ registration_model.cpython-313.pyc
│  │     │     ├─ score_model.cpython-313.pyc
│  │     │     ├─ student_history_model.cpython-313.pyc
│  │     │     ├─ student_model.cpython-313.pyc
│  │     │     ├─ teacher_model.cpython-313.pyc
│  │     │     ├─ token_model.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     ├─ repositories
│  │     │  ├─ account_repo.py
│  │     │  ├─ analytic_repo.py
│  │     │  ├─ course_repo.py
│  │     │  ├─ department_repo.py
│  │     │  ├─ overview_repo.py
│  │     │  ├─ registration_repo.py
│  │     │  ├─ score_repo.py
│  │     │  ├─ student_command_repo.py
│  │     │  ├─ student_history_repo.py
│  │     │  ├─ student_query_repo.py
│  │     │  ├─ token_repo.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ account_repo.cpython-313.pyc
│  │     │     ├─ analytic_repo.cpython-313.pyc
│  │     │     ├─ course_repo.cpython-313.pyc
│  │     │     ├─ department_repo.cpython-313.pyc
│  │     │     ├─ overview_repo.cpython-313.pyc
│  │     │     ├─ registration_repo.cpython-313.pyc
│  │     │     ├─ score_repo.cpython-313.pyc
│  │     │     ├─ student_command_repo.cpython-313.pyc
│  │     │     ├─ student_history_repo.cpython-313.pyc
│  │     │     ├─ student_query_repo.cpython-313.pyc
│  │     │     ├─ student_repo.cpython-313.pyc
│  │     │     ├─ token_repo.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     ├─ visualization
│  │     │  ├─ seaborn_chart_service.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ seaborn_chart_service.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     └─ __pycache__
│  │        └─ db.cpython-313.pyc
│  ├─ presentation
│  │  ├─ api
│  │  │  ├─ dependencies.py
│  │  │  ├─ main.py
│  │  │  ├─ routers
│  │  │  │  ├─ analytics.py
│  │  │  │  ├─ auth.py
│  │  │  │  ├─ courses.py
│  │  │  │  ├─ overview.py
│  │  │  │  ├─ scores.py
│  │  │  │  ├─ student_command.py
│  │  │  │  ├─ student_history.py
│  │  │  │  ├─ student_import_file.py
│  │  │  │  ├─ student_query.py
│  │  │  │  ├─ view_config.py
│  │  │  │  ├─ __init__.py
│  │  │  │  └─ __pycache__
│  │  │  │     ├─ account.cpython-313.pyc
│  │  │  │     ├─ analytics.cpython-313.pyc
│  │  │  │     ├─ auth.cpython-313.pyc
│  │  │  │     ├─ courses.cpython-313.pyc
│  │  │  │     ├─ overview.cpython-313.pyc
│  │  │  │     ├─ plot_chart.cpython-313.pyc
│  │  │  │     ├─ scores.cpython-313.pyc
│  │  │  │     ├─ students.cpython-313.pyc
│  │  │  │     ├─ student_command.cpython-313.pyc
│  │  │  │     ├─ student_history.cpython-313.pyc
│  │  │  │     ├─ student_import_file.cpython-313.pyc
│  │  │  │     ├─ student_query.cpython-313.pyc
│  │  │  │     ├─ view_config.cpython-313.pyc
│  │  │  │     └─ __init__.cpython-313.pyc
│  │  │  └─ __pycache__
│  │  │     ├─ dependencies.cpython-313.pyc
│  │  │     └─ main.cpython-313.pyc
│  │  └─ ui
│  │     ├─ admin
│  │     │  ├─ dashboard.py
│  │     │  ├─ manage_course.py
│  │     │  ├─ manage_student.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ dashboard.cpython-313.pyc
│  │     │     ├─ Management.cpython-313.pyc
│  │     │     ├─ manage_course.cpython-313.pyc
│  │     │     ├─ manage_student.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     ├─ components
│  │     │  ├─ action.py
│  │     │  ├─ layout.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ action.cpython-313.pyc
│  │     │     ├─ layout.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     ├─ form
│  │     │  ├─ history
│  │     │  │  ├─ student.py
│  │     │  │  ├─ __init__.py
│  │     │  │  └─ __pycache__
│  │     │  │     ├─ student.cpython-313.pyc
│  │     │  │     └─ __init__.cpython-313.pyc
│  │     │  ├─ update
│  │     │  │  ├─ course.py
│  │     │  │  ├─ score.py
│  │     │  │  ├─ student.py
│  │     │  │  ├─ __init__.py
│  │     │  │  └─ __pycache__
│  │     │  │     ├─ course.cpython-313.pyc
│  │     │  │     ├─ score.cpython-313.pyc
│  │     │  │     ├─ student.cpython-313.pyc
│  │     │  │     └─ __init__.cpython-313.pyc
│  │     │  ├─ upload
│  │     │  │  ├─ course.py
│  │     │  │  ├─ score.py
│  │     │  │  ├─ student.py
│  │     │  │  ├─ __init__.py
│  │     │  │  └─ __pycache__
│  │     │  │     ├─ course.cpython-313.pyc
│  │     │  │     ├─ form_upload.cpython-313.pyc
│  │     │  │     ├─ score.cpython-313.pyc
│  │     │  │     ├─ student.cpython-313.pyc
│  │     │  │     └─ __init__.cpython-313.pyc
│  │     │  ├─ view
│  │     │  │  ├─ course.py
│  │     │  │  ├─ score.py
│  │     │  │  ├─ student.py
│  │     │  │  ├─ __init__.py
│  │     │  │  └─ __pycache__
│  │     │  │     ├─ course.cpython-313.pyc
│  │     │  │     ├─ form_view.cpython-313.pyc
│  │     │  │     ├─ score.cpython-313.pyc
│  │     │  │     ├─ student.cpython-313.pyc
│  │     │  │     └─ __init__.cpython-313.pyc
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ form_update.cpython-313.pyc
│  │     │     ├─ form_upload.cpython-313.pyc
│  │     │     ├─ form_view.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     ├─ Home.py
│  │     ├─ student
│  │     │  ├─ profile.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ profile.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     ├─ utils
│  │     │  ├─ api_helper.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ api_helper.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     └─ __pycache__
│  │        ├─ form_dashboard.cpython-313.pyc
│  │        ├─ form_upload.cpython-313.pyc
│  │        ├─ form_view.cpython-313.pyc
│  │        └─ __init__.cpython-313.pyc
│  └─ utils
│     ├─ error_handling.py
│     ├─ exceptions.py
│     ├─ patterns
│     │  ├─ analytic.json
│     │  ├─ content_type.json
│     │  ├─ detail_student.json
│     │  ├─ docx.json
│     │  ├─ error.json
│     │  └─ formats.json
│     ├─ validators.py
│     ├─ __init__.py
│     └─ __pycache__
│        ├─ error_handling.cpython-313.pyc
│        ├─ exceptions.cpython-313.pyc
│        ├─ validators.cpython-313.pyc
│        └─ __init__.cpython-313.pyc
└─ __pycache__
   └─ test.cpython-313.pyc

```