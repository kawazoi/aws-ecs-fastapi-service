from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ItemSchema(BaseModel):
    email: EmailStr = Field(...)
    field_1: str = Field(...)
    field_2: str = Field(...)
    field_3: int = Field(..., gt=0, lt=9)

    class Config:
        schema_extra = {
            "example": {
                "email": "abc@gmail.com",
                "field_1": "My field 1 text",
                "field_2": "My field 2 text",
                "field_3": 123,
            }
        }


# class UpdateStudentModel(BaseModel):
#     fullname: Optional[str]
#     email: Optional[EmailStr]
#     course_of_study: Optional[str]
#     year: Optional[int]
#     gpa: Optional[float]

#     class Config:
#         schema_extra = {
#             "example": {
#                 "fullname": "John Doe",
#                 "email": "jdoe@x.edu.ng",
#                 "course_of_study": "Water resources and environmental engineering",
#                 "year": 4,
#                 "gpa": "4.0",
#             }
#         }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
