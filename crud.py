from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from security import get_password_hash
import models, schemas


def create_user(db: Session, user: schemas.UserInDB):
    db_user = models.User(username=user.username, password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()


def get_teachers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Teacher).offset(skip).limit(limit).all()


def get_len_name(db: Session, teacher_id: int):
    name = db.query(models.Teacher.name).filter(models.Teacher.id == teacher_id).first()
    return len(name[0])


def create_teacher(db: Session, teacher: schemas.TeacherBase):
    db_teacher = models.Teacher(name=teacher.name, age=teacher.age)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def delete_teacher(db: Session, id: int):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id)
    if not teacher.first():
        raise HTTPException(status_code=404, detail="Not found teacher!!")
    teacher.delete(synchronize_session=False)
    db.commit()
    return "Deleted Successfull!!!"


def update_teacher(db: Session, id: int, body: schemas.TeacherBase):
    # Sử dụng `first` để lấy giá trị thực sự từ truy vấn
    teacher = db.query(models.Teacher).filter(models.Teacher.id == id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Not found teacher!!")
    # Cập nhật các trường trong teacher với các giá trị mới từ `body`
    for key, value in body.dict().items():
        setattr(teacher, key, value)
    db.commit()
    return "Updated Successfully!!!"


def get_student(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()


def create_teacher_teach_student(db: Session, student: schemas.Student_Base_Teacher):
    db_student = models.Student(name=student.name, age=student.age, teacher_id=student.teacher_id, maths=student.maths,
                                physic=student.maths, chemistry=student.chemistry)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_student_point(db: Session, id: int):
    math_point = db.query(models.Student.maths).filter(models.Student.id == id).first()[0]
    physic_point = db.query(models.Student.physic).filter(models.Student.id == id).first()[0]
    chemistry_point = db.query(models.Student.chemistry).filter(models.Student.id == id).first()[0]
    return math_point + chemistry_point + physic_point
