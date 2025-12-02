from fastapi import APIRouter, HTTPException
from routers import students, courses
from routers.enrollments import list_enrollments

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    responses={404: {"message": "No encontrado"}}
)

@router.get("/student/{student_id}/courses")
async def report_student_courses(student_id: int):

    # Verificar si el estudiante existe
    student = next((s for s in students.list_students if s.id == student_id), None)
    if student is None:
        raise HTTPException(status_code=404, detail="ESTUDIANTE NO EXISTE")

    # Obtener todas las matrículas del estudiante
    student_enrollments = [
        enr for enr in list_enrollments if enr.student_id == student_id
    ]

    # Obtener los cursos donde está matriculado
    courses_info = []
    for enr in student_enrollments:
        course = next((c for c in courses.list_courses if c.id == enr.course_id), None)
        if course:
            courses_info.append(course)

    return {
        "student": student,
        "total_courses": len(courses_info),
        "courses": courses_info
    }


@router.get("/course/{course_id}/students")
async def report_course_students(course_id: int):

    # Verificar si el curso existe
    course = next((c for c in courses.list_courses if c.id == course_id), None)
    if course is None:
        raise HTTPException(status_code=404, detail="CURSO NO EXISTE")

    # Obtener matrículas del curso
    course_enrollments = [
        enr for enr in list_enrollments if enr.course_id == course_id
    ]

    # Obtener estudiantes matriculados
    students_info = []
    for enr in course_enrollments:
        student = next((s for s in students.list_students if s.id == enr.student_id), None)
        if student:
            students_info.append(student)

    return {
        "course": course,
        "total_students": len(students_info),
        "students": students_info
    }
