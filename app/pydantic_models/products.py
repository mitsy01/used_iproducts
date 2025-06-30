from typing import Optional

from pydantic import BaseModel


class ProductModel(BaseModel):
    name_prod: str
    description: Optional[str]| None
    price: float
    count: str
    

class ProductModelResponse(BaseModel):
    id: str
    name_prod: str
    description: Optional[str]| None
    price: float
    count: str

