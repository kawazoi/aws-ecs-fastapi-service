from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from src.server.crud.my_classifier import (
    process,
)
from src.server.models.my_classifier import (
    MyClassifierModel,
    ResponseModel,
    ErrorResponseModel,
)


router = APIRouter()


@router.post("/", response_description="Item processed")
async def post_process_text(text):
    resp = await process_text(text)
    if resp:
        return ResponseModel(MyClassifierModel(**resp), "Item processed successfully")
    return ErrorResponseModel("An error occurred.", 404, "Item could not be processed.")
