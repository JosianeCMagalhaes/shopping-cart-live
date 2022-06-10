from pydantic import BaseModel
from customer import PeeweeGetterDict


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    weight: float
    code: str

class ProductUpdate(BaseModel):
    name: str
    description: str
    price: str

class ProductList(ProductBase):
    id: int
    
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict
    
