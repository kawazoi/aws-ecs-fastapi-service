from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MyClassifierModel(BaseModel):
    created: Optional[datetime] = Schema(..., alias="createdAt")
    created_at: Optional[datetime] = Schema(..., alias="createdAt")
    my_model_output = JSONAttribute()

    class Config:
        schema_extra = {
            "example": {
                "created": "abc@gmail.com",
                "my_model_output": "My field 1 text",
            }
        }
