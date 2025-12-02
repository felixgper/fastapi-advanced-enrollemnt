from pydantic import BaseModel

class Enrollments(BaseModel):
    enrollment_id: int
    student_id: int
    course_id: int
    date: str