from dataclasses import dataclass

# THEO TỪNG DEPARTMENT

@dataclass(frozen=True)
class DepartmentCourseCountDTO:
    department_name: str
    total_courses: int

@dataclass(frozen=True)
class DepartmentStudentSexCountDTO:
    department_name: str
    total_students_sex: int

@dataclass(frozen=True)
class DepartmentStudentCountDTO:
    department_name: str
    total_students: int
    
@dataclass(frozen=True)
class DepartmentCourseAvgGpaDTO:
    department_name: str
    avg_gpa: float
    
@dataclass(frozen=True)
class DepartmentCourseMaxGpaDTO:
    department_name: str
    max_gpa: float

@dataclass(frozen=True)
class DepartmentCourseMinGpaDTO:
    department_name: str
    min_gpa: float
    
@dataclass(frozen=True)
class DepartmentCourseAvgFinalGradeDTO:
    department_name: str
    avg_final_grade: float
    
@dataclass(frozen=True)
class DepartmentCourseMinFinalGradeDTO:
    department_name: str
    min_final_grade: float
    
@dataclass(frozen=True)
class DepartmentCourseMaxFinalGradeDTO:
    department_name: str
    max_final_grade: float

    