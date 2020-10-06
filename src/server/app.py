from fastapi import FastAPI

from src.server.routes.my_classifier import router as MyClassifier


app = FastAPI()


app.include_router(MyClassifier, tags=["MyClassifier"], prefix="/my_classifier")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
