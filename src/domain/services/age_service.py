from datetime import date

def compute_age(birthdate: date) -> int:
    if not birthdate:
        return None
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age