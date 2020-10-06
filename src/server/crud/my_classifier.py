from ..db.mongodb import AsyncIOMotorClient
from pydantic import EmailStr
from bson.objectid import ObjectId

from ..core.config import database_name, users_collection_name
from ..models.user import UserInCreate, UserInDB, UserInUpdate


async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    dbuser = UserInDB(**user.dict())
    dbuser.change_password(user.password)

    row = await conn[database_name][users_collection_name].insert_one(dbuser.dict())

    dbuser.id = row.inserted_id
    dbuser.created_at = ObjectId(dbuser.id ).generation_time
    dbuser.updated_at = ObjectId(dbuser.id ).generation_time

    return dbuser
