from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Student(BaseModel):
    name: str
    age: Optional[int] = None
    email : EmailStr
    cgpa: float = Field(gt=0, le=4.0, default=3.5, description="cgpa out of 4.0")


new_student = {"name": "durv", "age": "20", "email": "durv@gmail.com"}

student = Student(**new_student)

# print(type(student))
# print(student)
student_dict = dict(student)

print(student_dict['age'])