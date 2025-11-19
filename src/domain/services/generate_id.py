import shortuuid

def generate_student_code() -> str:
    random_part = shortuuid.uuid()[:8].upper()
    return f"SGU-{random_part}"

def generate_teacher_code() -> str:
    random_part = shortuuid.uuid()[:8].upper()
    return f"TEACHER-{random_part}"

def generate_department_code() -> str:
    random_part = shortuuid.uuid()[:8].upper()
    return f"D-{random_part}"

def generate_course_code() -> str:
    random_part = shortuuid.uuid()[:8].upper()
    return f"C-{random_part}"

def generate_classroom_code() -> str:
    random_part = shortuuid.uuid()[:8].upper()
    return f"CLASS-{random_part}"