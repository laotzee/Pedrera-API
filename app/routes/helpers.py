def serialize_student(student):
    """Format student object to dict"""
    return {
        "id": student.id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "school_id": student.school_id
    }

def serialize_school(school, include_students=True):
    """Format school object to dict, optionally nesting students."""
    data = {
        "id": school.id,
        "name": school.name,
        "capacity": school.capacity,
        "student_count": len(school.students)
    }
    if include_students:
        data["students"] = [serialize_student(s) for s in school.students]
    return data
