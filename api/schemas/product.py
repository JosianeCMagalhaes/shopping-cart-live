from typing import Optional
from pydantic import BaseModel, Field

class ProductSchema(BaseModel):
    name: str = Field(max_length=100)
    description: str
    price: float
    image: str
    code: int 

class ProductUpdatedSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    image: Optional[str]
    code: int
    
class ProductList(ProductSchema):
    _id: str
    code: str
    
    class Config:
        orm_mode = True