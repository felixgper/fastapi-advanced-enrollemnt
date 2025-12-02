from fastapi import APIRouter, HTTPException
from models.students import Students

router = APIRouter(prefix= "/students",
                   tags= ["students"],
                   responses= {404: {"message" : "No encontrado"}}
                   )

list_students = []

def search_id(id: int):
    for student in list_students:
        if student.id == id:
            return student
    return None

@router.get("/")
async def get_students():
    if not list_students:
        raise HTTPException(status_code= 404, detail= "LISTA NO ENCONTRADA")
    return list_students

@router.get("/{id}")
async def get_students(id: int):
    if search_id(id) is None:
        raise HTTPException(status_code= 404, detail= "ESTUDIANTE NO ENCONTRADO")
    return search_id(id)

@router.post("/")
async def post_students(student :Students):
    if student.age < 16:
        raise HTTPException(status_code= 409, detail= "EL ESTUDIANTE DEBE SER MAYOR DE 16 AÑOS")
    if len(student.dni) != 8:
        raise HTTPException(status_code= 409, detail= "EL DNI DEBE TENER 8 DIGITOS")
    if len(student.name) < 3 :
        raise HTTPException(status_code= 409, detail= "EL NOMBRE DEL ESTUDIANTE ES MUY CORTO")
    list_students.append(student)
    return student

@router.put("/{id}")
async def put_students(id: int, student: Students):
    if student.age < 16:
        raise HTTPException(status_code= 409, detail= "EL ESTUDIANTE DEBE SER MAYOR DE 16 AÑOS")
    if len(student.dni) != 8:
        raise HTTPException(status_code= 409, detail= "EL DNI DEBE TENER 8 DIGITOS")
    if len(student.name) < 3 :
        raise HTTPException(status_code= 409, detail= "EL NOMBRE DEL ESTUDIANTE ES MUY CORTO")
    if student.id != id:
        raise HTTPException(status_code=400, detail="NO PUEDES CAMBIAR EL ID DEL ESTUDIANTE")
    for index, value in enumerate(list_students):
        if value.id == id:
            list_students[index] = student
            return {"message" : "Student updated"}
    raise HTTPException(status_code= 409, detail= "NO SE PUDO ACTUALIZAR EL ESTUDIANTE")

@router.delete("/{id}")
async def delete_students(id: int):
    for index, value in enumerate(list_students):
        if value.id == id:
            del list_students[index]
            return {"message" : "Student deleted"}
    raise HTTPException(status_code= 409, detail= "NO SE PUDO ELIMINAR EL ESTUDIANTE")
    