from fastapi import APIRouter, HTTPException
from models.courses import Courses

router = APIRouter(prefix= "/courses",
                   tags= ["courses"],
                   responses= {404: {"message" : "No encontrado"}}
                   )

list_courses = []

def search_id(id: int):
    for course in list_courses:
        if course.id == id:
            return course
    return None

@router.get("/")
async def get_courses():
    if not list_courses:
        raise HTTPException(status_code= 404, detail= "LISTA NO ENCONTRADA")
    return list_courses

@router.get("/{id}")
async def get_course(id: int):
    if search_id(id) is None:
        raise HTTPException(status_code= 404, detail= "CURSO NO ENCONTRADO")
    return search_id(id)

@router.post("/")
async def post_courses(course :Courses):
    if search_id(course.id):
        raise HTTPException(status_code=409, detail="EL ID YA EXISTE")
    if len(course.name)< 4 :
        raise HTTPException(status_code= 409, detail= "EL NOMBRE DEL CURSO ES MUY CHICO")
    if not (1 <= course.credits <= 6):
        raise HTTPException(status_code=409, detail="CREDITO DEBE ESTAR ENTRE 1 Y 6")
    list_courses.append(course)
    return course

@router.put("/{id}")
async def put_courses(id: int, course :Courses):
    if len(course.name)< 4 :
        raise HTTPException(status_code= 409, detail= "EL NOMBRE DEL CURSO ES MUY CHICO")
    if not (1 <= course.credits <= 6):
        raise HTTPException(status_code=409, detail="CREDITO DEBE ESTAR ENTRE 1 Y 6")
    if course.id != id:
        raise HTTPException(status_code=400, detail="NO PUEDES CAMBIAR EL ID DEL CURSO")

    for index, value in enumerate(list_courses):
        if value.id == id:
            list_courses[index] = course
            return {"message" : "Course updated"}
    raise HTTPException(status_code= 404, detail= "NO SE PUDO ACTUALIZAR EL CURSO")

@router.delete("/{id}")
async def delete_courses(id: int):
    for index, value in enumerate(list_courses):
        if value.id == id:
            del list_courses[index]
            return {"message" : "Course deleted"}
    raise HTTPException(status_code= 404, detail= "NO SE PUDO ELIMINAR EL CURSO")
    