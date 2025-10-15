def compute_gpa(coursework: float, midterm: float, final: float) -> float:
    """
    Tính điểm GPA theo công thức: 20% coursework, 30% midterm, 50% final.
    """
    return round(0.2 * coursework + 0.3 * midterm + 0.5 * final, 2)