from fastapi import FastAPI
from routers import students, courses, enrollments, reports

app = FastAPI(
    title="API de Clínica Educativa",
    description="Proyecto de práctica con routers, validaciones y relaciones",
    version="1.0.0"
)

# Registrar routers
app.include_router(students.router)
app.include_router(courses.router)
app.include_router(enrollments.router)
app.include_router(reports.router)

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API"}
