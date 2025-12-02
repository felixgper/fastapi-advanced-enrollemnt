from pydantic import BaseModel

class Courses(BaseModel):
    id: int
    name: str
    credits: int
    active: bool