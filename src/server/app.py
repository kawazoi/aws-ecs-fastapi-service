from fastapi import FastAPI

from src.server.routes.my_api import router as MyApi
# from src.server.db.mongodb_utils import close_mongo_connection, connect_to_mongo


app = FastAPI()

# app.add_event_handler("startup", connect_to_mongo)
# app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(MyApi, tags=["MyApi"], prefix="/my_api")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
