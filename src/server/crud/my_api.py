import logging
from bson.objectid import ObjectId

import motor.motor_asyncio

from src.server.core.config import ConfigManager
from src.server.db.mongodb import AsyncIOMotorClient
from src.server.db.mongodb_utils import connect_to_mongo
from src.server.models.my_api import ItemSchema,


cfg = ConfigManager()
logging.basicConfig(level=logging.INFO, format=cfg.log["LOG_FORMAT"])


# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# database = client.students

# student_collection = database.get_collection("students_collection")


# def student_helper(student) -> dict:
#     return {
#         "id": str(student["_id"]),
#         "fullname": student["fullname"],
#         "email": student["email"],
#         "course_of_study": student["course_of_study"],
#         "year": student["year"],
#         "GPA": student["gpa"],
#     }


# # Retrieve all students present in the database
# async def retrieve_items(item_id: int) -> list:
#     students = []

#     logging.info("=" * 50)
#     logging.info(cfg.mongo["MONGODB_URL"])
#     logging.info("=" * 50)
#     # db.client
#     # database = conn.students
#     logging.info(conn)
#     logging.info("=" * 50)
#     # student_collection = database.get_collection("students_collection")
#     # async for student in student_collection.find():
#     #     students.append(student_helper(student))
#     return students


# # Add a new student into to the database
# async def add_student(student_data: dict) -> dict:
#     student = await student_collection.insert_one(student_data)
#     new_student = await student_collection.find_one({"_id": student.inserted_id})
#     return student_helper(new_student)


# Retrieve a student with a matching ID
async def retrieve_item(conn: AsyncIOMotorClient, id: str) -> ItemSchema:
    # row = await conn[cfg.mongo["DB_NAME"]]["item_collection"].find_one({"_id": ObjectId(id)})
    # row = await item_collection.find_one({"_id": ObjectId(id)})
    row = {
                "email": "def@gmail.com",
                "field_1": "My field 1 text retrieve item",
                "field_2": "My field 2 text retrieve item",
                "field_3": 123,
            }
    if row:
        return ItemSchema(**row)


# # Update a student with a matching ID
# async def update_student(id: str, data: dict):
#     # Return false if an empty request body is sent.
#     if len(data) < 1:
#         return False
#     student = await student_collection.find_one({"_id": ObjectId(id)})
#     if student:
#         updated_student = await student_collection.update_one(
#             {"_id": ObjectId(id)}, {"$set": data}
#         )
#         if updated_student:
#             return True
#         return False


# # Delete a student from the database
# async def delete_student(id: str):
#     student = await student_collection.find_one({"_id": ObjectId(id)})
#     if student:
#         await student_collection.delete_one({"_id": ObjectId(id)})
#         return True
