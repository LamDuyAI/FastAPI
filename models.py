from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer,  primary_key= True)
    username = Column(String)
    password = Column(String)

class Teacher(Base):
    __tablename__ = "teachers"
    # Information
    id = Column(Integer, primary_key= True)
    name = Column(String(50), index=True)
    age = Column(Integer, index=True)
    students = relationship("Student", back_populates="owner")


class Student(Base):
    __tablename__ = "students"
    # Information
    id = Column(Integer, primary_key= True)
    name = Column(String(50), unique=True, index=True)
    age = Column(Integer)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    owner = relationship("Teacher", back_populates="students")

    # Subject - Point
    maths = Column(Float)
    physic = Column(Float)
    chemistry = Column(Float)

