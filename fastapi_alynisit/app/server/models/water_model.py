from typing import Optional
from pydantic import BaseModel, Field

class WaterSchema(BaseModel):
    Day: int = Field(..., ge=1, lt=61)
    H: float = Field(..., ge=0.0)
    Q: float = Field(..., ge=0.0)

def ResponseModel(data, code, message):
    return {
        "data": [data],
        "code": code,
        "message": message,
}