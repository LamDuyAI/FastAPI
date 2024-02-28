from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, models, schemas, security
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from passlib.context import CryptContext
from jose import JWTError, jwt

models.Base.metadata.create_all(bind=engine)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user-create/", tags=["Login"])
async def create_user(user: schemas.UserInDB, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/token", tags=["Login"])
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
) -> schemas.Token:
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@app.post("/teachers/", response_model=schemas.TeacherBase, status_code=status.HTTP_201_CREATED, tags=["Teacher"])
async def create_teacher(current_user: Annotated[models.User, Depends(security.get_current_active_user)],
                         teacher: schemas.TeacherBase,
                         db: Session = Depends(get_db)):
    # db_teacher = crud.create_teacher(db, teacher)
    # if db_teacher:
    # raise HTTPException(status_code= 400, detail= "Teacher have been registered!!!")
    return crud.create_teacher(db=db, teacher=teacher)


@app.get("/teacher/{teacher_id}", tags=["Teacher"])
async def read_teacher(current_user: Annotated[models.User, Depends(security.get_current_active_user)], skip: int = 0,
                       limit: int = 100, db: Session = Depends(get_db)):
    teachers = crud.get_teacher(db, skip=skip, limit=limit)
    return teachers


@app.get("/teachers/{teacher_id}", response_model=schemas.Teacher, tags=["Teacher"])
async def read_teacher(current_user: Annotated[models.User, Depends(security.get_current_active_user)], teacher_id: int,
                       db: Session = Depends(get_db)):
    db_teacher = crud.get_teacher(db, teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found!!!")
    return db_teacher


@app.get("/teachers/lens_name_teachers/{teacher_id}", tags=["Teacher"])
async def return_lens_teacher_name(current_user: Annotated[models.User, Depends(security.get_current_active_user)],
                                   teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = crud.get_len_name(db, teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found!!!")
    return db_teacher


@app.delete("/teachers/{teacher_id}", tags=["Teacher"])
async def delete_teacher(current_user: Annotated[models.User, Depends(security.get_current_active_user)],
                         teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = crud.get_teacher(db, teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found!!!")
    return crud.delete_teacher(db, teacher_id)


@app.put("/teachers/{teacher_id}", tags=["Teacher"])
async def update_teacher(current_user: Annotated[models.User, Depends(security.get_current_active_user)],
                         body: schemas.TeacherBase, teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = crud.get_teacher(db, teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found!!!")
    return crud.update_teacher(db, teacher_id, body)


@app.post("/students", response_model=schemas.Student, tags=["Student"])
async def create_student_for_teacher(
        current_user: Annotated[models.User, Depends(security.get_current_active_user)],
        student: schemas.Student_Base_Teacher,
        db: Session = Depends(get_db)
):
    return crud.create_teacher_teach_student(db=db, student=student)


@app.get("/students/", response_model=list[schemas.Student], tags=["Student"])
async def read_students(current_user: Annotated[models.User, Depends(security.get_current_active_user)], skip: int = 0,
                        limit: int = 100, db: Session = Depends(get_db)):
    student = crud.get_student(db, skip=skip, limit=limit)
    return student


@app.get("/student/{student_id}/SumPoint_of_student", tags=["Student"])
async def return_SumPoint_of_Student(current_user: Annotated[models.User, Depends(security.get_current_active_user)],
                                     student_id: int, db: Session = Depends(get_db)):
    SumPoint_of_student = crud.get_student_point(db, student_id)
    if SumPoint_of_student is None:
        raise HTTPException(status_code=404, detail="Student not found!!!")
    return SumPoint_of_student
