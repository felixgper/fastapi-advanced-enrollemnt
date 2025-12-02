from pydantic import BaseModel

class Students(BaseModel):
    id: int
    name: str
    age: int
    dni: str
    active: bool