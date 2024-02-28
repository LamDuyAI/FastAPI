from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str
    class Config:
        orm_mode = True



class StudentCreate(BaseModel):
    name: str
    age: int
    maths: float
    physic: float
    chemistry: float

class Student(StudentCreate):
    id: int
    teacher_id: int
    class Config:
        orm_mode = True
class Student_Base_Teacher(StudentCreate):
    teacher_id: int
class TeacherBase(BaseModel):
    name: str
    age: int


class Teacher(TeacherBase):
    id: int
    students: list[Student] = []
    class Config:
        orm_mode = True




