from fastapi import APIRouter, HTTPException
from models.courses import Courses
from models.students import Students
from routers import courses,students
from models.enrollments import Enrollments
from datetime import datetime

router = APIRouter(prefix= "/enrollments",
                   tags= ["enrollments"],
                   responses= {404: {"message" : "No encontrado"}}
                   )

list_enrollments = []

def search_id(enrollment_id: int):
    for enrr in list_enrollments:
        if enrr.enrollment_id == enrollment_id:
            return enrr
    return None

@router.get("/")
async def get_enrollments():
    if not list_enrollments:
        raise HTTPException(status_code= 404, detail= "LISTA NO ENCONTRADA")
    return list_enrollments

@router.get("/{enrollment_id}")
async def get_enrollments(enrollment_id: int):
    if search_id(enrollment_id) is None:
        raise HTTPException(status_code= 404, detail= "MATRÍCULA NO ENCONTRADA")
    return search_id(enrollment_id)

@router.post("/")
async def post_enrollments(enrollments: Enrollments):
    
    #Verificar si el estudiante existe
    student_exist = next((stud for stud in students.list_students if stud.id == enrollments.student_id), None)
    if student_exist is None:
        raise HTTPException(status_code= 404, detail= "ESTUDIANTE NO EXISTE")
    
    #Verificar si el curso existe
    course_exist = next((cours for cours in courses.list_courses if cours.id == enrollments.course_id), None)
    if course_exist is None:
        raise HTTPException(status_code= 404, detail = "CURSO NO EXISTE")
    
    #Verificar que ambos esten activos
    if not student_exist.active:
        raise HTTPException(status_code= 409, detail= "NO ESTA ACTIVO EL ESTUDIANTE")
    
    if not course_exist.active:
        raise HTTPException(status_code= 409, detail= "NO ESTA ACTIVO EL CURSO")
    
    #No permitir que un estudiante se matricule dos veces en el mismo curso
    duplicate = next(
    (enr for enr in list_enrollments
     if enr.student_id == enrollments.student_id and enr.course_id == enrollments.course_id),
    None
)

    if duplicate:
        raise HTTPException(status_code=409, detail="ESTUDIANTE YA MATRICULADO EN ESTE CURSO")
    
    # Validar formato de fecha YYYY-MM-DD
    try:
        datetime.strptime(enrollments.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="FORMATO DE FECHA INCORRECTO. USE YYYY-MM-DD")

    #Un estudiante no puede tener más de 5 matrículas activas
    
    active_enrollments = sum(
    1 for enr in list_enrollments
    if enr.student_id == enrollments.student_id
    )

    if active_enrollments >= 5:
        raise HTTPException(status_code=409, detail="EL ESTUDIANTE YA TIENE 5 MATRÍCULAS")
    
    #Registramos la cita
    list_enrollments.append(enrollments)
    
    return{
        "message": "Matrícula registrada",
        "student": student_exist,
        "course": course_exist,
        "enrollment": enrollments
    }

@router.delete("/{enrollment_id}")
async def delete_enrollments(enrollment_id: int):
    
    found = False
    
    for index, value in enumerate(list_enrollments):
        if value.enrollment_id == enrollment_id:
            del list_enrollments[index]
            found = True
            return {
                "message" : "MATRICULA ELIMINADA"
            }
    
    if not found:
        raise HTTPException(status_code= 404, detail= "MATRICULA NO ENCONTRADA")