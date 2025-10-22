
```
Đồ án cuối khóa
├─ .bat
├─ notebooks
│  ├─ student_score.db
│  └─ test.ipynb
├─ src
│  ├─ .env
│  ├─ app.py
│  ├─ application
│  │  ├─ dtos
│  │  │  ├─ analytic_view_dto.py
│  │  │  ├─ course_dto.py
│  │  │  ├─ department_dto.py
│  │  │  ├─ overview_dto.py
│  │  │  ├─ score_dto.py
│  │  │  ├─ student_dto.py
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  │     ├─ analytic_view_dto.cpython-313.pyc
│  │  │     ├─ course_dto.cpython-313.pyc
│  │  │     ├─ department_dto.cpython-313.pyc
│  │  │     ├─ overview_dto.cpython-313.pyc
│  │  │     ├─ score_dto.cpython-313.pyc
│  │  │     ├─ student_dto.cpython-313.pyc
│  │  │     └─ __init__.cpython-313.pyc
│  │  └─ services
│  │     ├─ analytic.py
│  │     ├─ course.py
│  │     ├─ department.py
│  │     ├─ overview.py
│  │     ├─ score.py
│  │     ├─ student.py
│  │     ├─ __init__.py
│  │     └─ __pycache__
│  │        ├─ analytic.cpython-313.pyc
│  │        ├─ course.cpython-313.pyc
│  │        ├─ department.cpython-313.pyc
│  │        ├─ overview.cpython-313.pyc
│  │        ├─ score.cpython-313.pyc
│  │        ├─ student.cpython-313.pyc
│  │        └─ __init__.cpython-313.pyc
│  ├─ data
│  │  ├─ seed
│  │  │  ├─ courses.csv
│  │  │  ├─ departments.csv
│  │  │  ├─ registrations.csv
│  │  │  ├─ scores.csv
│  │  │  └─ students.csv
│  │  ├─ seed_data.py
│  │  └─ __pycache__
│  │     └─ seed_data.cpython-313.pyc
│  ├─ domain
│  │  ├─ entities
│  │  │  ├─ course.py
│  │  │  ├─ department.py
│  │  │  ├─ dtos.py
│  │  │  ├─ registration.py
│  │  │  ├─ score.py
│  │  │  ├─ student.py
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  │     ├─ course.cpython-313.pyc
│  │  │     ├─ department.cpython-313.pyc
│  │  │     ├─ dtos.cpython-313.pyc
│  │  │     ├─ registration.cpython-313.pyc
│  │  │     ├─ score.cpython-313.pyc
│  │  │     ├─ student.cpython-313.pyc
│  │  │     └─ __init__.cpython-313.pyc
│  │  ├─ repositories
│  │  │  ├─ analytic_repo.py
│  │  │  ├─ course_repo.py
│  │  │  ├─ department_repo.py
│  │  │  ├─ overview_repo.py
│  │  │  ├─ registration_repo.py
│  │  │  ├─ score_repo.py
│  │  │  ├─ student_repo.py
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  │     ├─ analytic_repo.cpython-313.pyc
│  │  │     ├─ course_repo.cpython-313.pyc
│  │  │     ├─ department_repo.cpython-313.pyc
│  │  │     ├─ overview_repo.cpython-313.pyc
│  │  │     ├─ registration_repo.cpython-313.pyc
│  │  │     ├─ score_repo.cpython-313.pyc
│  │  │     ├─ student_repo.cpython-313.pyc
│  │  │     └─ __init__.cpython-313.pyc
│  │  └─ services
│  │     ├─ age_service.py
│  │     ├─ compare_date_service.py
│  │     ├─ end_course.py
│  │     ├─ gpa_service.py
│  │     ├─ __init__.py
│  │     └─ __pycache__
│  │        ├─ age_service.cpython-313.pyc
│  │        ├─ compare_date_service.cpython-313.pyc
│  │        ├─ end_course.cpython-313.pyc
│  │        ├─ gpa_service.cpython-313.pyc
│  │        └─ __init__.cpython-313.pyc
│  ├─ infrastructure
│  │  └─ persistence
│  │     ├─ db.py
│  │     ├─ models
│  │     │  ├─ course_model.py
│  │     │  ├─ department_model.py
│  │     │  ├─ registration_model.py
│  │     │  ├─ score_model.py
│  │     │  ├─ student_model.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ course_model.cpython-313.pyc
│  │     │     ├─ department_model.cpython-313.pyc
│  │     │     ├─ registration_model.cpython-313.pyc
│  │     │     ├─ score_model.cpython-313.pyc
│  │     │     ├─ student_model.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     ├─ repositories
│  │     │  ├─ analytic_repo.py
│  │     │  ├─ course_repo.py
│  │     │  ├─ department_repo.py
│  │     │  ├─ overview_repo.py
│  │     │  ├─ registration_repo.py
│  │     │  ├─ score_repo.py
│  │     │  ├─ student_repo.py
│  │     │  ├─ __init__.py
│  │     │  └─ __pycache__
│  │     │     ├─ analytic_repo.cpython-313.pyc
│  │     │     ├─ course_repo.cpython-313.pyc
│  │     │     ├─ department_repo.cpython-313.pyc
│  │     │     ├─ overview_repo.cpython-313.pyc
│  │     │     ├─ registration_repo.cpython-313.pyc
│  │     │     ├─ score_repo.cpython-313.pyc
│  │     │     ├─ student_repo.cpython-313.pyc
│  │     │     └─ __init__.cpython-313.pyc
│  │     └─ __pycache__
│  │        └─ db.cpython-313.pyc
│  ├─ presentation
│  │  ├─ api
│  │  │  ├─ dependencies.py
│  │  │  ├─ main.py
│  │  │  ├─ routers
│  │  │  │  ├─ analytics.py
│  │  │  │  ├─ courses.py
│  │  │  │  ├─ overview.py
│  │  │  │  ├─ scores.py
│  │  │  │  ├─ students.py
│  │  │  │  ├─ __init__.py
│  │  │  │  └─ __pycache__
│  │  │  │     ├─ analytics.cpython-313.pyc
│  │  │  │     ├─ courses.cpython-313.pyc
│  │  │  │     ├─ overview.cpython-313.pyc
│  │  │  │     ├─ scores.cpython-313.pyc
│  │  │  │     ├─ students.cpython-313.pyc
│  │  │  │     └─ __init__.cpython-313.pyc
│  │  │  └─ __pycache__
│  │  │     ├─ dependencies.cpython-313.pyc
│  │  │     └─ main.cpython-313.pyc
│  │  └─ ui
│  │     ├─ form_dashboard.py
│  │     ├─ form_upload.py
│  │     └─ form_view.py
│  ├─ pyproject.toml
│  └─ utils
│     ├─ error_handling.py
│     ├─ exceptions.py
│     ├─ patterns
│     │  ├─ analytic.json
│     │  ├─ error.json
│     │  └─ formats.json
│     ├─ validators.py
│     ├─ __init__.py
│     └─ __pycache__
│        ├─ error_handling.cpython-313.pyc
│        ├─ exceptions.cpython-313.pyc
│        ├─ validators.cpython-313.pyc
│        └─ __init__.cpython-313.pyc
└─ student_score.db

```